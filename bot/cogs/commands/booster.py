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
from utils.emoji import CROSS, NITRO_BOOST, TICK, TIMER
import asyncio
import logging
import aiosqlite
import json
from discord.ext import commands
from utils.Tools import *
from discord.ext.commands import Context
from discord import app_commands
import time
import datetime
import re
from typing import *
from time import strftime
from core import Cog, zyrox, Context
from discord.ui import LayoutView, TextDisplay, Separator, Container
from utils.cv2 import CV2, build_container


class CV2(LayoutView):
    def __init__(self, title, *sections):
        super().__init__(timeout=None)
        items = [TextDisplay(f"**{title}**")]
        for s in sections:
            if s:
                items.append(Separator(visible=True))
                items.append(TextDisplay(str(s)))
        self.add_item(build_container(*items))


logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class Booster(Cog):
    def __init__(self, bot: Zyrox):
        self.bot = bot
        self.color = 0xFF0000
        self.db_path = "db/boost.db"
        self.bot.loop.create_task(self.setup_database())

        self.url_pattern = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

    async def setup_database(self):
        """Initialize boost database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS boost_config (
                    guild_id INTEGER PRIMARY KEY,
                    config TEXT NOT NULL
                )
            """)
            await db.commit()

    async def get_boost_config(self, guild_id: int) -> dict:
        """Get boost configuration for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT config FROM boost_config WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return json.loads(row[0])

                default_config = {
                    "boost": {
                        "channel": [],
                        "message": "{user.mention} just boosted {server.name}! 🎉",
                        "embed": True,
                        "ping": False,
                        "image": "",
                        "thumbnail": "",
                        "autodel": 0,
                    },
                    "boost_roles": {"roles": []},
                }
                await self.update_boost_config(guild_id, default_config)
                return default_config

    async def update_boost_config(self, guild_id: int, config: dict):
        """Update boost configuration for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO boost_config (guild_id, config) VALUES (?, ?)",
                (guild_id, json.dumps(config)),
            )
            await db.commit()

    def is_authorized(self, ctx) -> bool:
        """Check if user is authorized to use admin commands"""
        return (
            ctx.author == ctx.guild.owner
            or ctx.author.guild_permissions.administrator
            or ctx.author.top_role.position >= ctx.guild.me.top_role.position
        )

    def format_boost_message(
        self, message: str, user: discord.Member, guild: discord.Guild
    ) -> str:
        """Format boost message with new variable style"""
        replacements = {
            "{server.name}": guild.name,
            "{server.id}": str(guild.id),
            "{server.owner}": str(guild.owner),
            "{server.icon}": guild.icon.url if guild.icon else "",
            "{server.boost_count}": str(guild.premium_subscription_count),
            "{server.boost_level}": f"Level {guild.premium_tier}",
            "{server.member_count}": str(guild.member_count),
            "{user.name}": user.display_name,
            "{user.mention}": user.mention,
            "{user.tag}": str(user),
            "{user.id}": str(user.id),
            "{user.avatar}": user.display_avatar.url,
            "{user.created_at}": f"<t:{int(user.created_at.timestamp())}:F>",
            "{user.joined_at}": (
                f"<t:{int(user.joined_at.timestamp())}:F>"
                if user.joined_at
                else "Unknown"
            ),
            "{user.top_role}": user.top_role.name if user.top_role else "None",
            "{user.is_booster}": str(bool(user.premium_since)),
            "{user.is_mobile}": str(user.is_on_mobile()),
            "{user.boosted_at}": (
                f"<t:{int(user.premium_since.timestamp())}:F>"
                if user.premium_since
                else "Unknown"
            ),
        }

        for old, new in replacements.items():
            message = message.replace(old, new)

        return message

    async def send_permission_error(self, ctx):
        """Send permission error embed"""
        await ctx.send(
            view=CV2(
                "Erreur de permission",
                "```diff\n- You must have Administrator permission.\n- Your top role should be above my top role.\n```",
            )
        )

    @commands.group(
        name="boost",
        aliases=["bst"],
        invoke_without_command=True,
        help="Commandes de configuration du message de boost",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_boost.command(name="thumbnail", help="Définir la miniature du message de boost")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_thumbnail(self, ctx, thumbnail_url: str):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        if not self.url_pattern.match(thumbnail_url):
            await ctx.send(
                view=CV2("Error", f"{CROSS} Merci de fournir une URL valide.")
            )

            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["thumbnail"] = thumbnail_url
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès",
                f"{TICK} URL de la miniature de boost mise à jour avec succès.",
            )
        )

    @_boost.command(name="image", help="Définir l’image du message de boost")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_image(self, ctx, *, image_url: str):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        if not self.url_pattern.match(image_url):
            await ctx.send(
                view=CV2("Error", f"{CROSS} Merci de fournir une URL valide.")
            )

            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["image"] = image_url
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès", f"{TICK} URL de l’image de boost mise à jour avec succès."
            )
        )

    @_boost.command(
        name="autodel",
        help="Définir le délai de suppression auto des messages de boost (0 pour désactiver)",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_autodel(self, ctx, seconds: int):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        if seconds < 0:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Le délai de suppression auto doit être de 0 ou plus.",
                )
            )

            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["autodel"] = seconds
        await self.update_boost_config(ctx.guild.id, data)

        description = f"{TICK} Délai de suppression auto défini sur {seconds} secondes."
        if seconds == 0:
            description = f"{TICK} La suppression auto a été désactivée."

        await ctx.send(view=CV2("Succès", description))

    @_boost.command(name="message", help="Définir le contenu du message de boost")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_message(self, ctx):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return
        variables_text = (
            "Send your boost message in this channel now.\n\n**Available Variables:**\n"
            "```\n"
            "{server.name}         - Server name\n"
            "{server.id}           - Server ID\n"
            "{server.owner}        - Server owner\n"
            "{server.icon}         - Server icon URL\n"
            "{server.boost_count}  - Current boost count\n"
            "{server.boost_level}  - Boost level (e.g., Level 2)\n"
            "{server.member_count} - Total member count\n\n"
            "{user.name}        - Booster's display name\n"
            "{user.mention}     - Mention the booster\n"
            "{user.tag}         - Booster's full tag\n"
            "{user.id}          - Booster's ID\n"
            "{user.avatar}      - Booster's avatar URL\n"
            "{user.created_at}  - When the account was created\n"
            "{user.joined_at}   - When user joined the server\n"
            "{user.top_role}    - Booster's top role name\n"
            "{user.is_booster}  - Whether they're a booster\n"
            "{user.is_mobile}   - Whether on mobile\n"
            "{user.boosted_at}  - Boost timestamp\n"
            "```\n*Tu as 60 secondes pour répondre*"
        )
        await ctx.send(
            view=CV2(f"{TICK} Configuration du message de boost", variables_text)
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            message = await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(
                view=CV2("Temps écoulé", f"{TIMER} Temps écoulé ! Réessaie.")
            )

            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["message"] = message.content
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2("Succès", f"{TICK} Message de boost mis à jour avec succès.")
        )

    @_boost.command(
        name="embed",
        help="Activer/désactiver le format embed pour les messages de boost",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_embed(self, ctx):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["embed"] = not data["boost"]["embed"]
        await self.update_boost_config(ctx.guild.id, data)

        status = "enabled" if data["boost"]["embed"] else "disabled"
        await ctx.send(
            view=CV2("Succès", f"{TICK} Le format embed a été **{status}**.")
        )

    @_boost.command(name="ping", help="Activer/désactiver la mention du booster")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_ping(self, ctx):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        data["boost"]["ping"] = not data["boost"]["ping"]
        await self.update_boost_config(ctx.guild.id, data)

        status = "enabled" if data["boost"]["ping"] else "disabled"
        await ctx.send(
            view=CV2("Succès", f"{TICK} La mention du booster a été **{status}**.")
        )

    @_boost.group(name="channel", help="Gérer les salons de notification de boost")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_channel(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_boost_channel.command(
        name="add", help="Ajouter un salon de notification de boost"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_channel_add(self, ctx, channel: discord.TextChannel):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        channels = data["boost"]["channel"]

        if len(channels) >= 3:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Limite maximale de salons de boost atteinte (3 salons).",
                )
            )
            return

        if str(channel.id) in channels:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Ce salon est déjà dans la liste des salons de boost.",
                )
            )
            return

        channels.append(str(channel.id))
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès",
                f"{TICK} {channel.mention} ajouté à la liste des salons de boost avec succès.",
            )
        )

    @_boost_channel.command(
        name="remove", help="Retirer un salon de notification de boost"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_channel_remove(self, ctx, channel: discord.TextChannel):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        channels = data["boost"]["channel"]

        if not channels:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Aucun salon de boost n’est actuellement configuré.",
                )
            )
            return

        if str(channel.id) not in channels:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Ce salon n’est pas dans la liste des salons de boost.",
                )
            )
            return

        channels.remove(str(channel.id))
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès",
                f"{TICK} {channel.mention} retiré de la liste des salons de boost avec succès.",
            )
        )

    @_boost.command(name="test", help="Tester l’aperçu du message de boost")
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boost_test(self, ctx):
        data = await self.get_boost_config(ctx.guild.id)
        channels = data["boost"]["channel"]

        if not channels:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Configure d’abord un salon de boost avec `boost channel add #channel`.",
                )
            )
            return

        formatted_message = self.format_boost_message(
            data["boost"]["message"], ctx.author, ctx.guild
        )

        channel = self.bot.get_channel(int(channels[0]))
        if not channel:
            await ctx.send(
                view=CV2("Error", f"{CROSS} Le salon de boost configuré n’existe plus.")
            )

            return

        try:
            if data["boost"]["embed"]:
                embed = discord.Embed(description=formatted_message, color=self.color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
                )
                embed.timestamp = discord.utils.utcnow()

                if data["boost"]["image"]:
                    embed.set_image(url=data["boost"]["image"])

                if data["boost"]["thumbnail"]:
                    embed.set_thumbnail(url=data["boost"]["thumbnail"])

                if ctx.guild.icon:
                    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)

                ping_content = ctx.author.mention if data["boost"]["ping"] else ""
                await channel.send(ping_content, embed=embed)
            else:
                await channel.send(formatted_message)

        except discord.Forbidden:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Je n’ai pas la permission d’envoyer des messages dans le salon de boost.",
                )
            )

        except Exception as e:
            await ctx.send(
                view=CV2("Error", f"{CROSS} Une erreur est survenue : `{str(e)}`")
            )

    @_boost.command(name="config", help="Voir la configuration actuelle des boosts")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _boost_config(self, ctx):
        data = await self.get_boost_config(ctx.guild.id)
        channels = data["boost"]["channel"]

        if not channels:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Configure d’abord un salon de boost avec `boost channel add #channel`.",
                )
            )

            return

        channel_mentions = []
        for channel_id in channels:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                channel_mentions.append(channel.mention)

        embed_status = (
            f"{TICK} Enabled" if data["boost"]["embed"] else f"{CROSS} Disabled"
        )
        ping_status = (
            f"{TICK} Enabled" if data["boost"]["ping"] else f"{CROSS} Disabled"
        )
        autodel_status = (
            f"{data['boost']['autodel']}s" if data["boost"]["autodel"] else "Disabled"
        )
        channels_str = "\n".join(channel_mentions) if channel_mentions else "None"

        config_text = (
            f"**Salons**\n{channels_str}\n\n"
            f"**Message**\n```{data['boost']['message']}```\n"
            f"**Embed :** {embed_status}\n"
            f"**Mention :** {ping_status}\n"
            f"**Suppression auto :** {autodel_status}"
        )

        await ctx.send(
            view=CV2(
                f"{NITRO_BOOST} Configuration des boosts pour {ctx.guild.name}",
                config_text,
            )
        )

    @_boost.command(name="reset", help="Réinitialiser la configuration des boosts")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _boost_reset(self, ctx):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)

        if not data["boost"]["channel"]:
            await ctx.send(
                view=CV2(
                    "Error", f"{CROSS} Aucune configuration de boost à réinitialiser."
                )
            )
            return

        data["boost"]["channel"] = []
        data["boost"]["image"] = ""
        data["boost"]["message"] = "{user.mention} just boosted {server.name}! 🎉"
        data["boost"]["thumbnail"] = ""
        data["boost"]["embed"] = True
        data["boost"]["ping"] = False
        data["boost"]["autodel"] = 0

        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès",
                f"{TICK} Toute la configuration des boosts a été réinitialisée.",
            )
        )

    @commands.group(
        name="boostrole", invoke_without_command=True, help="Gérer les rôles de boost"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @blacklist_check()
    @ignore_check()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boostrole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_boostrole.command(name="config", help="Voir la configuration des rôles de boost")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _boostrole_config(self, ctx):
        data = await self.get_boost_config(ctx.guild.id)
        role_ids = data["boost_roles"]["roles"]

        if not role_ids:
            await ctx.send(
                view=CV2(
                    f"Rôles de boost - {ctx.guild.name}",
                    "Aucun rôle de boost configuré.",
                )
            )
            return

        roles = []
        for role_id in role_ids:
            role = ctx.guild.get_role(int(role_id))
            if role:
                roles.append(role.mention)

        roles_str = "\n".join(roles) if roles else "Aucun rôle valide trouvé"
        await ctx.send(view=CV2(f"Rôles de boost - {ctx.guild.name}", roles_str))

    @_boostrole.command(name="add", help="Ajouter un rôle de boost")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boostrole_add(self, ctx, role: discord.Role):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        roles = data["boost_roles"]["roles"]

        if len(roles) >= 10:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Limite maximale de rôles de boost atteinte (10 rôles).",
                )
            )
            return

        if str(role.id) in roles:
            await ctx.send(
                view=CV2("Error", f"{CROSS} {role.mention} est déjà un rôle de boost.")
            )
            return

        roles.append(str(role.id))
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès", f"{TICK} {role.mention} a été ajouté comme rôle de boost."
            )
        )

    @_boostrole.command(name="remove", help="Retirer un rôle de boost")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _boostrole_remove(self, ctx, role: discord.Role):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)
        roles = data["boost_roles"]["roles"]

        if not roles:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Aucun rôle de boost n’est actuellement configuré.",
                )
            )
            return

        if str(role.id) not in roles:
            await ctx.send(
                view=CV2("Error", f"{CROSS} {role.mention} n’est pas un rôle de boost.")
            )
            return

        roles.remove(str(role.id))
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2(
                "Succès", f"{TICK} {role.mention} a été retiré des rôles de boost."
            )
        )

    @_boostrole.command(
        name="reset", help="Réinitialiser la configuration des rôles de boost"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _boostrole_reset(self, ctx):
        if not self.is_authorized(ctx):
            await self.send_permission_error(ctx)
            return

        data = await self.get_boost_config(ctx.guild.id)

        if not data["boost_roles"]["roles"]:
            await ctx.send(
                view=CV2(
                    "Error",
                    f"{CROSS} Aucun rôle de boost n’est actuellement configuré.",
                )
            )
            return

        data["boost_roles"]["roles"] = []
        await self.update_boost_config(ctx.guild.id, data)

        await ctx.send(
            view=CV2("Succès", f"{TICK} Tous les rôles de boost ont été effacés.")
        )


async def setup(bot):
    await bot.add_cog(Booster(bot))
