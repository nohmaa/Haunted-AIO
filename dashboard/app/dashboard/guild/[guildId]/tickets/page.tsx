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
import { Ticket, ExternalLink } from "lucide-react";
import nextDynamic from "next/dynamic";
import { api } from "@/lib/api";
import { ModuleUnavailable } from "@/components/dashboard/module-unavailable";
import { Button } from "@/components/ui/button";

const TicketsForm = nextDynamic(() => import("@/components/dashboard/tickets-form").then(mod => mod.TicketsForm), {
  loading: () => <div className="h-96 w-full animate-pulse bg-white/[0.02] rounded-3xl" />
});

export const dynamic = "force-dynamic";

export default async function TicketsPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const config = await api.getTickets(guildId);

  if (!config) {
    return <ModuleUnavailable module="Tickets" />;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500 pb-20">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Ticket className="h-6 w-6 text-primary" />
            Système de tickets
          </h2>
          <p className="text-slate-400 mt-1">Gérez les salons d’assistance privés et les catégories de demandes.</p>
        </div>
        <div className="flex items-center gap-4">
          {/* État réel du module : déduit du panneau configuré, rien d'inventé. */}
          <div
            className={
              config.panel_channel
                ? "bg-teal-300/10 border border-teal-300/20 px-4 py-2 rounded-2xl flex items-center gap-2"
                : "bg-white/[0.03] border border-white/[0.06] px-4 py-2 rounded-2xl flex items-center gap-2"
            }
          >
            <div
              className={
                config.panel_channel ? "h-2 w-2 rounded-full bg-teal-400" : "h-2 w-2 rounded-full bg-slate-500"
              }
            />
            <span
              className={
                config.panel_channel
                  ? "text-xs font-bold text-teal-300 uppercase"
                  : "text-xs font-bold text-slate-400 uppercase"
              }
            >
              {config.panel_channel ? "Panneau configuré" : "Aucun panneau configuré"}
            </span>
          </div>
          {/* <Button variant="outline" className="gap-2">
            <ExternalLink className="h-4 w-4" />
            Preview Panel
          </Button> */}
        </div>
      </div>

      <TicketsForm initialConfig={config} guildId={guildId} />
    </div>
  );
}
