"use client";

import * as React from "react";
import Link from "next/link";
import { Power } from "lucide-react";
import { api } from "@/lib/api";
import { Switch } from "@/components/ui/switch";
import type { ModuleState } from "@/types/api";

export function ModulesManager({
  guildId,
  initialModules,
}: {
  guildId: string;
  initialModules: ModuleState[];
}) {
  const [modules, setModules] = React.useState<ModuleState[]>(initialModules);
  const [pending, setPending] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  async function toggle(key: string, enabled: boolean) {
    setPending(key);
    setError(null);
    // Mise à jour optimiste
    setModules((prev) => prev.map((m) => (m.key === key ? { ...m, enabled } : m)));
    try {
      await api.setModule(guildId, key, enabled);
    } catch (e: unknown) {
      // Annule en cas d'échec
      setModules((prev) => prev.map((m) => (m.key === key ? { ...m, enabled: !enabled } : m)));
      setError(e instanceof Error ? e.message : "Échec de la mise à jour du module.");
    } finally {
      setPending(null);
    }
  }

  const enabledCount = modules.filter((m) => m.enabled).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {enabledCount} module{enabledCount > 1 ? "s" : ""} activé{enabledCount > 1 ? "s" : ""} sur {modules.length}
        </p>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-2xl px-5 py-3">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modules.map((mod) => (
          <div
            key={mod.key}
            className="bg-haunted-surface border border-white/[0.06] p-5 rounded-2xl flex items-start gap-4"
          >
            <div className="h-10 w-10 shrink-0 bg-white/[0.05] rounded-xl flex items-center justify-center text-primary">
              <Power className="h-5 w-5" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-bold text-white">{mod.label}</h3>
                <Switch
                  checked={mod.enabled}
                  disabled={pending === mod.key}
                  onCheckedChange={(checked) => toggle(mod.key, checked)}
                  aria-label={`Activer ${mod.label}`}
                />
              </div>
              <p className="text-xs text-slate-500 leading-relaxed mt-1">{mod.description}</p>
              <div className="flex items-center gap-3 mt-3">
                <span
                  className={
                    mod.enabled
                      ? "text-[10px] font-black uppercase text-teal-300 bg-teal-300/10 px-2 py-0.5 rounded-full border border-teal-300/20"
                      : "text-[10px] font-black uppercase text-slate-500 bg-slate-500/10 px-2 py-0.5 rounded-full border border-slate-500/20"
                  }
                >
                  {mod.enabled ? "Activé" : "Désactivé"}
                </span>
                {mod.route && (
                  <Link
                    href={`/dashboard/guild/${guildId}/${mod.route}`}
                    className="text-[11px] font-bold text-primary hover:underline"
                  >
                    Configurer →
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
