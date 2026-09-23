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

"use client";

import React from "react";
import Link from "next/link";
import { Bot, ChevronLeft, ShieldCheck, Lock, Eye, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-haunted-crypt text-slate-200 font-sans">
      {/* Habillage : brume de manoir */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-fog" />
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-vignette" />

      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-haunted-crypt/80 backdrop-blur-3xl px-6 h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-4 group">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-red-600 to-red-900 border border-white/10 flex items-center justify-center mr-4">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <span className="text-xl font-bold text-white font-outfit uppercase tracking-tighter">
            {process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"}
          </span>
        </Link>
        <Link href="/">
          <Button variant="ghost" className="text-slate-400 hover:text-white gap-2">
            <ChevronLeft className="h-4 w-4" />
            Retour à l&apos;accueil
          </Button>
        </Link>
      </nav>

      <main className="relative z-10 pt-40 pb-32 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-500 text-[10px] font-black uppercase tracking-widest mb-8">
            <ShieldCheck className="h-3 w-3" />
            Confidentialité
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white font-outfit tracking-tighter uppercase mb-12 italic">
            Données <span className="text-red-500 not-italic">conservées.</span>
          </h1>

          <div className="haunted-panel p-10 md:p-16 space-y-12">
            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Eye className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Collecte des données</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                Le bot ne conserve que les identifiants Discord nécessaires à son fonctionnement :
                identifiant du serveur, des salons, des rôles et des membres concernés par une
                configuration (liste blanche, sanction, compteur d&apos;invitations, expérience). Sont
                également stockés les paramètres que vous enregistrez depuis le dashboard. Le contenu
                des messages n&apos;est conservé que si une fonctionnalité de journalisation ou de
                transcription est explicitement activée par les administrateurs du serveur.
              </p>
            </section>

            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Lock className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Où sont les données</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                Les configurations sont enregistrées dans les bases SQLite du bot, sur son hébergement,
                et ne sont <span className="text-slate-200 font-bold">pas chiffrées au repos</span>.
                L&apos;accès à l&apos;API du bot exige une clé secrète et le dashboard ne conserve aucune
                copie de ces données : il interroge l&apos;API à chaque affichage. Nous ne vendons ni ne
                partageons vos données avec des tiers ; seul Discord (et le service Lavalink configuré
                pour la musique) reçoit les informations nécessaires à son fonctionnement.
              </p>
            </section>

            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <FileText className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Vos droits</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                La suppression des configurations d&apos;un serveur se fait depuis le support (les
                pages du dashboard ne proposent pas encore d&apos;effacement automatique). Si le bot
                quitte un serveur, ses configurations restent en base jusqu&apos;à leur suppression
                manuelle. Vous pouvez demander une copie des données liées à votre serveur auprès du
                même support.
              </p>
            </section>

            <div className="pt-12 border-t border-white/5">
              <p className="text-[10px] font-black uppercase text-slate-600 tracking-[0.4em]">
                Dernière modification : septembre 2026
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
