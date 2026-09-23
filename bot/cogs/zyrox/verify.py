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
from utils.emoji import THUNDER
from discord.ext import commands


class _verify(commands.Cog):

    module_key = "verification"

    def __init__(self, bot):
        self.bot = bot

    """Verification commands help"""

    def help_custom(self):
        emoji = THUNDER
        label = "Commandes de vérification"
        description = "Affiche les commandes de vérification"
        return emoji, label, description

    @commands.group()
    async def __Verification__(self, ctx: commands.Context):
        """`verification setup`, `verification status`, `verification enable`, `verification disable`, `verification logs`, `verification reset`, `verification verify`, `verification fix`"""
        pass


async def setup(bot):
    await bot.add_cog(_verify(bot))
