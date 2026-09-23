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
import { Bot, ChevronLeft, Scale, Terminal, ShieldAlert, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans">
      {/* Background Decor */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-red-600/[0.03] blur-[120px] rounded-full" />
      </div>

      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-[#020617]/80 backdrop-blur-3xl px-6 h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-4 group">
          <div className="h-10 w-10 rounded-xl bg-red-600 flex items-center justify-center group-hover:rotate-12 transition-transform">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <span className="text-xl font-bold text-white font-outfit uppercase tracking-tighter">{process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"} Engine</span>
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
            <Scale className="h-3 w-3" />
            Protocole neuronal v2.4
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white font-outfit tracking-tighter uppercase mb-12 italic text-right">
            Conditions d&apos;<span className="text-red-500 not-italic">Utilisation.</span>
          </h1>

          <div className="glass border-white/5 rounded-[40px] p-10 md:p-16 space-y-12 bg-gradient-to-br from-white/[0.01] to-transparent">
            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Terminal className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Acceptation du protocole</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                En intégrant le moteur {process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"} à votre serveur Discord, vous acceptez de respecter ces conditions. Le moteur est fourni « en l&apos;état » et, malgré notre objectif de 100 % de disponibilité grâce à nos clusters edge neuronaux, nous ne sommes pas responsables des pertes de données liées aux interruptions d&apos;API tierces.
              </p>
            </section>

            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <ShieldAlert className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Restrictions d&apos;utilisation</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                Vous ne pouvez pas utiliser le moteur {process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"} pour des activités illicites, notamment : harcèlement automatisé, vol de tokens ou coordination de raids. Toute infraction entraînera une désautorisation neuronale immédiate et un bannissement du réseau mondial de clusters.
              </p>
            </section>

            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Cpu className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">API et mise à l&apos;échelle</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                Nous nous réservons le droit de limiter l&apos;accès à l&apos;API pour les serveurs dépassant une allocation disproportionnée de ressources. Des clusters entreprise à grande échelle sont disponibles pour les communautés nécessitant des shards neuronaux dédiés.
              </p>
            </section>

            <div className="pt-12 border-t border-white/5">
              <p className="text-[10px] font-black uppercase text-slate-600 tracking-[0.4em]">
                Mars 2026 // Distribué via {process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"} Neural Cloud
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
