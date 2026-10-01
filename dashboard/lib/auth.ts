/**
 * ╔══════════════════════════════════════════════════════════════════╗
 * ║                                                                  ║
 * ║   ░█▀▀░█▀█░█▀▄░█▀▀░█░█   ░█▀▄░█▀▀░█░█░█▀▀                     ║
 * ║   ░█░░░█░█░█░█░█▀▀░▄▀▄   ░█░█░█▀▀░▀▄▀░▀▀█                     ║
 * ║   ░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀   ░▀▀░░▀▀▀░░▀░░▀▀▀                     ║
 * ║                                                                  ║
 * ║           © 2026 Arsonist   — All Rights Reserved               ║
 * ║                                                                  ║
 * ║   discord  ──  https://discord.gg/DvetGPq9q5                    ║
 * ║                                                                  ║
 * ╚══════════════════════════════════════════════════════════════════╝
 */

import DiscordProvider from "next-auth/providers/discord";
import { AuthOptions } from "next-auth";

export const authOptions: AuthOptions = {
  providers: [
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID || "",
      clientSecret: process.env.DISCORD_CLIENT_SECRET || "",
      authorization: { params: { scope: "identify guilds" } },
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
        const expiresIn = Number(account.expires_in || 0);
        const expiresAt = Number(account.expires_at || 0) * 1000;
        token.accessTokenExpires = expiresAt > Date.now()
          ? expiresAt
          : Date.now() + expiresIn * 1000;
        token.refreshToken = account.refresh_token;
        token.error = undefined;
      }

      if (token.accessToken && Date.now() < Number(token.accessTokenExpires || 0) - 60_000) {
        return token;
      }

      if (!token.accessToken && !token.refreshToken) {
        return token;
      }

      if (!token.refreshToken) {
        token.error = "RefreshAccessTokenError";
        return token;
      }

      try {
        const response = await fetch("https://discord.com/api/oauth2/token", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            client_id: process.env.DISCORD_CLIENT_ID || "",
            client_secret: process.env.DISCORD_CLIENT_SECRET || "",
            grant_type: "refresh_token",
            refresh_token: String(token.refreshToken),
          }),
          cache: "no-store",
          signal: AbortSignal.timeout(10000),
        });
        if (!response.ok) throw new Error(`Discord token refresh returned ${response.status}`);
        const refreshed = await response.json();
        token.accessToken = refreshed.access_token;
        token.accessTokenExpires = Date.now() + Number(refreshed.expires_in) * 1000;
        token.refreshToken = refreshed.refresh_token ?? token.refreshToken;
        token.error = undefined;
      } catch (error) {
        console.error("[Discord OAuth] Échec du renouvellement du jeton d'accès.", error instanceof Error ? error.message : "unknown error");
        token.error = "RefreshAccessTokenError";
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        // @ts-expect-error next-auth session user extension
        session.user.id = token.sub;
        // Seul un booléen d'affichage est renvoyé ; l'allowlist reste privée,
        // et la page + le proxy refont toujours le contrôle côté serveur.
        session.user.isAdmin = (process.env.DASHBOARD_ADMIN_IDS || process.env.ADMIN_IDS || "")
          .split(",")
          .map((id) => id.trim())
          .includes(String(token.sub || ""));
      }
      if (token.error) {
        (session as typeof session & { error?: string }).error = String(token.error);
      }
      return session;
    },
  },
  session: {
    // Le jeton OAuth Discord reste dans le JWT chiffré côté serveur ; il n'est
    // jamais renvoyé par /api/auth/session au navigateur.
    strategy: "jwt",
    maxAge: 8 * 60 * 60,
  },
  useSecureCookies: process.env.NEXTAUTH_URL?.startsWith("https://") ?? false,
  pages: {
    signIn: "/",
  },
};

/** Variant utilisée uniquement dans les appels serveur internes au dashboard. */
export const serverAuthOptions: AuthOptions = {
  ...authOptions,
  callbacks: {
    ...authOptions.callbacks,
    async session({ session, token }) {
      const publicSession = await authOptions.callbacks!.session!({ session, token } as never);
      if (publicSession && token.accessToken) {
        (publicSession as typeof publicSession & { accessToken?: string }).accessToken = String(token.accessToken);
      }
      if (publicSession && token.error) {
        (publicSession as typeof publicSession & { error?: string }).error = String(token.error);
      }
      return publicSession;
    },
  },
};
