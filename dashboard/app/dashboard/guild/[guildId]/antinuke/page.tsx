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
import { ShieldAlert } from "lucide-react";
import nextDynamic from "next/dynamic";
import { api } from "@/lib/api";

const AntiNukeForm = nextDynamic(() => import("@/components/dashboard/antinuke-form").then(mod => mod.AntiNukeForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-slate-800/20 rounded-3xl" />
});

export const dynamic = "force-dynamic";

export default async function AntiNukePage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const config = await api.getAntiNuke(guildId);

  if (!config) return null;

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="h-6 w-6 text-red-500" />
            Protection Anti-Nuke
          </h2>
          <p className="text-slate-400 mt-1">Protégez votre serveur contre les suppressions et bannissements massifs malveillants.</p>
        </div>
      </div>

      <AntiNukeForm initialConfig={config} guildId={guildId} />
    </div>
  );
}
