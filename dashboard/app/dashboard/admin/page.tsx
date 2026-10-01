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
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/lib/auth";
import { redirect } from "next/navigation";
import { isDashboardAdmin } from "@/lib/server-auth";
import { Shield, Users, Server, Activity, Database, Cpu, Globe, Lock, Settings } from "lucide-react";

import { AdminContent } from "@/components/dashboard/admin-content";

export default async function AdminPage() {
  const session = await getServerSession(authOptions);
  
  // Server-side protection
  if (!session || !isDashboardAdmin(session.user?.id)) {
    redirect("/dashboard");
  }

  return <AdminContent />;
}


