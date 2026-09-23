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

import os
import discord
from utils.emoji import BOOST, CODEBASE, CROSS, KING, TICK, UPTIME, ZWARNING
from discord.ext import commands
import datetime
import sys
from discord.ui import (
    Button,
    View,
    LayoutView,
    TextDisplay,
    Separator,
    Container,
    ActionRow,
    MediaGallery,
)
from utils.cv2 import CV2, build_container
import psutil
import time
from utils.Tools import *
from discord.ext import commands, menus
from discord.ext.commands import BucketType, cooldown
import requests
from typing import *
from utils import *
from utils.config import BotName, serverLink
from utils import (
    Paginator,
    DescriptionEmbedPaginator,
    FieldPagePaginator,
    TextPaginator,
)
from core import Cog, zyrox, Context
from typing import Optional
import aiosqlite
import asyncio
import aiohttp

start_time = time.time()


def datetime_to_seconds(thing: datetime.datetime):
    current_time = datetime.datetime.fromtimestamp(time.time())
    return round(
        round(time.time()) + (current_time - thing.replace(tzinfo=None)).total_seconds()
    )


tick = f"{TICK}>"
cross = CROSS


class RoleInfoView(View):
    def __init__(self, role: discord.Role, author_id):
        super().__init__(timeout=180)
        self.role = role
        self.author_id = author_id

    @discord.ui.button(
        label="Afficher les permissions",
        emoji=f"{CODEBASE} ",
        style=discord.ButtonStyle.secondary,
    )
    async def show_permissions(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Oups ! Ce message ne t’appartient pas. Tu dois exécuter cette commande pour interagir.",
                ephemeral=True,
            )
            return

        permissions = [
            perm.replace("_", " ").title()
            for perm, value in self.role.permissions
            if value
        ]
        permission_text = ", ".join(permissions) if permissions else "None"
        await interaction.response.send_message(
            view=CV2(
                f"Permissions pour {self.role.name}",
                permission_text or "Aucune permission.",
            ),
            ephemeral=True,
        )


class OverwritesView(View):
    def __init__(self, channel, author_id):
        super().__init__(timeout=180)
        self.channel = channel
        self.author_id = author_id

    @discord.ui.button(
        label="Afficher les overwrites", style=discord.ButtonStyle.primary
    )
    async def show_overwrites(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Oups ! Ce message ne t’appartient pas. Tu dois exécuter cette commande pour interagir.",
                ephemeral=True,
            )
            return

        overwrites = []
        for target, perms in self.channel.overwrites.items():
            permissions = {
                "Voir le salon": perms.view_channel,
                "Envoyer des messages": perms.send_messages,
                "Lire l’historique des messages": perms.read_message_history,
                "Gérer les messages": perms.manage_messages,
                "Intégrer des liens": perms.embed_links,
                "Joindre des fichiers": perms.attach_files,
                "Gérer les salons": perms.manage_channels,
                "Gérer les permissions": perms.manage_permissions,
                "Gérer les webhooks": perms.manage_webhooks,
                "Créer une invitation instantanée": perms.create_instant_invite,
                "Ajouter des réactions": perms.add_reactions,
                "Mentionner Everyone": perms.mention_everyone,
                "Expulser des membres": perms.kick_members,
                "Bannir des membres": perms.ban_members,
                "Modérer les membres": perms.moderate_members,
                "Envoyer des messages TTS": perms.send_tts_messages,
                "Utiliser des emojis externes": perms.external_emojis,
                "Utiliser des stickers externes": perms.external_stickers,
                "Voir le journal d’audit": perms.view_audit_log,
                "Rendre muets des membres (vocal)": perms.mute_members,
                "Rendre sourds des membres (vocal)": perms.deafen_members,
                "Administrateur": perms.administrator,
            }

            overwrites.append(
                f"**For {target.name}**\n"
                + "\n".join(
                    f"  * **{perm}:** {'{TICK}>' if value else '{CROSS}' if value is False else '⛔'}"
                    for perm, value in permissions.items()
                )
            )

        ow_text = (
            "\n".join(overwrites) if overwrites else "Aucun overwrite pour ce salon."
        )
        footer = f"{TICK} = Autorisé, {CROSS} = Refusé, ⛔ = Aucun"
        await interaction.response.send_message(
            view=CV2(f"Overwrites pour {self.channel.name}", ow_text, footer),
            ephemeral=True,
        )


