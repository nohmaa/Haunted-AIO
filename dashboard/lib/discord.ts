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

import { cache } from "react";

/**
 * Droits Discord de l'utilisateur connecté, source unique de vérité pour
 * savoir quels serveurs le dashboard a le droit de lui montrer et de modifier.
 */

const MANAGE_GUILD = BigInt(0x20);
const ADMINISTRATOR = BigInt(0x8);

export interface DiscordUserGuild {
  id: string;
  name: string;
  permissions: string;
  owner: boolean;
}

export function canManageGuild(guild: DiscordUserGuild): boolean {
  if (guild.owner === true) return true;
  try {
    const perms = BigInt(guild.permissions);
    return (perms & ADMINISTRATOR) === ADMINISTRATOR || (perms & MANAGE_GUILD) === MANAGE_GUILD;
  } catch {
    return false;
  }
}

/**
 * Identifiants des serveurs gérables par l'utilisateur (permission « Gérer le
 * serveur », administrateur ou propriétaire).
 *
 * Renvoie `null` quand Discord n'a pas pu être interrogé : l'appelant doit
 * alors afficher une indisponibilité honnête plutôt que de tout refuser.
 */
export const getManageableGuildIds = cache(
  async (accessToken: string): Promise<Set<string> | null> => {
    try {
      const response = await fetch("https://discord.com/api/users/@me/guilds", {
        headers: { Authorization: `Bearer ${accessToken}` },
        next: { revalidate: 300 },
      });

      if (!response.ok) {
        console.error(`[Discord] /users/@me/guilds a répondu ${response.status}`);
        return null;
      }

      const guilds = (await response.json()) as DiscordUserGuild[];
      return new Set(guilds.filter(canManageGuild).map((guild) => String(guild.id)));
    } catch (error) {
      console.error("[Discord] Échec de récupération des serveurs de l'utilisateur :", error);
      return null;
    }
  }
);
