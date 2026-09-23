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
import { Search, Save, RefreshCcw, Bell } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

export default function TrackingPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = use(params);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [channels, setChannels] = useState<any[]>([]);
  const [config, setConfig] = useState<any>({
    channel_id: null,
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [configData, channelsData] = await Promise.all([
        api.getTracking(guildId),
        api.getChannels(guildId),
      ]);
      setConfig(configData);
      setChannels(channelsData);
    } catch (error) {
      console.error("Échec de récupération des données de suivi :", error);
      toast.error("Échec du chargement du suivi des invitations");
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
      await api.updateTracking(guildId, config);
      toast.success("Suivi enregistré");
    } catch (error) {
      console.error("Échec d’enregistrement du suivi :", error);
      toast.error("Échec de l’enregistrement du suivi");
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
        <h2 className="text-3xl font-bold tracking-tight">Suivi des invitations</h2>
        <p className="text-muted-foreground">
          Choisissez où le bot consigne les invitations à l’arrivée d’un membre.
        </p>
      </div>

      <Card className="border-primary/20 bg-background/50 backdrop-blur-xl">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Search className="w-5 h-5 text-primary" />
            <CardTitle>Configuration des logs</CardTitle>
          </div>
          <CardDescription>
            Choisissez un salon pour les notifications d’invitations et sources d’arrivée.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label>Salon de logs</Label>
            <Select
              value={config.channel_id?.toString() || "none"}
              onValueChange={(val) => setConfig({ ...config, channel_id: val === "none" ? null : parseInt(val) })}
              options={[
                { value: "none", label: "Désactivé" },
                ...channels.map((chan) => ({ value: chan.id.toString(), label: `#${chan.name}` }))
              ]}
            />
          </div>

          <div className="flex justify-end pt-4">
            <Button onClick={handleSave} disabled={saving} className="gap-2">
              {saving ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Enregistrer
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card className="border-yellow-500/20 bg-yellow-500/5">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-yellow-500" />
            <CardTitle className="text-yellow-500">Information</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Le module suit toutes les arrivées et tente d’identifier le lien d’invitation utilisé. Ces informations sont consignées dans le salon choisi.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
