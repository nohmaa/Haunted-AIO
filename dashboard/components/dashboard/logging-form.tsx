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
import { 
  MessageSquare,
  UserPlus,
  ShieldAlert,
  Mic,
  Settings,
  Hash,
  ChevronRight,
  BellRing,
  Info
} from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Select } from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { LoggingConfig, DiscordChannel } from "@/types/api";

const LOG_CATEGORIES = [
  { id: "message_events", name: "Messages", icon: MessageSquare, description: "Journalise les suppressions, modifications et suppressions groupées de messages." },
  { id: "join_leave_events", name: "Arrivées & Départs", icon: UserPlus, description: "Suit les arrivées et les départs des membres du serveur." },
  { id: "member_moderation", name: "Modération", icon: ShieldAlert, description: "Journalise les expulsions, bannissements et exclusions temporaires." },
  { id: "voice_events", name: "Événements vocaux", icon: Mic, description: "Suit les connexions, déconnexions et déplacements dans les salons vocaux." },
  { id: "role_events", name: "Changements de rôles", icon: Settings, description: "Journalise la création, la suppression et la modification des rôles." },
  { id: "channel_events", name: "Changements de salons", icon: Hash, description: "Suit la création, la suppression et la modification des salons." },
];

interface LoggingFormProps {
  initialConfig: LoggingConfig;
  channels: DiscordChannel[];
  guildId: string;
}

