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
  ShieldAlert,
  Server,
  User,
  Settings,
  RefreshCcw,
  Save,
  MessageSquare,
  Plus,
  Trash2,
  ShieldCheck
} from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { AntiNukeConfig } from "@/types/api";

const FEATURES = [
  { id: 'anti_ban_kick', name: 'Anti-Ban & Anti-Kick', desc: 'Bannit automatiquement les admins malveillants', icon: User },
  { id: 'anti_server_edit', name: 'Anti-Modification du serveur', desc: 'Protège l’icône, le nom et la région', icon: Server },
  { id: 'anti_role_modifier', name: 'Anti-Modification des rôles', desc: 'Protège tous les rôles et permissions', icon: Settings },
  { id: 'anti_channel_nukes', name: 'Anti-Suppression de salons', desc: 'Empêche la suppression massive des salons', icon: MessageSquare },
];

interface AntiNukeFormProps {
  initialConfig: AntiNukeConfig;
  guildId: string;
}

export function AntiNukeForm({ initialConfig, guildId }: AntiNukeFormProps) {
  const [config, setConfig] = useState<AntiNukeConfig>(initialConfig);
  const [saving, setSaving] = useState(false);
  const [wlInput, setWlInput] = useState("");
  const [whitelistedUsers, setWhitelistedUsers] = useState<string[]>(initialConfig.whitelisted_users || []);

  const handleSave = async () => {
    setSaving(true);
    const promise = api.updateAntiNuke(guildId, config);

    toast.promise(promise, {
      loading: 'Enregistrement de la configuration Anti-Nuke...',
      success: 'Paramètres Anti-Nuke enregistrés avec succès !',
      error: 'Échec de la mise à jour des paramètres Anti-Nuke',
    });

    try {
      await promise;
    } catch (err: any) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleAddWhitelist = async () => {
    if (!wlInput.trim() || isNaN(Number(wlInput))) {
      toast.error('Veuillez saisir un ID d’utilisateur valide');
      return;
    }
    if (whitelistedUsers.includes(wlInput.trim())) {
      toast.error('Cet utilisateur est déjà whitelisté');
      return;
    }

    setSaving(true);
    try {
      await api.updateAntiNuke(guildId, { status: config.status, add_whitelist: wlInput.trim() });
      setWhitelistedUsers([...whitelistedUsers, wlInput.trim()]);
      setWlInput('');
      toast.success('Utilisateur ajouté à la whitelist avec succès');
    } catch (err: any) {
      toast.error('Échec de l’ajout à la whitelist');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleRemoveWhitelist = async (userId: string) => {
    setSaving(true);
    try {
      await api.updateAntiNuke(guildId, { status: config.status, remove_whitelist: userId });
      setWhitelistedUsers(whitelistedUsers.filter(id => id !== userId));
      toast.success('Utilisateur retiré de la whitelist');
    } catch (err: any) {
      toast.error('Échec du retrait de la whitelist');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3 space-y-6">
        <div className="bg-[#141B2D] border border-slate-800 rounded-3xl overflow-hidden shadow-xl">
          <div className="p-8 space-y-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-black uppercase text-slate-500 tracking-widest">Contrôle principal</h3>
              <Switch 
                checked={config.status} 
                onCheckedChange={(val) => setConfig({ ...config, status: val })}
              />
            </div>

            <div className="space-y-4">
              {FEATURES.map((feature) => (
                <div 
                  key={feature.id}
                  className={cn(
                    "p-6 rounded-2xl border transition-all duration-300",
                    config.status ? "bg-slate-900/40 border-slate-800" : "bg-slate-900/10 border-slate-900 opacity-40 grayscale"
                  )}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                    <div className="flex items-center gap-4">
                      <div className={cn(
                        "h-12 w-12 rounded-xl flex items-center justify-center transition-colors",
                        config.status ? "bg-primary/20 text-primary" : "bg-slate-800 text-slate-500"
                      )}>
                        <feature.icon className="h-6 w-6" />
                      </div>
                      <div>
                        <h3 className="font-bold text-white">{feature.name}</h3>
                        <p className="text-xs text-slate-500 max-w-xs">{feature.desc}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                       {config.status && (
                         <div className="flex items-center gap-2 animate-in fade-in slide-in-from-right-2 duration-300">
                           <ShieldAlert className="h-4 w-4 text-emerald-500" />
                           <span className="text-xs font-bold text-emerald-500 uppercase">Protégé</span>
                         </div>
                       )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-6 border-t border-slate-800">
              <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-emerald-500" />
                Utilisateurs whitelistés
              </h4>
              
              <div className="flex gap-2 mb-4">
                <Input 
                  placeholder="ID d’utilisateur..." 
                  value={wlInput}
                  onChange={(e) => setWlInput(e.target.value)}
                  className="bg-slate-900/50"
                />
                <Button onClick={handleAddWhitelist} disabled={saving} variant="secondary">
                  <Plus className="h-5 w-5" />
                </Button>
              </div>

              <div className="space-y-2 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
                {whitelistedUsers.length === 0 ? (
                  <p className="text-xs text-slate-500 italic text-center py-4">Aucun utilisateur whitelisté.</p>
                ) : (
                  whitelistedUsers.map(userId => (
                    <div key={userId} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/30 border border-slate-800/50">
                      <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-full bg-slate-800 flex items-center justify-center">
                          <User className="h-4 w-4 text-slate-400" />
                        </div>
                        <span className="text-sm font-mono text-slate-300">{userId}</span>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => handleRemoveWhitelist(userId)}
                        disabled={saving}
                        className="text-red-400 hover:text-red-300 hover:bg-red-400/10 h-8 w-8 p-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))
                )}
              </div>
            </div>

            <Button 
              onClick={handleSave}
              disabled={saving}
              className="w-full h-14 text-base font-bold gap-2"
            >
              {saving ? <RefreshCcw className="h-5 w-5 animate-spin" /> : <Save className="h-5 w-5" />}
              Enregistrer la configuration
            </Button>
          </div>
        </div>
      </div>

      <div className="space-y-6">
         <div className="bg-gradient-to-br from-red-500/10 to-transparent border border-red-500/20 rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
              <ShieldAlert className="h-32 w-32 text-red-500" />
            </div>
            <h3 className="text-sm font-bold text-red-400 mb-2">Protection maximale</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">L’Anti-Nuke bannit instantanément les utilisateurs malveillants. Assurez-vous que le rôle de Haunted est TOUT EN HAUT de la hiérarchie des rôles pour pouvoir bannir les admins.</p>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
              <span className="text-[10px] font-black uppercase text-red-500">Sanctions fixes</span>
            </div>
         </div>
      </div>
    </div>
  );
}
