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

from utils import getConfig
from utils.config import BotName, SUPPORT_SERVER
import discord
from utils.emoji import ARROWRED, CODEBASE, HEART3, INDEX, ZYROXLINKS
from discord.ui import LayoutView, TextDisplay, Separator, Container, ActionRow, Select
from discord.ext import commands
from utils.Tools import get_ignore_data
import aiosqlite


class MentionSelectView(LayoutView):
    def __init__(self, message, bot, prefix):
        super().__init__(timeout=300)
        self.message = message
        self.bot = bot
        self.prefix = prefix

        self.select = Select(
            placeholder=f"Commencer avec {BotName}",
            options=[
                discord.SelectOption(
                    label="Accueil",
                    emoji=INDEX,
                    description="Aller au menu principal",
                ),
                discord.SelectOption(
                    label="Infos développeur",
                    emoji=CODEBASE,
                    description="Voir qui m’a créé",
                ),
                discord.SelectOption(
                    label="Liens",
                    emoji=ZYROXLINKS,
                    description="Liens utiles du bot",
                ),
            ],
        )
        self.select.callback = self.on_select

        self.add_item(
            Container(
                TextDisplay(f"**{message.guild.name}**"),
                Separator(visible=True),
                TextDisplay(
                    f"> {HEART3} **Salut {message.author.mention}**\n"
                    f"> {ARROWRED} **Préfixe pour ce serveur : `{prefix}`**\n\n"
                    f"___Tapez `{prefix}help` pour plus d’informations.___"
                ),
                ActionRow(self.select),
            )
        )

    async def on_select(self, interaction: discord.Interaction):
        if interaction.user.id != self.message.author.id:
            await interaction.response.send_message(
                "Ce menu n’est pas pour vous !", ephemeral=True
            )
            return

        selected = interaction.data.get("values", ["Accueil"])[0]

        if selected == "Accueil":
            content = (
                f"> {HEART3} **Salut {interaction.user.mention}**\n"
                f"> {ARROWRED} **Préfixe pour ce serveur : `{self.prefix}`**\n\n"
                f"___Tapez `{self.prefix}help` pour plus d’informations.___"
            )
        elif selected == "Infos développeur":
            content = (
                "Il n’y a que 2 fondateurs qui m’ont créé. Merci à eux 💞.\n\n"
                "**Les fondateurs**\n"
                "**[01]. [Ray](https://discord.com/users/870179991462236170)**\n**[02]. [runxking](https://discord.com/users/767979794411028491)**"
            )
        elif selected == "Liens":
            content = (
                f"**[Inviter {BotName}](https://discord.com/oauth2/authorize?client_id={self.message.guild.me.id}&permissions=8&integration_type=0&scope=bot+applications.commands)**\n"
                f"**[Rejoindre le serveur support]({SUPPORT_SERVER})**"
            )

        new_container = Container(
            TextDisplay(f"**{self.message.guild.name}**"),
            Separator(visible=True),
            TextDisplay(content),
            ActionRow(self.select),
        )

        self.clear_items()
        self.add_item(new_container)

        await interaction.response.edit_message(view=self)


class Mention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xFF0000
        self.bot_name = BotName

    async def is_blacklisted(self, message):
        async with aiosqlite.connect("db/block.db") as db:
            cursor = await db.execute(
                "SELECT 1 FROM guild_blacklist WHERE guild_id = ?", (message.guild.id,)
            )
            if await cursor.fetchone():
                return True
            cursor = await db.execute(
                "SELECT 1 FROM user_blacklist WHERE user_id = ?", (message.author.id,)
            )
            if await cursor.fetchone():
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        if await self.is_blacklisted(message):
            return

        ignore_data = await get_ignore_data(message.guild.id)
        if (
            str(message.author.id) in ignore_data["user"]
            or str(message.channel.id) in ignore_data["channel"]
        ):
            return

        if (
            self.bot.user in message.mentions
            and len(message.content.strip().split()) == 1
        ):
            guild_id = message.guild.id
            data = await getConfig(guild_id)
            prefix = data["prefix"]

            view = MentionSelectView(message, self.bot, prefix)
            await message.channel.send(view=view)


def setup(bot):
    bot.add_cog(Mention(bot))
