import "server-only";

import { createApi } from "@/lib/api-factory";
import { authorizeBotRequest } from "@/lib/bot-proxy";

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const body = options.body ? new TextEncoder().encode(String(options.body)) : new Uint8Array();
  const method = (options.method || "GET").toUpperCase();
  const authorized = await authorizeBotRequest({
    method,
    botPath: endpoint,
    body,
  });
  const response = await fetch(authorized.url, {
    method,
    headers: {
      ...authorized.headers,
      ...(options.headers as Record<string, string> | undefined),
      ...(body.byteLength ? { "Content-Type": "application/json" } : {}),
    },
    body: method === "GET" ? undefined : body,
    cache: "no-store",
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    let detail = response.statusText || "Une erreur est survenue.";
    try {
      const error = await response.json();
      detail = typeof error.detail === "string" ? error.detail : detail;
    } catch {
      // Preserve the status text on non-JSON API errors.
    }
    throw Object.assign(new Error(detail), { status: response.status });
  }
  return (await response.json()) as T;
}

export const api = createApi(request);
