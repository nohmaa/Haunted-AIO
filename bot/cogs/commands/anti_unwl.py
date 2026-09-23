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
from utils.emoji import CROSS, MANAGER, REDDOT, TICK
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, Container
import aiosqlite
from utils.Tools import *
from utils.cv2 import CV2, build_container


class Unwhitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize_db())

    # @commands.Cog.listener()
    async def initialize_db(self):
        self.db = await aiosqlite.connect("db/anti.db")

    @commands.hybrid_command(
        name="unwhitelist",
        aliases=["unwl"],
        help="Retirer un utilisateur de la whitelist antinuke",
    )
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def unwhitelist(self, ctx, member: discord.Member = None):
        if ctx.guild.member_count < 2:
            view = CV2(
                f"{CROSS} Error",
                "Votre serveur ne remplit pas mon critère de 30 membres",
            )
            return await ctx.send(view=view)

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id),
        ) as cursor:
            check = await cursor.fetchone()

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            antinuke = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            view = CV2(
                f"{CROSS} Accès refusé",
                "Seul le propriétaire du serveur ou un Extra Owner peut exécuter cette commande !",
            )
            return await ctx.send(view=view)

        if not antinuke or not antinuke[0]:
            view = CV2(
                f"{ctx.guild.name} Security Settings {MANAGER}",
                f"Ohh NO! looks like your server doesn't enabled security\n\nCurrent Status : {CROSS}\n\nTo enable use `antinuke enable`",
            )
            return await ctx.send(view=view)

        if not member:
            view = CV2(
                "__Commandes Unwhitelist__",
                "**Retire l’utilisateur des whitelistés, le module antinuke agira donc contre lui s’il le déclenche.**",
                f"**Usage**\n{REDDOT} `unwhitelist @user/id`\n{REDDOT} `unwl @user`",
            )
            return await ctx.send(view=view)

        async with self.db.execute(
            "SELECT * FROM whitelisted_users WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id),
        ) as cursor:
            data = await cursor.fetchone()

        if not data:
            view = CV2(
                f"{CROSS} Error", f"<@{member.id}> n’est pas un membre whitelisté."
            )
            return await ctx.send(view=view)

        await self.db.execute(
            "DELETE FROM whitelisted_users WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id),
        )
        await self.db.commit()

        view = CV2(
            f"{TICK} Succès",
            f"L’utilisateur <@!{member.id}> a été retiré de la whitelist.",
        )
        await ctx.send(view=view)
