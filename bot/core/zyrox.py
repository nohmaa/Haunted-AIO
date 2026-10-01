# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║   ░█▀▀░█▀█░█▀▄░█▀▀░█░█   ░█▀▄░█▀▀░█░█░█▀▀                     ║
# ║   ░█░░░█░█░█░█░█▀▀░▄▀▄   ░█░█░█▀▀░▀▄▀░▀▀█                     ║
# ║   ░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀░▀   ░▀▀░░▀▀▀░░▀░░▀▀▀                     ║
# ║                                                                  ║
# ║            © 2026 Arsonist   — All Rights Reserved              ║
# ║                                                                  ║
# ║   discord  ──  https://discord.gg/DvetGPq9q5                    ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

from __future__ import annotations
from discord.ext import commands, tasks
import discord
import aiohttp
import json
import jishaku
import asyncio
import time
import typing
from typing import List
import aiosqlite
from utils.config import OWNER_IDS, BotName
from utils import getConfig, updateConfig
from .Context import Context
from colorama import Fore, Style, init
import importlib
import inspect

init(autoreset=True)

# Corrected the extensions list
extensions: List[str] = [
    "cogs"
]

_MAINTENANCE_CACHE: tuple[float, bool] = (0.0, False)


async def _maintenance_mode_enabled() -> bool:
    """Read global command maintenance state with a short process-local cache."""
    global _MAINTENANCE_CACHE
    now = time.monotonic()
    if now - _MAINTENANCE_CACHE[0] < 1.0:
        return _MAINTENANCE_CACHE[1]

    try:
        async with aiosqlite.connect("db/admin_config.db", timeout=2) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)"
            )
            async with db.execute(
                "SELECT value FROM config WHERE key = 'maintenance_mode'"
            ) as cursor:
                row = await cursor.fetchone()
        enabled = bool(row and str(row[0]).lower() == "true")
    except Exception:
        enabled = True

    _MAINTENANCE_CACHE = (time.monotonic(), enabled)
    return enabled

