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
import { Link2, Trash2, Plus, RefreshCcw, Save } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { VanityRoleSetup, DiscordChannel } from "@/types/api";

interface VanityRoleFormProps {
  initialSetups: VanityRoleSetup[];
  channels: DiscordChannel[];
  roles: any[];
  guildId: string;
}

export function VanityRoleForm({ initialSetups, channels, roles, guildId }: VanityRoleFormProps) {
  const [setups, setSetups] = useState<VanityRoleSetup[]>(initialSetups);
  const [saving, setSaving] = useState(false);
  
  const textChannels = channels.filter(c => c.type === "0" || c.type === "text" || !c.type); // ensure text channels

  const [newVanity, setNewVanity] = useState("");
  const [newRole, setNewRole] = useState<string | null>(null);
  const [newChannel, setNewChannel] = useState<string | null>(null);

  const handleCreate = async () => {
    if (!newVanity || !newRole || !newChannel) {
      toast.error("Veuillez remplir tous les champs (vanity, rôle, salon).");
      return;
    }

    setSaving(true);
    try {
      await api.addVanityRole(guildId, {
        vanity: newVanity,
        role_id: newRole,
        log_channel_id: newChannel
      });
      setSetups([...setups, { vanity: newVanity, role_id: newRole, log_channel_id: newChannel }]);
      setNewVanity("");
      setNewRole(null);
      setNewChannel(null);
      toast.success("Configuration de rôle vanity ajoutée !");
    } catch (err) {
      toast.error("Échec de l'ajout de la configuration de rôle vanity.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (vanity: string) => {
    setSaving(true);
    try {
      await api.deleteVanityRole(guildId, vanity);
      setSetups(setups.filter(s => s.vanity !== vanity));
      toast.success("Configuration de rôle vanity supprimée.");
    } catch (err) {
      toast.error("Échec de la suppression de la configuration de rôle vanity.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* List Existing Ones */}
      <div className="bg-[#141B2D] border border-slate-800 rounded-3xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Rôles vanity actifs</h3>
        
        {setups.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-10 text-slate-500">
            <Link2 className="h-12 w-12 mb-4 opacity-50 bg-slate-800 p-2 rounded-xl" />
            <p>Aucun rôle vanity configuré pour le moment.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {setups.map((setup, idx) => {
              const r = roles.find(ro => ro.id.toString() === setup.role_id?.toString());
              const c = channels.find(ch => ch.id.toString() === setup.log_channel_id?.toString());
              return (
                <div key={idx} className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 relative group">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="font-bold text-lg text-primary">{setup.vanity}</h4>
                    <Button 
                      variant="destructive" 
                      size="icon" 
                      onClick={() => handleDelete(setup.vanity)}
                      disabled={saving}
                      className="opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-slate-400">Rôle :</span>
                      <span className="text-white font-medium">
                        {r ? r.name : setup.role_id}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-slate-400">Salon de logs :</span>
                      <span className="text-white font-medium">
                        {c ? `#${c.name}` : setup.log_channel_id}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Add New Setup */}
      <div className="bg-[#141B2D] border border-slate-800 rounded-3xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-white mb-6">Ajouter un nouveau rôle vanity</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-3">
            <label className="text-sm font-bold text-slate-300">Code vanity</label>
            <Input 
              value={newVanity}
              onChange={(e) => setNewVanity(e.target.value)}
              placeholder="ex. zyx"
              className="h-12 bg-slate-900 border-slate-800"
            />
          </div>
          
          <div className="space-y-3">
            <label className="text-sm font-bold text-slate-300">Rôle récompense</label>
            <Select
              value={newRole || ""}
              onValueChange={(val) => setNewRole(val)}
            >
              <SelectTrigger className="w-full h-12 bg-slate-900 border-slate-800 text-left">
                <SelectValue placeholder="Sélectionner un rôle..." />
              </SelectTrigger>
              <SelectContent className="bg-slate-900 border-slate-800">
                {roles.map((r) => (
                  <SelectItem key={r.id} value={r.id.toString()} className="focus:bg-slate-800">
                    {r.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-3">
            <label className="text-sm font-bold text-slate-300">Salon de logs</label>
            <Select
              value={newChannel || ""}
              onValueChange={(val) => setNewChannel(val)}
            >
              <SelectTrigger className="w-full h-12 bg-slate-900 border-slate-800 text-left">
                <SelectValue placeholder="Sélectionner un salon de logs..." />
              </SelectTrigger>
              <SelectContent className="bg-slate-900 border-slate-800">
                {textChannels.map((c) => (
                  <SelectItem key={c.id} value={c.id.toString()} className="focus:bg-slate-800">
                    # {c.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Button 
          onClick={handleCreate}
          disabled={saving}
          className="w-full h-14 mt-8 font-bold gap-2 text-base"
        >
          {saving ? <RefreshCcw className="h-5 w-5 animate-spin" /> : <Plus className="h-5 w-5" />}
          Ajouter la configuration vanity
        </Button>
      </div>

    </div>
  );
}
