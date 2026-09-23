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
from utils.emoji import CROSS, TICK, ZWARNING
import discord
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


class Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF0000

    @commands.group(name="role", invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @top_check()
    @blacklist_check()
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):
        if not ctx.guild.me.guild_permissions.manage_roles:
            return await ctx.send(
                f"{ZWARNING} Je n’ai pas la permission de gérer les rôles !"
            )

        if role >= ctx.guild.me.top_role:
            error = discord.Embed(
                color=self.color,
                description="Je ne peux pas gérer les rôles d’un utilisateur avec un rôle supérieur ou égal !",
            )

            error.set_author(name="Erreur")
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
            error.set_author(name="Accès refusé")
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
                success.set_author(name="Rôle ajouté")
                success.set_footer(
                    text=f"Requested by {ctx.author}",
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
                success.set_author(name="Rôle retiré")
                success.set_footer(
                    text=f"Requested by {ctx.author}",
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

    @role.command(help="Donne un rôle à un membre pour une durée déterminée")
    @commands.bot_has_permissions(manage_roles=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def temp(self, ctx, role: discord.Role, time, *, user: discord.Member):
        if (
            ctx.author != ctx.guild.owner
            and role.position >= ctx.author.top_role.position
        ):
            embed = discord.Embed(
                description=f"Vous ne pouvez pas gérer un rôle supérieur ou égal à votre rôle le plus élevé !",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        else:
            if role.position >= ctx.guild.me.top_role.position:
                embed1 = discord.Embed(
                    description=f"{role} est au-dessus de mon rôle le plus élevé, déplacez mon rôle au-dessus de {role}.",
                    color=self.color,
                )
                embed1.set_author(name="Erreur")
                embed1.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=(
                        ctx.author.avatar.url
                        if ctx.author.avatar
                        else ctx.author.default_avatar.url
                    ),
                )
                return await ctx.send(embed=embed1)
        seconds = convert(time)
        await user.add_roles(role, reason=None)
        success = discord.Embed(
            description=f"{role.mention} ajouté à {user.mention} avec succès .",
            color=self.color,
        )
        success.set_author(name="Succès")
        success.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        await ctx.send(embed=success)
        await asyncio.sleep(seconds)
        await user.remove_roles(role)

    @role.command(help="Supprime un rôle du serveur")
    @blacklist_check()
    @ignore_check()
    @top_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def delete(self, ctx, *, role: discord.Role):
        if (
            ctx.author != ctx.guild.owner
            and role.position >= ctx.author.top_role.position
        ):
            embed = discord.Embed(
                description=f"Vous ne pouvez pas supprimer un rôle supérieur ou égal à votre rôle le plus élevé !",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(
                description=f"Je ne peux pas supprimer {role} car il est au-dessus de mon rôle le plus élevé. Veuillez déplacer mon rôle au-dessus de {role}.",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        if role is None:
            embed = discord.Embed(
                description=f"Aucun rôle nommé {role} trouvé sur ce serveur.",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        await role.delete()

        embed = discord.Embed(
            description=f"{role} supprimé avec succès.", color=self.color
        )
        embed.set_author(name="Success")
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        await ctx.send(embed=embed)

    @role.command(help="Crée un rôle sur le serveur")
    @blacklist_check()
    @ignore_check()
    @top_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def create(self, ctx, *, name):
        embed = discord.Embed(
            description=f"Successfully created a role named {name}.", color=self.color
        )
        embed.set_author(name="Success")
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        await ctx.guild.create_role(name=name, color=discord.Color.default())
        await ctx.send(embed=embed)

    @role.command(help="Renames a role in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def rename(self, ctx, role: discord.Role, *, newname):

        if role.position >= ctx.author.top_role.position:
            embed = discord.Embed(
                description=f"You can't manage the role {role.mention} because it is higher or equal to your top role.",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        if role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(
                description=f"I can't manage the role {role.mention} because it is higher than my top role.",
                color=self.color,
            )
            embed.set_author(name="Erreur")
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            return await ctx.send(embed=embed)

        await role.edit(name=newname)
        embed = discord.Embed(
            description=f"Role {role.name} has been renamed to {newname}.",
            color=self.color,
        )
        embed.set_author(name="Success")
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        await ctx.send(embed=embed)

    @role.command(name="humans", help="Gives role to all humans in the guild")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role_humans(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Assigning {role.mention} to all humans...",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            if not member.bot and role not in member.roles:
                                try:
                                    await member.add_roles(
                                        role,
                                        reason=f"Role Humans Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully assigned {role.mention} to {count} human(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content=f"{ZWARNING} I am missing the required permissions. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. No humans will be assigned the role {role.mention}.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            members_without_role = [
                member
                for member in ctx.guild.members
                if not member.bot and role not in member.roles
            ]
            if len(members_without_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{ZWARNING} | All humans already have the {role.mention} role.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"Are you sure you want to assign {role.mention} to {len(members_without_role)} members?",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)

        else:
            denied = discord.Embed(
                title=f"{ZWARNING} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @role.command(name="bots", help="Gives role to all the bots in the guild")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role_bots(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Adding {role.mention} to all bots...",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            if member.bot and role not in member.roles:
                                try:
                                    await member.add_roles(
                                        role,
                                        reason=f"Role Bots Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully added {role.mention} to {count} bot(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. No bots will be assigned the role {role.mention}.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            bots_without_role = [
                member
                for member in ctx.guild.members
                if member.bot and role not in member.roles
            ]
            if len(bots_without_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{ZWARNING} | All bots already have the {role.mention} role.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to give {role.mention} to {len(bots_without_role)} bots?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)

        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @role.command(
        name="unverified", help="Gives role to all the unverified members in the guild"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role_unverified(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Adding {role.mention} to all unverified members.",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            if member.avatar is None and role not in member.roles:
                                try:
                                    await member.add_roles(
                                        role,
                                        reason=f"Role Unverified Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully added {role.mention} to {count} unverified member(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. No unverified members will be assigned the role {role.mention}.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            embed = discord.Embed(
                color=self.color,
                description=f"**Are you sure you want to give {role.mention} to all unverified members in this guild?**",
            )
            view = View()
            button.callback = button_callback
            button1.callback = button1_callback
            view.add_item(button)
            view.add_item(button1)
            await ctx.reply(embed=embed, view=view, mention_author=False)

        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @role.command(name="all", help="Gives role to all the members in the guild")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Adding {role.mention} to all members.",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            try:
                                await member.add_roles(
                                    role,
                                    reason=f"Role All Command Executed By: {ctx.author}",
                                )
                                count += 1
                            except Exception as e:
                                print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully added {role.mention} to {count} member(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. No members will be assigned the role {role.mention}.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            members_without_role = [
                member for member in ctx.guild.members if role not in member.roles
            ]
            if len(members_without_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"{ZWARNING} | {role.mention} is already given to all the members of the server.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to give {role.mention} to {len(members_without_role)} members?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @commands.group(
        name="removerole",
        invoke_without_command=True,
        aliases=["rrole"],
        help="remove a role from all members .",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @blacklist_check()
    @commands.has_permissions(administrator=True)
    async def rrole(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @rrole.command(
        name="humans", help="Removes a role from all the humans in the server."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def rrole_humans(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Removing {role.mention} from all humans.",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            if not member.bot and role in member.roles:
                                try:
                                    await member.remove_roles(
                                        role,
                                        reason=f"Remove Role Humans Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}>| Successfully removed {role.mention} from {count} human(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. {role.mention} will not be removed from any humans.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            humans_with_role = [
                member
                for member in ctx.guild.members
                if not member.bot and role in member.roles
            ]
            if len(humans_with_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"| Already no humans have {role.mention}.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to remove {role.mention} from {len(humans_with_role)} humans in this guild?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

            await ctx.send(embed=embed, mention_author=False)

    @rrole.command(name="bots", help="Removes a role from all the bots in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def rrole_bots(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Removing {role.mention} from all bots...",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)
                        for member in interaction.guild.members:
                            if member.bot and role in member.roles:
                                try:
                                    await member.remove_roles(
                                        role,
                                        reason=f"Remove Role Bots Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully removed {role.mention} from {count} bot(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. {role.mention} will not be removed from any bots.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            bots_with_role = [
                member
                for member in ctx.guild.members
                if member.bot and role in member.roles
            ]
            if len(bots_with_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"| Already no bots have {role.mention}.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to remove {role.mention} from {len(bots_with_role)} bots in this guild?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @rrole.command(name="all", help="Removes a role from all members in the server.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def rrole_all(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Confirm", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="Cancel", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                removed_count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Removing {role.mention} from all members.",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)

                        for member in interaction.guild.members:
                            if role in member.roles:
                                try:
                                    await member.remove_roles(
                                        role,
                                        reason=f"Remove Role All Command Executed By: {ctx.author}",
                                    )
                                    removed_count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}>| Successfully removed {role.mention} from {removed_count} member(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. {role.mention} will not be removed from anyone.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            members_with_role = [
                member for member in ctx.guild.members if role in member.roles
            ]
            if len(members_with_role) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"| No members currently have {role.mention}.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to remove {role.mention} from {len(members_with_role)} members in this guild?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)

    @rrole.command(
        name="unverified",
        help="Removes a role from all the unverified members in the server.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def rrole_unverified(self, ctx, *, role: discord.Role):
        if (
            ctx.author == ctx.guild.owner
            or ctx.author.top_role.position > ctx.guild.me.top_role.position
        ):
            button = Button(
                label="Yes", style=discord.ButtonStyle.green, emoji=f"{TICK}>"
            )
            button1 = Button(label="No", style=discord.ButtonStyle.red, emoji=CROSS)

            async def button_callback(interaction: discord.Interaction):
                count = 0
                if interaction.user == ctx.author:
                    if interaction.guild.me.guild_permissions.manage_roles:
                        embed1 = discord.Embed(
                            color=self.color,
                            description=f"Removing {role.mention} from all unverified members.",
                        )
                        await interaction.response.edit_message(embed=embed1, view=None)

                        for member in interaction.guild.members:
                            if member.avatar is None and role in member.roles:
                                try:
                                    await member.remove_roles(
                                        role,
                                        reason=f"Remove Role Unverified Command Executed By: {ctx.author}",
                                    )
                                    count += 1
                                except Exception as e:
                                    print(e)

                        await interaction.channel.send(
                            content=f"{TICK}> | Successfully removed {role.mention} from {count} unverified member(s)."
                        )
                    else:
                        await interaction.response.edit_message(
                            content="I am missing the required permission. Please grant the necessary permissions and try again.",
                            embed=None,
                            view=None,
                        )
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            async def button1_callback(interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    embed2 = discord.Embed(
                        color=self.color,
                        description=f"Action cancelled. {role.mention} will not be removed from any unverified members.",
                    )
                    await interaction.response.edit_message(embed=embed2, view=None)
                else:
                    await interaction.response.send_message(
                        "This action is not for you!",
                        embed=None,
                        view=None,
                        ephemeral=True,
                    )

            unverified_members = [
                member
                for member in ctx.guild.members
                if member.avatar is None and role in member.roles
            ]
            if len(unverified_members) == 0:
                return await ctx.reply(
                    embed=discord.Embed(
                        description=f"| Already no unverified members have {role.mention}.",
                        color=self.color,
                    )
                )
            else:
                embed = discord.Embed(
                    color=self.color,
                    description=f"**Are you sure you want to remove {role.mention} from {len(unverified_members)} unverified members in this guild?**",
                )
                view = View()
                button.callback = button_callback
                button1.callback = button1_callback
                view.add_item(button)
                view.add_item(button1)
                await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            denied = discord.Embed(
                title=f"{CROSS} Access Denied",
                description="Your role should be above my top role.",
                color=0xFF0000,
            )
            denied.set_footer(
                text=f"“{ctx.command.qualified_name}” Command executed by {ctx.author}",
                icon_url=(
                    ctx.author.avatar.url
                    if ctx.author.avatar
                    else ctx.author.default_avatar.url
                ),
            )
            await ctx.send(embed=denied, mention_author=False)
