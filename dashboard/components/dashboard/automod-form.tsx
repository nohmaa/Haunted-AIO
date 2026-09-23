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
  Zap,
  Type,
  Link as LinkIcon,
  MessageSquare,
  UserMinus,
  ShieldAlert,
  Gavel,
  RefreshCcw,
  Save
} from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Select } from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { AutomodConfig } from "@/types/api";

const PUNISHMENT_OPTIONS = [
  { value: "delete", label: "Supprimer le message" },
  { value: "warn", label: "Avertir l'utilisateur" },
  { value: "mute", label: "Rendre l'utilisateur muet" },
  { value: "kick", label: "Expulser l'utilisateur" },
  { value: "ban", label: "Bannir l'utilisateur" },
];

const RULES = [
  { id: 'anti_spam', name: 'Anti-Spam', desc: 'Détecte et supprime les messages répétitifs ou envoyés en rafale.', icon: Zap },
  { id: 'anti_caps', name: 'Anti-Majuscules', desc: 'Empêche l’utilisation excessive de majuscules.', icon: Type },
  { id: 'anti_links', name: 'Anti-Liens', desc: 'Bloque les liens externes non autorisés dans les salons.', icon: LinkIcon },
  { id: 'anti_invites', name: 'Anti-Invitations', desc: 'Supprime automatiquement les liens d’invitation Discord.', icon: MessageSquare },
  { id: 'anti_mentions', name: 'Anti-Mentions massives', desc: 'Protège contre le spam de mentions (@everyone, @here).', icon: UserMinus },
];

interface AutomodFormProps {
  initialConfig: AutomodConfig;
  guildId: string;
}

export function AutomodForm({ initialConfig, guildId }: AutomodFormProps) {
  const [config, setConfig] = useState<AutomodConfig>(initialConfig);
  const [saving, setSaving] = useState(false);

  const handleToggle = (key: string) => {
    setConfig({
      ...config,
      enabled: key === 'master' ? !config.enabled : config.enabled,
    });
  };

  const handlePunishmentChange = (ruleId: string, value: string) => {
    const newPunishments = { ...config.punishments };
    newPunishments[ruleId] = value;
    setConfig({ ...config, punishments: newPunishments });
  };

  const handleSave = async () => {
    setSaving(true);

    const promise = api.updateAutomod(guildId, {
      enabled: config.enabled,
      punishments: config.punishments,
    });

    toast.promise(promise, {
      loading: 'Enregistrement de la configuration...',
      success: 'Configuration enregistrée avec succès !',
      error: (err) => err.message || 'Échec de la mise à jour des paramètres',
    });

    try {
      await promise;
    } catch (err: any) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3 space-y-6">
        <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl overflow-hidden shadow-xl">
          <div className="p-8 space-y-6">
            <div className="flex items-center justify-between mb-4">
               <h3 className="text-sm font-black uppercase text-slate-500 tracking-widest">Contrôle principal</h3>
               <Switch 
                  checked={config.enabled} 
                  onCheckedChange={() => handleToggle('master')}
               />
            </div>

            <div className="space-y-4">
              {RULES.map((rule) => {
                const isEnabled = config.enabled && config.punishments?.[rule.id] !== undefined;
                return (
                  <div 
                    key={rule.id}
                    className={cn(
                      "p-6 rounded-2xl border transition-all duration-300",
                      config.enabled ? "bg-white/[0.02] border-white/[0.06]" : "bg-white/[0.01] border-white/[0.04] opacity-40 grayscale"
                    )}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                      <div className="flex items-center gap-4">
                        <div className={cn(
                          "h-12 w-12 rounded-xl flex items-center justify-center transition-colors",
                          isEnabled ? "bg-primary/20 text-primary" : "bg-white/[0.05] text-slate-500"
                        )}>
                          <rule.icon className="h-6 w-6" />
                        </div>
                        <div>
                          <h3 className="font-bold text-white">{rule.name}</h3>
                          <p className="text-xs text-slate-500 max-w-xs">{rule.desc}</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                         {isEnabled && (
                           <div className="flex items-center gap-2 animate-in fade-in slide-in-from-right-2 duration-300">
                             <Gavel className="h-4 w-4 text-primary" />
                             <Select 
                               value={config.punishments[rule.id] || "delete"}
                               onValueChange={(val) => handlePunishmentChange(rule.id, val)}
                               options={PUNISHMENT_OPTIONS}
                               className="w-40"
                             />
                           </div>
                         )}
                         <div className="h-8 w-[1px] bg-white/[0.05] hidden sm:block" />
                         <Switch 
                          disabled={!config.enabled}
                          checked={config.punishments?.[rule.id] !== undefined}
                          onCheckedChange={() => {
                            const newPunishments = { ...config.punishments };
                            if (newPunishments[rule.id]) {
                              delete newPunishments[rule.id];
                            } else {
                              newPunishments[rule.id] = "delete";
                            }
                            setConfig({...config, punishments: newPunishments});
                          }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <Button 
              onClick={handleSave}
              disabled={saving}
              className="w-full h-14 text-base font-bold gap-2"
            >
              {saving ? <RefreshCcw className="h-5 w-5 animate-spin" /> : <Save className="h-5 w-5" />}
              Enregistrer les règles de modération
            </Button>
          </div>
        </div>
      </div>

      <div className="space-y-6">
         <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl p-6">
            <h3 className="text-sm font-black uppercase text-slate-500 tracking-widest mb-4">Niveau des logs</h3>
            <div className="space-y-3">
               <div className="p-3 bg-white/[0.02] rounded-xl border border-white/5 flex items-center justify-between">
                  <span className="text-sm text-slate-400">Salon de logs</span>
                  <span className="text-xs font-mono text-primary">#{config.logging_channel || 'Aucun'}</span>
               </div>
               <p className="text-[10px] text-slate-500 italic text-center">Les logs de modération sont automatiquement envoyés dans le salon configuré.</p>
            </div>
         </div>

         <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
              <ShieldAlert className="h-32 w-32 text-white" />
            </div>
            <h3 className="text-sm font-bold text-white mb-2">Automod IA</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">Notre réseau de neurones analyse le contexte des messages pour éviter les faux positifs.</p>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-primary" />
              <span className="text-[10px] font-black uppercase text-primary">V2 Active</span>
            </div>
         </div>
      </div>
    </div>
  );
}
