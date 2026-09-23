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

import discord
from utils.emoji import CROSS, DENIED, TICK, ZWARNING
import asyncio
import datetime
import re
import typing
import typing as t
from typing import *
from utils.Tools import *
from core import Cog, zyrox, Context
from discord.ext.commands import Converter
from discord.ext import commands, tasks
from discord.ui import Button, View
from typing import Union, Optional
from utils import (
    Paginator,
    DescriptionEmbedPaginator,
    FieldPagePaginator,
    TextPaginator,
)
from typing import Union, Optional
from io import BytesIO
import requests
import aiohttp
import time
from datetime import datetime, timezone, timedelta
import sqlite3
from typing import *
from discord.utils import utcnow

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} est une clé de temps invalide ! h|m|s|d sont des arguments valides"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} n’est pas un nombre !")
    return round(time)


async def do_removal(ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.error(f"Trop de messages à rechercher ({limit}/2000)")

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(
            limit=limit, before=before, after=after, check=predicate
        )
    except discord.Forbidden as e:
        return await ctx.error(
            "Je n’ai pas les permissions pour supprimer des messages."
        )
    except discord.HTTPException as e:
        return await ctx.error(f"Erreur : {e} (essayez une recherche plus petite ?)")

    spammers = Counter(m.author.display_name for m in deleted)
    deleted = len(deleted)
    messages = [
        f"{TICK}> | {deleted} message{'' if deleted == 1 else 's'} supprimé{'' if deleted == 1 else 's'}."
    ]
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(
            f"{TICK}> | {deleted} messages supprimés avec succès.", delete_after=7
        )
    else:
        await ctx.send(to_send, delete_after=7)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF0000
        self.sniped = {}

    def convert(self, time):
        pos = ["s", "m", "h", "d"]

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
        unit = time[-1]
        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2
        return val * time_dict[unit]

    @commands.command()
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def enlarge(
        self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str]
    ):
        url = emoji.url
        await ctx.send(url)

    @commands.hybrid_command(
        name="unlockall",
        help="Déverrouille tous les salons du serveur.",
        usage="unlockall",
    )
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def unlockall(self, ctx):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(
                label="Annuler", style=discord.ButtonStyle.red, emoji=ZWARNING
            )

            async def button_callback(interaction: discord.Interaction):
                a = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Déverrouillage de tous les salons sur {ctx.guild.name} .",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for channel in interaction.guild.channels:
                            try:
                                await channel.set_permissions(
                                    ctx.guild.default_role,
                                    overwrite=discord.PermissionOverwrite(
                                        send_messages=True, read_messages=True
                                    ),
                                    reason="Commande Unlockall exécutée par : {}".format(
                                        ctx.author
                                    ),
                                )
                                a += 1
                            except Exception as e:
                                print(e)
                        await interaction.channel.send(
                            content=f"{TICK}> | {a} salons déverrouillés avec succès"
                        )
                        return
                    else:
                        await interaction.response.edit_message(
                            content=f"{ZWARNING} | Il me manque les permissions nécessaires. Veuillez m’accorder la permission `manage roles` puis réessayez.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Annulé, je ne vais déverrouiller aucun salon.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            embed = discord.Embed(
                color=self.color,
                description=f"**Voulez-vous vraiment déverrouiller tous les salons sur {ctx.guild.name}**",
            )
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            embed.set_footer(
                text="Veuillez cliquer sur « Confirmer » ou « Annuler » pour continuer. Vous avez 30 secondes pour décider !"
            )
            await ctx.reply(
                embed=embed, view=view, mention_author=False, delete_after=30
            )

        else:
            embed5 = discord.Embed(
                title=f"{ZWARNING} Accès refusé",
                description="Votre rôle doit être au-dessus de mon rôle le plus élevé.",
                color=0xFF0000,
            )
            embed5.set_footer(
                text=f"“{ctx.command.qualified_name}” Commande exécutée par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=embed5, mention_author=False)

    @commands.hybrid_command(
        name="lockall", help="Verrouille tous les salons du serveur.", usage="lockall"
    )
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def lockall(self, ctx):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(
                label="Annuler", style=discord.ButtonStyle.red, emoji=CROSS
            )

            async def button_callback(interaction: discord.Interaction):
                a = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Verrouillage de tous les salons sur {ctx.guild.name}...",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for channel in interaction.guild.channels:
                            try:
                                await channel.set_permissions(
                                    ctx.guild.default_role,
                                    overwrite=discord.PermissionOverwrite(
                                        send_messages=False, read_messages=True
                                    ),
                                    reason="Commande Lockall exécutée par : {}".format(
                                        ctx.author
                                    ),
                                )
                                a += 1
                            except Exception as e:
                                print(e)
                        await interaction.channel.send(
                            content=f"{TICK}>| {a} salons verrouillés avec succès"
                        )
                        return
                    else:
                        await interaction.response.edit_message(
                            content=f"{ZWARNING} | Il me manque les permissions nécessaires. Veuillez m’accorder la permission `manage roles` puis réessayez.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Annulé, je ne vais verrouiller aucun salon.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            embed = discord.Embed(
                color=self.color,
                description=f"**Voulez-vous vraiment verrouiller tous les salons sur {ctx.guild.name}**",
            )
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            embed.set_footer(
                text=f"Veuillez cliquer sur « Confirmer » ou « Annuler » pour continuer. Vous avez 30 secondes pour décider !"
            )
            await ctx.reply(
                embed=embed, view=view, mention_author=False, delete_after=30
            )

        else:
            denied = discord.Embed(
                title=f"{ZWARNING} Accès refusé",
                description="Votre rôle doit être au-dessus de mon rôle le plus élevé.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Commande exécutée par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @commands.hybrid_command(
        name="give",
        help="Donne un rôle à l’utilisateur mentionné.",
        usage="give <user> <role>",
        aliases=["addrole"],
    )
    @blacklist_check()
    @ignore_check()
    @top_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def give(self, ctx, member: discord.Member, *, role: discord.Role):
        if not ctx.guild.me.guild_permissions.manage_roles:
            return await ctx.send(
                f"{DENIED} Je n’ai pas la permission de gérer les rôles !"
            )

        if role >= ctx.guild.me.top_role:
            error = discord.Embed(
                color=self.color,
                description="Je ne peux pas gérer les rôles d’un utilisateur avec un rôle supérieur ou égal !",
            )

            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            error = discord.Embed(
                color=self.color,
                description="Vous ne pouvez pas gérer les rôles d’un utilisateur avec un rôle supérieur ou égal au vôtre !",
            )
            error.set_author(
                name="Accès refusé",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        try:
            if role not in member.roles:
                await member.add_roles(
                    role, reason=f"Rôle ajouté par {ctx.author} (ID : {ctx.author.id})"
                )
                success = discord.Embed(
                    color=self.color,
                    description=f"Rôle {role.name} **ajouté** à {member.mention} avec succès.",
                )
                success.set_author(
                    name="Rôle ajouté",
                    icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
                )
                success.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
            else:
                await member.remove_roles(
                    role, reason=f"Rôle retiré par {ctx.author} (ID : {ctx.author.id})"
                )
                success = discord.Embed(
                    color=self.color,
                    description=f"Rôle {role.name} **retiré** de {member.mention} avec succès.",
                )
                success.set_author(
                    name="Rôle retiré",
                    icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
                )
                success.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
            await ctx.send(embed=success)
        except discord.Forbidden:
            error = discord.Embed(
                color=self.color,
                description=f"{ZWARNING} Je n’ai pas la permission de gérer les rôles de cet utilisateur !",
            )
            await ctx.send(embed=error)
        except Exception as e:
            error = discord.Embed(
                color=self.color,
                description=f"{ZWARNING} Une erreur inattendue s’est produite : {str(e)}",
            )
            await ctx.send(embed=error)

    @commands.hybrid_command(
        name="hideall", help="Masque tous les salons.", usage="hideall"
    )
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def hideall(self, ctx):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(
                label="Annuler", style=discord.ButtonStyle.red, emoji=CROSS
            )

            async def button_callback(interaction: discord.Interaction):
                a = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Masquage de tous les salons sur {ctx.guild.name} ...",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for channel in interaction.guild.channels:
                            try:
                                await channel.set_permissions(
                                    ctx.guild.default_role,
                                    view_channel=False,
                                    reason="Commande Hideall exécutée par : {}".format(
                                        ctx.author
                                    ),
                                )
                                a += 1
                            except Exception as e:
                                print(e)
                        await interaction.channel.send(
                            content=f"{TICK}> | {a} salon(s) masqué(s) avec succès."
                        )
                        return
                    else:
                        await interaction.response.edit_message(
                            content=f"{ZWARNING} | Il me manque les permissions nécessaires. Veuillez m’accorder la permission `manage channels` puis réessayez.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Annulé, je ne vais masquer aucun salon.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            embed = discord.Embed(
                color=self.color,
                description=f"**Voulez-vous vraiment masquer tous les salons sur {ctx.guild.name}**",
            )
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            embed.set_footer(
                text=f"Veuillez cliquer sur « Confirmer » ou « Annuler » pour continuer. Vous avez 30 secondes pour décider !"
            )
            await ctx.reply(
                embed=embed, view=view, mention_author=False, delete_after=30
            )

        else:
            denied = discord.Embed(
                title=f"{ZWARNING} Accès refusé",
                description="Votre rôle doit être au-dessus de mon rôle le plus élevé.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Commande exécutée par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @commands.hybrid_command(
        name="unhideall",
        help="Réaffiche tous les salons du serveur.",
        usage="unhideall",
    )
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def unhideall(self, ctx):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(
                label="Annuler", style=discord.ButtonStyle.red, emoji=CROSS
            )

            async def button_callback(interaction: discord.Interaction):
                a = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Réaffichage de tous les salons sur {ctx.guild.name} .",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for channel in interaction.guild.channels:
                            try:
                                await channel.set_permissions(
                                    ctx.guild.default_role,
                                    view_channel=True,
                                    reason="Commande Unhideall exécutée par : {}".format(
                                        ctx.author
                                    ),
                                )
                                a += 1
                            except Exception as e:
                                print(e)
                        await interaction.channel.send(
                            content=f"{TICK}> | {a} salon(s) réaffiché(s) avec succès."
                        )
                        return
                    else:
                        await interaction.response.edit_message(
                            content=f"{ZWARNING} | Il me manque les permissions nécessaires. Veuillez m’accorder la permission `manage channels` puis réessayez.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Annulé, je ne vais réafficher aucun salon.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            embed = discord.Embed(
                color=self.color,
                description=f"**Voulez-vous vraiment réafficher tous les salons sur {ctx.guild.name}**",
            )
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            embed.set_footer(
                text=f"Veuillez cliquer sur « Confirmer » ou « Annuler » pour continuer. Vous avez 30 secondes pour décider !"
            )
            await ctx.reply(
                embed=embed, view=view, mention_author=False, delete_after=30
            )

        else:
            denied = discord.Embed(
                title=f"{ZWARNING} Accès refusé",
                description="Votre rôle doit être au-dessus de mon rôle le plus élevé.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Commande exécutée par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @commands.hybrid_command(
        name="prefix",
        aliases=["setprefix", "prefixset"],
        help="Permet de changer le préfixe du bot pour ce serveur",
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _prefix(self, ctx: commands.Context, prefix: str):
        if not prefix:
            await ctx.reply(
                embed=discord.Embed(
                    title=f"{CROSS} Erreur",
                    description="Le préfixe ne peut pas être vide. Veuillez fournir un préfixe valide.",
                    color=self.color,
                )
            )
            return

        data = await getConfig(ctx.guild.id)
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            data["prefix"] = str(prefix)
            await updateConfig(ctx.guild.id, data)
            embed1 = discord.Embed(
                title=f"{TICK}> Succès",
                description=f"Préfixe changé pour ce serveur : `{prefix}`\n\nNouveau préfixe pour **{ctx.guild.name}** : `{prefix}`\nUtilisez `{prefix}help` pour en savoir plus.",
                color=self.color,
            )
            await ctx.reply(embed=embed1)
        else:
            denied = discord.Embed(
                title=f"{ZWARNING} Accès refusé",
                description="Votre rôle doit être au-dessus de mon rôle le plus élevé.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Commande exécutée par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @commands.hybrid_command(name="clone", help="Clone un salon.")
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx: commands.Context, channel: discord.TextChannel):

        if not ctx.guild.me.guild_permissions.manage_channels:
            error = discord.Embed(
                color=self.color,
                description="Je n’ai pas la permission de gérer les salons !",
            )
            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        try:

            await channel.clone()
            success = discord.Embed(
                color=self.color, description=f"{channel.name} a été cloné avec succès"
            )
            success.set_author(
                name="Succès",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            success.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=success)
        except discord.Forbidden:
            error = discord.Embed(
                color=self.color,
                description="Je n’ai pas la permission de cloner des salons !",
            )
            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            await ctx.send(embed=error)
        except Exception as e:
            error = discord.Embed(
                color=self.color,
                description=f"Une erreur s’est produite en essayant de cloner le salon : {str(e)}",
            )
            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            await ctx.send(embed=error)

    @commands.hybrid_command(
        name="nick",
        aliases=["setnick"],
        help="Pour changer le pseudo de quelqu’un.",
        usage="nick [member]",
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def changenickname(
        self, ctx: commands.Context, member: discord.Member, *, name: str = None
    ):

        if member == ctx.guild.owner:
            error = discord.Embed(
                color=self.color,
                description="Je ne peux pas changer le pseudo du propriétaire du serveur !",
            )
            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        if member.top_role >= ctx.guild.me.top_role:
            error = discord.Embed(
                color=self.color,
                description="Je ne peux pas changer le pseudo d’un utilisateur avec un rôle supérieur ou égal au mien !",
            )
            error.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            error = discord.Embed(
                color=self.color,
                description="Vous ne pouvez pas changer le pseudo d’un utilisateur avec un rôle supérieur ou égal au vôtre !",
            )
            error.set_author(
                name="Accès refusé",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error)

        try:
            await member.edit(nick=name)
            if name:
                success = discord.Embed(
                    color=self.color,
                    description=f"Pseudo de {member.mention} changé en {name} avec succès.",
                )
                success.set_author(
                    name="Pseudo mis à jour",
                    icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
                )
                success.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
            else:
                success = discord.Embed(
                    color=self.color,
                    description=f"Pseudo de {member.mention} effacé avec succès.",
                )
                success.set_author(
                    name="Pseudo effacé",
                    icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
                )
                success.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
            await ctx.send(embed=success)
        except discord.Forbidden:
            error = discord.Embed(
                color=self.color,
                description=f"{ZWARNING} | Je n’ai pas la permission de gérer le pseudo de cet utilisateur !",
            )
            await ctx.send(embed=error)
        except Exception as e:
            error = discord.Embed(
                color=self.color,
                description=f"{ZWARNING} | Une erreur s’est produite en changeant le pseudo : {str(e)}",
            )
            await ctx.send(embed=error)

    @commands.hybrid_command(name="nuke", help="Recrée un salon", usage="nuke")
    @blacklist_check()
    @ignore_check()
    @top_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _nuke(self, ctx: commands.Context):
        button = Button(
            label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
        )
        button1 = Button(label="Annuler", style=discord.ButtonStyle.red, emoji=CROSS)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.manage_channels:
                    channel = interaction.channel
                    newchannel = await channel.clone()
                    await newchannel.edit(position=channel.position)

                    await channel.delete()
                    embed = discord.Embed(
                        description="Le salon a été recréé avec succès par **`%s`**"
                        % (ctx.author),
                        color=self.color,
                    )
                    embed.set_author(
                        name="Salon recréé",
                        icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
                    )
                    embed.set_footer(
                        text=f"Demandé par {ctx.author}",
                        icon_url=(
                            ctx.author.avatar.url
                            if ctx.author.avatar
                            else ctx.author.default_avatar.url
                        ),
                    )
                    await newchannel.send(embed=embed)
                else:
                    await interaction.response.edit_message(
                        content=f"{ZWARNING} | Il me manque les permissions nécessaires. Veuillez m’accorder la permission `manage channel` puis réessayez.",
                        embed=None,
                        view=None,
                    )
            else:
                await interaction.response.send_message(
                    "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                    embed=None,
                    view=None,
                    ephemeral=True,
                )

        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                await interaction.response.edit_message(
                    content="Annulé, je ne vais pas recréer ce salon.",
                    embed=None,
                    view=None,
                )
            else:
                await interaction.response.send_message(
                    "Oups ! Ce message ne vous appartient pas. Vous devez exécuter la commande vous-même pour interagir.",
                    embed=None,
                    view=None,
                    ephemeral=True,
                )

        embed = discord.Embed(
            color=self.color, description="**Voulez-vous vraiment recréer le salon ?**"
        )

        view = View()
        button.callback = button_callback
        button1.callback = button1_callback
        view.add_item(button)
        view.add_item(button1)
        embed.set_footer(
            text="Veuillez cliquer sur « Confirmer » ou « Annuler » pour continuer. Vous avez 30 secondes pour décider !"
        )
        await ctx.reply(embed=embed, view=view, mention_author=False, delete_after=30)

    @commands.hybrid_command(
        name="slowmode",
        help="Change le mode lent",
        usage="slowmode [seconds]",
        aliases=["slow"],
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def _slowmode(self, ctx: commands.Context, seconds: int = 0):
        if seconds > 120:
            embed = discord.Embed(
                description="Le mode lent ne peut pas dépasser 2 minutes",
                color=self.color,
            )
            embed.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(
                embed=discord.Embed(
                    title="Mode lent",
                    description="Le mode lent est désactivé",
                    color=self.color,
                )
            )
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(
                description="Mode lent défini sur **`%s`** avec succès" % (seconds),
                color=self.color,
            )
            embed.set_author(
                name="Mode lent activé",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="unslowmode",
        help="Désactive le mode lent",
        usage="unslowmode",
        aliases=["unslow"],
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _unslowmode(self, ctx: commands.Context):
        await ctx.channel.edit(slowmode_delay=0)
        embed = discord.Embed(
            description="Mode lent désactivé avec succès", color=self.color
        )
        embed.set_author(
            name="Mode lent désactivé",
            icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
        )
        embed.set_footer(
            text=f"Demandé par {ctx.author}",
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["deletesticker", "removesticker"],
        description="Supprime le sticker du serveur",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def delsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("Aucun message répondu trouvé")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("Aucun sticker trouvé")
        try:
            name = ""
            for i in msg.stickers:
                name = i.name
                await ctx.guild.delete_sticker(i)
            await ctx.reply(f"{TICK}> Sticker nommé `{name}` supprimé avec succès")
        except:
            await ctx.reply("Échec de la suppression du sticker")

    @commands.command(
        aliases=["deleteemoji", "removeemoji"],
        description="Supprime l’emoji du serveur",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_emojis=True)
    async def delemoji(self, ctx, emoji: str = None):
        init_message = await ctx.reply(
            "Suppression des emojis en cours...", mention_author=False
        )
        message_content = None

        if ctx.message.reference is not None:
            referenced_message = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            message_content = str(referenced_message.content)
        else:
            message_content = str(ctx.message.content)

        if message_content:

            emoji_pattern = r"<a?:\w+:(\d+)>"
            found_emojis = re.findall(emoji_pattern, message_content)
            delete_count = 0

            if len(found_emojis) != 0:

                if len(found_emojis) > 15:
                    await init_message.delete()
                    return await ctx.reply(
                        "Maximum 15 emojis peuvent être supprimés à la fois."
                    )

                for emoji_id in found_emojis:
                    try:
                        emoji_to_delete = await ctx.guild.fetch_emoji(int(emoji_id))
                        await emoji_to_delete.delete(
                            reason=f"Supprimé par {ctx.author}"
                        )
                        delete_count += 1
                    except discord.NotFound:
                        continue
                    except discord.Forbidden:
                        continue
                await init_message.delete()
                return await ctx.reply(
                    f"{TICK}> | {delete_count}/{len(found_emojis)} emoji(s) supprimé(s) avec succès."
                )

        await init_message.delete()
        return await ctx.reply("Aucun emoji valide à supprimer trouvé.")

    @commands.command(description="Change l’icône du rôle.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def roleicon(
        self,
        ctx: commands.Context,
        role: discord.Role,
        *,
        icon: Union[discord.Emoji, discord.PartialEmoji, str] = None,
    ):

        if role.position >= ctx.guild.me.top_role.position:
            error_embed = discord.Embed(
                description=f"{role.mention} est au-dessus de mon rôle. Veuillez déplacer mon rôle au-dessus.",
                color=self.color,
            )
            error_embed.set_author(
                name="Erreur",
                icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.png?size=1024",
            )
            error_embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error_embed)

        if (
            ctx.author != ctx.guild.owner
            and ctx.author.top_role.position <= role.position
        ):
            error_embed = discord.Embed(
                description=f"{role.mention} a une position égale ou supérieure à votre rôle le plus élevé !",
                color=self.color,
            )
            error_embed.set_author(name="Erreur")
            error_embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=error_embed)

        if icon is None:
            attachment_found = False
            attachment_url = None
            for attachment in ctx.message.attachments:
                attachment_url = attachment.url
                attachment_found = True

            if attachment_found:
                try:
                    async with aiohttp.request("GET", attachment_url) as r:
                        image_data = await r.read()
                    await role.edit(display_icon=image_data)
                    success_embed = discord.Embed(
                        description=f"L’icône de {role.mention} a été changée avec succès.",
                        color=self.color,
                    )
                    success_embed.set_author(name="Icône mise à jour")
                    success_embed.set_footer(
                        text=f"Demandé par {ctx.author}",
                        icon_url=(
                            ctx.author.avatar.url
                            if ctx.author.avatar
                            else ctx.author.default_avatar.url
                        ),
                    )
                    return await ctx.send(embed=success_embed)
                except Exception as e:
                    print(e)
                    return await ctx.reply("Échec du changement de l’icône du rôle.")
            else:
                await role.edit(display_icon=None)
                removal_embed = discord.Embed(
                    description=f"L’icône a été retirée de {role.mention} avec succès.",
                    color=self.color,
                )
                removal_embed.set_author(name="Icône retirée")
                removal_embed.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
                return await ctx.reply(embed=removal_embed, mention_author=False)

        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            emoji_url = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
                async with aiohttp.request("GET", emoji_url) as r:
                    image_data = await r.read()
                await role.edit(display_icon=image_data)
                success_embed = discord.Embed(
                    description=f"L’icône de {role.mention} a été changée en {icon} avec succès.",
                    color=self.color,
                )
                success_embed.set_author(name="Icône mise à jour")
                success_embed.set_footer(
                    text=f"Demandé par {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
                return await ctx.reply(embed=success_embed, mention_author=False)
            except Exception as e:
                print(e)
                return await ctx.reply("Échec du changement de l’icône du rôle.")

        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Veuillez fournir un lien valide.")
            try:
                async with aiohttp.request("GET", icon) as r:
                    image_data = await r.read()
                await role.edit(display_icon=image_data)
                success_embed = discord.Embed(
                    description=f"{TICK}>| L’icône de {role.mention} a été changée avec succès.",
                    color=self.color,
                )
                return await ctx.reply(embed=success_embed, mention_author=False)
            except Exception as e:
                print(e)
                return await ctx.reply(
                    "Une erreur s’est produite en changeant l’icône du rôle."
                )

    @commands.hybrid_command(
        name="unbanall",
        help="Débannit tout le monde sur le serveur !",
        aliases=["massunban"],
        usage="Unbanall",
        with_app_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unbanall(self, ctx):
        button = Button(
            label="Confirmer", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
        )
        button1 = Button(label="Annuler", style=discord.ButtonStyle.red, emoji=CROSS)

        async def button_callback(interaction: discord.Interaction):
            a = 0
            if interaction.user == ctx.author:
                if interaction.guild.me.guild_permissions.ban_members:
                    await interaction.response.edit_message(
                        content="Débannissement de tous les membres bannis...",
                        embed=None,
                        view=None,
                    )
                    async for idk in interaction.guild.bans(limit=None):
                        await interaction.guild.unban(
                            user=idk.user,
                            reason="Commande Unbanall exécutée par : {}".format(
                                ctx.author
                            ),
                        )
                        a += 1
                    await interaction.channel.send(
                        content=f"{TICK}> {a} membres débannis avec succès"
                    )
                else:
                    await interaction.response.edit_message(
                        content="Il me manque la permission `ban members` sur ce serveur.",
                        embed=None,
                        view=None,
                    )
            else:
                await interaction.response.send_message(
                    "Oh oh ! Ce message ne vous appartient pas.\nVous devez exécuter cette commande pour interagir.",
                    embed=None,
                    view=None,
                    ephemeral=True,
                )

        async def button1_callback(interaction: discord.Interaction):
            if interaction.user == ctx.author:
                await interaction.response.edit_message(
                    content="Annulé, je ne vais débannir personne.",
                    embed=None,
                    view=None,
                )
            else:
                await interaction.response.send_message(
                    "Oh oh ! Ce message ne vous appartient pas.\nVous devez exécuter cette commande pour interagir.",
                    embed=None,
                    view=None,
                    ephemeral=True,
                )

        embed = discord.Embed(
            color=self.color,
            description="**Êtes-vous sûr de vouloir débannir tous les membres de ce serveur ?**",
        )

        view = View()
        button.callback = button_callback
        button1.callback = button1_callback
        view.add_item(button)
        view.add_item(button1)
        await ctx.reply(embed=embed, view=view, mention_author=False)

    @commands.hybrid_command(
        name="audit", help="Voir les actions récentes du journal d’audit du serveur."
    )
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(view_audit_log=True)
    @commands.bot_has_permissions(view_audit_log=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def auditlog(self, ctx, limit: int):
        if limit >= 31:
            await ctx.reply(
                "Action refusée, vous ne pouvez pas récupérer plus de `30` entrées.",
                mention_author=False,
            )
            return
        idk = []
        str = ""
        async for entry in ctx.guild.audit_logs(limit=limit):
            idk.append(f"""Utilisateur : `{entry.user}`
Action : `{entry.action}`
Cible : `{entry.target}`
Raison : `{entry.reason}`\n\n""")
        for n in idk:
            str += n
        str = str.replace("AuditLogAction.", "")
        embed = discord.Embed(
            title=f"Logs d’audit de {ctx.guild.name}",
            description=f">>> {str}",
            color=0xFF0000,
        )
        embed.set_footer(text=f"Actions du journal d’audit pour {ctx.guild.name}")
        await ctx.reply(embed=embed, mention_author=False)
