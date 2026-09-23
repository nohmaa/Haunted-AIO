"use client";

import React, { useTransition } from "react";
import { useRouter } from "next/navigation";
import { RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

/** Relance le rendu serveur de la page courante (données rechargées depuis l'API). */
export function RetryButton({
  label = "Réessayer la connexion",
  className,
}: {
  label?: string;
  className?: string;
}) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();

  return (
    <button
      onClick={() => startTransition(() => router.refresh())}
      disabled={isPending}
      className={cn(
        "inline-flex items-center gap-2.5 px-6 py-3 rounded-2xl border border-white/10 bg-white/[0.03] text-xs font-black uppercase tracking-widest text-slate-200 hover:bg-white/[0.06] hover:border-red-500/30 transition-all disabled:opacity-50",
        className
      )}
    >
      <RefreshCw className={cn("h-4 w-4", isPending && "animate-spin")} />
      {isPending ? "Nouvelle tentative..." : label}
    </button>
  );
}
