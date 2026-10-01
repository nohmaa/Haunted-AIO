import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: ["/", "/docs", "/privacy", "/terms"], disallow: ["/dashboard", "/api/"] },
    ],
    sitemap: `${process.env.NEXTAUTH_URL || "https://www.haunted-mind.site"}/sitemap.xml`,
  };
}
