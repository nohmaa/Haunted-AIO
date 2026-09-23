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

import React from "react";
import { ShieldCheck } from "lucide-react";
import nextDynamic from "next/dynamic";
import { api } from "@/lib/api";
import { ModuleUnavailable } from "@/components/dashboard/module-unavailable";

const AutomodForm = nextDynamic(() => import("@/components/dashboard/automod-form").then(mod => mod.AutomodForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-white/[0.02] rounded-3xl" />
});

export const dynamic = "force-dynamic";

export default async function AutomodPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const config = await api.getAutomod(guildId);

  if (!config) {
    return <ModuleUnavailable module="Auto-modération" />;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="h-6 w-6 text-primary" />
            Auto-modération
          </h2>
          <p className="text-slate-400 mt-1">Protégez votre communauté avec des filtres automatiques.</p>
        </div>
      </div>

      <AutomodForm initialConfig={config} guildId={guildId} />
    </div>
  );
}
