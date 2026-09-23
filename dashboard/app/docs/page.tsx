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

import React, { useState } from "react";
import Link from "next/link";
import { 
  Bot, 
  ChevronLeft, 
  Search, 
  ShieldCheck, 
  Zap, 
  Activity, 
  Layers, 
  Sparkles,
  Search as SearchIcon,
  BookOpen,
  Menu,
  X
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const DOCS_NAV = [
  {
    title: "Pour commencer",
    items: [
      { name: "Introduction", description: "Découvrez le Neural Core." },
      { name: "Démarrage rapide", description: "Déployé en 30 secondes." },
      { name: "Architecture", description: "Plongée dans notre moteur." }
    ]
  },
  {
    title: "Modules de sécurité",
    items: [
      { name: "Anti-Nuke", description: "Protocoles de verrouillage absolu." },
      { name: "Vérification", description: "Captchas et contrôles neuronaux." },
      { name: "Automod", description: "Filtrage IA contextuel." }
    ]
  },
  {
    title: "Gestion",
    items: [
      { name: "Salons temporaires", description: "Salons vocaux dynamiques." },
      { name: "Niveaux", description: "Génération de rangs cinématiques." },
      { name: "Tickets", description: "Assistance de niveau entreprise." }
    ]
  }
];

export default function DocsPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("Introduction");

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans">
      {/* Background Decor */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-red-500/[0.02] blur-[150px] rounded-full" />
      </div>

      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-[#020617]/80 backdrop-blur-3xl px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-4 group">
            <div className="h-8 w-8 rounded-lg bg-red-600 flex items-center justify-center mr-3">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white font-outfit uppercase tracking-tighter hidden md:block">Documentation Haunted</span>
          </Link>
          
          <div className="hidden lg:flex items-center w-80 relative group">
            <SearchIcon className="absolute left-4 h-4 w-4 text-slate-500 group-focus-within:text-red-500 transition-colors" />
            <input 
              type="text" 
              placeholder="Rechercher dans la documentation..."
              className="w-full bg-white/[0.03] border border-white/5 rounded-2xl py-2.5 pl-12 pr-4 text-xs font-bold text-slate-300 focus:outline-none focus:ring-1 focus:ring-red-500/30 focus:bg-white/[0.05] transition-all"
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
           <button 
             className="lg:hidden p-2 text-slate-400"
             onClick={() => setIsSidebarOpen(!isSidebarOpen)}
           >
             {isSidebarOpen ? <X /> : <Menu />}
           </button>
           <Link href="/">
            <Button variant="ghost" className="text-slate-400 hover:text-white gap-2 text-xs font-black uppercase tracking-widest">
              Quitter la documentation
            </Button>
          </Link>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto flex pt-20">
        {/* Sidebar */}
        <aside className={cn(
          "fixed inset-y-0 left-0 z-40 w-80 bg-[#020617] border-r border-white/5 pt-20 transition-transform lg:translate-x-0 lg:static lg:bg-transparent",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}>
          <div className="h-full p-8 overflow-y-auto no-scrollbar">
            {DOCS_NAV.map((section) => (
              <div key={section.title} className="mb-10">
                <h4 className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-600 mb-6">{section.title}</h4>
                <div className="space-y-1">
                  {section.items.map((item) => (
                    <button
                      key={item.name}
                      onClick={() => {
                        setActiveTab(item.name);
                        setIsSidebarOpen(false);
                      }}
                      className={cn(
                        "w-full flex flex-col items-start gap-1 p-4 rounded-2xl transition-all text-left",
                        activeTab === item.name 
                          ? "bg-red-500/10 border border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.05)]" 
                          : "hover:bg-white/[0.02] border border-transparent"
                      )}
                    >
                      <span className={cn("text-sm font-bold", activeTab === item.name ? "text-red-500" : "text-slate-300")}>{item.name}</span>
                      <span className="text-[10px] text-slate-600 font-bold uppercase tracking-tight">{item.description}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Content */}
        <main className="flex-1 p-8 lg:p-16 relative z-10 max-w-4xl">
           <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-500 text-[10px] font-black uppercase tracking-widest mb-8">
            <BookOpen className="h-3 w-3" />
            Environnement d&apos;exécution v2.4
          </div>

          <h1 className="text-6xl font-bold text-white font-outfit tracking-tighter uppercase mb-8 italic">
            {activeTab}<span className="text-red-500 not-italic">.</span>
          </h1>

          <div className="prose prose-invert max-w-none">
             <p className="text-lg text-slate-400 mb-12 leading-relaxed">
               Bienvenue dans la section {activeTab} de la documentation Haunted Engine. Notre moteur est conçu pour les communautés qui exigent des performances absolues et des outils de gestion cinématiques.
             </p>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-8 rounded-[32px] glass border-white/5 space-y-4">
                   <Zap className="h-6 w-6 text-red-500" />
                   <h3 className="text-xl font-bold text-white font-outfit uppercase">Exécution rapide</h3>
                   <p className="text-sm text-slate-500 font-bold uppercase tracking-tight">Les commandes sont exécutées via notre réseau edge mondial en moins de 12 ms.</p>
                </div>
                <div className="p-8 rounded-[32px] glass border-white/5 space-y-4">
                   <ShieldCheck className="h-6 w-6 text-emerald-500" />
                   <h3 className="text-xl font-bold text-white font-outfit uppercase">Nœud sécurisé</h3>
                   <p className="text-sm text-slate-500 font-bold uppercase tracking-tight">Chaque module s&apos;exécute dans un bac à sable neuronal dédié avec chiffrement AES-256.</p>
                </div>
             </div>

             <div className="p-8 rounded-[40px] bg-red-500/[0.02] border border-red-500/10 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                   <Layers className="h-32 w-32 text-red-500" />
                </div>
                <h2 className="text-2xl font-bold text-white font-outfit uppercase tracking-tight mb-4">Architecture neurale</h2>
                  <h3 className="text-white font-bold">Aperçu du protocole</h3>
                <p className="text-slate-500 font-bold leading-relaxed mb-8">
                  Haunted Engine utilise un modèle décentralisé de traitement de flux d&apos;événements. Lorsqu&apos;un événement Discord est reçu, il est instantanément routé vers le cluster edge le plus proche.
                </p>
                <div className="bg-black/40 p-6 rounded-2xl border border-white/5 font-mono text-sm text-red-500 mb-8">
                  $ haunted initialize --cluster-shard [neural_07] --mode enterprise
                </div>
             </div>
          </div>

          <div className="mt-20 pt-12 border-t border-white/5 flex items-center justify-between">
             <div>
                <p className="text-[10px] font-black uppercase text-slate-600 tracking-[0.4em] mb-2">Réf interne</p>
                <p className="text-sm font-bold text-slate-400">DOC-ID: CX_7749_B</p>
             </div>
             <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
                <span className="text-[10px] font-black uppercase text-red-500 tracking-[0.2em]">Flux en direct actif</span>
             </div>
          </div>
        </main>
      </div>
    </div>
  );
}
