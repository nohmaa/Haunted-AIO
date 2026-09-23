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
import { MousePointer2, Save, RefreshCcw, Plus, Trash2, BellRing, Settings } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";

interface ReactionRolesFormProps {
  initialConfig: any;
  roles: any[];
  guildId: string;
}

export function ReactionRolesForm({ initialConfig, roles, guildId }: ReactionRolesFormProps) {
  const [config, setConfig] = useState<any>(initialConfig);
  const [saving, setSaving] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);

  const [newRR, setNewRR] = useState({
    message_id: "",
    emoji: "",
    role_id: "",
  });

  const filteredRoles = roles.filter(r => r.name !== "@everyone");

  const toggleDM = async (val: boolean) => {
    try {
      await api.updateRR(guildId, { dm_enabled: val });
      setConfig({ ...config, dm_enabled: val });
      toast.success(`Notifications DM ${val ? "activées" : "désactivées"}`);
    } catch (error) {
      toast.error("Échec de la mise à jour des notifications DM");
    }
  };

  const handleAdd = async () => {
    if (!newRR.message_id || !newRR.emoji || !newRR.role_id) {
      toast.error("Veuillez remplir tous les champs");
      return;
    }

    try {
      setLoadingAction(true);
      await api.updateRR(guildId, {
        add_role: {
          message_id: parseInt(newRR.message_id),
          emoji: newRR.emoji,
          role_id: parseInt(newRR.role_id),
        },
      });
      // Try to optimistically add to the UI
      setConfig({
        ...config,
        roles: [...config.roles, { message_id: newRR.message_id, emoji: newRR.emoji, role_id: newRR.role_id }]
      });
      toast.success("Rôle à réaction ajouté");
      setNewRR({ message_id: "", emoji: "", role_id: "" });
    } catch (error) {
      toast.error("Échec de l’ajout du rôle à réaction");
    } finally {
      setLoadingAction(false);
    }
  };

  const handleDelete = async (messageId: number, emoji: string) => {
    try {
      setLoadingAction(true);
      await api.updateRR(guildId, {
        remove_role_message_id: messageId,
        remove_role_emoji: emoji,
      });
      setConfig({
        ...config,
        roles: config.roles.filter((r: any) => !(r.message_id === messageId && r.emoji === emoji))
      });
      toast.success("Rôle à réaction supprimé");
    } catch (error) {
      toast.error("Échec de la suppression du rôle à réaction");
    } finally {
      setLoadingAction(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3 space-y-6">
        <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl shadow-xl p-8 space-y-8">
          
          <div className="flex items-center justify-between p-6 bg-white/[0.02] rounded-2xl border border-white/[0.06]">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary/20 text-primary rounded-xl">
                <BellRing className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white">Notifications DM</h3>
                <p className="text-sm text-slate-400 mt-1">Envoyer un message privé lorsqu’un membre reçoit ou perd un rôle.</p>
              </div>
            </div>
            <Switch 
              checked={config.dm_enabled} 
              onCheckedChange={toggleDM}
              className="scale-125"
            />
          </div>

          <div className="pt-6 border-t border-white/[0.06]">
            <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <Plus className="h-5 w-5 text-primary" />
              Créer un nouveau rôle à réaction
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400">ID du message</label>
                <Input 
                  placeholder="ex. 1234567890" 
                  value={newRR.message_id}
                  onChange={(e) => setNewRR({ ...newRR, message_id: e.target.value })}
                  className="bg-white/[0.02] h-10"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400">Emoji</label>
                <Input 
                  placeholder="ex. ✅" 
                  value={newRR.emoji}
                  onChange={(e) => setNewRR({ ...newRR, emoji: e.target.value })}
                  className="bg-white/[0.02] h-10"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400">Rôle à attribuer</label>
                <Select
                  value={newRR.role_id ? newRR.role_id.toString() : ""}
                  onValueChange={(val) => setNewRR({ ...newRR, role_id: val })}
                >
                  <SelectTrigger className="w-full h-10 bg-white/[0.02] border-white/[0.06]">
                    <SelectValue placeholder="Choisir un rôle..." />
                  </SelectTrigger>
                  <SelectContent className="bg-haunted-surface border-white/[0.06] max-h-[250px]">
                    {filteredRoles.map((role) => (
                      <SelectItem key={role.id} value={role.id.toString()} className="focus:bg-white/[0.05]">
                        {role.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <Button 
              onClick={handleAdd} 
              disabled={loadingAction} 
              className="w-full gap-2"
              variant="secondary"
            >
              {loadingAction ? <RefreshCcw className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
              Ajouter aux écoutes actives
            </Button>
          </div>

          <div className="pt-6 border-t border-white/[0.06]">
            <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <MousePointer2 className="h-5 w-5 text-primary" />
              Rôles à réaction actifs
            </h4>

            <div className="space-y-3">
              {config.roles.length === 0 ? (
                <div className="text-center p-8 bg-white/[0.01] rounded-2xl border border-dashed border-white/[0.08]">
                  <p className="text-sm text-slate-500 italic">Aucun rôle à réaction configuré pour le moment.</p>
                </div>
              ) : (
                config.roles.map((rr: any, idx: number) => {
                  const roleName = roles.find(r => r.id === rr.role_id.toString())?.name || "Rôle inconnu";
                  
                  return (
                    <div key={idx} className="flex items-center justify-between p-4 bg-white/[0.02] rounded-xl border border-white/[0.06]">
                      <div className="flex items-center gap-6">
                        <div className="flex flex-col">
                          <span className="text-[10px] uppercase font-bold text-slate-500">ID du message</span>
                          <span className="text-sm font-mono text-slate-300">{rr.message_id}</span>
                        </div>
                        <div className="flex flex-col items-center">
                          <span className="text-[10px] uppercase font-bold text-slate-500">Emoji</span>
                          <span className="text-lg">{rr.emoji}</span>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[10px] uppercase font-bold text-slate-500">Rôle</span>
                          <span className="text-sm font-medium text-primary">{roleName}</span>
                        </div>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => handleDelete(rr.message_id, rr.emoji)}
                        disabled={loadingAction}
                        className="text-red-400 hover:text-red-300 hover:bg-red-400/10 h-8 w-8 p-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-3xl p-6 relative overflow-hidden group">
          <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
            <MousePointer2 className="h-32 w-32 text-primary" />
          </div>
          <h3 className="text-sm font-bold text-primary mb-2">Guide d’utilisation</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            Les rôles à réaction permettent aux membres de s’attribuer eux-mêmes des rôles en un seul clic.
          </p>
          <ul className="text-xs text-slate-500 space-y-2">
             <li>• Le bot doit avoir accès au message que vous indiquez.</li>
             <li>• Assurez-vous que le rôle du bot est AU-DESSUS du rôle que vous essayez d’attribuer.</li>
             <li>• Le bot réagira automatiquement au message une fois que vous aurez cliqué sur « Ajouter aux écoutes actives ».</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
