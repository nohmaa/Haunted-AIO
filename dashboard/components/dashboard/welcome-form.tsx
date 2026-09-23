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
  Save,
  MessageSquare,
  Type,
  LayoutTemplate,
  RefreshCcw
} from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { WelcomeConfig, DiscordChannel } from "@/types/api";

interface WelcomeFormProps {
  initialConfig: WelcomeConfig;
  channels: DiscordChannel[];
  guildId: string;
}

export function WelcomeForm({ initialConfig, channels, guildId }: WelcomeFormProps) {
  const [config, setConfig] = useState<WelcomeConfig>(initialConfig);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    const promise = api.updateWelcome(guildId, config);

    toast.promise(promise, {
      loading: 'Enregistrement de la configuration de bienvenue...',
      success: 'Paramètres de bienvenue enregistrés avec succès !',
      error: 'Échec de la mise à jour des paramètres de bienvenue',
    });

    try {
      await promise;
    } catch (err: any) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const channelOptions = channels.map(c => ({
    value: c.id.toString(),
    label: `#${c.name}`
  }));

  const typeOptions = [
    { value: "simple", label: "Message texte simple" },
    { value: "embed", label: "Message embed riche" }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl shadow-xl p-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Type de réponse</label>
              <Select 
                value={config.welcome_type || "simple"}
                onValueChange={(val) => setConfig({ ...config, welcome_type: val })}
                options={typeOptions}
                className="mt-2"
              />
            </div>

            <div>
              <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Salon de bienvenue</label>
              <Select 
                value={config.channel_id || ""}
                onValueChange={(val) => setConfig({ ...config, channel_id: val })}
                options={channelOptions}
                placeholder="Sélectionner un salon..."
                className="mt-2"
              />
            </div>

            {config.welcome_type === "simple" && (
              <div>
                <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Contenu du message</label>
                <textarea 
                  value={config.welcome_message || ""}
                  onChange={(e) => setConfig({ ...config, welcome_message: e.target.value })}
                  placeholder="Bienvenue {user} sur {server_name} !"
                  className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white min-h-[120px]"
                />
              </div>
            )}

            {config.welcome_type === "embed" && (
              <div className="space-y-4 pt-4 border-t border-white/[0.05]">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Titre de l'embed</label>
                    <input 
                      type="text"
                      value={config.embed_data?.title || ""}
                      onChange={(e) => setConfig({ ...config, embed_data: { ...config.embed_data, title: e.target.value }})}
                      className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                      placeholder="Bienvenue sur le serveur !"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Couleur de l'embed (Hex)</label>
                    <input 
                      type="text"
                      value={config.embed_data?.color || ""}
                      onChange={(e) => setConfig({ ...config, embed_data: { ...config.embed_data, color: e.target.value }})}
                      className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                      placeholder="#3498db"
                    />
                  </div>
                </div>
                
                <div>
                  <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">Description de l'embed</label>
                  <textarea 
                    value={config.embed_data?.description || ""}
                    onChange={(e) => setConfig({ ...config, embed_data: { ...config.embed_data, description: e.target.value }})}
                    placeholder="Nous sommes ravis de t'accueillir ici, {user} !"
                    className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white min-h-[100px]"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">URL de la miniature</label>
                    <input 
                      type="text"
                      value={config.embed_data?.thumbnail || ""}
                      onChange={(e) => setConfig({ ...config, embed_data: { ...config.embed_data, thumbnail: e.target.value }})}
                      className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                      placeholder="{user_avatar} ou https://..."
                    />
                  </div>
                  <div>
                    <label className="text-xs font-black uppercase text-slate-500 tracking-widest pl-1">URL de l'image</label>
                    <input 
                      type="text"
                      value={config.embed_data?.image || ""}
                      onChange={(e) => setConfig({ ...config, embed_data: { ...config.embed_data, image: e.target.value }})}
                      className="w-full mt-2 bg-haunted-crypt border border-white/[0.06] rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 text-white"
                      placeholder="https://..."
                    />
                  </div>
                </div>
              </div>
            )}
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
         <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl p-6 shadow-xl">
            <h3 className="text-sm font-black uppercase text-slate-500 tracking-widest mb-4">Variables</h3>
            <div className="space-y-2 text-xs text-slate-400 font-mono bg-white/[0.02] p-4 rounded-2xl border border-white/5">
               <p className="flex justify-between hover:text-white transition-colors"><span>{'{user}'}</span> <span>@Pseudo</span></p>
               <p className="flex justify-between hover:text-white transition-colors"><span>{'{user_name}'}</span> <span>Pseudo</span></p>
               <p className="flex justify-between hover:text-white transition-colors"><span>{'{server_name}'}</span> <span>Nom du serveur</span></p>
               <p className="flex justify-between hover:text-white transition-colors"><span>{'{server_membercount}'}</span> <span>Total des membres</span></p>
               <p className="border-t border-white/[0.06] my-2 pt-2 flex justify-between hover:text-white transition-colors"><span>{'{user_avatar}'}</span> <span>Image d'avatar</span></p>
               <p className="flex justify-between hover:text-white transition-colors"><span>{'{server_icon}'}</span> <span>Logo du serveur</span></p>
            </div>
            <p className="text-[10px] text-slate-500 italic text-center mt-4">Vous pouvez utiliser ces variables dans le contenu du message et les embeds pour personnaliser les bienvenues.</p>
         </div>
         
         <div className="bg-haunted-surface border border-white/[0.06] rounded-3xl p-6 shadow-xl">
            <h3 className="text-sm font-black uppercase text-slate-500 tracking-widest mb-4">Configuration auto</h3>
            <Button onClick={() => setConfig({
                ...config,
                welcome_type: "embed",
                embed_data: {
                  ...config.embed_data,
                  title: "Bienvenue sur {server_name} !",
                  description: "Salut {user}, ravi que tu nous aies rejoints ! Tu es le membre #{server_membercount}.",
                  color: "2f3136",
                  thumbnail: "{user_avatar}"
                }
              })} 
              variant="outline" 
              className="w-full border-primary/50 hover:bg-primary/20 text-primary"
            >
              <LayoutTemplate className="w-4 h-4 mr-2" />
              Appliquer le modèle par défaut
            </Button>
         </div>
      </div>
    </div>
  );
}
