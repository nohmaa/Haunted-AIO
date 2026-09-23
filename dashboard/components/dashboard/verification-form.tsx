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
import { ShieldCheck, RefreshCcw, Save, Hash, Settings, User } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { VerificationConfig, DiscordChannel } from "@/types/api";

interface VerificationFormProps {
  initialConfig: VerificationConfig;
  channels: DiscordChannel[];
  roles: any[]; // We don't have a rigid Role interface but they have id, name.
  guildId: string;
}

export function VerificationForm({ initialConfig, channels, roles, guildId }: VerificationFormProps) {
  const [config, setConfig] = useState<VerificationConfig>(initialConfig);
  const [saving, setSaving] = useState(false);

  const textChannels = channels.filter((c) => c.type === "0");

  const handleSave = async () => {
    setSaving(true);
    const promise = api.updateVerification(guildId, config);

    toast.promise(promise, {
      loading: 'Enregistrement de la configuration de vérification...',
      success: 'Paramètres de vérification enregistrés avec succès !',
      error: 'Échec de la mise à jour de la configuration de vérification',
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
        <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl shadow-xl p-8 space-y-8">
          
          {/* Main Toggle */}
          <div className="flex items-center justify-between p-6 bg-white/[0.02] rounded-2xl border border-white/[0.06]">
            <div>
              <h3 className="text-lg font-black text-white">Système de vérification</h3>
              <p className="text-sm text-slate-400 mt-1">Activer ou désactiver la vérification du serveur.</p>
            </div>
            <Switch 
              checked={config.enabled} 
              onCheckedChange={(val) => setConfig({ ...config, enabled: val })}
              className="scale-125"
            />
          </div>

          <div className={`space-y-6 transition-all duration-300 ${!config.enabled && "opacity-50 pointer-events-none"}`}>
            {/* Channel Setup */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <div className="space-y-3">
                <label className="text-sm font-bold text-slate-300 flex items-center gap-2">
                  <Hash className="h-4 w-4 text-slate-400" />
                  Salon de vérification
                </label>
                <Select
                  value={config.verification_channel_id || "none"}
                  onValueChange={(val) => setConfig({ ...config, verification_channel_id: val === "none" ? null : val })}
                >
                  <SelectTrigger className="w-full h-12 bg-haunted-surface border-white/[0.06] font-medium">
                    <SelectValue placeholder="Choisir un salon..." />
                  </SelectTrigger>
                  <SelectContent className="bg-haunted-surface border-white/[0.06]">
                    <SelectItem value="none" className="text-slate-400 focus:bg-white/[0.05]">Non défini</SelectItem>
                    {textChannels.map((c) => (
                      <SelectItem key={c.id} value={c.id.toString()} className="focus:bg-white/[0.05]">
                        # {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500">Le salon où les utilisateurs en cours de vérification utiliseront la commande ou les boutons.</p>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-bold text-slate-300 flex items-center gap-2">
                  <Hash className="h-4 w-4 text-slate-400" />
                  Salon de logs
                </label>
                <Select
                  value={config.log_channel_id || "none"}
                  onValueChange={(val) => setConfig({ ...config, log_channel_id: val === "none" ? null : val })}
                >
                  <SelectTrigger className="w-full h-12 bg-haunted-surface border-white/[0.06] font-medium">
                    <SelectValue placeholder="Choisir le salon de logs..." />
                  </SelectTrigger>
                  <SelectContent className="bg-haunted-surface border-white/[0.06]">
                    <SelectItem value="none" className="text-slate-400 focus:bg-white/[0.05]">Non défini</SelectItem>
                    {textChannels.map((c) => (
                      <SelectItem key={c.id} value={c.id.toString()} className="focus:bg-white/[0.05]">
                        # {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500">Salon où seront envoyés les logs de vérification réussie ou échouée.</p>
              </div>

            </div>

            {/* Role Setup & Method */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              <div className="space-y-3">
                <label className="text-sm font-bold text-slate-300 flex items-center gap-2">
                  <User className="h-4 w-4 text-slate-400" />
                  Rôle vérifié
                </label>
                <Select
                  value={config.verified_role_id || "none"}
                  onValueChange={(val) => setConfig({ ...config, verified_role_id: val === "none" ? null : val })}
                >
                  <SelectTrigger className="w-full h-12 bg-haunted-surface border-white/[0.06] font-medium">
                    <SelectValue placeholder="Choisir le rôle vérifié..." />
                  </SelectTrigger>
                  <SelectContent className="bg-haunted-surface border-white/[0.06]">
                    <SelectItem value="none" className="text-slate-400 focus:bg-white/[0.05]">Non défini</SelectItem>
                    {roles.map((r) => (
                      <SelectItem key={r.id} value={r.id.toString()} className="focus:bg-white/[0.05]">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: `#${r.color.toString(16).padStart(6, '0')}` }} />
                          {r.name}
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500">Le rôle attribué après une vérification réussie.</p>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-bold text-slate-300 flex items-center gap-2">
                  <Settings className="h-4 w-4 text-slate-400" />
                  Méthode de vérification
                </label>
                <Select
                  value={config.verification_method || "both"}
                  onValueChange={(val) => setConfig({ ...config, verification_method: val })}
                >
                  <SelectTrigger className="w-full h-12 bg-haunted-surface border-white/[0.06] font-medium">
                    <SelectValue placeholder="Choisir une méthode..." />
                  </SelectTrigger>
                  <SelectContent className="bg-haunted-surface border-white/[0.06]">
                    <SelectItem value="captcha" className="focus:bg-white/[0.05]">CAPTCHA uniquement</SelectItem>
                    <SelectItem value="button" className="focus:bg-white/[0.05]">Bouton uniquement</SelectItem>
                    <SelectItem value="both" className="focus:bg-white/[0.05]">Les deux choix</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500">Choisissez comment les utilisateurs seront vérifiés.</p>
              </div>

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

      <div className="space-y-6">
        <div className="bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 rounded-3xl p-6 relative overflow-hidden group">
          <div className="absolute -right-4 -top-4 opacity-[0.03] group-hover:scale-110 transition-transform">
            <ShieldCheck className="h-32 w-32 text-primary" />
          </div>
          <h3 className="text-sm font-bold text-primary mb-2">Comment ça fonctionne</h3>
          <p className="text-xs text-slate-400 leading-relaxed mb-4">
            La vérification Haunted garantit qu’aucun bot non autorisé ni utilisateur malveillant n’entre sur votre serveur sans vérification.
          </p>
          <ul className="text-xs text-slate-500 space-y-2">
             <li>• Le bot créera un panneau dans votre salon de vérification.</li>
             <li>• Les membres non vérifiés doivent cliquer sur « Vérifier ».</li>
             <li>• Le captcha présente une séquence d’images unique.</li>
             <li>• En cas de succès, le rôle est attribué.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
