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
from utils.emoji import WIFI
from discord.ext import commands


class _server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Server commands"""

    def help_custom(self):
        emoji = WIFI
        label = "Commandes de serveur"
        description = "Affiche les commandes de serveur"
        return emoji, label, description

    @commands.group()
    async def __Setup__(self, ctx: commands.Context):
        """`setup` , `setup create <name>` , `setup delete <name>`  , `setup list` , `setup staff` , `setup girl` , `setup friend` , `setup vip` , `setup guest` , `setup config` , `setup reset` , `staff` , `girl` , `friend` , `vip` , `guest`\n\n__**Rôle automatique**__\n`autorole bots add` , `autorole bots remove` , `autorole bots` , `autorole config` , `autorole humans add` , `autorole humans remove` , `autorole humans` , `autorole reset all` , `autorole reset bots` , `autorole reset humans` , `autorole`\n\n__**Réponse automatique**__\n`autoresponder` , `autoresponder create` , `autoresponder delete` , `autoresponder edit` , `autoresponder config`\n\n__**Commandes de réaction automatique**__\n`react` , `react add` , `react remove` , `react list` , `react reset`"""
