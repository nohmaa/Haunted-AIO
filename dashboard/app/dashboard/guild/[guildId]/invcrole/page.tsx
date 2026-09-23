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
import { Volume2, Save, RefreshCcw, ShieldCheck, Info, Power } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";

export const dynamic = "force-dynamic";

export default function InvcRolePage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = use(params);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [roles, setRoles] = useState<any[]>([]);
  const [config, setConfig] = useState<any>({ role_id: null, enabled: false });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [configData, rolesData] = await Promise.all([
        api.getInvcRole(guildId),
        api.getRoles(guildId),
      ]);
      setConfig(configData);
      setRoles(rolesData);
    } catch (error) {
      console.error("Échec de récupération des données du rôle vocal :", error);
      toast.error("Échec du chargement de la configuration du rôle vocal");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [guildId]);

  const handleSave = async () => {
    setSaving(true);
    const promise = api.updateInvcRole(guildId, { 
      role_id: config.role_id,
      enabled: config.enabled
    });
    toast.promise(promise, {
      loading: 'Enregistrement…',
      success: 'Rôle vocal enregistré !',
      error: 'Échec de l’enregistrement',
    });
    try { await promise; } catch {} finally { setSaving(false); }
  };

  const filteredRoles = roles.filter(r => r.name !== "@everyone");

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <RefreshCcw className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  const formatColor = (decimal: number) => {
    if (!decimal || decimal === 0) return "#94a3b8";
    return `#${decimal.toString(16).padStart(6, '0')}`;
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Volume2 className="h-6 w-6 text-primary" />
            Rôle vocal
          </h2>
          <p className="text-slate-400 mt-1">Attribue automatiquement un rôle quand un membre rejoint un salon vocal.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-3 space-y-6">
          <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl overflow-hidden shadow-xl p-8 space-y-8">
            
            {/* Status & Toggle */}
            <div className="flex items-center justify-between p-6 bg-white/[0.02] rounded-2xl border border-white/[0.06]">
              <div className="flex items-center gap-4">
                <div className={cn("p-3 rounded-xl transition-colors", config.enabled ? "bg-teal-300/20 text-teal-300" : "bg-red-500/20 text-red-500")}>
                  <Power className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-black text-white">Système de rôle vocal</h3>
                  <p className="text-sm text-slate-400 mt-1">{config.enabled ? "Le système est actif et surveille les salons." : "Le système est désactivé."}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="px-3 py-1 rounded-full bg-haunted-surface border border-white/[0.06] flex items-center gap-2">
                  <div className={cn("w-2 h-2 rounded-full", config.enabled ? 'bg-teal-400 animate-pulse' : 'bg-red-500')} />
                  <span className="text-[10px] font-bold uppercase text-slate-400">
                    {config.enabled ? 'En direct' : 'Coupé'}
                  </span>
                </div>
                <Switch 
                  checked={config.enabled} 
                  onCheckedChange={(checked) => setConfig({ ...config, enabled: checked })}
                  className="data-[state=checked]:bg-teal-400"
                />
              </div>
            </div>

            {/* Role Selector */}
            <div className={cn("p-6 border rounded-2xl space-y-4 transition-all duration-300", 
              config.enabled ? "bg-white/[0.02] border-white/[0.06] opacity-100" : "bg-white/[0.01] border-white/[0.04] opacity-50 pointer-events-none grayscale")}>
              <div className="flex items-center gap-3">
                <div className="p-3 bg-primary/20 text-primary rounded-xl">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-white">Rôle de présence vocale</h4>
                  <p className="text-xs text-slate-400 mt-1">Choisissez le rôle attribué automatiquement aux participants vocaux.</p>
                </div>
              </div>
              <Select
                value={config.role_id || "none"}
                onValueChange={(val) => setConfig({ ...config, role_id: val === "none" ? null : val })}
                disabled={!config.enabled}
              >
                <SelectTrigger className="w-full h-12 bg-haunted-surface border-white/[0.06] font-medium">
                  <SelectValue placeholder="Choisir un rôle…" />
                </SelectTrigger>
                <SelectContent className="bg-haunted-surface border-white/[0.06] max-h-[300px]">
                  <SelectItem value="none" className="text-slate-400 focus:bg-white/[0.05]">Aucun rôle</SelectItem>
                  {filteredRoles.map((r) => (
                    <SelectItem key={r.id} value={r.id} className="focus:bg-white/[0.05]">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: formatColor(r.color) }} />
                        {r.name}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <Button onClick={handleSave} disabled={saving} className="w-full h-14 text-base font-bold gap-2 shadow-lg shadow-primary/20 transition-all hover:scale-[1.01] active:scale-[0.99]">
              {saving ? <RefreshCcw className="h-5 w-5 animate-spin" /> : <Save className="h-5 w-5" />}
              Tout enregistrer
            </Button>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-3xl p-6 relative overflow-hidden group">
            <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
              <Volume2 className="h-32 w-32 text-primary" />
            </div>
            <div className="flex items-center gap-2 mb-4">
              <Info className="h-4 w-4 text-primary" />
              <h3 className="text-sm font-bold text-white">Comment ça marche</h3>
            </div>
            <ul className="text-xs text-slate-500 space-y-3 leading-relaxed">
              <li className="flex gap-2">
                <span className="text-primary font-bold">01</span>
                <span>Le rôle est ajouté quand un membre rejoint un salon vocal.</span>
              </li>
              <li className="flex gap-2">
                <span className="text-primary font-bold">02</span>
                <span>Le rôle est retiré à la déconnexion de tous les salons.</span>
              </li>
              <li className="flex gap-2">
                <span className="text-primary font-bold">03</span>
                <span>Vérifiez que le rôle du bot est au-dessus du rôle choisi.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
