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
from utils.emoji import CROSS, ICONS_WARNING, TICK
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, Container
import aiosqlite
import re
from utils.Tools import *
from utils.cv2 import CV2, build_container


class AutoReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/autoreact.db"
        self.bot.loop.create_task(self.setup_database())

    async def setup_database(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS autoreact (
                    guild_id INTEGER,
                    trigger TEXT,
                    emojis TEXT
                )
            """)
            await db.commit()

    async def get_triggers(self, guild_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT trigger, emojis FROM autoreact WHERE guild_id = ?", (guild_id,)
            )
            return await cursor.fetchall()

    async def trigger_exists(self, guild_id, trigger):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT 1 FROM autoreact WHERE guild_id = ? AND trigger = ?",
                (guild_id, trigger),
            )
            return await cursor.fetchone()

    @commands.group(
        name="react",
        aliases=["autoreact"],
        help="Liste toutes les sous-commandes du groupe autoreact.",
        invoke_without_command=True,
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def react(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @react.command(
        name="add",
        aliases=["set", "create"],
        help="Ajoute un déclencheur et ses emojis à l’autoreact.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, trigger: str, *, emojis: str):
        if len(trigger.split()) > 1:
            view = CV2(
                f"{CROSS} Déclencheur invalide",
                "Les déclencheurs ne peuvent contenir qu’un seul mot.",
            )
            return await ctx.reply(view=view)

        emoji_list = re.findall(r"<a?:\w+:\d+>|[\u263a-\U0001f645]", emojis)
        if len(emoji_list) > 10:
            view = CV2(
                f"{CROSS} Trop d’emojis",
                "Tu ne peux définir que **10** emojis maximum par déclencheur.",
            )
            return await ctx.reply(view=view)

        triggers = await self.get_triggers(ctx.guild.id)
        if len(triggers) >= 10:
            view = CV2(
                f"{ICONS_WARNING} Limite de déclencheurs atteinte",
                "Tu ne peux définir que 10 déclencheurs de réactions auto sur ce serveur.",
            )
            return await ctx.reply(view=view)

        if await self.trigger_exists(ctx.guild.id, trigger):
            view = CV2(
                f"{ICONS_WARNING} Déclencheur existant",
                f"Le déclencheur ‘{trigger}’ existe déjà. Retire-le avant de l’ajouter à nouveau.",
            )
            return await ctx.reply(view=view)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO autoreact (guild_id, trigger, emojis) VALUES (?, ?, ?)",
                (ctx.guild.id, trigger, " ".join(emoji_list)),
            )
            await db.commit()

        view = CV2(
            f"{TICK} Déclencheur ajouté",
            f"Déclencheur '{trigger}' ajouté avec succès avec les emojis {', '.join(emoji_list)}.",
        )
        await ctx.reply(view=view)

    @react.command(
        name="remove",
        aliases=["clear", "delete"],
        help="Retire un déclencheur et ses emojis de l’autoreact.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, trigger: str):
        if not await self.trigger_exists(ctx.guild.id, trigger):
            view = CV2(
                f"{CROSS} Déclencheur introuvable",
                f"Le déclencheur ‘{trigger}’ n’existe pas.",
            )
            return await ctx.reply(view=view)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM autoreact WHERE guild_id = ? AND trigger = ?",
                (ctx.guild.id, trigger),
            )
            await db.commit()

        view = CV2(
            f"{TICK} Déclencheur retiré", f"Déclencheur '{trigger}' retiré avec succès."
        )
        await ctx.reply(view=view)

    @react.command(
        name="list",
        aliases=["show", "config"],
        help="Liste tous les déclencheurs et leurs emojis du module autoreact.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def list(self, ctx):
        triggers = await self.get_triggers(ctx.guild.id)
        if not triggers:
            view = CV2(
                "Non Triggers Set",
                "Aucun déclencheur de réaction auto défini sur ce serveur.",
            )
            return await ctx.reply(view=view)

        trigger_list = "\n".join([f"**{t[0]}:** {t[1]}" for t in triggers])
        view = CV2("Déclencheurs de réactions auto", trigger_list)
        await ctx.reply(view=view)

    @react.command(
        name="reset",
        help="Réinitialise tous les déclencheurs et leurs emojis du module autoreact.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        triggers = await self.get_triggers(ctx.guild.id)
        if not triggers:
            view = CV2(
                f"{CROSS} Non Triggers Set",
                "Aucun déclencheur de réaction auto à réinitialiser.",
            )
            return await ctx.reply(view=view)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM autoreact WHERE guild_id = ?", (ctx.guild.id,)
            )
            await db.commit()

        view = CV2(
            f"{TICK} Tous les déclencheurs réinitialisés",
            "Tous les déclencheurs de réactions auto ont été supprimés.",
        )
        await ctx.reply(view=view)


async def setup(bot):
    await bot.add_cog(AutoReaction(bot))
