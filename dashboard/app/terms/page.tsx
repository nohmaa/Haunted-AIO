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
    <div className="min-h-screen bg-haunted-crypt text-slate-200 font-sans">
      {/* Habillage : brume de manoir */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-fog" />
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-vignette" />

      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-haunted-crypt/80 backdrop-blur-3xl px-6 h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-4 group">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-red-600 to-red-900 border border-white/10 flex items-center justify-center group-hover:rotate-6 transition-transform">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <span className="text-xl font-bold text-white font-outfit uppercase tracking-tighter">{process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"}</span>
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
            Conditions d'utilisation
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white font-outfit tracking-tighter uppercase mb-12 italic text-right">
            Conditions d&apos;<span className="text-red-500 not-italic">Utilisation.</span>
          </h1>

          <div className="haunted-panel p-10 md:p-16 space-y-12">
            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Terminal className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Acceptation</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                En utilisant {process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted"} ou son dashboard, vous
                acceptez ces conditions. Le service est fourni « en l&apos;état », sans garantie de
                disponibilité : le bot peut être interrompu par son hébergement, par une coupure du
                tunnel reliant l&apos;API ou par une panne de Discord. Les configurations restent sous
                votre responsabilité ; sauvegardez les valeurs importantes avant une modification.
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
                L&apos;utilisation du bot pour harceler, raider, usurper une identité ou contourner les
                protections d&apos;un serveur est interdite. La liste noire du bot et l&apos;accès au
                dashboard peuvent être retirés sans préavis en cas d&apos;usage abusif, et le bot peut
                être retiré d&apos;un serveur à tout moment.
              </p>
            </section>

            <section className="space-y-6">
              <div className="flex items-center gap-4 text-white">
                <div className="h-10 w-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-red-500">
                   <Cpu className="h-5 w-5" />
                </div>
                <h2 className="text-2xl font-bold font-outfit uppercase tracking-tight">Accès à l&apos;API</h2>
              </div>
              <p className="text-slate-400 leading-relaxed font-medium">
                L&apos;API du bot est privée : elle exige une clé et son usage est réservé au dashboard.
                Les requêtes sont limitées en débit, et un usage automatisé excessif peut entraîner un
                blocage temporaire des appels.
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
