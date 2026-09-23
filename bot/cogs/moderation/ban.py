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
from utils.emoji import TICK, ZWARNING
from discord.ext import commands
from discord import ui
from utils.Tools import *


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 0, 0)

    def get_user_avatar(self, user):
        return user.avatar.url if user.avatar else user.default_avatar.url

    @commands.hybrid_command(
        name="ban",
        help="Bannit un utilisateur du serveur",
        usage="ban <member>",
        aliases=["fuckban", "hackban", "kuttaban"],
    )
    @blacklist_check()
    @ignore_check()
    @top_check()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason=None):

        member = ctx.guild.get_member(user.id)
        if not member:
            try:
                user = await self.bot.fetch_user(user.id)
            except discord.NotFound:
                # User not found container
                container = ui.Container()
                container.add_item(
                    ui.TextDisplay(
                        f"❌ **Utilisateur introuvable**\nUtilisateur avec l’ID {user.id} introuvable."
                    )
                )
                view = ui.LayoutView()
                view.add_item(container)
                await ctx.send(view=view)
                return

        bans = [entry async for entry in ctx.guild.bans()]
        if any(ban_entry.user.id == user.id for ban_entry in bans):
            # Already banned container
            container = ui.Container()
            container.add_item(ui.TextDisplay(f"⚠️ **{user.name} est déjà banni !**"))
            container.add_item(
                ui.TextDisplay(
                    "**L’utilisateur demandé est déjà banni sur ce serveur.**"
                )
            )
            container.add_item(ui.TextDisplay(f"*Demandé par {ctx.author}*"))
            view = ui.LayoutView()
            view.add_item(container)
            await ctx.send(view=view)
            return

        if member == ctx.guild.owner:
            # Server owner error container
            container = ui.Container()
            container.add_item(ui.TextDisplay("❌ **Erreur lors du bannissement**"))
            container.add_item(
                ui.TextDisplay("Je ne peux pas bannir le propriétaire du serveur !")
            )
            container.add_item(ui.TextDisplay(f"*Demandé par {ctx.author}*"))
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.send(view=view)

        if (
            isinstance(member, discord.Member)
            and member.top_role >= ctx.guild.me.top_role
        ):
            # Role hierarchy error container
            container = ui.Container()
            container.add_item(ui.TextDisplay("❌ **Erreur lors du bannissement**"))
            container.add_item(
                ui.TextDisplay(
                    "Je ne peux pas bannir un utilisateur avec un rôle supérieur ou égal !"
                )
            )
            container.add_item(ui.TextDisplay(f"*Demandé par {ctx.author}*"))
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.send(view=view)

        if isinstance(member, discord.Member):
            if ctx.author != ctx.guild.owner:
                if member.top_role >= ctx.author.top_role:
                    # Author role hierarchy error container
                    container = ui.Container()
                    container.add_item(
                        ui.TextDisplay("❌ **Erreur lors du bannissement**")
                    )
                    container.add_item(
                        ui.TextDisplay(
                            "Vous ne pouvez pas bannir un utilisateur avec un rôle supérieur ou égal !"
                        )
                    )
                    container.add_item(ui.TextDisplay(f"*Demandé par {ctx.author}*"))
                    view = ui.LayoutView()
                    view.add_item(container)
                    return await ctx.send(view=view)

        # Try to DM the user
        try:
            await user.send(
                f"{ZWARNING} Vous avez été banni de **{ctx.guild.name}** par **{ctx.author}**. Raison : {reason or 'Aucune raison fournie'}"
            )
            dm_status = "Yes"
        except discord.Forbidden:
            dm_status = "No"
        except discord.HTTPException:
            dm_status = "No"

        # Ban the user
        await ctx.guild.ban(
            user,
            reason=f"Bannissement demandé par {ctx.author} pour la raison : {reason or 'Aucune raison fournie'}",
        )

        # Success container with Components V2
        container = ui.Container()
        container.add_item(ui.TextDisplay(f"✅ **{user.name} banni avec succès**"))
        container.add_item(ui.Separator())
        container.add_item(
            ui.TextDisplay(
                f"**{TICK} | [{user}](https://discord.com/users/{user.id}) a été banni avec succès**"
                f"\n**Raison :** {reason or 'Aucune raison fournie'}"
                f"\n**MP envoyé :** {dm_status}"
                f"\n**Modérateur :** {ctx.author.mention}"
            )
        )
        container.add_item(ui.Separator())
        container.add_item(
            ui.TextDisplay(
                f"*Demandé par {ctx.author} • {discord.utils.format_dt(discord.utils.utcnow(), 'R')}*"
            )
        )

        view = ui.LayoutView()
        view.add_item(container)

        message = await ctx.send(view=view)


async def setup(bot):
    await bot.add_cog(Ban(bot))
