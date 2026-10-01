import { NextRequest, NextResponse } from "next/server";
import { authorizeBotRequest, ProxyAuthorizationError } from "@/lib/bot-proxy";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

const MAX_BODY_BYTES = 64 * 1024;

async function readLimitedBody(request: NextRequest): Promise<Uint8Array> {
  const reader = request.body?.getReader();
  if (!reader) return new Uint8Array();
  const chunks: Uint8Array[] = [];
  let total = 0;

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > MAX_BODY_BYTES) {
        await reader.cancel();
        throw new ProxyAuthorizationError(413, "Corps de requête trop volumineux.");
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }

  const body = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return body;
}

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  try {
    const { path } = await context.params;
    if (!path?.length || path.some((part) => !part || part === "." || part === ".." || /[\\\u0000-\u001f?#]/.test(part))) {
      return NextResponse.json({ detail: "Chemin API invalide." }, { status: 400 });
    }

    const method = request.method.toUpperCase();
    if (!["GET", "POST", "PATCH", "DELETE"].includes(method)) {
      return NextResponse.json({ detail: "Méthode non autorisée." }, { status: 405 });
    }

    if (method !== "GET" && request.headers.get("origin") !== request.nextUrl.origin) {
      return NextResponse.json({ detail: "Origine de requête invalide." }, { status: 403 });
    }
    if (method !== "GET" && request.headers.get("x-haunted-request") !== "dashboard") {
      return NextResponse.json({ detail: "Jeton CSRF manquant ou invalide." }, { status: 403 });
    }
    if (method !== "GET" && method !== "DELETE" && !request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) {
      return NextResponse.json({ detail: "Le type de contenu doit être application/json." }, { status: 415 });
    }

    let body: Uint8Array<ArrayBufferLike> = new Uint8Array();
    if (method !== "GET") {
      const contentLength = Number(request.headers.get("content-length") || "0");
      if (contentLength > MAX_BODY_BYTES) {
        return NextResponse.json({ detail: "Corps de requête trop volumineux." }, { status: 413 });
      }
      body = await readLimitedBody(request);
    }

    const encodedPath = path.map((part) => encodeURIComponent(part)).join("/") +
      (request.nextUrl.pathname.endsWith("/") ? "/" : "");
    const rawTarget = `${request.nextUrl.pathname.replace(/^\/api\/bot/, "/api/v1")}${request.nextUrl.search}`;
    const authorized = await authorizeBotRequest({
      requestHeaders: request.headers,
      method,
      botPath: `/${encodedPath}`,
      search: request.nextUrl.search,
      signedPathAndQuery: rawTarget,
      body,
    });

    const requestId = crypto.randomUUID();
    const upstream = await fetch(authorized.url, {
      method,
      headers: {
        ...authorized.headers,
        "X-Request-ID": requestId,
        ...(request.headers.get("content-type")
          ? { "Content-Type": request.headers.get("content-type") as string }
          : {}),
      },
      body: method === "GET" ? undefined : Buffer.from(body),
      cache: "no-store",
      signal: AbortSignal.timeout(15000),
    });

    if (upstream.status === 429) {
      return NextResponse.json(
        { detail: "Trop de requêtes ; patientez avant de réessayer." },
        {
          status: 429,
          headers: {
            "Retry-After": upstream.headers.get("retry-after") || "60",
            "Cache-Control": "no-store, private",
          },
        },
      );
    }

    let responseBody = await upstream.text();
    if (upstream.ok && ["/api/v1/guilds", "/api/v1/guilds/"].includes(authorized.url.pathname)) {
      const guildIds = authorized.authorizedGuildIds;
      if (!guildIds) return NextResponse.json({ detail: "Discord est indisponible ; vos permissions n'ont pas pu être vérifiées." }, { status: 503 });
      try {
        const guilds = JSON.parse(responseBody) as Array<{ id: string }>;
        responseBody = JSON.stringify(guilds.filter((guild) => guildIds.has(String(guild.id))));
      } catch {
        return NextResponse.json({ detail: "Réponse invalide de l'API du bot." }, { status: 502 });
      }
    }

    return new NextResponse(responseBody, {
      status: upstream.status,
      headers: {
        "Content-Type": upstream.headers.get("content-type") || "application/json",
        "Cache-Control": "no-store, private",
        "X-Content-Type-Options": "nosniff",
        "X-Request-ID": upstream.headers.get("x-request-id") || requestId,
      },
    });
  } catch (error) {
    if (error instanceof ProxyAuthorizationError) {
      return NextResponse.json({ detail: error.message }, { status: error.status });
    }
    console.error("[Bot API proxy] Request failed:", error instanceof Error ? error.message : "unknown error");
    return NextResponse.json({ detail: "L'API du bot est temporairement indisponible." }, { status: 503 });
  }
}

export const GET = proxy;
export const POST = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