export function LoggingForm({ initialConfig, channels, guildId }: LoggingFormProps) {
  const [config, setConfig] = useState<LoggingConfig>(initialConfig);
  const [saving, setSaving] = useState(false);

  const handleToggle = async (categoryId: string, enabled: boolean) => {
    // Optimistic update
    const newLogEnabled = { ...config.log_enabled, [categoryId]: enabled };
    setConfig({ ...config, log_enabled: newLogEnabled });

    try {
      await api.updateLogging(guildId, {
        log_enabled: { [categoryId]: enabled }
      });
      toast.success(`Journalisation ${categoryId.replace('_', ' ')} ${enabled ? 'activée' : 'désactivée'}`);
    } catch (err: any) {
      setConfig(config);
      toast.error("Échec de la mise à jour du paramètre de journalisation.");
    }
  };

  const handleChannelChange = async (categoryId: string, channelId: string) => {
    // Optimistic update
    const newLogChannels = { ...config.log_channels, [categoryId]: parseInt(channelId) };
    setConfig({ ...config, log_channels: newLogChannels });

    setSaving(true);
    const promise = api.updateLogging(guildId, {
      log_channels: { [categoryId]: parseInt(channelId) }
    });

    toast.promise(promise, {
      loading: 'Mise à jour du salon de logs...',
      success: 'Salon de logs mis à jour avec succès',
      error: 'Échec de la mise à jour du salon de logs',
    });

    try {
      await promise;
    } catch (err: any) {
      setConfig(config);
    } finally {
      setSaving(false);
    }
  };

  /** Active ou coupe toutes les catégories d'un coup (écriture réelle côté bot). */
  const handleBulkToggle = async (enabled: boolean) => {
    const previous = config;
    const allEnabled = Object.fromEntries(
      LOG_CATEGORIES.map((cat) => [cat.id, enabled])
    ) as Record<string, boolean>;
    setConfig({ ...config, log_enabled: allEnabled });

    setSaving(true);
    const promise = api.updateLogging(guildId, { log_enabled: allEnabled });
    toast.promise(promise, {
      loading: enabled ? 'Activation de toutes les catégories...' : 'Coupure de toutes les catégories...',
      success: enabled ? 'Toutes les catégories sont actives' : 'Toutes les catégories sont silencieuses',
      error: 'Échec de la mise à jour groupée de la journalisation',
    });

    try {
      await promise;
    } catch {
      setConfig(previous);
    } finally {
      setSaving(false);
    }
  };

  const channelOptions = channels.map(c => ({
    value: c.id.toString(),
    label: `#${c.name}`
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3 space-y-4">
         {LOG_CATEGORIES.map((cat) => (
            <div key={cat.id} className="bg-haunted-surface border border-white/[0.06] p-8 rounded-[40px] shadow-xl hover:border-primary/20 transition-all group">
               <div className="flex flex-col md:flex-row md:items-center justify-between gap-8">
                  <div className="flex items-start gap-5">
                     <div className="h-14 w-14 rounded-2xl bg-white/[0.04] flex items-center justify-center text-slate-400 group-hover:text-primary transition-colors border border-white/5 shrink-0">
                        <cat.icon className="h-7 w-7" />
                     </div>
                     <div className="flex flex-col">
                        <h3 className="text-lg font-black text-white tracking-tight">{cat.name}</h3>
                        <p className="text-[12px] text-slate-500 font-medium leading-relaxed max-w-sm mt-1">
                          {cat.description}
                        </p>
                     </div>
                  </div>

                  <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 md:gap-8 lg:min-w-[320px]">
                     <div className="w-full sm:w-48 lg:w-56">
                        <p className="text-[10px] font-black uppercase text-slate-600 mb-2 tracking-widest pl-1">Destination</p>
                        <Select 
                          value={config.log_channels[cat.id]?.toString() || ""}
                          onValueChange={(val) => handleChannelChange(cat.id, val)}
                          options={channelOptions}
                          placeholder="Sélectionner un salon..."
                          className="bg-black/20 border-white/[0.06] rounded-xl"
                        />
                     </div>

                     <div className="flex items-center gap-4 border-l border-white/[0.05] pl-4 md:pl-8">
                        <div className="flex-col items-end hidden sm:flex">
                           <span className={cn(
                             "text-[10px] font-black uppercase tracking-widest",
                             config.log_enabled[cat.id] ? "text-teal-300" : "text-slate-600"
                           )}>
                             {config.log_enabled[cat.id] ? "Actif" : "Silencieux"}
                           </span>
                        </div>
                        <Switch 
                          checked={!!config.log_enabled[cat.id]} 
                          onCheckedChange={(val) => handleToggle(cat.id, val)}
                        />
                     </div>
                  </div>
               </div>
            </div>
         ))}
      </div>

      <div className="space-y-6">
         <section className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-[40px] p-8 relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
              <BellRing className="h-32 w-32 text-white" />
            </div>
            <div className="flex items-center gap-2 mb-6">
              <Info className="h-5 w-5 text-primary" />
              <h3 className="font-bold text-white text-lg tracking-tight">Moteur de logs</h3>
            </div>
            <div className="space-y-4 relative z-10">
               <div className="p-4 bg-black/20 rounded-2xl border border-white/5 space-y-2">
                  <p className="text-[10px] uppercase font-bold text-slate-500">Routage intelligent</p>
                  <p className="text-xs text-slate-300 leading-relaxed font-medium">Assignez des salons spécifiques aux différents types d'événements pour une meilleure organisation.</p>
               </div>
               <div className="p-4 bg-black/20 rounded-2xl border border-white/5 space-y-2">
                  <p className="text-[10px] uppercase font-bold text-slate-500">Webhooks</p>
                  <p className="text-xs text-slate-300 leading-relaxed font-medium">Bientôt disponible : exportez les logs d'audit vers des webhooks externes.</p>
               </div>
            </div>
            <div className="grid grid-cols-1 gap-3 mt-8">
               <Button
                 onClick={() => handleBulkToggle(true)}
                 disabled={saving}
                 variant="secondary"
                 className="w-full py-6 rounded-[24px] font-black uppercase tracking-tighter text-xs"
               >
                  Activer toutes les catégories
               </Button>
               <Button
                 onClick={() => handleBulkToggle(false)}
                 disabled={saving}
                 variant="outline"
                 className="w-full py-6 rounded-[24px] font-black uppercase tracking-tighter text-xs border-white/[0.08]"
               >
                  Tout passer en silencieux
               </Button>
            </div>
         </section>

         <div className="bg-haunted-surface border border-white/[0.06] rounded-[40px] p-8 shadow-xl">
           <h3 className="text-xs font-black uppercase text-slate-500 tracking-[0.15em] mb-6 flex items-center gap-2">
             <ShieldAlert className="h-4 w-4 text-amber-500" />
             Protection d'audit
           </h3>
           <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-white/[0.02] rounded-xl border border-white/[0.06] hover:border-white/[0.08] transition-colors">
                 <span className="text-xs font-bold text-slate-400">Rôles protégés</span>
                 <span className="bg-white/[0.05] text-slate-300 px-2 py-1 rounded-md text-[10px] font-black">{config.ignore_roles.length}</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-white/[0.02] rounded-xl border border-white/[0.06] hover:border-white/[0.08] transition-colors">
                 <span className="text-xs font-bold text-slate-400">Salons sécurisés</span>
                 <span className="bg-white/[0.05] text-slate-300 px-2 py-1 rounded-md text-[10px] font-black">{config.ignore_channels.length}</span>
              </div>
           </div>
           <p className="text-[10px] text-slate-600 mt-6 leading-relaxed italic text-center">
             Les événements de ces éléments sont actuellement ignorés par le journal d'audit.
           </p>
         </div>
      </div>
    </div>
  );
}
