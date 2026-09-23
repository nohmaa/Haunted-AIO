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
import aiosqlite
from utils import Paginator, DescriptionEmbedPaginator
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


class Block(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.set_db())

        # @commands.Cog.listener()

    async def set_db(self):
        async with aiosqlite.connect("db/block.db") as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS user_blacklist (
                user_id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
            await db.execute("""
            CREATE TABLE IF NOT EXISTS guild_blacklist (
                guild_id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
            await db.commit()

    @commands.group(name="blacklist", aliases=["bl"], invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.subcommand_passed is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send_help(ctx.command)

    @blacklist.group(
        name="user",
        help="Ajouter/Retirer un utilisateur de la blacklist.",
        invoke_without_command=True,
    )
    @commands.is_owner()
    async def user(self, ctx):
        if ctx.subcommand_passed is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send_help(ctx.command)

    @user.command(name="add", help="Ajoute un utilisateur à la blacklist.")
    @commands.is_owner()
    async def add_user(self, ctx, user: discord.User):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute(
                "SELECT user_id FROM user_blacklist WHERE user_id = ?", (user.id,)
            )
            if await cursor.fetchone():
                await ctx.reply(
                    view=CV2(
                        "Utilisateur déjà blacklisté",
                        f"{user.mention} est déjà blacklisté.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO user_blacklist (user_id) VALUES (?)", (user.id,)
                )
                await db.commit()
                await ctx.reply(
                    view=CV2(
                        f"{TICK} Utilisateur blacklisté",
                        f"{user.mention} a été ajouté à la blacklist.",
                    )
                )

    @user.command(name="remove", help="Retire un utilisateur de la blacklist.")
    @commands.is_owner()
    async def remove_user(self, ctx, user: discord.User):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute(
                "SELECT user_id FROM user_blacklist WHERE user_id = ?", (user.id,)
            )
            if not await cursor.fetchone():
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Utilisateur non blacklisté",
                        f"{user.mention} n’est pas dans la blacklist.",
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM user_blacklist WHERE user_id = ?", (user.id,)
                )
                await db.commit()
                await ctx.reply(
                    view=CV2(
                        f"{TICK} Utilisateur déblacklisté",
                        f"{user.mention} a été retiré de la blacklist.",
                    )
                )

    @user.command(
        name="show", aliases=["list"], help="Affiche tous les utilisateurs blacklistés."
    )
    @commands.is_owner()
    async def show_users(self, ctx):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute("SELECT user_id FROM user_blacklist")
            rows = await cursor.fetchall()
            if not rows:
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Non Blacklisted Users",
                        "Il n’y a aucun utilisateur dans la blacklist.",
                    )
                )
                return

            blacklist = []
            for row in rows:
                user_id = row[0]
                try:
                    user = await self.bot.fetch_user(user_id)
                    username = user.name
                    user_link = f"https://discord.com/users/{user_id}"
                    # indexx = [""for index, user in enumerate(blacklist)]

                    blacklist.append(f"**[{username}]({user_link})** - ({user_id})")
                except discord.NotFound:
                    blacklist.append(
                        f"ID utilisateur : {user_id} (Utilisateur introuvable)"
                    )
            entries = [f"{index +1 }. {user}" for index, user in enumerate(blacklist)]
            paginator = Paginator(
                source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=f"Liste des utilisateurs blacklistés - {len(blacklist)}",
                    description="",
                    per_page=10,
                    color=0xFF0000,
                ),
                ctx=ctx,
            )
            await paginator.paginate()

    @blacklist.group(
        name="guild",
        help="Ajouter/Retirer un serveur de la blacklist.",
        invoke_without_command=True,
    )
    @commands.is_owner()
    async def guild(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @guild.command(name="add", help="Ajoute un serveur à la blacklist.")
    @commands.is_owner()
    async def add_guild(self, ctx, guild_id: int):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute(
                "SELECT guild_id FROM guild_blacklist WHERE guild_id = ?", (guild_id,)
            )
            if await cursor.fetchone():
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Serveur déjà blacklisté",
                        f"Le serveur avec l’ID `{guild_id}` est déjà blacklisté.",
                    )
                )
            else:
                await db.execute(
                    "INSERT INTO guild_blacklist (guild_id) VALUES (?)", (guild_id,)
                )
                await db.commit()
                await ctx.reply(
                    view=CV2(
                        f"{TICK} Serveur blacklisté",
                        f"Le serveur avec l’ID `{guild_id}` a été ajouté à la blacklist.",
                    )
                )

    @guild.command(name="remove", help="Retire un serveur de la blacklist.")
    @commands.is_owner()
    async def remove_guild(self, ctx, guild_id: int):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute(
                "SELECT guild_id FROM guild_blacklist WHERE guild_id = ?", (guild_id,)
            )
            if not await cursor.fetchone():
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Serveur non blacklisté",
                        f"Le serveur avec l’ID `{guild_id}` n’est pas dans la blacklist.",
                    )
                )
            else:
                await db.execute(
                    "DELETE FROM guild_blacklist WHERE guild_id = ?", (guild_id,)
                )
                await db.commit()
                await ctx.reply(
                    view=CV2(
                        f"{TICK} Serveur déblacklisté",
                        f"Le serveur avec l’ID `{guild_id}` a été retiré de la blacklist.",
                    )
                )

    @guild.command(
        name="show", aliases=["list"], help="Affiche la liste des serveurs blacklistés"
    )
    @commands.is_owner()
    async def show_guilds(self, ctx):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute("SELECT guild_id FROM guild_blacklist")
            rows = await cursor.fetchall()
            if not rows:
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Non Blacklisted Guilds",
                        "Il n’y a aucun serveur dans la blacklist.",
                    )
                )
                return

            blacklist = []
            for row in rows:
                guild_id = row[0]
                try:
                    guild = await self.bot.fetch_guild(guild_id)
                    guild_name = guild.name
                    guild_link = f"https://discord.com/guilds/{guild_id}"
                    blacklist.append(f"[{guild_name}]({guild_link}) - ({guild_id})")
                except discord.NotFound:
                    blacklist.append(f"ID serveur : {guild_id} (Serveur introuvable)")
            entries = [f"{index +1 }. {guild}" for index, guild in enumerate(blacklist)]
            paginator = Paginator(
                source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=f"Liste des serveurs blacklistés - {len(blacklist)}",
                    description="",
                    per_page=10,
                    color=0xFF0000,
                ),
                ctx=ctx,
            )
            await paginator.paginate()
