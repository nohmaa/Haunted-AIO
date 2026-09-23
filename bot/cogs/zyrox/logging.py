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
from utils.emoji import CAST
from discord.ext import commands


class _logging(commands.Cog):
    module_key = "logging"

    def __init__(self, bot):
        self.bot = bot

    """Logging commands"""

    def help_custom(self):
        emoji = CAST
        label = "Commandes de logs"
        description = "Affiche les commandes de logs"
        return emoji, label, description

    @commands.group()
    async def __Logging__(self, ctx: commands.Context):
        """`log`, `log enable`, `log disable`, `log config`, `log ignore`, `log status`, `log toggle`"""
