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
import { 
  Users, 
  ShieldCheck, 
  Ticket, 
  BarChart4, 
  FileText, 
  Settings,
  Hash,
  Shield,
  Layers,
  ArrowLeft,
  ShieldAlert
} from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/lib/auth";
import { getManageableGuildIds } from "@/lib/discord";
import { redirect } from "next/navigation";

export const revalidate = 0; // Never cache any guild dashboard page

import { Button } from "@/components/ui/button";
import { GuildTabs } from "@/components/guild-tabs";

interface GuildLayoutProps {
  children: React.ReactNode;
  params: Promise<{ guildId: string }>;
}

export const dynamic = "force-dynamic";

export default async function GuildLayout({
  children,
  params,
}: GuildLayoutProps) {
  const { guildId } = await params;

  // Contrôle d'accès : la clé d'API du bot ne porte aucune identité, donc
  // l'autorisation doit être vérifiée ici, avec les droits Discord réels de
  // l'utilisateur connecté (et non de simples hypothèses côté client).
  const session = await getServerSession(authOptions);
  const accessToken = (session as { accessToken?: string } | null)?.accessToken;

  if (!session || !accessToken) {
    redirect("/");
  }

  const manageableGuildIds = await getManageableGuildIds(accessToken);

  if (manageableGuildIds === null) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] border-2 border-dashed border-amber-500/20 rounded-3xl bg-amber-500/5 p-12 text-center">
        <ShieldAlert className="h-16 w-16 text-amber-500 mb-6 opacity-50" />
        <h2 className="text-2xl font-bold text-white">Vérification impossible</h2>
        <p className="text-slate-400 mt-2 max-w-md">
          Discord n&apos;a pas répondu, les droits de gestion du serveur n&apos;ont donc pas pu être
          vérifiés. Aucune donnée n&apos;est affichée par précaution.
        </p>
        <Link href={`/dashboard/guild/${guildId}`} className="mt-8">
          <Button variant="outline">Réessayer</Button>
        </Link>
      </div>
    );
  }

  if (!manageableGuildIds.has(String(guildId))) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] border-2 border-dashed border-red-500/20 rounded-3xl bg-red-500/5 p-12 text-center">
        <ShieldAlert className="h-16 w-16 text-red-500 mb-6 opacity-50" />
        <h2 className="text-2xl font-bold text-white">Accès refusé</h2>
        <p className="text-slate-400 mt-2 max-w-md">
          Vous n&apos;avez pas la permission « Gérer le serveur » sur ce serveur.
        </p>
        <Link href="/dashboard/guilds" className="mt-8">
          <Button variant="outline">Retour aux serveurs</Button>
        </Link>
      </div>
    );
  }

  let guild;
  let error = null;

  try {
    guild = await api.getGuildDetails(guildId);
  } catch (err: any) {
    console.error("Échec de récupération des données du serveur :", err);
    error = err.message || "Échec du chargement des données du serveur.";
  }

  if (error || !guild) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] border-2 border-dashed border-red-500/20 rounded-3xl bg-red-500/5 p-12 text-center">
        <ShieldAlert className="h-16 w-16 text-red-500 mb-6 opacity-50" />
        <h2 className="text-2xl font-bold text-white">Accès refusé</h2>
        <p className="text-slate-400 mt-2 max-w-md">{error || "Ce serveur n'existe pas ou vous n'avez pas la permission de le gérer."}</p>
        <Link href="/dashboard/guilds" className="mt-8">
          <Button variant="outline">Retour aux serveurs</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Breadcrumb / Back button */}
      <Link href="/dashboard/guilds" className="inline-flex items-center gap-2 text-slate-500 hover:text-white transition-colors text-sm font-medium group">
        <ArrowLeft className="h-4 w-4 group-hover:-translate-x-1 transition-transform" />
        Retour à tous les serveurs
      </Link>

      {/* Guild Header */}
      <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl p-8 shadow-xl shadow-black/20">
        <div className="flex flex-col lg:flex-row lg:items-center gap-8">
          <div className="relative">
            {guild.icon ? (
              <Image 
                src={guild.icon} 
                alt={guild.name}
                width={120}
                height={120}
                className="rounded-3xl border-4 border-white/[0.06] shadow-2xl"
              />
            ) : (
              <div className="h-[120px] w-[120px] bg-primary rounded-3xl flex items-center justify-center text-4xl font-bold text-white shadow-2xl border-4 border-white/[0.06]">
                {guild.name.charAt(0)}
              </div>
            )}
            <div className="absolute -bottom-2 -right-2 bg-teal-400 text-white p-2 rounded-xl shadow-lg border-2 border-haunted-crypt" title="Actif">
              <div className="h-3 w-3 rounded-full bg-white animate-pulse" />
            </div>
          </div>

          <div className="flex-1 space-y-4">
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-4xl font-black text-white tracking-tight">{guild.name}</h1>
                <span className="px-3 py-1 bg-white/[0.05] rounded-lg text-[10px] uppercase font-black text-slate-500 tracking-tighter border border-white/5">
                  ID: {guildId}
                </span>
              </div>
              <p className="text-slate-400 mt-1 italic opacity-80">Tableau de bord du serveur</p>
            </div>

            <div className="flex flex-wrap gap-4">
              {[
                { label: "Membres", value: guild.member_count, icon: Users, color: "text-blue-400" },
                { label: "Rôles", value: guild.role_count, icon: Shield, color: "text-teal-300" },
                { label: "Salons", value: guild.channel_count, icon: Hash, color: "text-purple-400" },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-3 bg-white/[0.04] px-5 py-3 rounded-2xl border border-white/5 shadow-inner">
                  <div className={cn("p-2 rounded-lg bg-white/[0.02]", item.color)}>
                    <item.icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-[10px] uppercase font-bold text-slate-500 tracking-wider leading-none mb-1">{item.label}</p>
                    <p className="text-xl font-bold text-white leading-none">{item.value.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex flex-col sm:flex-row lg:flex-col gap-3">
            <Link href={`/dashboard/guild/${guildId}`} className="w-full">
             <Button className="w-full">
               Actualiser 
             </Button>
            </Link>
             <Link href={`/dashboard/guild/${guildId}/settings`} className="w-full">
              <Button variant="secondary" className="w-full">
                Paramètres du serveur
              </Button>
             </Link>
          </div>
        </div>
      </div>

      {/* Modern Tab Navigation */}
      <GuildTabs guildId={guildId} />

      {/* Tab Content */}
      <div className="min-h-[400px]">
        {children}
      </div>
    </div>
  );
}
