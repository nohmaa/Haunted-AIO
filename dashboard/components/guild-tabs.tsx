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

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  ShieldCheck, 
  Ticket, 
  BarChart4, 
  FileText, 
  Settings,
  Layers,
  Sword,
  Activity,
  SmilePlus,
  Rocket,
  Shield,
  MessageSquare,
  Sparkles,
  Link as LinkIcon,
  Bot,
  ChevronLeft,
  ChevronRight,
  Volume2,
  Link2,
  Zap,
  Mic,
  Mail
} from "lucide-react";

interface Tab {
  name: string;
  href: string;
  icon: any;
}

export function GuildTabs({ guildId }: { guildId: string }) {
  const pathname = usePathname();
  const scrollContainerRef = React.useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = 200;
      scrollContainerRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  const tabs: Tab[] = [
    { name: "Vue d'ensemble", href: `/dashboard/guild/${guildId}`, icon: Layers },
    { name: "Modules", href: `/dashboard/guild/${guildId}/modules`, icon: Zap },
    { name: "Anti-Nuke", href: `/dashboard/guild/${guildId}/antinuke`, icon: Sword },
    { name: "Auto-modération", href: `/dashboard/guild/${guildId}/automod`, icon: ShieldCheck },
    { name: "Tickets", href: `/dashboard/guild/${guildId}/tickets`, icon: Ticket },
    { name: "Vérification", href: `/dashboard/guild/${guildId}/verification`, icon: Shield },
    { name: "Bienvenue", href: `/dashboard/guild/${guildId}/welcome`, icon: SmilePlus },
    { name: "Invitations", href: `/dashboard/guild/${guildId}/invites`, icon: LinkIcon },
    { name: "Rôles auto", href: `/dashboard/guild/${guildId}/autorole`, icon: Bot },
    { name: "Rôles à réactions", href: `/dashboard/guild/${guildId}/reactionroles`, icon: Activity },
    { name: "Salons temporaires", href: `/dashboard/guild/${guildId}/j2c`, icon: Mic },
    { name: "Rôle vocal", href: `/dashboard/guild/${guildId}/invcrole`, icon: Volume2 },
    { name: "Rôles vanity", href: `/dashboard/guild/${guildId}/vanityroles`, icon: Link2 },
    { name: "Réactions auto", href: `/dashboard/guild/${guildId}/autoreact`, icon: Zap },
    { name: "Rôles perso", href: `/dashboard/guild/${guildId}/customroles`, icon: Sparkles },
    { name: "MP de bienvenue", href: `/dashboard/guild/${guildId}/joindm`, icon: Mail },
    { name: "Niveaux", href: `/dashboard/guild/${guildId}/leveling`, icon: BarChart4 },
    { name: "Journaux", href: `/dashboard/guild/${guildId}/logging`, icon: FileText },
    { name: "Paramètres", href: `/dashboard/guild/${guildId}/settings`, icon: Settings },
  ].filter(tab => tab.href); // Filter out any undefined hrefs

  return (
    <div className="relative group/tabs flex items-center w-full mb-8 sticky top-[64px] z-20 transition-all duration-300">
      {/* Scroll Arrows */}
      <button 
        onClick={() => scroll("left")}
        className="absolute left-[-16px] z-30 p-2 rounded-full bg-white/[0.05] border border-white/[0.08] text-white shadow-xl opacity-0 group-hover/tabs:opacity-100 transition-opacity hover:bg-primary"
      >
        <ChevronLeft className="h-4 w-4" />
      </button>

      {/* Left Fade */}
      <div className="absolute left-0 top-0 bottom-0 w-16 bg-gradient-to-r from-haunted-crypt to-transparent z-10 pointer-events-none opacity-0 group-hover/tabs:opacity-100 transition-opacity" />
      
      <div 
        ref={scrollContainerRef}
        className="flex gap-2 p-1.5 bg-haunted-surface/40 border border-white/[0.05] rounded-[20px] overflow-x-auto no-scrollbar w-full scroll-smooth shadow-2xl shadow-black/20"
      >
        {tabs.map((tab) => {
          const isActive = pathname === tab.href;
          return (
            <Link
              key={tab.name}
              href={tab.href}
              className="shrink-0"
            >
              <div className={cn(
                "flex items-center gap-2.5 px-6 py-2.5 rounded-[14px] text-[11px] font-black uppercase tracking-wider transition-all duration-500 whitespace-nowrap",
                "hover:bg-white/[0.06] hover:text-white",
                isActive 
                  ? "bg-primary text-white shadow-lg shadow-primary/30 ring-1 ring-white/10" 
                  : "text-slate-400 bg-white/[0.02] border border-white/[0.05] hover:border-white/[0.08]"
              )}>
                <tab.icon className={cn("h-3.5 w-3.5", isActive ? "animate-pulse" : "opacity-50")} />
                {tab.name}
              </div>
            </Link>
          );
        })}
      </div>

      {/* Right Fade */}
      <div className="absolute right-0 top-0 bottom-0 w-16 bg-gradient-to-l from-haunted-crypt to-transparent z-10 pointer-events-none opacity-0 group-hover/tabs:opacity-100 transition-opacity" />

      <button 
        onClick={() => scroll("right")}
        className="absolute right-[-16px] z-30 p-2 rounded-full bg-white/[0.05] border border-white/[0.08] text-white shadow-xl opacity-0 group-hover/tabs:opacity-100 transition-opacity hover:bg-primary"
      >
        <ChevronRight className="h-4 w-4" />
      </button>
    </div>
  );
}
