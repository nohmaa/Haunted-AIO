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
from utils.emoji import CROSS, TICK
from discord.ext import commands
from discord.ext import menus
import aiosqlite
import os
from utils.Tools import *
from utils.cv2 import CV2, build_container
from typing import Union
from discord.ui import LayoutView, TextDisplay, Separator, Container


class CV2(LayoutView):
    def __init__(self, title, *sections):
        super().__init__(timeout=None)
        items = [TextDisplay(f"**{title}**")]
        for s in sections:
            if s:
                items.append(Separator(visible=True))
                items.append(TextDisplay(str(s)))
        self.add_item(build_container(*items))


from utils.paginator import Paginator as sonu


class BlacklistWordSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        embed = discord.Embed(
            title="Mot blacklisté [7]",
            description="< > Obligatoire | [ ] Optionnel",
            color=0xFF0000,
        )
        for entry in entries:
            embed.add_field(name="", value=entry, inline=False)

        embed.set_footer(
            text="Les utilisateurs avec Administrateur peuvent utiliser les mots blacklistés",
            icon_url="https://cdn.discordapp.com/avatars/1396114795102470196/198b9bc616ec574f6fd2f7121a1d3abc.webp?size=4096",
        )
        return embed


DB_PATH = "db/blword.db"


async def create_blacklist_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blacklist (
                guild_id TEXT,
                word TEXT,
                PRIMARY KEY (guild_id, word)
            )
        """)
        await db.commit()


async def create_bypass_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bypass (
                guild_id TEXT,
                user_id INTEGER,
                PRIMARY KEY (guild_id, user_id)
            )
        """)
        await db.commit()


