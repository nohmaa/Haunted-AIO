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
import Link from "next/link";
import {
  Users,
  Zap,
  Activity,
  Server as ServerIcon,
  ShieldAlert,
  FileText,
  LifeBuoy,
} from "lucide-react";
import { api } from "@/lib/api";
import { BotInfo, BotStatus } from "@/types/api";

export const dynamic = "force-dynamic";

const SUPPORT_SERVER = process.env.NEXT_PUBLIC_SUPPORT_SERVER || "https://discord.gg/DvetGPq9q5";

/** Une donnée absente s'affiche « — », jamais un zéro inventé. */
const UNKNOWN = "—";

export default async function DashboardPage() {
  let botInfo: BotInfo | null = null;
  let botStatus: BotStatus | null = null;
  let error: string | null = null;

  try {
    botInfo = await api.getBotInfo();
  } catch (err: any) {
    console.error("Failed to fetch bot info:", err);
    error = err.message || "Échec de connexion à l'API du bot.";
  }

  if (!error) {
    try {
      botStatus = await api.getBotStatus();
    } catch (err: any) {
      console.error("Failed to fetch bot status:", err);
    }
  }

  const stats = [
    {
      name: "Serveurs suivis",
      value: botInfo ? botInfo.guilds.toLocaleString("fr-FR") : UNKNOWN,
      icon: ServerIcon,
    },
    {
      name: "Membres cumulés",
      value: botInfo ? botInfo.users.toLocaleString("fr-FR") : UNKNOWN,
      icon: Users,
    },
    {
      name: "Commandes chargées",
      value: botInfo ? botInfo.commands.toLocaleString("fr-FR") : UNKNOWN,
      icon: Zap,
    },
    {
      name: "Latence passerelle",
      value: botInfo ? botInfo.latency : UNKNOWN,
      icon: Activity,
    },
  ];

  // Uniquement des mesures réellement renvoyées par l'API du bot.
  const gateway = [
    {
      name: "Passerelle Discord",
      value: botStatus ? `${Math.round(botStatus.latency)} ms` : UNKNOWN,
    },
    {
      name: "Shards actifs",
      value: botStatus?.shards != null ? String(botStatus.shards) : UNKNOWN,
    },
    {
      name: "Serveurs suivis",
      value: botStatus ? String(botStatus.guild_count) : UNKNOWN,
    },
    {
      name: "Membres cumulés",
      value: botStatus ? botStatus.user_count.toLocaleString("fr-FR") : UNKNOWN,
    },
  ];

  return (
    <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 px-2">
        <div>
          <h1 className="text-4xl md:text-5xl font-bold text-white font-outfit tracking-tight">
            Système <span className="text-red-500 italic">Core.</span>
          </h1>
          <p className="text-slate-400 mt-3 font-medium flex items-center gap-2">
            État du bot
            {botInfo?.name && (
              <span className="text-red-500 font-bold px-2 py-0.5 rounded-lg bg-red-500/10 border border-red-500/20">
                {botInfo.name}
              </span>
            )}
          </p>
        </div>

        {error && (
          <div className="flex items-center gap-2 px-5 py-2.5 glass-red rounded-2xl text-red-500 text-xs font-bold uppercase tracking-widest">
            <ShieldAlert className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="group haunted-panel p-7 relative overflow-hidden hover:border-red-500/30 transition-all duration-500"
          >
            <div className="flex items-center justify-between relative z-10">
              <div>
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-2">
                  {stat.name}
                </p>
                <p className="text-3xl font-bold text-white font-outfit tracking-tight">
                  {stat.value}
                </p>
              </div>
              <div className="p-4 bg-red-500/10 rounded-2xl border border-red-500/20 group-hover:scale-105 transition-transform duration-500">
                <stat.icon className="h-6 w-6 text-red-500" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Actions & passerelle */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 haunted-panel p-10">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold text-white font-outfit tracking-tight">
              Actions rapides
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                title: "Gérer les serveurs",
                desc: "Choisir un serveur et ouvrir ses modules.",
                icon: ServerIcon,
                href: "/dashboard/guilds",
                external: false,
              },
              {
                title: "Documentation",
                desc: "Comprendre le dashboard et ses modules.",
                icon: FileText,
                href: "/docs",
                external: false,
              },
              {
                title: "Serveur support",
                desc: "Poser une question à l'équipe.",
                icon: LifeBuoy,
                href: SUPPORT_SERVER,
                external: true,
              },
            ].map((item) => (
              <Link
                key={item.title}
                href={item.href}
                target={item.external ? "_blank" : undefined}
                rel={item.external ? "noreferrer" : undefined}
                className="flex items-center gap-5 p-4 rounded-2xl bg-white/[0.02] border border-white/[0.04] group/item hover:bg-white/[0.05] hover:border-red-500/20 transition-all"
              >
                <div className="h-12 w-12 rounded-2xl bg-red-500/5 border border-red-500/10 flex items-center justify-center group-hover/item:bg-red-500/10 transition-colors">
                  <item.icon className="h-5 w-5 text-red-500/60 group-hover/item:text-red-500 transition-colors" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white group-hover/item:text-red-500 transition-colors">
                    {item.title}
                  </h4>
                  <p className="text-[10px] text-slate-500 font-medium uppercase tracking-wider">
                    {item.desc}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div className="haunted-panel p-10 flex flex-col justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white mb-3 font-outfit">Passerelle</h2>
            <p className="text-slate-500 text-sm mb-8 font-medium">
              Mesures lues en direct sur l'API du bot.
            </p>

            <div className="space-y-4">
              {gateway.map((entry) => (
                <div
                  key={entry.name}
                  className="flex items-center justify-between p-4 bg-white/[0.02] rounded-2xl border border-white/[0.05] hover:border-red-500/20 transition-colors"
                >
                  <span className="text-xs font-bold text-slate-300">{entry.name}</span>
                  <span className="text-[11px] uppercase font-black text-red-400 tracking-widest">
                    {entry.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {!botStatus && (
            <p className="mt-8 text-[11px] text-slate-500 leading-relaxed">
              Les mesures détaillées sont indisponibles : l'API du bot n'a pas répondu à la demande
              de statut.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
