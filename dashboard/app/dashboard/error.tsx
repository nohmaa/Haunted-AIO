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

import React, { useEffect } from "react";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Dashboard Error:", error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] p-6 text-center animate-in fade-in zoom-in-95 duration-500">
      <div className="h-20 w-20 bg-red-500/10 rounded-3xl flex items-center justify-center mb-6">
        <AlertTriangle className="h-10 w-10 text-red-500" />
      </div>
      
      <h2 className="text-2xl font-black text-white mb-2 tracking-tight">Défaillance système détectée</h2>
      <p className="text-slate-400 max-w-md mb-8">
        La liaison neuronale a subi une interruption inattendue. Cela peut être dû à un délai de connexion dépassé ou à une défaillance interne de l'API.
      </p>

      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-xs">
        <Button 
          onClick={() => reset()}
          className="flex-1 gap-2 h-12 font-bold"
        >
          <RefreshCw className="h-4 w-4" />
          Réessayer la connexion
        </Button>
        <Link href="/dashboard" className="flex-1">
          <Button 
            variant="outline"
            className="w-full gap-2 h-12 font-bold border-white/[0.06]"
          >
            <Home className="h-4 w-4" />
            Retour à l'accueil
          </Button>
        </Link>
      </div>
      
      {process.env.NODE_ENV === 'development' && (
        <pre className="mt-8 p-4 bg-black/40 border border-white/[0.06] rounded-xl text-left text-xs text-red-400 overflow-auto max-w-full font-mono">
          {error.message}
        </pre>
      )}
    </div>
  );
}
