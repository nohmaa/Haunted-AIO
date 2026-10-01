import "server-only";

import { getServerSession } from "next-auth/next";
import { serverAuthOptions } from "@/lib/auth";
import { getManageableGuildIds } from "@/lib/discord";
import { isDashboardAdmin } from "@/lib/server-auth";
import { signedProxyHeaders, type ProxyScope } from "@/lib/proxy-signature";

const API_BASE = (process.env.API_URL || "http://localhost:8000/api/v1").replace(/\/+$/, "");
const parsedApiBase = new URL(API_BASE);
const REQUEST_WINDOW_MS = 60_000;
const REQUESTS_PER_MINUTE = 120;
const MAX_TRACKED_USERS = 4096;
const requestTimesByUser = new Map<string, number[]>();
if (
  !["http:", "https:"].includes(parsedApiBase.protocol) ||
  parsedApiBase.username ||
  parsedApiBase.password ||
  !(parsedApiBase.pathname === "/api/v1" || parsedApiBase.pathname === "/api/v1/")
) {
  throw new Error("API_URL must be an HTTP(S) API base URL ending in /api/v1, without embedded credentials.");
}

export class ProxyAuthorizationError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

export interface AuthorizedBotRequest {
  userId: string;
  scope: ProxyScope;
  url: URL;
  headers: Record<string, string>;
  body: Uint8Array;
  authorizedGuildIds?: Set<string>;
}

