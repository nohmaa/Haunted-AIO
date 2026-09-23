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
from utils.emoji import CROSS, ICONS_WARNING, TICK
import aiosqlite
import logging
from discord.ext import commands
from typing import List, Dict
from discord.ui import LayoutView, TextDisplay, Separator, Container
from utils.Tools import *
from utils.cv2 import CV2, build_container
from utils.config import OWNER_IDS

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

DATABASE_PATH = "db/autorole.db"


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if (
            interaction.user.id != self.ctx.author.id
            and interaction.user.id not in OWNER_IDS
        ):
            await interaction.response.send_message(
                "Uh oh! That message doesn't belong to you.\nYou must run this command to interact with it.",
                ephemeral=True,
            )
            return False
        return True


class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.create_table())
        self.color = 0xFF0000

    async def create_table(self):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS autorole (
                guild_id INTEGER PRIMARY KEY,
                bots TEXT NOT NULL,
                humans TEXT NOT NULL
            )
            """)
            await db.commit()

    async def get_autorole(self, guild_id: int) -> Dict[str, List[int]]:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT bots, humans FROM autorole WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    bots, humans = row

                    bots = [
                        int(role_id)
                        for role_id in bots.replace("[", "")
                        .replace("]", "")
                        .replace(" ", "")
                        .split(",")
                        if role_id
                    ]
                    humans = [
                        int(role_id)
                        for role_id in humans.replace("[", "")
                        .replace("]", "")
                        .replace(" ", "")
                        .split(",")
                        if role_id
                    ]

                    return {"bots": bots, "humans": humans}
                else:
                    return {"bots": [], "humans": []}

    async def update_autorole(self, guild_id: int, data: Dict[str, List[int]]):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            bots = ",".join(map(str, data["bots"]))
            humans = ",".join(map(str, data["humans"]))

            await db.execute(
                "INSERT OR REPLACE INTO autorole (guild_id, bots, humans) VALUES (?, ?, ?)",
                (guild_id, bots, humans),
            )
            await db.commit()

    @commands.group(name="autorole", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole.command(
        name="config", help="Affiche la configuration actuelle de l’autorole"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _ar_config(self, ctx):

        data = await self.get_autorole(ctx.guild.id)
        if data:
            fetched_humans = [
                ctx.guild.get_role(role_id)
                for role_id in data["humans"]
                if ctx.guild.get_role(role_id)
            ]
            fetched_bots = [
                ctx.guild.get_role(role_id)
                for role_id in data["bots"]
                if ctx.guild.get_role(role_id)
            ]

            hums = "\n".join(role.mention for role in fetched_humans) or "None"
            bos = "\n".join(role.mention for role in fetched_bots) or "None"

            view = CV2(
                f"Configuration Autorole pour {ctx.guild.name}",
                f"__Humans__\n{hums}",
                f"__Bots__\n{bos}",
            )
            await ctx.send(view=view)
        else:
            view = CV2(
                "Configuration Autorole",
                "Aucune configuration autorole trouvée sur ce serveur.",
            )
            await ctx.reply(view=view)

    @_autorole.group(name="reset", help="Effacer la configuration autorole du serveur")
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_reset.command(
        name="humans", help="Effacer la configuration autorole pour les humains"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_reset(self, ctx):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT humans FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data and data[0]:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "UPDATE autorole SET humans = ? WHERE guild_id = ?",
                    ("[]", ctx.guild.id),
                )
                await db.commit()
            view = CV2(
                f"{TICK} Succès",
                "Tous les autoroles humains ont été effacés sur ce serveur.",
            )
        else:
            view = CV2(f"{CROSS} Error", "Non Autoroles set for humans in this Guild.")

        await ctx.reply(view=view)

    @_autorole_reset.command(
        name="bots", help="Effacer la configuration autorole pour les bots"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @ignore_check()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_reset(self, ctx):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT bots FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data and data[0]:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "UPDATE autorole SET bots = ? WHERE guild_id = ?",
                    ("[]", ctx.guild.id),
                )
                await db.commit()
            view = CV2(
                f"{TICK} Succès",
                "Tous les autoroles bots ont été effacés sur ce serveur.",
            )
        else:
            view = CV2(f"{CROSS} Error", "Non Autoroles set for Bots in this Guild.")

        await ctx.reply(view=view)

    @_autorole_reset.command(
        name="all", help="Effacer toute la configuration autorole du serveur"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_reset_all(self, ctx):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT humans, bots FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data and (data[0] or data[1]):
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "UPDATE autorole SET humans = ?, bots = ? WHERE guild_id = ?",
                    ("[]", "[]", ctx.guild.id),
                )
                await db.commit()
            view = CV2(
                f"{TICK} Succès", "Tous les autoroles ont été effacés sur ce serveur."
            )
        else:
            view = CV2(f"{CROSS} Error", "Non Autoroles set in this Guild.")

        await ctx.reply(view=view)

    @_autorole.group(name="humans", help="Configurer les autoroles pour les humains")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_humans.command(
        name="add", help="Ajouter un rôle à la liste des autoroles humains."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_add(self, ctx, *, role: discord.Role):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT humans FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data:
            humans = eval(data[0])
            if role.id in humans:
                view = CV2(
                    f"{ICONS_WARNING} Accès refusé",
                    f"{role.mention} est déjà dans les autoroles humains.",
                )
            elif len(humans) >= 10:
                view = CV2(
                    f"{ICONS_WARNING} Accès refusé",
                    "Tu ne peux ajouter que 10 autoroles humains maximum.",
                )
            else:
                humans.append(role.id)
                async with aiosqlite.connect(DATABASE_PATH) as db:
                    await db.execute(
                        "UPDATE autorole SET humans = ? WHERE guild_id = ?",
                        (str(humans), ctx.guild.id),
                    )
                    await db.commit()
                view = CV2(
                    f"{TICK} Succès",
                    f"{role.mention} a été ajouté aux autoroles humains.",
                )
        else:
            humans = [role.id]
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "INSERT INTO autorole (guild_id, humans, bots) VALUES (?, ?, ?)",
                    (ctx.guild.id, str(humans), "[]"),
                )
                await db.commit()
            view = CV2(
                f"{TICK} Succès", f"{role.mention} a été ajouté aux autoroles humains."
            )

        await ctx.reply(view=view)

    @_autorole_humans.command(
        name="remove", help="Retirer un rôle des autoroles humains."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_humans_remove(self, ctx, *, role: discord.Role):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT humans FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data:
            humans = eval(data[0])
            if role.id not in humans:
                view = CV2(
                    f"{CROSS} Error",
                    f"{role.mention} n’est pas dans les autoroles humains.",
                )
            else:
                humans.remove(role.id)
                async with aiosqlite.connect(DATABASE_PATH) as db:
                    await db.execute(
                        "UPDATE autorole SET humans = ? WHERE guild_id = ?",
                        (str(humans), ctx.guild.id),
                    )
                    await db.commit()
                view = CV2(
                    f"{TICK} Succès",
                    f"{role.mention} a été retiré des autoroles humains.",
                )
        else:
            view = CV2(f"{CROSS} Error", "Non Autoroles set in this guild for humans.")

        await ctx.reply(view=view)

    @_autorole.group(name="bots", help="Configurer les autoroles pour les bots")
    @blacklist_check()
    @ignore_check()
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @_autorole_bots.command(name="add", help="Ajouter un rôle aux autoroles bots.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_add(self, ctx, *, role: discord.Role):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT bots FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data:
            bots = eval(data[0])
            if role.id in bots:
                view = CV2(
                    f"{ICONS_WARNING} Accès refusé",
                    f"{role.mention} est déjà dans les autoroles bots.",
                )
            elif len(bots) >= 10:
                view = CV2(
                    f"{ICONS_WARNING} Accès refusé",
                    "Tu ne peux ajouter que 10 autoroles bots maximum",
                )
            else:
                bots.append(role.id)
                async with aiosqlite.connect(DATABASE_PATH) as db:
                    await db.execute(
                        "UPDATE autorole SET bots = ? WHERE guild_id = ?",
                        (str(bots), ctx.guild.id),
                    )
                    await db.commit()
                view = CV2(
                    f"{TICK} Succès", f"{role.mention} a été ajouté aux autoroles bots."
                )
        else:
            bots = [role.id]
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "INSERT INTO autorole (guild_id, humans, bots) VALUES (?, ?, ?)",
                    (ctx.guild.id, "[]", str(bots)),
                )
                await db.commit()
            view = CV2(
                f"{TICK} Succès", f"{role.mention} a été ajouté aux autoroles bots."
            )

        await ctx.reply(view=view)

    @_autorole_bots.command(name="remove", help="Retirer un rôle des autoroles bots.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _autorole_bots_remove(self, ctx, *, role: discord.Role):
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT bots FROM autorole WHERE guild_id = ?", (ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()

        if data:
            bots = eval(data[0])
            if role.id not in bots:
                view = CV2(
                    f"{CROSS} Error",
                    f"{role.mention} n’est pas dans les autoroles bots.",
                )
            else:
                bots.remove(role.id)
                async with aiosqlite.connect(DATABASE_PATH) as db:
                    await db.execute(
                        "UPDATE autorole SET bots = ? WHERE guild_id = ?",
                        (str(bots), ctx.guild.id),
                    )
                    await db.commit()
                view = CV2(
                    f"{TICK} Succès", f"{role.mention} a été retiré des autoroles bots."
                )
        else:
            view = CV2(f"{CROSS} Error", "Non Autoroles set in this guild for bots.")

        await ctx.reply(view=view)
