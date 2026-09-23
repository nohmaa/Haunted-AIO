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

import React, { useState, useEffect, use } from "react";
import { Link2, RefreshCcw, Plus, Trash2, Info, Save } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";

export const dynamic = "force-dynamic";

export default function VanityRolesPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = use(params);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [roles, setRoles] = useState<any[]>([]);
  const [channels, setChannels] = useState<any[]>([]);
  const [setups, setSetups] = useState<any[]>([]);
  const [newSetup, setNewSetup] = useState({ vanity: "", role_id: "", log_channel_id: "" });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [setupsData, rolesData, channelsData] = await Promise.all([
        api.getVanityRoles(guildId),
        api.getRoles(guildId),
        api.getChannels(guildId),
      ]);
      setSetups(setupsData);
      setRoles(rolesData);
      setChannels(channelsData);
    } catch (error) {
      console.error("Échec de récupération des rôles vanity :", error);
      toast.error("Échec du chargement des rôles vanity");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [guildId]);

  const textChannels = channels.filter(c => c.type === "0" || c.type === 0);
  const filteredRoles = roles.filter(r => r.name !== "@everyone");

  const handleAdd = async () => {
    if (!newSetup.vanity || !newSetup.role_id || !newSetup.log_channel_id) {
      toast.error("Veuillez remplir tous les champs");
      return;
    }
    setSaving(true);
    try {
      await api.addVanityRole(guildId, {
        vanity: newSetup.vanity,
        role_id: newSetup.role_id,
        log_channel_id: newSetup.log_channel_id,
      });
      toast.success("Configuration vanity ajoutée !");
      setNewSetup({ vanity: "", role_id: "", log_channel_id: "" });
      fetchData();
    } catch (error) {
      toast.error("Échec de l’ajout de la configuration vanity");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (vanity: string) => {
    try {
      await api.deleteVanityRole(guildId, vanity);
      toast.success("Configuration vanity supprimée");
      fetchData();
    } catch (error) {
      toast.error("Échec de la suppression de la configuration vanity");
    }
  };

  const formatColor = (decimal: number) => {
    if (!decimal || decimal === 0) return "#94a3b8";
    return `#${decimal.toString(16).padStart(6, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <RefreshCcw className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Link2 className="h-6 w-6 text-primary" />
            Rôles vanity
          </h2>
          <p className="text-slate-400 mt-1">Offrez des rôles aux membres avec votre lien vanity/invitation en statut.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-3 space-y-6">
          <div className="bg-[#141B2D] border border-slate-800 rounded-3xl overflow-hidden shadow-xl p-8 space-y-8">
            
            {/* Add New Setup */}
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-primary/10 text-primary"><Plus className="h-5 w-5" /></div>
                <h4 className="font-bold text-white text-base">Ajouter une configuration vanity</h4>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400">Texte / URL vanity</label>
                  <Input
                    placeholder="ex. .gg/mon-serveur"
                    value={newSetup.vanity}
                    onChange={(e) => setNewSetup({ ...newSetup, vanity: e.target.value })}
                    className="bg-slate-900/50 border-slate-800 h-12"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400">Rôle à offrir</label>
                  <Select value={newSetup.role_id} onValueChange={(val) => setNewSetup({ ...newSetup, role_id: val })}>
                    <SelectTrigger className="w-full h-12 bg-slate-900/50 border-slate-800">
                      <SelectValue placeholder="Choisir un rôle…" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-900 border-slate-800 max-h-[300px]">
                      {filteredRoles.map((r) => (
                        <SelectItem key={r.id} value={r.id} className="focus:bg-slate-800">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: formatColor(r.color) }} />
                            {r.name}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400">Salon de logs</label>
                  <Select value={newSetup.log_channel_id} onValueChange={(val) => setNewSetup({ ...newSetup, log_channel_id: val })}>
                    <SelectTrigger className="w-full h-12 bg-slate-900/50 border-slate-800">
                      <SelectValue placeholder="Choisir un salon…" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-900 border-slate-800 max-h-[300px]">
                      {textChannels.map((c) => (
                        <SelectItem key={c.id} value={c.id} className="focus:bg-slate-800">#{c.name}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button onClick={handleAdd} disabled={saving} className="w-full gap-2" variant="secondary">
                {saving ? <RefreshCcw className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
                Ajouter la configuration
              </Button>
            </div>

            {/* Configurations actives */}
            <div className="pt-6 border-t border-slate-800 space-y-4">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <Link2 className="h-5 w-5 text-primary" /> Configurations actives
              </h4>
              {setups.length === 0 ? (
                <div className="text-center p-8 bg-slate-900/20 rounded-2xl border border-dashed border-slate-700">
                  <Link2 className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                  <p className="text-sm text-slate-500">Aucune configuration vanity pour l’instant.</p>
                </div>
              ) : (
                setups.map((setup, index) => {
                  const role = filteredRoles.find(r => r.id === String(setup.role_id));
                  const channel = channels.find(c => c.id === String(setup.log_channel_id));
                  return (
                    <div key={index} className="flex items-center justify-between p-4 bg-slate-900/40 rounded-xl border border-slate-800 animate-in zoom-in-95 duration-200">
                      <div className="flex items-center gap-8">
                        <div className="flex flex-col">
                          <span className="text-[10px] uppercase font-bold text-slate-500">Texte vanity</span>
                          <span className="font-medium text-primary">{setup.vanity}</span>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[10px] uppercase font-bold text-slate-500">Rôle</span>
                          <span className="font-medium text-slate-200">{role?.name || "Unknown"}</span>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-[10px] uppercase font-bold text-slate-500">Salon de logs</span>
                          <span className="font-medium text-slate-200">#{channel?.name || "Unknown"}</span>
                        </div>
                      </div>
                      <Button variant="ghost" size="sm" onClick={() => handleDelete(setup.vanity)} className="text-red-400 hover:text-red-300 hover:bg-red-400/10 h-8 w-8 p-0">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
              <Link2 className="h-32 w-32 text-primary" />
            </div>
            <div className="flex items-center gap-2 mb-4">
              <Info className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-bold text-white">Comment ça marche</h3>
            </div>
            <ul className="text-xs text-slate-500 space-y-2">
              <li>• Le bot surveille les statuts personnalisés des membres.</li>
              <li>• Si un membre ajoute le texte vanity, le rôle est attribué.</li>
              <li>• Retirer le texte retire le rôle.</li>
              <li>• Les logs sont envoyés dans le salon configuré.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
