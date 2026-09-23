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
import json
import aiosqlite
from discord.ext import commands
from utils.config import serverLink
from core import zyrox, Cog, Context
from utils.Tools import get_ignore_data


class Errors(Cog):
    def __init__(self, client: zyrox):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if ctx.command is None:
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.CheckFailure):
            data = await get_ignore_data(ctx.guild.id)
            ch = data["channel"]
            iuser = data["user"]
            cmd = data["command"]
            buser = data["bypassuser"]

            if str(ctx.author.id) in buser:
                return

            if str(ctx.channel.id) in ch:
                await ctx.reply(
                    f"{ctx.author.mention} **Ce salon est dans la liste des salons ignorés, essayez mes commandes dans un autre salon**.",
                    delete_after=8,
                )
                return

            if str(ctx.author.id) in iuser:
                await ctx.reply(
                    f"{ctx.author.mention} **Vous êtes défini comme utilisateur ignoré pour ce serveur. Veuillez essayer mes commandes sur un autre serveur.**",
                    delete_after=8,
                )
                return

            if ctx.command.name in cmd or any(
                alias in cmd for alias in ctx.command.aliases
            ):
                await ctx.reply(
                    f"{ctx.author.mention} **Cette commande est ignorée sur ce serveur. Veuillez utiliser d’autres commandes ou essayer cette commande sur un autre serveur**",
                    delete_after=8,
                )
                return

        if isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(
                color=0xFF0000,
                description="Vous ne pouvez pas utiliser mes commandes en MP.",
            )
            embed.set_author(
                name=ctx.author,
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            embed.set_thumbnail(
                url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                )
            )
            await ctx.reply(embed=embed, delete_after=20)
            return

        if isinstance(error, commands.TooManyArguments):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                color=0xFF0000,
                description=f"**{ctx.author.mention} Temps de recharge actif, réessayez dans {error.retry_after:.2f} secondes**.",
            )
            embed.set_author(
                name="Temps d’attente", icon_url=self.client.user.avatar.url
            )

            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.reply(embed=embed, delete_after=10)
            return

        if isinstance(error, commands.MaxConcurrencyReached):
            embed = discord.Embed(
                color=0xFF0000,
                description=f"{ctx.author.mention} Cette commande est déjà en cours. Veuillez la laisser se terminer puis réessayez.",
            )
            embed.set_author(
                name="Commande en cours.", icon_url=self.client.user.avatar.url
            )

            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.reply(embed=embed, delete_after=10)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            fmt = (
                "{}, and {}".format(", ".join(missing[:-1]), missing[-1])
                if len(missing) > 2
                else " and ".join(missing)
            )
            embed = discord.Embed(
                color=0xFF0000,
                description=f"**Oups ! Il vous manque la permission {fmt} pour exécuter la commande {ctx.command.name} !**",
            )
            embed.set_author(
                name="Permissions manquantes", icon_url=self.client.user.avatar.url
            )

            embed.set_footer(
                text=f"Demandé par {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.reply(embed=embed, delete_after=7)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(error.missing_permissions)
            await ctx.reply(
                f"** Hein ! J’ai besoin de la permission {missing} pour exécuter la commande {ctx.command.qualified_name} ! Donnez-moi la permission {missing} **",
                delete_after=7,
            )
            return

        if isinstance(error, discord.HTTPException):
            print(f"[ERROR] HTTPException in {ctx.command}: {error}")
            return

        if isinstance(error, commands.CommandInvokeError):
            print(f"[ERROR] CommandInvokeError in {ctx.command}: {error}")
            print(f"  Original: {error.original}")
            return
