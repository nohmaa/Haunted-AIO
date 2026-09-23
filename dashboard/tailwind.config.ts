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

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: {
          DEFAULT: "#ef4444", // Vivid Red
          hover: "#dc2626",
          glow: "rgba(239, 68, 68, 0.5)",
        },
        secondary: {
          DEFAULT: "#020617", // Deep Navy/Black
          light: "#0f172a",
        },
        accent: {
          red: "rgba(239, 68, 68, 0.1)",
          glass: "rgba(255, 255, 255, 0.03)",
        },
        // Palette « manoir hanté » : obsidienne, sang, ectoplasme, chandelle.
        haunted: {
          crypt: "#06060b",
          surface: "#0c0b12",
          raised: "#12101a",
          blood: "#ef4444",
          deep: "#7f1d1d",
          ectoplasm: "#5eead4",
          candle: "#f59e0b",
          bone: "#e7e5e4",
          ash: "#94a3b8",
        }
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [],
};
export default config;
