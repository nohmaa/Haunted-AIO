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
from utils.emoji import ZCIRCLE
from discord.ext import commands


class _birth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Birthday commands"""

    def help_custom(self):
        emoji = ZCIRCLE
        label = "Commandes Anniversaire"
        description = "Affiche les commandes d’anniversaire"
        return emoji, label, description

    @commands.group()
    async def __Birthday__(self, ctx: commands.Context):
        """`birthdaysetup` , `setbirthday` , `removebirthday` , `listbirthdays` , `birthday`"""
        pass
