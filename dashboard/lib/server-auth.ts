import "server-only";

import { getServerSession } from "next-auth/next";
import { serverAuthOptions } from "@/lib/auth";

/** Récupère le jeton Discord depuis le cookie JWT chiffré, sans l'exposer à la session cliente. */
export async function getDiscordAccessToken(): Promise<string | null> {
  const session = await getServerSession(serverAuthOptions);
  const token = (session as (typeof session & { accessToken?: string; error?: string }) | null)?.accessToken;
  return typeof token === "string" && !(session as (typeof session & { error?: string }) | null)?.error
    ? token
    : null;
}

export function isDashboardAdmin(userId: string | null | undefined): boolean {
  if (!userId) return false;
  const adminIds = (process.env.DASHBOARD_ADMIN_IDS || process.env.ADMIN_IDS || "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
  return adminIds.includes(userId);
}
