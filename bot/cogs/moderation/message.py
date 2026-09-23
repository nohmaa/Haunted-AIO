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
from utils.emoji import TICK
from discord.ext import commands, tasks
import asyncio
import datetime
import re
from typing import *
from utils.Tools import *
from discord.ui import Button, View
from typing import Union, Optional
from typing import Union, Optional
from io import BytesIO
import requests
import aiohttp
import time
from datetime import datetime, timezone, timedelta

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
        f"{TICK} | {deleted} message{'' if deleted == 1 else 's'} supprimé{'' if deleted == 1 else 's'}."
    ]
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(
            f"{TICK} | {deleted} messages supprimés avec succès.", delete_after=7
        )
    else:
        await ctx.send(to_send, delete_after=7)


class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF0000

    @commands.group(
        invoke_without_command=True, aliases=["purge"], help="Supprime les messages"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, Choice: Union[discord.Member, int], Amount: int = None):
        await ctx.message.delete()

        if isinstance(Choice, discord.Member):
            search = Amount or 5
            return await do_removal(ctx, search, lambda e: e.author == Choice)

        elif isinstance(Choice, int):
            return await do_removal(ctx, Choice, lambda e: True)

    @clear.command(help="Supprime les messages contenant des embeds")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def embeds(self, ctx, search=100):
        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds))

    @clear.command(help="Supprime les messages contenant des fichiers")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def files(self, ctx, search=100):

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.attachments))

    @clear.command(help="Supprime les messages contenant des images")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def images(self, ctx, search=100):

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @clear.command(name="all", help="Supprime tous les messages")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _remove_all(self, ctx, search=100):

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: True)

    @clear.command(help="Supprime les messages d’un utilisateur précis")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def user(self, ctx, member: discord.Member, search=100):

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)

    @clear.command(help="Supprime les messages contenant un texte précis")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def contains(self, ctx, *, string: str):

        await ctx.message.delete()
        if len(string) < 3:
            await ctx.error("La longueur du texte doit être d’au moins 3 caractères.")
        else:
            await do_removal(ctx, 100, lambda e: string in e.content)

    @clear.command(
        name="bot",
        aliases=["bots", "b"],
        help="Supprime les messages envoyés par des bots",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _bot(self, ctx, prefix=None, search=100):

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (
                prefix and m.content.startswith(prefix)
            )

        await do_removal(ctx, search, predicate)

    @clear.command(
        name="emoji",
        aliases=["emojis"],
        help="Supprime les messages contenant des emojis",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _emoji(self, ctx, search=100):

        await ctx.message.delete()
        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate(m):
            return custom_emoji.search(m.content)

        await do_removal(ctx, search, predicate)

    @clear.command(name="reactions", help="Supprime les réactions des messages")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _reactions(self, ctx, search=100):

        await ctx.message.delete()

        if search > 2000:
            return await ctx.send(f"Trop de messages à rechercher ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.success(
            f"{TICK} | {total_reactions} réactions supprimées avec succès."
        )

    @commands.command(
        name="purgebots",
        aliases=["cleanup", "pb", "clearbot", "clearbots"],
        help="Supprime les messages récents des bots dans le salon",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purgebot(self, ctx, prefix=None, search=100):

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (
                prefix and m.content.startswith(prefix)
            )

        await do_removal(ctx, search, predicate)

    @commands.command(
        name="purgeuser",
        aliases=["pu", "cu", "clearuser"],
        help="Supprime les messages récents d’un utilisateur dans le salon",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purguser(self, ctx, member: discord.Member, search=100):

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)
