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
from utils.emoji import CHANNEL, TICK, ZCROSS
from discord.ext import commands


class Hide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(255, 0, 0)  # Red color for embeds

    @commands.hybrid_command(
        name="hide",
        help="Masque un salon au rôle par défaut (@everyone).",
        usage="hide [channel]",
        aliases=["hidechannel"],
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def hide_command(self, ctx, channel: discord.TextChannel = None):
        """Hides a channel from @everyone."""
        # If no channel is specified, default to the current channel
        channel = channel or ctx.channel

        # Get the authorf's avatar URL, handling cases where they might have a default avatar
        author_avatar_url = ctx.author.avatar.url if ctx.author.avatar else None

        # Check if the channel is already hidden
        if not channel.permissions_for(ctx.guild.default_role).read_messages:
            embed = discord.Embed(
                description=f"**{CHANNEL} Salon**: {channel.mention}\n{ZCROSS} **Statut**: Déjà masqué",
                color=self.color,
            )
            embed.set_author(name=f"{channel.name} est déjà masqué")
            # Set the author's avatar as the thumbnail
            if author_avatar_url:
                embed.set_thumbnail(url=author_avatar_url)
            await ctx.send(embed=embed)
            return

        # Hide the channel by updating permissions for the @everyone role
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)

        # Create the success embed
        embed = discord.Embed(
            description=f"**{TICK} | {channel.mention} a été masqué avec succès.**",
            color=self.color,
        )
        embed.set_author(name=f"Salon masqué")
        embed.set_footer(
            text=f"Action de {ctx.author.name}", icon_url=author_avatar_url
        )
        # Set the author's avatar as the thumbnail
        if author_avatar_url:
            embed.set_thumbnail(url=author_avatar_url)

        await ctx.send(embed=embed)


# Function to add the cog to your bot
async def setup(bot):
    await bot.add_cog(Hide(bot))
