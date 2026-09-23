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
import { 
  BellRing,
  ChevronRight
} from "lucide-react";
import dynamic from "next/dynamic";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";

const LoggingForm = dynamic(() => import("@/components/dashboard/logging-form").then(mod => mod.LoggingForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-slate-800/20 rounded-[40px]" />
});

export default async function LoggingPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const [loggingData, channelsData] = await Promise.all([
    api.getLogging(guildId),
    api.getChannels(guildId)
  ]);

  if (!loggingData) return null;

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500 pb-20">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-black text-white flex items-center gap-2 tracking-tight">
            <BellRing className="h-6 w-6 text-primary" />
            Journaux d’audit
          </h2>
          <p className="text-slate-400 mt-1 font-medium italic">Configurez les événements et leurs salons de destination.</p>
        </div>
        <div className="flex items-center gap-4">
           <Button variant="outline" className="gap-2 border-slate-800 bg-slate-900/50 rounded-2xl">
             Historique d’audit
             <ChevronRight className="h-4 w-4" />
           </Button>
        </div>
      </div>

      <LoggingForm 
        initialConfig={loggingData} 
        channels={channelsData} 
        guildId={guildId} 
      />
    </div>
  );
}
