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
import discord
from utils.emoji import CROSS, TICK, ZWARNING
from discord.ui import LayoutView, TextDisplay, Separator, Container
from discord.ext import commands
from core import *
from utils.Tools import *
from typing import Optional
import aiosqlite

color = 0xFF0000


class SuccessView(LayoutView):
    def __init__(self, title, description):
        super().__init__(timeout=None)
        self.add_item(
            Container(
                TextDisplay(f"**{TICK} {title}**"),
                Separator(visible=True),
                TextDisplay(description),
            )
        )


class ErrorView(LayoutView):
    def __init__(self, title, description):
        super().__init__(timeout=None)
        self.add_item(
            Container(
                TextDisplay(f"**{CROSS} {title}**"),
                Separator(visible=True),
                TextDisplay(description),
            )
        )


class WarningView(LayoutView):
    def __init__(self, title, description):
        super().__init__(timeout=None)
        self.add_item(
            Container(
                TextDisplay(f"**{ZWARNING} {title}**"),
                Separator(visible=True),
                TextDisplay(description),
            )
        )


class ListView(LayoutView):
    def __init__(self, title, items, empty_message, guild=None):
        super().__init__(timeout=None)

        if not items:
            self.add_item(
                Container(
                    TextDisplay(f"**{title}**"),
                    Separator(visible=True),
                    TextDisplay(empty_message),
                )
            )
        else:
            if guild:
                mentions = []
                for item in items:
                    if isinstance(item, int):
                        entity = guild.get_channel(item) or guild.get_member(item)
                        mentions.append(entity.mention if entity else f"ID {item}")
                    else:
                        mentions.append(f"`{item}`")
                description = "\n".join(mentions)
            else:
                description = "\n".join([f"`{item}`" for item in items])

            self.add_item(
                Container(
                    TextDisplay(f"**{title}**"),
                    Separator(visible=True),
                    TextDisplay(description),
                )
            )