class zyrox(commands.AutoShardedBot):
    def __init__(self, *arg, **kwargs):
        intents = discord.Intents.all()
        intents.presences = True
        intents.members = True
        super().__init__(command_prefix=self.get_prefix,
                         case_insensitive=True,
                         intents=intents,
                         # The status is already set to Do Not Disturb here
                         status=discord.Status.do_not_disturb,
                         strip_after_prefix=True,
                         owner_ids=OWNER_IDS,
                         allowed_mentions=discord.AllowedMentions(
                             everyone=False, replied_user=False, roles=False),
                         sync_commands_debug=True,
                         sync_commands=True,
                         shard_count=1)
        self.status_index = 0
        self.status_list = []
        # Prefix and slash commands share the same module switch. discord.py
        # does not route application commands through Bot.invoke().
        self.tree.interaction_check = self._module_interaction_check

    @staticmethod
    def _guild_id_from_event(args) -> int | None:
        """Find the guild attached to common discord.py listener payloads."""
        for value in args:
            guild = getattr(value, "guild", None)
            guild_id = getattr(guild, "id", None) or getattr(value, "guild_id", None)
            if guild_id is None and isinstance(value, discord.Guild):
                guild_id = value.id
            if guild_id is not None:
                return int(guild_id)
        return None

    async def add_cog(self, cog, /, *, override=False, guild=None, guilds=None):
        """Guard mapped cog listeners as well as commands when a module is off."""
        key = self._module_key_for_cog(cog)
        if key:
            listener_methods = []
            for _event_name, method_name in getattr(cog, "__cog_listeners__", ()):
                original = getattr(cog, method_name, None)
                if original is None or getattr(original, "__haunted_module_guard__", False):
                    continue
                listener_methods.append((method_name, original))

                async def guarded(*args, __callback=original, __key=key, **kwargs):
                    guild_id = self._guild_id_from_event(args)
                    if guild_id is not None:
                        try:
                            from utils.modules import is_module_enabled
                            if not await is_module_enabled(guild_id, __key):
                                return None
                        except Exception:
                            print(f"[Modules] Impossible de vérifier {__key}; écouteur ignoré par précaution.")
                            return None
                    return await __callback(*args, **kwargs)

                guarded.__haunted_module_guard__ = True
                setattr(cog, method_name, guarded)

            try:
                return await super().add_cog(cog, override=override, guild=guild, guilds=guilds)
            except Exception:
                for method_name, original in listener_methods:
                    setattr(cog, method_name, original)
                raise

        return await super().add_cog(cog, override=override, guild=guild, guilds=guilds)

    @staticmethod
    def _module_key_for_cog(cog):
        from api.modules_registry import COG_MODULE_MAP

        return getattr(cog, "module_key", None) or COG_MODULE_MAP.get(type(cog).__name__)

    async def _module_interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in OWNER_IDS and await _maintenance_mode_enabled():
            await self._respond_module_error(
                interaction,
                "Haunted est en maintenance. Réessayez plus tard.",
            )
            return False

        command = interaction.command
        cog = getattr(command, "binding", None) if command is not None else None
        key = self._module_key_for_cog(cog) if cog is not None else None
        if not key or interaction.guild_id is None:
            return True

        try:
            from utils.modules import is_module_enabled
            enabled = await is_module_enabled(interaction.guild_id, key)
        except Exception:
            print(f"[Modules] Impossible de vérifier l'état du module {key}; commande slash bloquée.")
            await self._respond_module_error(interaction, "Configuration du module indisponible. Réessayez plus tard.")
            return False

        if enabled:
            return True

        from api.modules_registry import MODULE_LABELS
        await self._respond_module_error(
            interaction,
            f"Le module {MODULE_LABELS.get(key, key)} est désactivé sur ce serveur.",
        )
        return False

    @staticmethod
    async def _respond_module_error(interaction: discord.Interaction, message: str) -> None:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    async def setup_hook(self):
        await self.load_extensions()
        self.status_task.start()

    async def load_extensions(self):
        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(Fore.GREEN + Style.BRIGHT + f"Loaded extension: {extension}")
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Failed to load extension {extension}. {e}")
        print(Fore.GREEN + Style.BRIGHT + "*" * 20)

    @tasks.loop(seconds=30)
    async def status_task(self):
        await self.wait_until_ready()
        if not self.guilds:
            return

        guild = self.guilds[0]  # Use first available guild for prefix
        try:
            config = await getConfig(guild.id)
            prefix = config.get("prefix", ">")
        except:
            prefix = ">"

        user_count = sum(g.member_count or 0 for g in self.guilds)
        guild_count = len(self.guilds)

        self.status_list = [
            (discord.ActivityType.playing, f"{prefix}help | Sécurité sur ton serveur"),
            (discord.ActivityType.watching, f"{user_count} membres"),
            (discord.ActivityType.watching, f"{guild_count} serveurs"),
            (discord.ActivityType.listening, "Chasse aux nukers"),
            (discord.ActivityType.playing, f"Protecteur {BotName}"),
        ]

        current = self.status_list[self.status_index % len(self.status_list)]
        # This task only changes the activity, not the online status (dnd, idle, etc.)
        await self.change_presence(activity=discord.Activity(type=current[0], name=current[1]))
        self.status_index += 1

    async def send_raw(self, channel_id: int, content: str, **kwargs) -> typing.Optional[discord.Message]:
        await self.http.send_message(channel_id, content, **kwargs)

    async def invoke_help_command(self, ctx: Context) -> None:
        return await ctx.send_help(ctx.command)

    async def fetch_message_by_channel(self, channel: discord.TextChannel, messageID: int) -> typing.Optional[discord.Message]:
        async for msg in channel.history(limit=1, before=discord.Object(messageID + 1), after=discord.Object(messageID - 1)):
            return msg

    async def get_prefix(self, message: discord.Message):
        if message.guild:
            guild_id = message.guild.id
            async with aiosqlite.connect('db/np.db') as db:
                async with db.execute("SELECT id FROM np WHERE id = ?", (message.author.id,)) as cursor:
                    row = await cursor.fetchone()
            data = await getConfig(guild_id)
            prefix = data["prefix"]
            if row:
                return commands.when_mentioned_or(prefix, '')(self, message)
            else:
                return commands.when_mentioned_or(prefix)(self, message)
        else:
            async with aiosqlite.connect('db/np.db') as db:
                async with db.execute("SELECT id FROM np WHERE id = ?", (message.author.id,)) as cursor:
                    row = await cursor.fetchone()
            if row:
                return commands.when_mentioned_or('?', '')(self, message)
            else:
                return commands.when_mentioned_or('')(self, message)

    async def on_message_edit(self, before, after):
        ctx: Context = await self.get_context(after, cls=Context)
        if before.content != after.content:
            if after.guild is None or after.author.bot:
                return
            if ctx.command is None:
                return
            if type(ctx.channel) == "public_thread":
                return
            await self.invoke(ctx)

    async def invoke(self, ctx: Context) -> None:
        """Bloque les commandes des modules désactivés depuis le dashboard."""
        if ctx.author.id not in OWNER_IDS and await _maintenance_mode_enabled():
            await ctx.send("Haunted est en maintenance. Réessayez plus tard.")
            return

        if ctx.guild is not None and ctx.command is not None and ctx.command.cog is not None:
            key = self._module_key_for_cog(ctx.command.cog)
            if key:
                try:
                    from api.modules_registry import MODULE_LABELS
                    from utils.modules import is_module_enabled
                    if not await is_module_enabled(ctx.guild.id, key):
                        from utils.i18n import t
                        await ctx.send(t("module_disabled", module=MODULE_LABELS.get(key, key)))
                        return
                except Exception:
                    print(f"[Modules] Impossible de vérifier l'état du module {key}; commande préfixe bloquée.")
                    await ctx.send("Configuration du module indisponible. Réessayez plus tard.")
                    return
        await super().invoke(ctx)

def setup_bot():
    intents = discord.Intents.all()
    bot = zyrox(intents=intents)
    return bot
