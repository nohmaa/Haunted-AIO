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
import { signIn } from "next-auth/react";
import {
  ShieldCheck,
  BarChart4,
  MessageSquare,
  ChevronRight,
  LayoutDashboard,
  LogIn,
  Sparkles,
  Bot,
  History,
  CheckCircle2,
  ShieldAlert,
  Terminal,
  Users2,
  Lock,
  Gamepad2,
  Music4,
  User,
  Globe,
} from "lucide-react";
import { cn } from "@/lib/utils";

const BRAND = process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted";
const SUPPORT_SERVER = process.env.NEXT_PUBLIC_SUPPORT_SERVER || "https://discord.gg/DvetGPq9q5";
const API_DOCS = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/../docs`;

const FEATURES = [
  {
    title: "Anti-nuke",
    desc: "Surveille les arrivées de rôles, salons et bannissements, puis sanctionne l'auteur du raid.",
    icon: ShieldAlert,
    color: "bg-red-500/10 border-red-500/20 text-red-500",
  },
  {
    title: "Auto-modération",
    desc: "Filtre spam, invitations, majuscules et mentions de masse avant que le salon ne s'embrase.",
    icon: ShieldCheck,
    color: "bg-orange-500/10 border-orange-500/20 text-orange-500",
  },
  {
    title: "Niveaux & classement",
    desc: "XP par message, rôles de palier et cartes de rang dessinées côté bot.",
    icon: BarChart4,
    color: "bg-red-600/10 border-red-600/20 text-red-400",
  },
  {
    title: "Tickets",
    desc: "Panneaux de support par boutons ou menus, catégories, transcriptions et journalisation.",
    icon: MessageSquare,
    color: "bg-slate-500/10 border-slate-500/20 text-slate-300",
  },
];

const MODULES = [
  { name: "Anti-Nuke", desc: "Verrouillage du serveur", icon: ShieldAlert },
  { name: "Vérification", desc: "Arrivées filtrées", icon: CheckCircle2 },
  { name: "Bienvenue", desc: "Messages d'arrivée", icon: Sparkles },
  { name: "Rôles vanity", desc: "Rôles liés au /vanity", icon: Gamepad2 },
  { name: "Rôle automatique", desc: "Rôles dès l'arrivée", icon: User },
  { name: "Salons temporaires", desc: "Vocal à la demande", icon: Music4 },
  { name: "Suivi", desc: "Invitations et départs", icon: History },
  { name: "Invitations", desc: "Classement des invitants", icon: Globe },
  { name: "Rôles sur mesure", desc: "Rôles configurables", icon: Lock },
  { name: "Rôles par réaction", desc: "Menus de rôles", icon: Users2 },
  { name: "Tickets", desc: "Support structuré", icon: MessageSquare },
  { name: "MP de bienvenue", desc: "Message privé d'accueil", icon: Bot },
];

const FAQ = [
  {
    q: "Comment configurer un module ?",
    a: "Connectez-vous avec Discord, choisissez le serveur, puis ouvrez la page du module concerné. Chaque champ est enregistré via l'API du bot et appliqué immédiatement.",
  },
  {
    q: "Qui peut modifier la configuration ?",
    a: "Uniquement les membres disposant de la permission « Gérer le serveur » ou « Administrateur » sur le serveur concerné.",
  },
  {
    q: "Où sont stockées les données ?",
    a: "Dans les bases SQLite du bot, sur son hébergement. Le dashboard ne fait que lire et écrire via l'API, il ne conserve aucune copie.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-haunted-crypt text-slate-200 selection:bg-red-500/30 font-sans overflow-x-hidden">
      {/* Brume de manoir + vignette : pur habillage, derrière le contenu */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-fog" />
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-vignette" />

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-haunted-crypt/80 backdrop-blur-3xl">
        <div className="max-w-6xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-red-600 to-red-900 flex items-center justify-center shadow-lg shadow-red-900/40 border border-white/10">
              <Bot className="h-6 w-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold tracking-tight text-white font-outfit leading-none">{BRAND}</span>
              <span className="text-[9px] font-black uppercase tracking-[0.2em] text-red-500/80 mt-1">
                Tableau de bord
              </span>
            </div>
          </div>

          <div className="hidden lg:flex items-center gap-10 text-[11px] font-black uppercase tracking-widest text-slate-500">
            <Link href="#features" className="hover:text-red-500 transition-colors">
              Fonctionnalités
            </Link>
            <Link href="#modules" className="hover:text-red-500 transition-colors">
              Modules
            </Link>
            <Link href="#stack" className="hover:text-red-500 transition-colors">
              Sous le capot
            </Link>
          </div>

          <button
            onClick={() => signIn("discord", { callbackUrl: "/dashboard" })}
            className="rounded-xl px-6 h-11 font-black uppercase tracking-widest text-[10px] gap-2.5 flex items-center shadow-xl shadow-red-900/20 hover:scale-[1.03] active:scale-95 transition-all bg-gradient-to-r from-red-600 to-red-800 border border-white/10"
          >
            <LogIn className="h-3.5 w-3.5" />
            Ouvrir la console
          </button>
        </div>
      </nav>

      {/* Hero */}
      <header className="relative z-10 pt-44 pb-24 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-3 px-5 py-2 rounded-2xl bg-red-500/[0.04] border border-red-500/10 text-red-400 text-[10px] font-black uppercase tracking-[0.3em] mb-10 backdrop-blur-md">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-red-600" />
            </span>
            Console ouverte, portes closes
          </div>

          <h1 className="text-5xl sm:text-7xl md:text-8xl font-bold text-white tracking-tighter leading-[0.85] mb-8 font-outfit uppercase">
            Le manoir <br />
            <span className="bg-gradient-to-r from-red-500 via-red-400 to-amber-500 bg-clip-text text-transparent italic font-black">
              veille.
            </span>
          </h1>

          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed mb-12">
            {BRAND} garde votre serveur Discord : anti-raid, auto-modération, niveaux, tickets et suivi
            des invitations — pilotés depuis un dashboard sombre, sans ligne de commande.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <button
              onClick={() => signIn("discord", { callbackUrl: "/dashboard" })}
              className="w-full sm:w-auto rounded-2xl px-12 py-7 text-base font-black uppercase gap-4 flex items-center justify-center shadow-[0_0_50px_rgba(127,29,29,0.35)] bg-red-600 text-white hover:bg-red-500 border border-red-400/20 transition-all hover:scale-[1.02]"
            >
              <LayoutDashboard className="h-5 w-5" />
              Ouvrir le tableau de bord
            </button>
            <Link
              href={SUPPORT_SERVER}
              target="_blank"
              rel="noreferrer"
              className="w-full sm:w-auto rounded-2xl px-12 py-7 text-base font-bold border border-white/5 bg-white/[0.02] backdrop-blur-3xl hover:bg-white/[0.05] gap-3 text-white transition-all flex items-center justify-center"
            >
              Rejoindre le serveur support
              <ChevronRight className="h-5 w-5 opacity-40" />
            </Link>
          </div>
        </div>
      </header>

      {/* Fonctionnalités */}
      <section id="features" className="py-24 px-6 relative">
        <div className="max-w-6xl mx-auto">
          <div className="max-w-2xl mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tighter font-outfit mb-6 uppercase">
              Ce qui rôde <span className="text-red-500 italic">la nuit.</span>
            </h2>
            <p className="text-lg text-slate-400 leading-relaxed">
              Quatre garde-fous actifs en permanence, configurables module par module.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {FEATURES.map((feature) => (
              <div
                key={feature.title}
                className="group haunted-panel p-8 hover:border-red-500/25 transition-all duration-500"
              >
                <div className="flex items-start gap-5">
                  <div
                    className={cn(
                      "h-14 w-14 shrink-0 rounded-2xl flex items-center justify-center border transition-transform duration-500 group-hover:scale-105",
                      feature.color
                    )}
                  >
                    <feature.icon className="h-7 w-7" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white mb-3 font-outfit">{feature.title}</h3>
                    <p className="text-sm text-slate-400 leading-relaxed">{feature.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sous le capot */}
      <section id="stack" className="py-24 px-6 bg-white/[0.01] border-y border-white/[0.03]">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <div className="inline-flex px-4 py-1.5 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-[10px] font-black uppercase tracking-[0.3em]">
              Sous le capot
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tighter font-outfit uppercase">
              Une seule maison, <span className="text-slate-500 italic">quatre pièces.</span>
            </h2>
            <p className="text-lg text-slate-400 leading-relaxed">
              Le bot, son API et ce dashboard communiquent par une API REST protégée par clé.
              Pas de magie : uniquement les technologies réellement déployées.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4">
              {[
                { icon: Bot, title: "Bot", desc: "Python + discord.py, commandes préfixe et slash." },
                { icon: Terminal, title: "API", desc: "FastAPI exposée via un tunnel Cloudflare." },
                { icon: LayoutDashboard, title: "Dashboard", desc: "Next.js 16, React 19, Tailwind 4." },
                { icon: Music4, title: "Musique", desc: "Lavalink v4 via wavelink." },
              ].map((item) => (
                <div key={item.title} className="space-y-3 p-6 rounded-3xl border border-white/[0.04] hover:bg-white/[0.02] transition-colors">
                  <item.icon className="h-5 w-5 text-red-500" />
                  <h4 className="text-base font-bold text-white font-outfit uppercase tracking-tight">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-500 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="relative aspect-square hidden lg:flex items-center justify-center">
            <div className="absolute inset-0 bg-red-600/5 blur-[120px] rounded-full" />
            <div className="h-[85%] w-[85%] border border-white/[0.06] rounded-full flex items-center justify-center relative ectoplasm-glow">
              <div className="absolute top-0 left-1/2 -translate-x-1/2 h-3 w-3 rounded-full bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)]" />
              <div className="h-[70%] w-[70%] border border-white/[0.05] rounded-full flex items-center justify-center">
                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 h-2.5 w-2.5 rounded-full bg-teal-300/40" />
                <Bot className="h-16 w-16 text-red-500/40" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Modules */}
      <section id="modules" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 space-y-5">
            <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tighter font-outfit uppercase">
              Les pièces <span className="text-red-500 italic">du manoir.</span>
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              Chaque module s'active ou se désactive depuis le dashboard, serveur par serveur.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {MODULES.map((mod) => (
              <div
                key={mod.name}
                className="group p-6 rounded-3xl bg-white/[0.01] border border-white/[0.04] hover:bg-red-500/[0.02] hover:border-red-500/20 transition-all duration-500"
              >
                <div className="h-12 w-12 rounded-2xl bg-white/[0.03] flex items-center justify-center mb-5 group-hover:bg-red-500/10 transition-colors">
                  <mod.icon className="h-5 w-5 text-slate-500 group-hover:text-red-500 transition-colors" />
                </div>
                <h4 className="text-base font-bold text-white font-outfit mb-1.5 tracking-tight">{mod.name}</h4>
                <p className="text-[11px] text-slate-500 font-bold uppercase tracking-widest">{mod.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-24 px-6 border-t border-white/[0.03]">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-black text-white font-outfit tracking-tighter uppercase mb-4">
              Questions fréquentes
            </h2>
            <div className="haunted-rule w-40 mx-auto" />
          </div>
          <div className="space-y-4">
            {FAQ.map((item) => (
              <div key={item.q} className="p-8 rounded-3xl haunted-panel group">
                <h4 className="text-base font-bold text-white mb-4 font-outfit uppercase tracking-tight flex items-center gap-4">
                  <span className="h-1.5 w-1.5 rounded-full bg-red-500 opacity-40 group-hover:opacity-100 transition-opacity" />
                  {item.q}
                </h4>
                <p className="text-sm text-slate-400 leading-relaxed">{item.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA — accès au dashboard uniquement (pas d'invitation de bot) */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto relative rounded-[48px] p-16 md:p-20 overflow-hidden bg-gradient-to-br from-red-800 to-red-950 border border-red-500/20 text-center shadow-[0_40px_100px_rgba(0,0,0,0.6)]">
          <div className="relative z-10">
            <h2 className="text-4xl md:text-6xl font-bold text-white tracking-tighter font-outfit mb-8 uppercase leading-[0.9] italic">
              Entrer dans <br />
              la console.
            </h2>
            <p className="text-lg text-white/70 max-w-xl mx-auto mb-12">
              Connectez-vous avec Discord pour configurer vos serveurs et surveiller les modules.
            </p>
            <button
              onClick={() => signIn("discord", { callbackUrl: "/dashboard" })}
              className="rounded-2xl px-12 py-6 bg-white text-black hover:bg-slate-100 border-none shadow-[0_20px_50px_rgba(0,0,0,0.4)] font-black text-base uppercase tracking-widest transition-transform hover:scale-[1.03] active:scale-95"
            >
              Se connecter avec Discord
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-white/[0.03] bg-haunted-crypt relative z-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
            <div className="col-span-1 md:col-span-2 space-y-6">
              <span className="text-2xl font-bold text-white font-outfit uppercase tracking-tighter">
                {BRAND}
              </span>
              <p className="text-slate-500 max-w-sm text-xs leading-relaxed uppercase tracking-widest">
                Bot Discord et tableau de bord pour la modération, la sécurité et l'animation de
                communautés.
              </p>
            </div>
            <div className="space-y-6">
              <h4 className="text-[10px] font-black uppercase tracking-[0.4em] text-white opacity-40">Ressources</h4>
              <ul className="space-y-4 text-[11px] font-black uppercase tracking-widest text-slate-500">
                <li>
                  <Link href="/docs" className="hover:text-red-500 transition-colors">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link href={API_DOCS} target="_blank" rel="noreferrer" className="hover:text-red-500 transition-colors">
                    Référence API
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-6">
              <h4 className="text-[10px] font-black uppercase tracking-[0.4em] text-white opacity-40">Identité</h4>
              <ul className="space-y-4 text-[11px] font-black uppercase tracking-widest text-slate-500">
                <li>
                  <Link href="/privacy" className="hover:text-red-500 transition-colors">
                    Confidentialité
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className="hover:text-red-500 transition-colors">
                    Conditions d'utilisation
                  </Link>
                </li>
                <li>
                  <Link href={SUPPORT_SERVER} target="_blank" rel="noreferrer" className="hover:text-red-500 transition-colors">
                    Serveur support
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="pt-10 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-6">
            <p className="text-slate-600 text-[10px] font-black uppercase tracking-[0.4em]">
              © 2026 {BRAND} — Tous droits réservés
            </p>
            <div className="flex items-center gap-3 text-[10px] font-black text-red-500/70 uppercase tracking-[0.3em]">
              <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
              Console privée
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
