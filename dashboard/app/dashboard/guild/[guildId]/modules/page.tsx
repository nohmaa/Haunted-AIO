import React from "react";
import { LayoutGrid } from "lucide-react";
import { api } from "@/lib/api";
import { ModulesManager } from "@/components/dashboard/modules-manager";

export const dynamic = "force-dynamic";

export default async function GuildModulesPage({ params }: { params: Promise<{ guildId: string }> }) {
  const { guildId } = await params;
  const config = await api.getModules(guildId);

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <LayoutGrid className="h-6 w-6 text-primary" />
          Modules du serveur
        </h2>
        <p className="text-slate-400 mt-1">
          Activez ou désactivez les fonctionnalités de Haunted pour ce serveur. Un module désactivé ne répond plus aux commandes.
        </p>
      </div>

      <ModulesManager guildId={guildId} initialModules={config.modules} />
    </div>
  );
}
