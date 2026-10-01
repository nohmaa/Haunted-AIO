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
import Image from "next/image";
import Link from "next/link";
import { Users, ShieldCheck, ChevronRight, Bot } from "lucide-react";
import { api } from "@/lib/api-server";
import { Button } from "@/components/ui/button";
import { RetryButton } from "@/components/dashboard/retry-button";

import { GuildSummary } from "@/types/api";
import { getServerSession } from "next-auth/next";
import { getManageableGuilds } from "@/lib/discord";
import { serverAuthOptions } from "@/lib/auth";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export default async function GuildsPage() {
  const session = await getServerSession(serverAuthOptions);
  const accessToken = (session as typeof session & { accessToken?: string } | null)?.accessToken;

  if (!session || !accessToken || session.error) {
    redirect("/");
  }

  let botGuilds: GuildSummary[] = [];
  let userDiscordError: string | null = null;
  let botError: string | null = null;

  // Requêtes serveur : vérifie la session + les droits guild dans le proxy,
  // puis filtre la liste avant qu'elle soit rendue au navigateur.
  const manageableGuilds = await getManageableGuilds(accessToken);
  if (manageableGuilds === null) {
    userDiscordError =
      "Discord n'a pas répondu : vos droits de gestion n'ont pas pu être vérifiés.";
  }

  try {
    botGuilds = await api.listGuilds();
  } catch (err: unknown) {
    console.error("Failed to fetch bot guilds:", err);
    botError = err instanceof Error ? err.message : "Échec du chargement des serveurs du bot.";
  }

  const botGuildById = new Map(botGuilds.map((guild) => [String(guild.id), guild]));
  const guilds = (manageableGuilds ?? []).map((discordGuild) => {
    const botGuild = botGuildById.get(String(discordGuild.id));
    const icon = discordGuild.icon
      ? `https://cdn.discordapp.com/icons/${discordGuild.id}/${discordGuild.icon}.png?size=128`
      : null;
    return {
      id: String(discordGuild.id),
      name: discordGuild.name,
      icon_url: botGuild?.icon_url || icon,
      owner_id: "",
      member_count: botGuild?.member_count ?? null,
      botPresent: Boolean(botGuild),
    };
  });
  const botMissingCount = guilds.filter((guild) => !guild.botPresent).length;
  const error = botError || userDiscordError;


  return (
    <div className="space-y-8">
      <div className="flex flex-wrap justify-between items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Vos serveurs</h1>
          <p className="text-slate-400 mt-2">
            Sélectionnez un serveur pour gérer sa configuration et ses modules.
          </p>
        </div>
        <div className="text-sm font-medium px-4 py-2 bg-white/[0.02] rounded-xl border border-white/[0.06] text-slate-300">
          <span className="text-white">{guilds.filter((guild) => guild.botPresent).length}</span> serveur(s) configurables
        </div>
      </div>

      {botMissingCount > 0 && (
        <p className="text-sm text-amber-200/90" role="status">
          {botMissingCount} serveur(s) que vous gérez n&apos;ont pas Haunted. Ils apparaissent ici uniquement pour distinguer l&apos;absence du bot ; aucune configuration n&apos;est disponible.
        </p>
      )}

      {error ? (
        <div className="bg-red-500/10 border border-red-500/20 p-8 rounded-2xl text-center">
          <ShieldCheck className="h-12 w-12 text-red-500 mx-auto mb-4 opacity-50" />
          <h3 className="text-white font-bold text-lg">Erreur de connexion</h3>
          <p className="text-slate-400 mt-2">{error}</p>
          <div className="mt-6 flex justify-center">
            <RetryButton />
          </div>
        </div>
      ) : guilds.length === 0 ? (
        <div className="bg-white/[0.01] border border-white/[0.06] border-dashed p-16 rounded-3xl text-center">
          <div className="h-16 w-16 bg-white/[0.03] rounded-full flex items-center justify-center mx-auto mb-6">
            <Users className="h-8 w-8 text-slate-600" />
          </div>
          <h3 className="text-white font-bold text-xl">Aucun serveur gérable</h3>
          <p className="text-slate-400 mt-2 max-w-md mx-auto">
            Aucun serveur où vous avez la permission « Gérer le serveur » ou « Administrateur » n&apos;a été trouvé.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {guilds.map((guild) => (
            <div 
              key={guild.id} 
              className="bg-haunted-surface border border-white/[0.06] rounded-3xl group hover:border-primary/50 hover:bg-white/[0.05] transition-all duration-300 overflow-hidden shadow-sm hover:shadow-primary/5 shadow-black/20"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-6">
                  <div className="relative">
                    {guild.icon_url ? (
                      <Image 
                        src={guild.icon_url} 
                        alt={guild.name}
                        width={64}
                        height={64}
                        className="rounded-2xl border-2 border-white/[0.06] shadow-xl group-hover:scale-105 transition-transform"
                      />
                    ) : (
                      <div className="h-16 w-16 bg-primary/20 rounded-2xl flex items-center justify-center border-2 border-white/[0.06] text-primary font-bold text-2xl shadow-xl group-hover:scale-105 transition-transform">
                        {guild.name.charAt(0)}
                      </div>
                    )}
                    <div className={`absolute -bottom-1 -right-1 h-4 w-4 rounded-full border-2 border-haunted-crypt ${guild.botPresent ? "bg-teal-300" : "bg-amber-400"}`} title={guild.botPresent ? "Bot présent sur ce serveur" : "Bot absent de ce serveur"} />
                  </div>
                  
                  <div className="flex flex-col items-end text-right">
                    <span className="text-[10px] uppercase font-bold text-slate-500 tracking-widest mb-1">ID du serveur</span>
                    <span className="text-xs font-mono text-slate-400 bg-black/20 px-2 py-1 rounded-lg border border-white/5 truncate max-w-[120px]">
                      {guild.id}
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-bold text-white truncate group-hover:text-primary transition-colors">
                    {guild.name}
                  </h3>
                  <div className="flex items-center gap-4 mt-4 text-slate-400">
                    <div className="flex items-center gap-1.5 bg-white/[0.04] px-3 py-1.5 rounded-xl border border-white/5">
                      <Users className="h-4 w-4 text-slate-500" />
                      <span className="text-sm font-semibold text-slate-300">{guild.member_count === null ? "—" : guild.member_count.toLocaleString()}</span>
                    </div>
                    <div className="flex items-center gap-1.5 bg-white/[0.04] px-3 py-1.5 rounded-xl border border-white/5">
                      <Bot className="h-4 w-4 text-slate-500" />
                      <span className="text-sm font-semibold text-slate-300">{guild.botPresent ? "Bot présent" : "Bot absent"}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="px-6 py-4 bg-white/[0.02] border-t border-white/[0.06] group-hover:bg-primary/5 transition-colors">
                {guild.botPresent ? (
                <Button className="w-full justify-between group/btn py-6" variant="secondary" asChild>
                  <Link href={`/dashboard/guild/${guild.id}`}>
                    <span>Gérer le serveur</span>
                    <ChevronRight className="h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                  </Link>
                </Button>
                ) : (
                  <p className="py-2 text-center text-sm text-amber-300">Ajoutez Haunted à ce serveur pour ouvrir sa configuration.</p>
                )}
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}
