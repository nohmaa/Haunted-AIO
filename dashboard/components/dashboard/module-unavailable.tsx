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

import React from "react";
import { Ghost } from "lucide-react";
import { RetryButton } from "@/components/dashboard/retry-button";

/**
 * État affiché quand l'API du bot ne renvoie pas la configuration d'un module.
 * On n'invente aucune valeur et on ne rend pas une page vide : on explique.
 */
export function ModuleUnavailable({ module }: { module: string }) {
  return (
    <div className="max-w-2xl mx-auto text-center border border-white/[0.06] border-dashed rounded-3xl bg-white/[0.01] p-12">
      <div className="h-16 w-16 rounded-2xl bg-red-500/10 border border-red-500/20 flex items-center justify-center mx-auto mb-6">
        <Ghost className="h-8 w-8 text-red-500/70" />
      </div>
      <h3 className="text-xl font-bold text-white">Données indisponibles</h3>
      <p className="text-slate-400 mt-3 text-sm">
        Le module « {module} » n&apos;a renvoyé aucune configuration. L&apos;API du bot est peut-être
        momentanément injoignable, ou ce serveur n&apos;a pas encore de configuration enregistrée.
      </p>
      <div className="mt-8 flex justify-center">
        <RetryButton />
      </div>
    </div>
  );
}
