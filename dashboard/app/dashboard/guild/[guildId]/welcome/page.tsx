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
import { SmilePlus } from "lucide-react";
import nextDynamic from "next/dynamic";
import { api } from "@/lib/api";
import { ModuleUnavailable } from "@/components/dashboard/module-unavailable";

const WelcomeForm = nextDynamic(() => import("@/components/dashboard/welcome-form").then(mod => mod.WelcomeForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-white/[0.02] rounded-3xl" />
});

export const dynamic = "force-dynamic";

export default async function WelcomePage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const [welcomeData, channelsData] = await Promise.all([
    api.getWelcome(guildId),
    api.getChannels(guildId)
  ]);

  if (!welcomeData) {
    return <ModuleUnavailable module="Bienvenue" />;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <SmilePlus className="h-6 w-6 text-primary" />
            Bienvenue
          </h2>
          <p className="text-slate-400 mt-1">Accueillez les nouveaux membres de votre serveur.</p>
        </div>
      </div>

      <WelcomeForm initialConfig={welcomeData} channels={channelsData} guildId={guildId} />
    </div>
  );
}
