import { createApi } from "@/lib/api-factory";

class ApiError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const method = (options.method || "GET").toUpperCase();
  const response = await fetch(`/api/bot${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
      ...(method !== "GET" ? { "X-Haunted-Request": "dashboard" } : {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let detail = response.statusText || "Une erreur est survenue.";
    try {
      const data = await response.json();
      detail = typeof data.detail === "string" ? data.detail : detail;
    } catch {
      // Keep the generic HTTP status message for non-JSON proxy responses.
    }
    throw new ApiError(response.status, detail);
  }
  return (await response.json()) as T;
}

const apiMethods = createApi(request);
export const api = {
  ...apiMethods,
   getPublicNotification: () => request<{ global_notification: string | null }>("/public/notification"),
};
