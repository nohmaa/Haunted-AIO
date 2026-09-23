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

import React, { useMemo, useState } from "react";
import Link from "next/link";
import { Bot, BookOpen, Menu, Search, X } from "lucide-react";
import { cn } from "@/lib/utils";

const BRAND = process.env.NEXT_PUBLIC_BRAND_NAME || "Haunted";

type DocPage = {
  name: string;
  description: string;
  intro: string;
  bullets: string[];
};

const DOCS_NAV: { title: string; items: DocPage[] }[] = [
  {
    title: "Pour commencer",
    items: [
      {
        name: "Introduction",
        description: "Ce que fait le bot.",
        intro: `${BRAND} est un bot Discord accompagné de son propre tableau de bord. Le bot applique la configuration, le dashboard la pilote.`,
        bullets: [
          "Le bot tourne en Python (discord.py) et expose une API FastAPI protégée par clé.",
          "Le dashboard (Next.js) appelle cette API côté serveur : il n'expose jamais la clé dans le navigateur.",
          "Les configurations sont stockées dans les bases SQLite du bot, sur son hébergement.",
        ],
      },
      {
        name: "Démarrage rapide",
        description: "Trois étapes.",
        intro: "Tout se configure depuis le dashboard, sans ligne de commande.",
        bullets: [
          "Connectez-vous avec Discord (bouton sur la page d'accueil).",
          "Ouvrez « Serveurs », puis choisissez un serveur où vous avez la permission « Gérer le serveur ».",
          "Choisissez un module dans la colonne de gauche, modifiez les champs et enregistrez.",
        ],
      },
      {
        name: "Architecture",
        description: "Bot, API et dashboard.",
        intro: "La même maison, trois pièces reliées par une API REST.",
        bullets: [
          "Bot : connexion Discord, commandes préfixe et slash, modules d'événements.",
          "API : FastAPI exposée via un tunnel Cloudflare, authentifiée par une clé Bearer.",
          "Dashboard : rendu côté serveur, donc les données affichées viennent directement de l'API du bot.",
          "Musique : lecture via Lavalink v4 (wavelink).",
        ],
      },
    ],
  },
  {
    title: "Sécurité",
    items: [
      {
        name: "Anti-Nuke",
        description: "Contre les raids et sabotages.",
        intro: "L'anti-nuke surveille les actions destructrices et sanctionne leur auteur.",
        bullets: [
          "Surveille notamment les créations et suppressions de salons et de rôles, les bannissements et l'ajout de bots.",
          "Une liste blanche permet d'épargner les administrateurs de confiance.",
          "Le statut (activé / désactivé) et la liste blanche se règlent sur la page Anti-Nuke.",
        ],
      },
      {
        name: "Vérification",
        description: "Filtrer les arrivées.",
        intro: "La vérification retient les nouveaux membres jusqu'à validation.",
        bullets: [
          "Définissez le salon de vérification, le rôle accordé après validation et le salon de journalisation.",
          "La méthode de vérification est enregistrée par serveur.",
          "Le module peut être activé ou désactivé d'un clic.",
        ],
      },
      {
        name: "Automod",
        description: "Filtres automatiques.",
        intro: "L'automod agit avant que la modération humaine n'intervienne.",
        bullets: [
          "Règles disponibles : spam, liens d'invitation, majuscules, mentions de masse, messages répétés.",
          "Chaque règle a sa sanction, et des rôles ou salons peuvent être ignorés.",
          "Un salon de journalisation conserve la trace des sanctions.",
        ],
      },
    ],
  },
  {
    title: "Animation & support",
    items: [
      {
        name: "Salons temporaires",
        description: "Vocal à la demande.",
        intro: "Le module « rejoindre pour créer » ouvre un salon vocal à chaque arrivée.",
        bullets: [
          "Renseignez le salon d'accueil (celui que les membres rejoignent) et la catégorie de création.",
          "Un salon de contrôle permet d'administrer les salons créés.",
        ],
      },
      {
        name: "Niveaux",
        description: "XP et classement.",
        intro: "Le module de niveaux récompense l'activité écrite.",
        bullets: [
          "XP par message et délai entre deux gains sont configurables.",
          "Un salon d'annonce peut recevoir les montées de niveau.",
          "Le classement du serveur est consultable depuis le dashboard.",
        ],
      },
      {
        name: "Tickets",
        description: "Support structuré.",
        intro: "Le module de tickets ouvre un salon privé par demande.",
        bullets: [
          "Choisissez le salon du panneau, le type d'affichage (boutons ou menu) et les rôles du staff.",
          "Chaque catégorie de ticket possède son nom et son icône.",
          "Les échanges sont journalisés dans le salon défini.",
        ],
      },
    ],
  },
];

