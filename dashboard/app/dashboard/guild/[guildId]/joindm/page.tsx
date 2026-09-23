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
import { MessageSquare, Save, RefreshCcw, Send } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

export default function JoinDMPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = use(params);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [config, setConfig] = useState<any>({
    message: "",
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const configData = await api.getJoinDM(guildId);
      setConfig(configData);
    } catch (error) {
      console.error("Échec de récupération des données du MP de bienvenue :", error);
      toast.error("Échec du chargement de la configuration du MP de bienvenue");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [guildId]);

  const handleSave = async () => {
    try {
      setSaving(true);
      await api.updateJoinDM(guildId, config);
      toast.success("MP de bienvenue enregistré");
    } catch (error) {
      console.error("Échec d’enregistrement du MP de bienvenue :", error);
      toast.error("Échec de l’enregistrement du MP de bienvenue");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <RefreshCcw className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">MP de bienvenue</h2>
        <p className="text-muted-foreground">
          Envoyez un message privé aux nouveaux membres à leur arrivée.
        </p>
      </div>

      <Card className="border-primary/20 bg-background/50 backdrop-blur-xl">
        <CardHeader>
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-primary" />
            <CardTitle>Message de bienvenue</CardTitle>
          </div>
          <CardDescription>
            Ce message sera envoyé en MP au membre. Accueillez-le avec votre texte.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Contenu du message</Label>
            <Textarea
              placeholder="Bienvenue sur le serveur ! Pense à lire le règlement…"
              className="min-h-[200px]"
              value={config.message || ""}
              onChange={(e) => setConfig({ ...config, message: e.target.value })}
            />
          </div>

          <div className="flex justify-end pt-4">
            <Button onClick={handleSave} disabled={saving} className="gap-2">
              {saving ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Enregistrer le message
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card className="border-blue-500/20 bg-blue-500/5">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Send className="w-5 h-5 text-blue-500" />
            <CardTitle className="text-blue-500 text-base">Note d’utilisation</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Le bot ajoutera automatiquement « Envoyé depuis [Nom du serveur] » à la fin de votre message. Vérifiez que le bot peut envoyer des MP aux membres (même serveur, non bloqué).
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
