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
from utils.emoji import ZPEOPLE

from discord.ext import commands


class inviteTracker(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    """Invite Tracker"""

    def help_custom(self):

        emoji = ZPEOPLE

        label = "Suivi d’invitations"

        description = "Affiche les commandes de suivi d’invitations"

        return emoji, label, description

    @commands.group()
    async def __InviteTracker__(self, ctx: commands.Context):
        """`>invites`, `>addinvites`, `>inviteleaderboard`, `>invitelogging`"""
