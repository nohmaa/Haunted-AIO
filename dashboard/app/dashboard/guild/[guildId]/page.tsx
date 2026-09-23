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
  LayoutGrid,
  Hash,
  Users,
  ShieldCheck,
  ShieldOff,
  Activity,
  AlertTriangle,
} from "lucide-react";
import { api } from "@/lib/api";
import { GuildDetails, ModulesConfig, AntiNukeConfig } from "@/types/api";

export const dynamic = "force-dynamic";

const UNKNOWN = "—";

export default async function GuildOverviewPage({
  params,
}: {
  params: Promise<{ guildId: string }>;
}) {
  const { guildId } = await params;

  let details: GuildDetails | null = null;
  let modules: ModulesConfig | null = null;
  let antinuke: AntiNukeConfig | null = null;
  let latency: number | null = null;
  let error: string | null = null;

  try {
    details = await api.getGuildDetails(guildId);
  } catch (err: any) {
    console.error("Échec du chargement des détails du serveur :", err);
    error = err.message || "Impossible de charger les informations de ce serveur.";
  }

  try {
    modules = await api.getModules(guildId);
  } catch (err) {
    console.error("Échec du chargement des modules :", err);
  }

  try {
    antinuke = await api.getAntiNuke(guildId);
  } catch (err) {
    console.error("Échec du chargement de l'anti-nuke :", err);
  }

  try {
    latency = (await api.getBotStatus()).latency;
  } catch (err) {
    console.error("Échec du chargement du statut du bot :", err);
  }

  const enabledModules = (modules?.modules || []).filter((mod) => mod.enabled);
  const totalModules = modules?.modules.length ?? 0;

  const serverStats = [
    { label: "Membres", value: details ? details.member_count.toLocaleString("fr-FR") : UNKNOWN, icon: Users },
    { label: "Salons", value: details ? String(details.channel_count) : UNKNOWN, icon: Hash },
    { label: "Rôles", value: details ? String(details.role_count) : UNKNOWN, icon: ShieldCheck },
    {
      label: "Latence passerelle",
      value: latency != null ? `${Math.round(latency)} ms` : UNKNOWN,
      icon: Activity,
    },
  ];

  return (
    <div className="space-y-8">
      {error && (
        <div className="flex items-center gap-3 px-6 py-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-bold">
          <AlertTriangle className="h-5 w-5 shrink-0" />
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Colonne modules */}
        <div className="space-y-8">
          <section>
            <div className="flex items-center gap-2 mb-6">
              <h2 className="text-xl font-bold text-white tracking-tight">Modules actifs</h2>
              <div className="h-[2px] flex-1 bg-white/[0.05]" />
              <Link
                href={`/dashboard/guild/${guildId}/modules`}
                className="text-[11px] font-bold text-primary hover:underline whitespace-nowrap"
              >
                Gérer les modules →
              </Link>
            </div>

            {modules === null ? (
              <div className="haunted-panel p-8 text-center">
                <p className="text-sm text-slate-400">
                  L'état des modules est indisponible : l'API du bot n'a pas répondu.
                </p>
              </div>
            ) : enabledModules.length === 0 ? (
              <div className="haunted-panel p-8 text-center">
                <LayoutGrid className="h-8 w-8 text-slate-600 mx-auto mb-4" />
                <p className="text-sm text-slate-400">
                  Aucun module n'est activé sur ce serveur
                  {totalModules > 0 ? ` (0 / ${totalModules})` : ""}.
                </p>
                <Link
                  href={`/dashboard/guild/${guildId}/modules`}
                  className="inline-block mt-4 text-[11px] font-black uppercase tracking-widest text-primary hover:underline"
                >
                  Activer un module
                </Link>
              </div>
            ) : (
              <>
                <p className="text-xs text-slate-500 mb-4 font-bold uppercase tracking-widest">
                  {enabledModules.length} / {totalModules} activés
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {enabledModules.map((mod) => {
                    const card = (
                      <div className="haunted-panel p-5 h-full group hover:border-red-500/25 transition-all">
                        <div className="flex items-start justify-between mb-4">
                          <div className="h-10 w-10 bg-white/[0.03] rounded-xl flex items-center justify-center text-red-500 border border-white/[0.04]">
                            <LayoutGrid className="h-5 w-5" />
                          </div>
                          <span className="text-[10px] font-black uppercase text-teal-300 bg-teal-300/10 px-2 py-0.5 rounded-full border border-teal-300/20">
                            Actif
                          </span>
                        </div>
                        <h3 className="font-bold text-white mb-1">{mod.label}</h3>
                        <p className="text-xs text-slate-500 leading-relaxed">{mod.description}</p>
                      </div>
                    );
                    return mod.route ? (
                      <Link key={mod.key} href={`/dashboard/guild/${guildId}/${mod.route}`}>
                        {card}
                      </Link>
                    ) : (
                      <div key={mod.key}>{card}</div>
                    );
                  })}
                </div>
              </>
            )}
          </section>
        </div>

        {/* Colonne mesures réelles */}
        <div className="space-y-8">
          <section className="haunted-panel p-8">
            <h2 className="text-xl font-bold text-white mb-6">Informations du serveur</h2>
            <div className="space-y-4">
              {serverStats.map((stat) => (
                <div
                  key={stat.label}
                  className="flex items-center justify-between p-4 bg-white/[0.02] rounded-2xl border border-white/[0.05]"
                >
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 bg-white/[0.03] rounded-lg flex items-center justify-center text-red-500">
                      <stat.icon className="h-4 w-4" />
                    </div>
                    <span className="text-sm font-medium text-slate-300">{stat.label}</span>
                  </div>
                  <span className="text-sm font-bold text-white tracking-widest">{stat.value}</span>
                </div>
              ))}
            </div>
            {details === null && (
              <p className="mt-6 text-[11px] text-slate-500 leading-relaxed">
                Ces mesures proviennent de l'API du bot ; elles sont indisponibles tant qu'elle ne
                répond pas.
              </p>
            )}
          </section>

          <section className="haunted-panel p-8">
            <h2 className="text-xl font-bold text-white mb-6">Protection du serveur</h2>
            {antinuke === null ? (
              <p className="text-sm text-slate-400">
                État anti-nuke indisponible (API injoignable).
              </p>
            ) : (
              <div className="flex items-center gap-6">
                <div
                  className={
                    antinuke.status
                      ? "h-16 w-16 rounded-full border-2 border-teal-300/40 flex items-center justify-center text-teal-300 ectoplasm-glow"
                      : "h-16 w-16 rounded-full border-2 border-slate-600 flex items-center justify-center text-slate-500"
                  }
                >
                  {antinuke.status ? (
                    <ShieldCheck className="h-7 w-7" />
                  ) : (
                    <ShieldOff className="h-7 w-7" />
                  )}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">
                    Anti-nuke {antinuke.status ? "activé" : "désactivé"}
                  </h3>
                  <p className="text-slate-400 text-sm mt-1">
                    {antinuke.status
                      ? `${antinuke.whitelisted_users?.length ?? 0} utilisateur(s) en liste blanche.`
                      : "Aucune protection anti-raid n'est appliquée actuellement."}
                  </p>
                  <Link
                    href={`/dashboard/guild/${guildId}/antinuke`}
                    className="inline-block mt-3 text-[11px] font-black uppercase tracking-widest text-primary hover:underline"
                  >
                    Configurer l'anti-nuke →
                  </Link>
                </div>
              </div>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
