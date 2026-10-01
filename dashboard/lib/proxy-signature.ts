import "server-only";

import { createHash, createHmac, randomBytes } from "node:crypto";

export type ProxyScope = "dashboard" | "admin" | `guild:${string}`;

/** Sign a single API request. The matching verifier lives in bot/api/proxy_auth.py. */
export function signedProxyHeaders(input: {
  method: string;
  pathAndQuery: string;
  body: Uint8Array;
  userId: string;
  scope: ProxyScope;
}): Record<string, string> {
  const secret = process.env.DASHBOARD_PROXY_SECRET;
  if (!secret || Buffer.byteLength(secret, "utf8") < 32) {
    throw new Error("DASHBOARD_PROXY_SECRET must contain at least 32 bytes.");
  }

  const timestamp = Math.floor(Date.now() / 1000).toString();
  const nonce = randomBytes(18).toString("base64url");
  const bodyDigest = createHash("sha256").update(input.body).digest("hex");
  const message = [
    input.method.toUpperCase(),
    input.pathAndQuery,
    bodyDigest,
    timestamp,
    nonce,
    input.userId,
    input.scope,
  ].join("\n");
  const signature = createHmac("sha256", secret).update(message).digest("hex");

  return {
    "X-Haunted-Proxy-User": input.userId,
    "X-Haunted-Proxy-Scope": input.scope,
    "X-Haunted-Proxy-Timestamp": timestamp,
    "X-Haunted-Proxy-Nonce": nonce,
    "X-Haunted-Proxy-Signature": signature,
  };
}