class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/ignore.db"
        self.color = 0xFF0000
        bot.loop.create_task(self.initialize_db())

    async def initialize_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS ignored_commands (guild_id INTEGER, command_name TEXT)"
            )
            await db.execute(
                "CREATE TABLE IF NOT EXISTS ignored_channels (guild_id INTEGER, channel_id INTEGER)"
            )
            await db.execute(
                "CREATE TABLE IF NOT EXISTS ignored_users (guild_id INTEGER, user_id INTEGER)"
            )
            await db.execute(
                "CREATE TABLE IF NOT EXISTS bypassed_users (guild_id INTEGER, user_id INTEGER)"
            )
            await db.commit()

    @commands.group(
        name="ignore",
        help="Gérer les commandes, salons, utilisateurs ignorés et les utilisateurs contournés.",
        invoke_without_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _ignore(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_ignore.group(
        name="command",
        help="Gérer les commandes ignorées sur ce serveur.",
        invoke_without_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _command(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_command.command(name="add", help="Ajoute une commande à la liste d’exceptions.")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def command_add(self, ctx: commands.Context, command_name: str):
        command_name_normalized = command_name.strip().lower()
        command = self.bot.get_command(command_name_normalized)
        if not command:
            await ctx.reply(
                view=ErrorView("Erreur", f"`{command_name}` is not a valid command.")
            )
            return

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM ignored_commands WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            count = await cursor.fetchone()
            if count[0] >= 25:
                await ctx.reply(
                    view=WarningView(
                        "Accès refusé",
                        "Tu ne peux ajouter que 25 commandes maximum à la liste d’exceptions.",
                    )
                )
                return

            cursor = await db.execute(
                "SELECT command_name FROM ignored_commands WHERE guild_id = ? AND command_name = ?",
                (ctx.guild.id, command_name_normalized),
            )
            result = await cursor.fetchone()
            if result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"`{command_name}` is already in the ignore commands list.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO ignored_commands (guild_id, command_name) VALUES (?, ?)",
                    (ctx.guild.id, command_name_normalized),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"`{command_name}` ajouté à la liste des commandes ignorées avec succès.",
                    )
                )

    @_command.command(
        name="remove", help="Retire une commande de la liste d’exceptions."
    )
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def command_remove(self, ctx: commands.Context, command_name: str):
        command_name_normalized = command_name.strip().lower()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT command_name FROM ignored_commands WHERE guild_id = ? AND command_name = ?",
                (ctx.guild.id, command_name_normalized),
            )
            result = await cursor.fetchone()
            if not result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"`{command_name}` is not in the ignore commands list.",
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM ignored_commands WHERE guild_id = ? AND command_name = ?",
                    (ctx.guild.id, command_name_normalized),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"`{command_name}` retiré de la liste des commandes ignorées avec succès.",
                    )
                )

    @_command.command(name="show", help="Affiche la liste des commandes ignorées.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def command_show(self, ctx: commands.Context):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT command_name FROM ignored_commands WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            commands = await cursor.fetchall()
            if not commands:
                await ctx.reply(
                    view=ListView(
                        "Ignored Commands",
                        [],
                        "Aucune commande n’est actuellement ignorée sur ce serveur.",
                    )
                )
            else:
                await ctx.reply(
                    view=ListView("Ignored Commands", [c[0] for c in commands], "")
                )

    @_ignore.group(
        name="channel",
        help="Gérer les salons ignorés sur ce serveur.",
        invoke_without_command=True,
    )
    @blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_channel.command(name="add", help="Ajoute un salon à la liste d’exceptions.")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def channel_add(self, ctx: commands.Context, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM ignored_channels WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            count = await cursor.fetchone()

            if count[0] >= 30:
                await ctx.reply(
                    view=WarningView(
                        "Accès refusé",
                        "Tu ne peux ajouter que 30 salons maximum à la liste d’exceptions.",
                    )
                )
                return

            cursor = await db.execute(
                "SELECT channel_id FROM ignored_channels WHERE guild_id = ? AND channel_id = ?",
                (ctx.guild.id, channel.id),
            )
            result = await cursor.fetchone()

            if result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"{channel.mention} is already in the ignore channels list.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO ignored_channels (guild_id, channel_id) VALUES (?, ?)",
                    (ctx.guild.id, channel.id),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"{channel.mention} ajouté à la liste des salons ignorés avec succès.",
                    )
                )

    @_channel.command(name="remove", help="Retire un salon de la liste d’exceptions.")
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def channel_remove(self, ctx: commands.Context, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT channel_id FROM ignored_channels WHERE guild_id = ? AND channel_id = ?",
                (ctx.guild.id, channel.id),
            )
            result = await cursor.fetchone()

            if not result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"{channel.mention} is not in the ignore channels list.",
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM ignored_channels WHERE guild_id = ? AND channel_id = ?",
                    (ctx.guild.id, channel.id),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"{channel.mention} retiré de la liste des salons ignorés avec succès.",
                    )
                )

    @_channel.command(name="show", help="Affiche la liste des salons ignorés.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def channel_show(self, ctx: commands.Context):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT channel_id FROM ignored_channels WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            channels = await cursor.fetchall()

            if not channels:
                await ctx.reply(
                    view=ListView(
                        "Salons ignorés",
                        [],
                        "Aucun salon n’est actuellement ignoré sur ce serveur.",
                    )
                )
            else:
                await ctx.reply(
                    view=ListView(
                        "Salons ignorés", [c[0] for c in channels], "", ctx.guild
                    )
                )

    @_ignore.group(
        name="user",
        help="Gérer les utilisateurs ignorés sur ce serveur.",
        invoke_without_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _user(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_user.command(name="add", help="Ajoute un utilisateur à la liste d’exceptions.")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    async def user_add(self, ctx: commands.Context, user: discord.User):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM ignored_users WHERE guild_id = ?", (ctx.guild.id,)
            )
            count = await cursor.fetchone()

            if count[0] >= 30:
                await ctx.reply(
                    view=WarningView(
                        "Accès refusé",
                        "Tu ne peux ajouter que 30 utilisateurs maximum à la liste d’exceptions.",
                    )
                )
                return

            cursor = await db.execute(
                "SELECT user_id FROM ignored_users WHERE guild_id = ? AND user_id = ?",
                (ctx.guild.id, user.id),
            )
            result = await cursor.fetchone()

            if result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"{user.mention} is already in the ignore users list.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO ignored_users (guild_id, user_id) VALUES (?, ?)",
                    (ctx.guild.id, user.id),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"{user.mention} ajouté à la liste des utilisateurs ignorés avec succès.",
                    )
                )

    @_user.command(
        name="remove", help="Retire un utilisateur de la liste d’exceptions."
    )
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def user_remove(self, ctx: commands.Context, user: discord.User):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id FROM ignored_users WHERE guild_id = ? AND user_id = ?",
                (ctx.guild.id, user.id),
            )
            result = await cursor.fetchone()

            if not result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur", f"{user.mention} is not in the ignore users list."
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM ignored_users WHERE guild_id = ? AND user_id = ?",
                    (ctx.guild.id, user.id),
                )
                await db.commit()
                await ctx.send(
                    view=SuccessView(
                        "Succès",
                        f"{user.mention} retiré de la liste des utilisateurs ignorés avec succès.",
                    )
                )

    @_user.command(name="show", help="Affiche la liste des utilisateurs ignorés.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def user_show(self, ctx: commands.Context):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id FROM ignored_users WHERE guild_id = ?", (ctx.guild.id,)
            )
            users = await cursor.fetchall()

            if not users:
                await ctx.reply(
                    view=ListView(
                        "Ignored Users",
                        [],
                        "Aucun utilisateur n’est actuellement ignoré sur ce serveur.",
                    )
                )
            else:
                await ctx.reply(
                    view=ListView("Ignored Users", [u[0] for u in users], "", ctx.guild)
                )

    @_ignore.group(
        name="bypass",
        help="Gérer les utilisateurs contournés sur ce serveur.",
        invoke_without_command=True,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _bypass(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_bypass.command(
        name="add", help="Ajoute un utilisateur à la liste de contournement."
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def bypass_add(self, ctx: commands.Context, user: discord.User):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM bypassed_users WHERE guild_id = ?",
                (ctx.guild.id,),
            )
            count = await cursor.fetchone()

            if count[0] >= 30:
                await ctx.reply(
                    view=WarningView(
                        "Accès refusé",
                        "Tu ne peux ajouter que 30 utilisateurs maximum à la liste de contournement.",
                    )
                )
                return

            cursor = await db.execute(
                "SELECT user_id FROM bypassed_users WHERE guild_id = ? AND user_id = ?",
                (ctx.guild.id, user.id),
            )
            result = await cursor.fetchone()

            if result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur",
                        f"{user.mention} is already in the bypass users list.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO bypassed_users (guild_id, user_id) VALUES (?, ?)",
                    (ctx.guild.id, user.id),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"{user.mention} ajouté à la liste des utilisateurs contournés avec succès.",
                    )
                )

    @_bypass.command(
        name="remove", help="Retire un utilisateur de la liste de contournement."
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def bypass_remove(self, ctx: commands.Context, user: discord.User):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id FROM bypassed_users WHERE guild_id = ? AND user_id = ?",
                (ctx.guild.id, user.id),
            )
            result = await cursor.fetchone()

            if not result:
                await ctx.reply(
                    view=ErrorView(
                        "Erreur", f"{user.mention} is not in the bypass users list."
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM bypassed_users WHERE guild_id = ? AND user_id = ?",
                    (ctx.guild.id, user.id),
                )
                await db.commit()
                await ctx.reply(
                    view=SuccessView(
                        "Succès",
                        f"{user.mention} retiré de la liste des utilisateurs contournés avec succès.",
                    )
                )

    @_bypass.command(
        name="show",
        aliases=["list"],
        help="Affiche la liste des utilisateurs contournés.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def bypass_show(self, ctx: commands.Context):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id FROM bypassed_users WHERE guild_id = ?", (ctx.guild.id,)
            )
            users = await cursor.fetchall()

            if not users:
                await ctx.reply(
                    view=ListView(
                        "Bypassed Users",
                        [],
                        "Aucun utilisateur n’est actuellement contourné sur ce serveur.",
                    )
                )
            else:
                await ctx.reply(
                    view=ListView(
                        "Bypassed Users", [u[0] for u in users], "", ctx.guild
                    )
                )