class Extra(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF0000
        self.start_time = datetime.datetime.now()

    @commands.hybrid_group(name="banner")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def banner(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @banner.command(name="server")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def server(self, ctx):
        if not ctx.guild.banner:
            await ctx.reply(
                view=CV2(f"{cross} Error", "Ce serveur n’a pas de bannière.")
            )
        else:
            webp = ctx.guild.banner.replace(format="webp")
            jpg = ctx.guild.banner.replace(format="jpg")
            png = ctx.guild.banner.replace(format="png")
            links = f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
            if ctx.guild.banner.is_animated():
                links += f" | [`GIF`]({ctx.guild.banner.replace(format='gif')})"
            view = LayoutView(timeout=None)
            gallery = MediaGallery()
            gallery.add_item(media=str(ctx.guild.banner.url))
            view.add_item(
                build_container(
                    TextDisplay(f"**{ctx.guild.name}**"),
                    Separator(visible=True),
                    TextDisplay(links),
                    gallery,
                )
            )
            await ctx.reply(view=view)

    @banner.command(name="user")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _user(
        self, ctx, member: Optional[Union[discord.Member, discord.User]] = None
    ):
        if member == None or member == "":
            member = ctx.author
        bannerUser = await self.bot.fetch_user(member.id)
        if not bannerUser.banner:
            await ctx.reply(
                view=CV2(f"{cross} Error", f"{member} n’a pas de bannière.")
            )
        else:
            webp = bannerUser.banner.replace(format="webp")
            jpg = bannerUser.banner.replace(format="jpg")
            png = bannerUser.banner.replace(format="png")
            links = f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
            if bannerUser.banner.is_animated():
                links += f" | [`GIF`]({bannerUser.banner.replace(format='gif')})"
            view = LayoutView(timeout=None)
            gallery = MediaGallery()
            gallery.add_item(media=str(bannerUser.banner.url))
            view.add_item(
                build_container(
                    TextDisplay(f"**{member}**"),
                    Separator(visible=True),
                    TextDisplay(links),
                    gallery,
                )
            )
            await ctx.send(view=view)

    @commands.command(name="uptime", description="Affiche l’uptime du bot.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def uptime(self, ctx):
        pfp = ctx.author.display_avatar.url

        uptime_seconds = int(round(time.time() - start_time))
        uptime_timedelta = datetime.timedelta(seconds=uptime_seconds)

        uptime_string = f"Up since {datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        uptime_duration_string = f"{uptime_timedelta.days} days, {uptime_timedelta.seconds // 3600} hours, {(uptime_timedelta.seconds // 60) % 60} minutes, {uptime_timedelta.seconds % 60} seconds"

        uptime_text = (
            f"**__UTC__**\n{ZWARNING} {uptime_string}\n\n"
            f"**__Online Duration__**\n{UPTIME} {uptime_duration_string}"
        )
        await ctx.send(view=CV2(f"{BRAND_NAME} Uptime du manager", uptime_text))

    @commands.hybrid_command(
        name="serverinfo", aliases=["sinfo", "si"], with_app_command=True
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx):
        c_at = ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        about = (
            f"**Name:** {ctx.guild.name}\n"
            f"**ID:** {ctx.guild.id}\n"
            f"**Owner {KING}:** {ctx.guild.owner} (<@{ctx.guild.owner_id}>)\n"
            f"**Created At:** {c_at}\n"
            f"**Members:** {len(ctx.guild.members)}"
        )
        desc_section = (
            f"\n\n**__Description__**\n{ctx.guild.description}"
            if ctx.guild.description
            else ""
        )
        stats = (
            f"**Verification Level:** {ctx.guild.verification_level}\n"
            f"**Channels:** {len(ctx.guild.channels)}\n"
            f"**Roles:** {len(ctx.guild.roles)}\n"
            f"**Emojis:** {len(ctx.guild.emojis)}\n"
            f"**Boost Status:** Level {ctx.guild.premium_tier} (Boosts: {ctx.guild.premium_subscription_count})"
        )
        features_text = ""
        if ctx.guild.features:
            features = "\n".join(
                [
                    f"{TICK}>: {f[:1].upper() + f[1:].lower().replace('_', ' ')}"
                    for f in ctx.guild.features
                ]
            )
            features_text = f"\n\n**__Features__**\n{features[:1000] if len(features) > 1024 else features}"
        regular_emojis = [e for e in ctx.guild.emojis if not e.animated]
        animated_emojis = [e for e in ctx.guild.emojis if e.animated]
        emoji_info = f"Regular: {len(regular_emojis)}/100 | Animated: {len(animated_emojis)}/100 | Total: {len(ctx.guild.emojis)}/200"
        roles = ctx.guild.roles
        roles_display = "\n".join([r.mention for r in roles[:10]])
        if len(roles) > 10:
            roles_display += f"\n...and {len(roles) - 10} more"
        full_text = (
            f"**__About__**\n{about}{desc_section}\n\n"
            f"**__General Stats__**\n{stats}{features_text}\n\n"
            f"**__Channels__**\n**Total:** {len(ctx.guild.channels)} — {len(ctx.guild.text_channels)} text, {len(ctx.guild.voice_channels)} voice\n\n"
            f"**__Emoji Info__**\n{emoji_info}\n\n"
            f"**__Boost Status__**\nLevel: {ctx.guild.premium_tier} [{BOOST}{ctx.guild.premium_subscription_count} boosts]\n\n"
            f"**__Server Roles__ [{len(roles)}]**\n{roles_display}"
        )
        icon_url = ctx.guild.icon.url if ctx.guild.icon else None
        view = LayoutView(timeout=None)
        items = [
            TextDisplay(f"# {ctx.guild.name}'s Information"),
            Separator(visible=True),
            TextDisplay(full_text),
        ]
        if icon_url or ctx.guild.banner:
            gallery = MediaGallery()
            if icon_url:
                gallery.add_item(media=str(icon_url))
            if ctx.guild.banner:
                gallery.add_item(media=str(ctx.guild.banner.url))
            items.append(gallery)
        view.add_item(build_container(*items))
        await ctx.send(view=view)

    @commands.hybrid_command(
        name="userinfo",
        aliases=["whois", "ui"],
        usage="Userinfo [user]",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _userinfo(
        self, ctx, member: Optional[Union[discord.Member, discord.User]] = None
    ):
        if member == None or member == "":
            member = ctx.author
        elif member not in ctx.guild.members:
            member = await self.bot.fetch_user(member.id)

        badges = ""
        if member.public_flags.hypesquad:
            badges += "HypeSquad Events, "
        if member.public_flags.hypesquad_balance:
            badges += "HypeSquad Balance, "
        if member.public_flags.hypesquad_bravery:
            badges += "HypeSquad Bravery, "
        if member.public_flags.hypesquad_brilliance:
            badges += "HypeSquad Brilliance, "
        if member.public_flags.early_supporter:
            badges += "Early Supporter, "
        if member.public_flags.active_developer:
            badges += "Active Developer, "
        if member.public_flags.verified_bot_developer:
            badges += "Early Verified Bot Developer, "
        if member.public_flags.discord_certified_moderator:
            badges += "Moderators Program Alumni, "
        if member.public_flags.staff:
            badges += "Discord Staff, "
        if member.public_flags.partner:
            badges += "Propriétaire de serveur partenaire "
        if badges == None or badges == "":
            badges += f"{cross}"

        if member in ctx.guild.members:
            nickk = f"{member.nick if member.nick else 'Aucun'}"
            joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
        else:
            nickk = "Aucun"
            joinedat = "Aucune"

        kp = ""
        if member in ctx.guild.members:
            if member.guild_permissions.kick_members:
                kp += "Expulser des membres"
            if member.guild_permissions.ban_members:
                kp += " , Bannir des membres"
            if member.guild_permissions.administrator:
                kp += " , Administrateur"
            if member.guild_permissions.manage_channels:
                kp += " , Gérer les salons"

            if member.guild_permissions.manage_guild:
                kp += " , Gérer le serveur"

            if member.guild_permissions.manage_messages:
                kp += " , Gérer les messages"
            if member.guild_permissions.mention_everyone:
                kp += " , Mentionner Everyone"
            if member.guild_permissions.manage_nicknames:
                kp += " , Gérer les pseudos"
            if member.guild_permissions.manage_roles:
                kp += " , Gérer les rôles"
            if member.guild_permissions.manage_webhooks:
                kp += " , Gérer les webhooks"
            if member.guild_permissions.manage_emojis:
                kp += " , Gérer les emojis"

            if kp is None or kp == "":
                kp = "Aucune"

        if member in ctx.guild.members:
            if member == ctx.guild.owner:
                aklm = "Propriétaire du serveur"
            elif member.guild_permissions.administrator:
                aklm = "Admin du serveur"
            elif (
                member.guild_permissions.ban_members
                or member.guild_permissions.kick_members
            ):
                aklm = "Modérateur du serveur"
            else:
                aklm = "Membre du serveur"

        bannerUser = await self.bot.fetch_user(member.id)
        embed = discord.Embed(color=self.color)
        embed.timestamp = discord.utils.utcnow()
        if not bannerUser.banner:
            pass
        else:
            embed.set_image(url=bannerUser.banner)
        embed.set_author(
            name=f"Informations de {member.name}",
            icon_url=member.avatar.url if member.avatar else member.default_avatar.url,
        )
        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.add_field(
            name="__Informations générales__",
            value=f"""
**Nom :** {member}
**ID :** {member.id}
**Pseudo :** {nickk}
**Bot ? :** {'{TICK}> Oui' if member.bot else '{CROSS} Non'}
**Badges :** {badges}
**Compte créé :** <t:{round(member.created_at.timestamp())}:R>
**Arrivé sur le serveur :** {joinedat}
            """,
            inline=False,
        )
        if member in ctx.guild.members:
            r = (
                ", ".join(role.mention for role in member.roles[1:][::-1])
                if len(member.roles) > 1
                else "Aucun."
            )
            embed.add_field(
                name="__Infos des rôles__",
                value=f"""
**Rôle le plus haut :** {member.top_role.mention if len(member.roles) > 1 else 'Aucun'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' et plus...'}
**Couleur :** {member.color if member.color else '99aab5'}
                """,
                inline=False,
            )
        if member in ctx.guild.members:
            embed.add_field(
                name="__Extra__",
                value=f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice :** {'None' if not member.voice else member.voice.channel.mention}",
                inline=False,
            )
        if member in ctx.guild.members:
            embed.add_field(
                name="__Permissions clés__", value=", ".join([kp]), inline=False
            )
        if member in ctx.guild.members:
            embed.add_field(name="__Reconnaissance__", value=f"{aklm}", inline=False)
        if member in ctx.guild.members:
            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
        else:
            if member not in ctx.guild.members:
                embed.set_footer(
                    text=f"{member.name} n’est pas sur ce serveur.",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="roleinfo",
        aliases=["ri"],
        help="Affiche les informations d’un rôle précis.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        members = role.members
        created_at = role.created_at.strftime("%Y-%m-%d %H:%M:%S")
        total_roles = len(ctx.guild.roles)
        role_position = total_roles - role.position
        role_text = (
            f"**__Informations générales__**\n"
            f"**ID:** {role.id}\n**Name:** {role.name}\n**Mention:** <@&{role.id}>\n"
            f"**Color:** {str(role.color)}\n**Total Members:** {len(role.members)}\n\n"
            f"**Position:** {role_position}\n**Mentionable:** {role.mentionable}\n"
            f"**Hoisted:** {role.hoist}\n**Managed:** {role.managed}\n**Created At:** {created_at}"
        )
        view = RoleInfoView(role, ctx.author.id)
        await ctx.send(content=role_text, view=view)

    @commands.command(
        name="boostcount",
        help="Affiche le nombre de boosts",
        usage="boosts",
        aliases=["bco"],
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def boosts(self, ctx):
        await ctx.send(
            view=CV2(
                f"{BOOST} Boosts Count Of {ctx.guild.name}",
                f"**Total `{ctx.guild.premium_subscription_count}` boosts**",
            )
        )

    @commands.hybrid_group(
        name="list", invoke_without_command=True, with_app_command=True
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def __list_(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @__list_.command(
        name="boosters",
        aliases=["boost", "booster"],
        usage="List boosters",
        help="Liste des boosters du serveur",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_boost(self, ctx):
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{round(mem.premium_since.timestamp())}:R>"
            for no, mem in enumerate(guild.premium_subscribers, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"List of Boosters in {guild.name} - {len(guild.premium_subscribers)}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="bans",
        help="Liste de tous les membres bannis du serveur",
        aliases=["ban"],
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(view_audit_log=True)
    @commands.bot_has_permissions(view_audit_log=True)
    async def list_ban(self, ctx):
        bans = [member async for member in ctx.guild.bans()]
        if len(bans) == 0:
            return await ctx.reply(
                "Il n’y a aucun utilisateur banni sur ce serveur.", mention_author=False
            )
        else:
            mems = [member async for member in ctx.guild.bans()]
            guild = ctx.guild
            entries = [f"`#{no}.` {mem}" for no, mem in enumerate(mems, start=1)]
            paginator = Paginator(
                source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=f"Banned Users in {guild.name} - {len(bans)}",
                    description="",
                    per_page=10,
                ),
                ctx=ctx,
            )
            await paginator.paginate()

    @__list_.command(
        name="inrole",
        aliases=["inside-role"],
        help="Liste des membres ayant le rôle spécifié",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_inrole(self, ctx, role: discord.Role):
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(role.members, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"List of Members in {role} - {len(role.members)}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="emojis",
        aliases=["emoji"],
        help="Liste des emojis du serveur avec leurs IDs",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_emojis(self, ctx):
        guild = ctx.guild
        entries = [
            f"`#{no}.` {e} - `{e}`" for no, e in enumerate(ctx.guild.emojis, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"List of Emojis in {guild.name} - {len(ctx.guild.emojis)}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="roles",
        aliases=["role"],
        help="Liste de tous les rôles du serveur avec leurs IDs",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def list_roles(self, ctx):
        guild = ctx.guild
        entries = [
            f"`#{no}.` {e.mention} - `[{e.id}]`"
            for no, e in enumerate(ctx.guild.roles, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"List of Roles in {guild.name} - {len(ctx.guild.roles)}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="bots",
        aliases=["bot"],
        help="Liste de tous les bots du serveur",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_bots(self, ctx):
        guild = ctx.guild
        people = filter(lambda member: member.bot, ctx.guild.members)
        people = sorted(people, key=lambda member: member.joined_at)
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}]"
            for no, mem in enumerate(people, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Bots in {guild.name} - {len(people)}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="admins",
        aliases=["admin"],
        help="Liste de tous les admins du serveur",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_admin(self, ctx):
        mems = [mem for mem in ctx.guild.members if mem.guild_permissions.administrator]
        mems = sorted(mems, key=lambda mem: not mem.bot)
        admins = len(
            [mem for mem in ctx.guild.members if mem.guild_permissions.administrator]
        )
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Admins in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="invoice",
        help="Liste de tous les utilisateurs dans un salon vocal",
        aliases=["invc"],
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def listusers(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("Tu n’es pas connecté à un salon vocal")
        members = ctx.author.voice.channel.members
        entries = [
            f"`[{n}]` | {member} [{member.mention}]"
            for n, member in enumerate(members, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                description="",
                title=f"Voice List of {ctx.author.voice.channel.name} - {len(members)}",
                color=self.color,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="moderators",
        help="Liste de tous les admins du serveur",
        aliases=["mods"],
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_mod(self, ctx):
        membs = [
            mem
            for mem in ctx.guild.members
            if mem.guild_permissions.ban_members or mem.guild_permissions.kick_members
        ]
        mems = filter(lambda member: member.bot, ctx.guild.members)
        mems = sorted(membs, key=lambda mem: mem.joined_at)
        admins = len(
            [
                mem
                for mem in ctx.guild.members
                if mem.guild_permissions.ban_members
                or mem.guild_permissions.kick_members
            ]
        )
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Mods in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="early",
        aliases=["sup"],
        help="Liste des membres ayant le badge Early Supporter.",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_early(self, ctx):
        mems = [memb for memb in ctx.guild.members if memb.public_flags.early_supporter]
        mems = sorted(mems, key=lambda memb: memb.created_at)
        admins = len(
            [memb for memb in ctx.guild.members if memb.public_flags.early_supporter]
        )
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id})  [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Early Supporters Id's in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="activedeveloper",
        help="Liste des membres ayant le badge Active Developer.",
        aliases=["activedev"],
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_activedeveloper(self, ctx):
        mems = [
            memb for memb in ctx.guild.members if memb.public_flags.active_developer
        ]
        mems = sorted(mems, key=lambda memb: memb.created_at)
        admins = len(
            [memb for memb in ctx.guild.members if memb.public_flags.active_developer]
        )
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) [{mem.mention}] - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Active Developer Id's in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="createdat",
        help="Liste des dates de création de compte de tous les utilisateurs",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_cpos(self, ctx):
        mems = [memb for memb in ctx.guild.members]
        mems = sorted(mems, key=lambda memb: memb.created_at)
        admins = len([memb for memb in ctx.guild.members])
        guild = ctx.guild
        entries = [
            f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Creation every id in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @__list_.command(
        name="joinedat",
        help="Liste des dates d’arrivée sur le serveur de tous les utilisateurs",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list_joinpos(self, ctx):
        mems = [memb for memb in ctx.guild.members]
        mems = sorted(mems, key=lambda memb: memb.joined_at)
        admins = len([memb for memb in ctx.guild.members])
        guild = ctx.guild
        entries = [
            f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) Joined At - <t:{int(mem.joined_at.timestamp())}:D>"
            for no, mem in enumerate(mems, start=1)
        ]
        paginator = Paginator(
            source=DescriptionEmbedPaginator(
                entries=entries,
                title=f"Join Position of every user in {guild.name} - {admins}",
                description="",
                per_page=10,
            ),
            ctx=ctx,
        )
        await paginator.paginate()

    @commands.command(
        name="joined-at",
        help="Affiche quand un utilisateur a rejoint",
        usage="joined-at [user]",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joined_at(self, ctx):
        joined = ctx.author.joined_at.strftime("%a, %d %b %Y %I:%M %p")
        await ctx.send(view=CV2("joined-at", f"**`{joined}`**"))

    @commands.command(name="github", usage="github [search]")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def github(self, ctx, *, search_query):
        json = requests.get(
            f"https://api.github.com/search/repositories?q={search_query}"
        ).json()

        if json["total_count"] == 0:
            await ctx.send(f"Aucun dépôt trouvé avec le nom : {search_query}")
        else:
            await ctx.send(
                f"Found result for '{search_query}':\n{json['items'][0]['html_url']}"
            )

    @commands.hybrid_command(
        name="vcinfo",
        description="Voir les informations d’un salon vocal.",
        help="Voir les informations d’un salon vocal.",
        usage="<VoiceChannel>",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def vcinfo(self, ctx, channel: discord.VoiceChannel = None):
        if channel is None:
            await ctx.reply(
                view=CV2(f"{cross} Error", "Merci de fournir un salon vocal valide.")
            )
            return
        vc_text = (
            f"**ID:** {channel.id}\n**Members:** {len(channel.members)}\n"
            f"**Bitrate:** {channel.bitrate/1000} kbps\n"
            f"**Created At:** {channel.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Category:** {channel.category.name if channel.category else 'None'}\n"
            f"**Region:** {channel.rtc_region}"
        )
        if channel.user_limit:
            vc_text += f"\n**User Limit:** {channel.user_limit}"
        view = LayoutView(timeout=None)
        join_btn = Button(
            label="Rejoindre",
            style=discord.ButtonStyle.link,
            url=f"https://discord.com/channels/{ctx.guild.id}/{channel.id}",
        )
        view.add_item(
            build_container(
                TextDisplay(f"**Infos du salon vocal — {channel.name}**"),
                Separator(visible=True),
                TextDisplay(vc_text),
                ActionRow(join_btn),
            )
        )
        await ctx.send(view=view)

    @commands.hybrid_command(
        name="channelinfo",
        aliases=["cinfo", "ci"],
        description="Obtenir les informations d’un salon.",
        help="Obtenir les informations d’un salon.",
        usage="<Channel>",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        ch_text = (
            f"**ID:** {channel.id}\n**Created At:** {channel.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**Category:** {channel.category.name if channel.category else 'None'}\n"
            f"**Topic:** {channel.topic if channel.topic else 'None'}\n"
            f"**Slowmode:** {f'{channel.slowmode_delay} seconds' if channel.slowmode_delay else 'None'}\n"
            f"**NSFW:** {channel.is_nsfw()}"
        )
        view = OverwritesView(channel, ctx.author.id)
        view.add_item(
            Button(
                label="Aller au salon",
                style=discord.ButtonStyle.green,
                url=f"https://discord.com/channels/{ctx.guild.id}/{channel.id}",
            )
        )
        await ctx.send(content=ch_text, view=view)

    @commands.hybrid_command(
        name="ping", aliases=["latency"], help="Vérifie les latences du bot."
    )
    @ignore_check()
    @blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        """Affiche les latences WebSocket, API et base de données du bot."""

        # 1. Start timer and send an initial "Pinging..." message
        start_time = time.monotonic()
        msg = await ctx.send(
            view=CV2(
                "Vérification de la latence...",
                "Calcul des temps de réponse, patiente.",
            )
        )
        end_time = time.monotonic()

        bot_latency = round(self.bot.latency * 1000)
        api_latency = round((end_time - start_time) * 1000)

        db_latency = "Non disponible"
        try:
            async with aiosqlite.connect("db/afk.db") as db:
                db_start_time = time.perf_counter()
                await db.execute("SELECT 1")
                db_end_time = time.perf_counter()
                db_latency = f"{round((db_end_time - db_start_time) * 1000)}ms"
        except Exception as e:
            print(f"Database latency check failed: {e}")

        latency_text = (
            f"**Bot (WebSocket):** `{bot_latency}ms`\n"
            f"**API (Roundtrip):** `{api_latency}ms`\n"
            f"**Database:** `{db_latency}`"
        )
        await msg.edit(view=CV2("Rapport de latence système", latency_text))

    @commands.command(
        name="permissions",
        aliases=["perms"],
        help="Vérifier et lister les permissions clés d’un utilisateur précis",
        usage="perms <user>",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def keyperms(self, ctx, member: discord.Member):
        key_permissions = []

        if member.guild_permissions.create_instant_invite:
            key_permissions.append("Créer une invitation instantanée")
        if member.guild_permissions.kick_members:
            key_permissions.append("Expulser des membres")
        if member.guild_permissions.ban_members:
            key_permissions.append("Bannir des membres")
        if member.guild_permissions.administrator:
            key_permissions.append("Administrateur")
        if member.guild_permissions.manage_channels:
            key_permissions.append("Gérer les salons")
        if member.guild_permissions.manage_messages:
            key_permissions.append("Gérer les messages")
        if member.guild_permissions.mention_everyone:
            key_permissions.append("Mentionner Everyone")
        if member.guild_permissions.manage_nicknames:
            key_permissions.append("Gérer les pseudos")
        if member.guild_permissions.manage_roles:
            key_permissions.append("Gérer les rôles")
        if member.guild_permissions.manage_webhooks:
            key_permissions.append("Gérer les webhooks")
        if member.guild_permissions.manage_emojis:
            key_permissions.append("Gérer les emojis")
        if member.guild_permissions.manage_guild:
            key_permissions.append("Gérer le serveur")
        if member.guild_permissions.manage_permissions:
            key_permissions.append("Gérer les permissions")
        if member.guild_permissions.manage_threads:
            key_permissions.append("Gérer les fils")
        if member.guild_permissions.moderate_members:
            key_permissions.append("Modérer les membres")
        if member.guild_permissions.move_members:
            key_permissions.append("Déplacer des membres")
        if member.guild_permissions.mute_members:
            key_permissions.append("Rendre muets les membres (vocal)")
        if member.guild_permissions.deafen_members:
            key_permissions.append("Rendre sourds les membres")
        if member.guild_permissions.priority_speaker:
            key_permissions.append("Orateur prioritaire")
        if member.guild_permissions.stream:
            key_permissions.append("Vidéo")

        permissions_list = ", ".join(key_permissions) if key_permissions else "None"

        await ctx.reply(
            view=CV2(
                f"Permissions clés de {member}",
                f"__**Key Permissions**__\n{permissions_list}",
            )
        )

    @commands.hybrid_command(
        name="report",
        aliases=["bug"],
        usage="Report <bug>",
        description="Signaler un bug à l’équipe de développement.",
        help="Signaler un bug à l’équipe de développement.",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def report(self, ctx, *, bug):
        channel = self.bot.get_channel(1396813063642153030)
        report_text = f"{bug}\n\n**Reported By:** {ctx.author.name}\n**Server:** {ctx.guild.name}\n**Channel:** {ctx.channel.name}"
        await channel.send(view=CV2("Bug signalé", report_text))
        await ctx.reply(
            view=CV2(
                f"{TICK} Bug signalé",
                "Merci d’avoir signalé ce bug. Nous allons l’examiner.",
            )
        )