const ALL_PAGES = DOCS_NAV.flatMap((section) => section.items);

export default function DocsPage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(ALL_PAGES[0].name);
  const [query, setQuery] = useState("");

  const filteredSections = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return DOCS_NAV;
    return DOCS_NAV.map((section) => ({
      ...section,
      items: section.items.filter(
        (item) =>
          item.name.toLowerCase().includes(needle) ||
          item.description.toLowerCase().includes(needle)
      ),
    })).filter((section) => section.items.length > 0);
  }, [query]);

  const active = ALL_PAGES.find((item) => item.name === activeTab) || ALL_PAGES[0];

  return (
    <div className="min-h-screen bg-haunted-crypt text-slate-200 font-sans">
      {/* Habillage : brume de manoir */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-fog" />
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 haunted-vignette" />

      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/[0.03] bg-haunted-crypt/80 backdrop-blur-3xl px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-red-600 to-red-900 border border-white/10 flex items-center justify-center">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-bold text-white font-outfit uppercase tracking-tighter hidden md:block">
              Documentation {BRAND}
            </span>
          </Link>

          <div className="hidden lg:flex items-center w-80 relative group">
            <Search className="absolute left-4 h-4 w-4 text-slate-500 group-focus-within:text-red-500 transition-colors" />
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Filtrer les sections..."
              aria-label="Filtrer les sections de la documentation"
              className="w-full bg-white/[0.03] border border-white/5 rounded-2xl py-2.5 pl-12 pr-4 text-xs font-bold text-slate-300 focus:outline-none focus:ring-1 focus:ring-red-500/30 focus:bg-white/[0.05] transition-all placeholder:text-slate-600"
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            className="lg:hidden p-2 text-slate-400"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            aria-label="Ouvrir la navigation de la documentation"
          >
            {isSidebarOpen ? <X /> : <Menu />}
          </button>
          <Link
            href="/"
            className="text-slate-400 hover:text-white text-xs font-black uppercase tracking-widest transition-colors"
          >
            Quitter la documentation
          </Link>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto flex pt-20">
        {/* Sommaire */}
        <aside
          className={cn(
            "fixed inset-y-0 left-0 z-40 w-80 bg-haunted-crypt border-r border-white/5 pt-20 transition-transform lg:translate-x-0 lg:static lg:bg-transparent",
            isSidebarOpen ? "translate-x-0" : "-translate-x-full"
          )}
        >
          <div className="h-full p-8 overflow-y-auto no-scrollbar">
            {filteredSections.length === 0 && (
              <p className="text-[11px] font-bold text-slate-500">
                Aucune section ne correspond à « {query} ».
              </p>
            )}
            {filteredSections.map((section) => (
              <div key={section.title} className="mb-10">
                <h4 className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-600 mb-6">
                  {section.title}
                </h4>
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
                          ? "bg-red-500/10 border border-red-500/20 haunted-glow"
                          : "hover:bg-white/[0.02] border border-transparent"
                      )}
                    >
                      <span
                        className={cn(
                          "text-sm font-bold",
                          activeTab === item.name ? "text-red-500" : "text-slate-300"
                        )}
                      >
                        {item.name}
                      </span>
                      <span className="text-[10px] text-slate-600 font-bold uppercase tracking-tight">
                        {item.description}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Contenu */}
        <main className="flex-1 p-8 lg:p-16 relative z-10 max-w-4xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-[10px] font-black uppercase tracking-widest mb-8">
            <BookOpen className="h-3 w-3" />
            Documentation du dashboard
          </div>

          <h1 className="text-4xl md:text-5xl font-bold text-white font-outfit tracking-tighter uppercase mb-8 italic">
            {active.name}
            <span className="text-red-500 not-italic">.</span>
          </h1>

          <p className="text-lg text-slate-400 mb-12 leading-relaxed">{active.intro}</p>

          <div className="haunted-panel p-8">
            <div className="haunted-rule mb-8" />
            <ul className="space-y-5">
              {active.bullets.map((line) => (
                <li key={line} className="flex gap-4 text-sm text-slate-300 leading-relaxed">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500/60" />
                  {line}
                </li>
              ))}
            </ul>
          </div>

          <p className="mt-10 text-xs text-slate-500 leading-relaxed">
            Une question qui n&apos;est pas traitée ici ? Le serveur support est accessible depuis le
            dashboard (menu de profil) ou depuis le pied de page de l&apos;accueil.
          </p>
        </main>
      </div>
    </div>
  );
}