/** Authenticate the dashboard session, authorize the requested resource, then sign it for FastAPI. */
export async function authorizeBotRequest(input: {
  requestHeaders?: Headers;
  method: string;
  botPath: string;
  search?: string;
  signedPathAndQuery?: string;
  body?: Uint8Array;
}): Promise<AuthorizedBotRequest> {
  if (!process.env.DASHBOARD_API_KEY) {
    throw new ProxyAuthorizationError(503, "L'API du bot n'est pas configurée sur le serveur dashboard.");
  }
  if (input.body && input.body.byteLength > 64 * 1024) {
    throw new ProxyAuthorizationError(413, "Corps de requête trop volumineux.");
  }
  if (!process.env.DASHBOARD_PROXY_SECRET || Buffer.byteLength(process.env.DASHBOARD_PROXY_SECRET, "utf8") < 32) {
    throw new ProxyAuthorizationError(503, "La signature sécurisée de l'API n'est pas configurée.");
  }

  const session = await getServerSession(serverAuthOptions);
  const userId = session?.user?.id;
  if (!userId) throw new ProxyAuthorizationError(401, "Connexion Discord requise.");
  const now = Date.now();
  const recentRequests = (requestTimesByUser.get(userId) || []).filter(
    (timestamp) => timestamp > now - REQUEST_WINDOW_MS,
  );
  if (!requestTimesByUser.has(userId) && requestTimesByUser.size >= MAX_TRACKED_USERS) {
    for (const [trackedUser, timestamps] of requestTimesByUser) {
      if (timestamps.every((timestamp) => timestamp <= now - REQUEST_WINDOW_MS)) {
        requestTimesByUser.delete(trackedUser);
      }
    }
    if (requestTimesByUser.size >= MAX_TRACKED_USERS) {
      throw new ProxyAuthorizationError(503, "Le proxy est temporairement saturé. Réessayez dans une minute.");
    }
  }
  if (recentRequests.length >= REQUESTS_PER_MINUTE) {
    requestTimesByUser.set(userId, recentRequests);
    throw new ProxyAuthorizationError(429, "Trop de requêtes dashboard ; réessayez dans une minute.");
  }
  recentRequests.push(now);
  requestTimesByUser.set(userId, recentRequests);
  if (requestTimesByUser.size > MAX_TRACKED_USERS) {
    for (const [key, times] of requestTimesByUser) {
      if (times.every((timestamp) => timestamp <= now - REQUEST_WINDOW_MS)) requestTimesByUser.delete(key);
    }
  }
  const accessToken = (session as typeof session & { accessToken?: string; error?: string } | null)?.accessToken;
  const sessionError = (session as typeof session & { error?: string } | null)?.error;

  const botPath = input.botPath.startsWith("/") ? input.botPath : `/${input.botPath}`;
  const url = new URL(`${API_BASE}${botPath}${input.search || ""}`);
  if (url.origin !== parsedApiBase.origin || !url.pathname.startsWith("/api/v1/")) {
    throw new ProxyAuthorizationError(400, "Route API invalide.");
  }
  try {
    if (decodeURI(url.pathname).includes("/../") || decodeURI(url.pathname).endsWith("/..")) {
      throw new ProxyAuthorizationError(400, "Chemin API invalide.");
    }
  } catch (error) {
    if (error instanceof ProxyAuthorizationError) throw error;
    throw new ProxyAuthorizationError(400, "Chemin API invalide.");
  }
  const guildMatch = url.pathname.match(/^\/api\/v1\/guilds\/(\d+)(?:\/|$)/);
  let scope: ProxyScope = "dashboard";
  let authorizedGuildIds: Set<string> | undefined;

  if (url.pathname.startsWith("/api/v1/admin/")) {
    if (sessionError) throw new ProxyAuthorizationError(401, "Session expirée. Reconnectez-vous.");
    if (!isDashboardAdmin(userId)) {
      throw new ProxyAuthorizationError(403, "Accès réservé aux administrateurs Haunted.");
    }
    scope = "admin";
  } else if (guildMatch) {
    if (sessionError) throw new ProxyAuthorizationError(401, "Session Discord expirée. Reconnectez-vous.");
    if (!accessToken) throw new ProxyAuthorizationError(401, "Session Discord expirée. Reconnectez-vous.");

    const manageableGuildIds = await getManageableGuildIds(accessToken);
    if (manageableGuildIds === null) {
      throw new ProxyAuthorizationError(503, "Discord est indisponible ; vos permissions n'ont pas pu être vérifiées.");
    }

    const guildId = guildMatch[1];
    authorizedGuildIds = manageableGuildIds;
    if (!manageableGuildIds.has(guildId)) {
      throw new ProxyAuthorizationError(403, "Vous ne pouvez pas administrer ce serveur.");
    }

    scope = `guild:${guildId}`;
    // Le proxy n'autorise pas une guilde simplement parce qu'elle est dans
    // l'URL : il confirme aussi que le bot y est toujours présent.
    if (url.pathname !== `/api/v1/guilds/${guildId}` || input.method.toUpperCase() !== "GET") {
      const presenceUrl = new URL(`${API_BASE}/guilds/${guildId}`);
      const presenceHeaders = signedProxyHeaders({
        method: "GET",
        pathAndQuery: presenceUrl.pathname,
        body: new Uint8Array(),
        userId,
        scope,
      });
      const presence = await fetch(presenceUrl, {
        headers: {
          Authorization: `Bearer ${process.env.DASHBOARD_API_KEY || ""}`,
          ...presenceHeaders,
        },
        cache: "no-store",
        signal: AbortSignal.timeout(10000),
      });
      if (presence.status === 404) throw new ProxyAuthorizationError(404, "Le bot n'est pas présent sur ce serveur.");
      if (!presence.ok) throw new ProxyAuthorizationError(503, "Impossible de vérifier la présence du bot.");
    }
  } else if (url.pathname === "/api/v1/guilds/" || url.pathname === "/api/v1/guilds") {
    if (sessionError) throw new ProxyAuthorizationError(401, "Session Discord expirée. Reconnectez-vous.");
    scope = "dashboard";
    if (!accessToken) throw new ProxyAuthorizationError(401, "Session Discord expirée. Reconnectez-vous.");
    authorizedGuildIds = await getManageableGuildIds(accessToken) || undefined;
    if (!authorizedGuildIds) {
      throw new ProxyAuthorizationError(503, "Discord est indisponible ; vos permissions n'ont pas pu être vérifiées.");
    }
  } else if (
    !url.pathname.startsWith("/api/v1/bot/") &&
    url.pathname !== "/api/v1/public/notification"
  ) {
    throw new ProxyAuthorizationError(404, "Route API inconnue.");
  } else if (url.pathname.startsWith("/api/v1/bot/")) {
    if (sessionError) throw new ProxyAuthorizationError(401, "Session expirée. Reconnectez-vous.");
  } else if (url.pathname === "/api/v1/public/notification") {
    if (sessionError) throw new ProxyAuthorizationError(401, "Session expirée. Reconnectez-vous.");
  }

  const safeSearch = new URLSearchParams(url.search);
  if (safeSearch.toString().length > 2048 || url.pathname.length > 1024) {
    throw new ProxyAuthorizationError(414, "Paramètres URL trop volumineux.");
  }

  const body = input.body ?? new Uint8Array();
  const signatureHeaders = signedProxyHeaders({
    method: input.method,
    pathAndQuery: input.signedPathAndQuery || `${url.pathname}${url.search}`,
    body,
    userId,
    scope,
  });

  return {
    userId,
    scope,
    url,
    body,
    headers: {
      Authorization: `Bearer ${process.env.DASHBOARD_API_KEY || ""}`,
      ...signatureHeaders,
    },
    authorizedGuildIds,
  };
}