async def create_bypass_roles_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bypass_roles (
                guild_id TEXT,
                role_id INTEGER,
                PRIMARY KEY (guild_id, role_id)
            )
        """)
        await db.commit()


class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(create_blacklist_table())
        self.bot.loop.create_task(create_bypass_table())
        self.bot.loop.create_task(create_bypass_roles_table())

    ############ FUNCTIONS ############
    async def is_word_blacklisted(self, guild_id, word):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT * FROM blacklist WHERE guild_id = ? AND word = ?",
                (guild_id, word),
            ) as cursor:
                return await cursor.fetchone() is not None

    async def add_word_to_blacklist(self, guild_id, word):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO blacklist (guild_id, word) VALUES (?, ?)", (guild_id, word)
            )
            await db.commit()

    async def remove_word_from_blacklist(self, guild_id, word):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "DELETE FROM blacklist WHERE guild_id = ? AND word = ?",
                (guild_id, word),
            )
            await db.commit()

    async def get_blacklisted_words(self, guild_id):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT word FROM blacklist WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                return [row[0] async for row in cursor]

    async def is_user_bypassed(self, guild_id, user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT * FROM bypass WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id),
            ) as cursor:
                return await cursor.fetchone() is not None

    async def add_user_to_bypass(self, guild_id, user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO bypass (guild_id, user_id) VALUES (?, ?)",
                (guild_id, user_id),
            )
            await db.commit()

    async def remove_user_from_bypass(self, guild_id, user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "DELETE FROM bypass WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id),
            )
            await db.commit()

    async def get_bypassed_users(self, guild_id):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT user_id FROM bypass WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                return [row[0] async for row in cursor]

    async def is_role_bypassed(self, guild_id, role_id):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT * FROM bypass_roles WHERE guild_id = ? AND role_id = ?",
                (guild_id, role_id),
            ) as cursor:
                return await cursor.fetchone() is not None

    async def add_role_to_bypass(self, guild_id, role_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO bypass_roles (guild_id, role_id) VALUES (?, ?)",
                (guild_id, role_id),
            )
            await db.commit()

    async def remove_role_from_bypass(self, guild_id, role_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "DELETE FROM bypass_roles WHERE guild_id = ? AND role_id = ?",
                (guild_id, role_id),
            )
            await db.commit()

    async def get_bypassed_roles(self, guild_id):
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT role_id FROM bypass_roles WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                return [row[0] async for row in cursor]

    async def remove_all_words_from_blacklist(self, guild_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("DELETE FROM blacklist WHERE guild_id = ?", (guild_id,))
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = str(message.guild.id)
        words = await self.get_blacklisted_words(guild_id)
        bypassed_users = await self.get_bypassed_users(guild_id)
        bypassed_roles = await self.get_bypassed_roles(guild_id)

        if (
            message.author.guild_permissions.administrator
            or message.author.id in bypassed_users
        ):
            return

        for role in message.author.roles:
            if role.id in bypassed_roles:
                return

        for word in words:
            if word in message.content.lower():
                await message.delete()
                warning_message = await message.channel.send(
                    f"{message.author.mention} surveille ton langage, ton message contient un mot blacklisté !"
                )
                await warning_message.delete(delay=3)
                break

    @commands.group(
        name="blacklistword", aliases=["blword"], invoke_without_command=True
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blacklistword(self, ctx):
        commands_list = [
            "➜ `blacklistword add <word>` - Add a word to the blacklist.",
            "➜ `blacklistword remove <word>` - Remove a word from the blacklist.",
            "➜ `blacklistword reset` - Effacer all blacklisted words for the guild.",
            "➜ `blacklistword config` - Show the list of blacklisted words for the guild.",
            "➜ `blacklistword bypass add <role>/<user>` - Add a role/user à la liste de contournement.",
            "➜ `blacklistword bypass remove <role>/<user>` - Remove a role/user de la liste de contournement.",
            "➜ `blacklistword bypass list` - Show the list of bypassed roles/users.",
        ]

        paginator = sonu(source=BlacklistWordSource(commands_list), ctx=ctx)

        await paginator.paginate()

    @blacklistword.command(name="add")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, word: str):
        guild_id = str(ctx.guild.id)
        if len(await self.get_blacklisted_words(guild_id)) >= 30:
            await ctx.reply("La blacklist est pleine. Maximum 30 mots autorisés.")
            return
        if await self.is_word_blacklisted(guild_id, word.lower()):
            await ctx.reply(
                view=CV2(
                    f"{TICK} Accès refusé", f"`{word}` est déjà dans la blacklist."
                )
            )
            return

        await self.add_word_to_blacklist(guild_id, word.lower())
        await ctx.reply(view=CV2(f"{TICK} Succès", f"`{word}` ajouté à la blacklist."))

    @blacklistword.command(name="remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, word: str):
        guild_id = str(ctx.guild.id)
        if not await self.is_word_blacklisted(guild_id, word.lower()):
            await ctx.reply(
                view=CV2(f"{CROSS} Error", f"`{word}` n’est pas dans la blacklist.")
            )
            return

        await self.remove_word_from_blacklist(guild_id, word.lower())
        await ctx.reply(view=CV2(f"{TICK} Succès", f"`{word}` retiré de la blacklist."))

    @blacklistword.command(name="reset")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        guild_id = str(ctx.guild.id)
        words = await self.get_blacklisted_words(guild_id)

        if not words:
            await ctx.reply(
                view=CV2(f"{CROSS} Error", "Aucun mot n’est actuellement blacklisté.")
            )
            return

        await self.remove_all_words_from_blacklist(guild_id)

        await ctx.reply(
            view=CV2(f"{TICK} Succès", "Tous les mots blacklistés ont été effacés.")
        )

    @blacklistword.command(name="config")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        guild_id = str(ctx.guild.id)
        words = await self.get_blacklisted_words(guild_id)
        if not words:
            await ctx.reply(
                view=CV2(f"{CROSS} Error", "Aucun mot n’est actuellement blacklisté.")
            )
            return

        await ctx.reply(
            view=CV2(f"Mots blacklistés pour {ctx.guild.name}", "\n".join(words))
        )

    @blacklistword.group(name="bypass", invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def bypass(self, ctx):
        await ctx.send(
            view=CV2(
                "Commandes de contournement",
                "➜ `blacklistword bypass add <role>/<user>` - Add a role/user à la liste de contournement.\n\n➜ `blacklistword bypass remove <role>/<user>` - Remove a role/user de la liste de contournement.\n\n➜ `blacklistword bypass list` - Show the list of bypassed roles/users.",
            )
        )

    @bypass.command(name="add")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def bypass_add(self, ctx, target: Union[discord.Member, discord.Role]):
        guild_id = str(ctx.guild.id)
        if isinstance(target, discord.Member):
            if len(await self.get_bypassed_users(guild_id)) >= 30:
                await ctx.reply(
                    "La liste de contournement des utilisateurs est pleine. Maximum 30 utilisateurs."
                )
                return
            if await self.is_user_bypassed(guild_id, target.id):
                await ctx.reply(
                    view=CV2("Error", f"{CROSS} | `{target}` est déjà contourné.")
                )
                return
            await self.add_user_to_bypass(guild_id, target.id)
            await ctx.reply(
                view=CV2(
                    f"{TICK} Succès", f"Added `{target}` à la liste de contournement."
                )
            )

        elif isinstance(target, discord.Role):
            if len(await self.get_bypassed_roles(guild_id)) >= 30:
                await ctx.reply(
                    "La liste de contournement des rôles est pleine. Maximum 30 rôles."
                )
                return
            if await self.is_role_bypassed(guild_id, target.id):
                await ctx.reply(
                    view=CV2(f"{CROSS} Error", f"`{target}` est déjà contourné.")
                )
                return
            await self.add_role_to_bypass(guild_id, target.id)
            await ctx.reply(
                view=CV2(
                    f"{TICK} Succès", f"Added `{target}` à la liste de contournement."
                )
            )

    @bypass.command(name="remove")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def bypass_remove(self, ctx, target: Union[discord.Member, discord.Role]):
        guild_id = str(ctx.guild.id)
        if isinstance(target, discord.Member):
            if not await self.is_user_bypassed(guild_id, target.id):
                await ctx.reply(
                    view=CV2(f"{CROSS} Error", f"`{target}` n’est pas contourné.")
                )
                return
            await self.remove_user_from_bypass(guild_id, target.id)
            await ctx.reply(
                view=CV2(
                    f"{TICK} Succès",
                    f"Removed `{target}` de la liste de contournement.",
                )
            )

        elif isinstance(target, discord.Role):
            if not await self.is_role_bypassed(guild_id, target.id):
                await ctx.reply(
                    view=CV2(f"{CROSS} Error", f"`{target}` n’est pas contourné.")
                )
                return
            await self.remove_role_from_bypass(guild_id, target.id)
            await ctx.reply(
                view=CV2(
                    f"{TICK} Succès",
                    f"Removed `{target}` de la liste de contournement.",
                )
            )

    @bypass.command(name="list")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def bypass_list(self, ctx):
        guild_id = str(ctx.guild.id)
        users = await self.get_bypassed_users(guild_id)
        roles = await self.get_bypassed_roles(guild_id)

        if not users and not roles:
            await ctx.send(
                view=CV2(
                    f"{CROSS} Error",
                    "Aucun utilisateur ou rôle n’est actuellement contourné.",
                )
            )
            return

        bypassed_users = [
            ctx.guild.get_member(user_id)
            for user_id in users
            if ctx.guild.get_member(user_id)
        ]
        bypassed_roles = [
            ctx.guild.get_role(role_id)
            for role_id in roles
            if ctx.guild.get_role(role_id)
        ]
        sections = []
        if bypassed_users:
            sections.append(
                f"**Users**\n" + ", ".join([user.name for user in bypassed_users])
            )
        if bypassed_roles:
            sections.append(
                f"**Roles**\n" + ", ".join([role.name for role in bypassed_roles])
            )
        await ctx.send(
            view=CV2(
                f"Utilisateurs et rôles contournés pour {ctx.guild.name}", *sections
            )
        )

    @add.error
    @remove.error
    @reset.error
    @config.error
    @bypass_add.error
    @bypass_remove.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            if not isinstance(error, commands.CommandOnCooldown):
                await ctx.reply(
                    view=CV2(
                        "Error",
                        f"{CROSS} | Une erreur est survenue pendant la commande. Assure-toi d’avoir la permission **Administrateur**.",
                    )
                )
