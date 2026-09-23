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
from utils.emoji import LOCK
from discord.ext import commands


class _encrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
        emoji = LOCK
        label = "Commandes Chiffrement"
        description = "Encode et décode du texte dans plusieurs formats"
        return emoji, label, description

    @commands.group(name="encryption", aliases=["encrypt"], invoke_without_command=True)
    async def _Encryption(self, ctx: commands.Context):
        """Affiche toutes les commandes de chiffrement disponibles"""
        embed = discord.Embed(
            title="Commandes de chiffrement",
            description=f"Utilise `{ctx.prefix}encode <type>` pour encoder du texte, `{ctx.prefix}decode <type>` pour décoder.",
            color=0x000000,
        )

        embed.add_field(
            name="📝 Commandes d’encodage",
            value=f"""
`{ctx.prefix}encode base32` / `{ctx.prefix}encode b32` - Encoder en base32
`{ctx.prefix}encode base64` / `{ctx.prefix}encode b64` - Encoder en base64
`{ctx.prefix}encode rot13` / `{ctx.prefix}encode r13` - Encoder en rot13
`{ctx.prefix}encode hex` - Encoder en hex
`{ctx.prefix}encode base85` / `{ctx.prefix}encode b85` - Encoder en base85
`{ctx.prefix}encode ascii85` / `{ctx.prefix}encode a85` - Encoder en ASCII85
""",
            inline=False,
        )

        embed.add_field(
            name="📄 Commandes de décodage",
            value=f"""
`{ctx.prefix}decode base32` / `{ctx.prefix}decode b32` - Décoder depuis base32
`{ctx.prefix}decode base64` / `{ctx.prefix}decode b64` - Décoder depuis base64
`{ctx.prefix}decode rot13` / `{ctx.prefix}decode r13` - Décoder depuis rot13
`{ctx.prefix}decode hex` - Décoder depuis hex
`{ctx.prefix}decode base85` / `{ctx.prefix}decode b85` - Décoder depuis base85
`{ctx.prefix}decode ascii85` / `{ctx.prefix}decode a85` - Décoder depuis ASCII85
""",
            inline=False,
        )

        embed.add_field(
            name="🔐 Utilitaire",
            value=f"`{ctx.prefix}password` - Génère un mot de passe sécurisé aléatoire (envoyé en DM)",
            inline=False,
        )

        embed.set_footer(
            text="Utilise les commandes encode/decode pour chiffrer ou déchiffrer ton texte"
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(_encrypt(bot))
