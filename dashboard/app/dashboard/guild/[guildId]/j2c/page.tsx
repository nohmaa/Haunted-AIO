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
import { Mic } from "lucide-react";
import nextDynamic from "next/dynamic";
import { api } from "@/lib/api";
import { ModuleUnavailable } from "@/components/dashboard/module-unavailable";

export const revalidate = 0; // Never cache this page


const J2CForm = nextDynamic(() => import("@/components/dashboard/j2c-form").then(mod => mod.J2CForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-white/[0.02] rounded-3xl" />
});

export const dynamic = "force-dynamic";

export default async function J2CPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const [config, channels] = await Promise.all([
    api.getJ2C(guildId),
    api.getChannels(guildId),
  ]);

  if (!config) {
    return <ModuleUnavailable module="Join to Create" />;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Mic className="h-6 w-6 text-primary" />
            Salons temporaires
          </h2>
          <p className="text-slate-400 mt-1">Créez des salons vocaux temporaires dès qu’un membre rejoint un salon précis.</p>
        </div>
      </div>

      <J2CForm initialConfig={config} channels={channels} guildId={guildId} />
    </div>
  );
}
