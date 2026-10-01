import type { Metadata } from "next";
import DashboardShell from "./dashboard-shell";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Console Haunted",
  robots: { index: false, follow: false },
};

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <DashboardShell>{children}</DashboardShell>;
}
