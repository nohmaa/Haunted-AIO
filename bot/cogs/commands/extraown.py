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
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, Container, ActionRow, Button
import aiosqlite
from utils.Tools import *
from utils.cv2 import CV2, build_container
from utils.config import OWNER_IDS_STR


class ConfirmView(LayoutView):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

        self.yes_btn = Button(label="Confirmer", style=discord.ButtonStyle.green)
        self.no_btn = Button(label="Annuler", style=discord.ButtonStyle.red)

        self.yes_btn.callback = self.confirm_callback
        self.no_btn.callback = self.cancel_callback

        container = build_container(
            TextDisplay("**Confirmer Action**"),
            Separator(visible=True),
            TextDisplay(self._desc),
            ActionRow(self.yes_btn, self.no_btn),
        )
        self.add_item(container)

    @property
    def _desc(self):
        return ""

    async def confirm_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "Tu ne peux pas interagir avec cette confirmation.", ephemeral=True
            )
        self.value = True
        await interaction.response.defer()
        self.stop()

    async def cancel_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "Tu ne peux pas interagir avec cette confirmation.", ephemeral=True
            )
        self.value = False
        await interaction.response.defer()
        self.stop()


class SetConfirmView(ConfirmView):
    def __init__(self, ctx, user):
        self._user = user
        super().__init__(ctx)

    @property
    def _desc(self):
        return (
            f"**Are you sure you want to set {self._user.mention} as the Extra Owner?**"
        )


class ResetConfirmView(ConfirmView):
    @property
    def _desc(self):
        return "**Es-tu sûr de vouloir réinitialiser l’Extra Owner ?**"


class Extraowner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize_db())

    async def initialize_db(self):
        self.db = await aiosqlite.connect("db/anti.db")
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS extraowners (
                guild_id INTEGER PRIMARY KEY,
                owner_id INTEGER
            )
        """)
        await self.db.commit()

    @commands.hybrid_command(
        name="extraowner", aliases=["owner"], help="Ajoute un Extra Owner au serveur"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def extraowner(self, ctx, option: str = None, user: discord.Member = None):
        guild_id = ctx.guild.id

        if ctx.guild.member_count < 2:
            return await ctx.send(
                view=CV2(
                    f"{CROSS} Error",
                    "Votre serveur ne remplit pas mon critère de 30 membres",
                )
            )

        Ray = OWNER_IDS_STR
        if ctx.author.id != ctx.guild.owner_id and str(ctx.author.id) not in Ray:
            return await ctx.send(
                view=CV2(
                    f"{ZWARNING} Accès refusé",
                    "Seul le propriétaire du serveur peut exécuter cette commande",
                )
            )

        if option is None:
            pre = ctx.prefix
            info_text = (
                "Extraowners can adjust server antinuke settings & manage whitelist events, "
                "so careful consideration is essential before assigning it to someone.\n\n"
                f"**Extraowner Set** — `{pre}extraowner set @user`\n"
                f"**Extraowner Reset** — `{pre}extraowner reset`\n"
                f"**Extraowner View** — `{pre}extraowner view`"
            )
            return await ctx.reply(view=CV2("__Extra Owner__", info_text))

        if option.lower() == "set":
            if user is None or user.bot:
                return await ctx.reply(
                    view=CV2(
                        f"{CROSS} Error",
                        "Merci de fournir une mention ou un ID d’utilisateur valide pour définir l’Extra Owner !",
                    )
                )

            view = SetConfirmView(ctx, user)
            message = await ctx.reply(view=view)
            await view.wait()

            if view.value is None:
                await message.edit(
                    view=CV2("⏰ Timed Out", "Confirmeration timed out.")
                )
            elif view.value:
                await self.db.execute(
                    "INSERT OR REPLACE INTO extraowners (guild_id, owner_id) VALUES (?, ?)",
                    (guild_id, user.id),
                )
                await self.db.commit()
                await message.edit(
                    view=CV2(f"{TICK} Succès", f"Added {user.mention} As Extraowner")
                )
            else:
                await message.edit(view=CV2(f"{CROSS} Annulerled", "Action annulée."))

        elif option.lower() == "reset":
            async with self.db.execute(
                "SELECT owner_id FROM extraowners WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Error",
                        "Aucun extra owner n’a été désigné pour ce serveur.",
                    )
                )
            else:
                view = ResetConfirmView(ctx)
                message = await ctx.reply(view=view)
                await view.wait()

                if view.value is None:
                    await message.edit(
                        view=CV2("⏰ Timed Out", "Confirmeration timed out.")
                    )
                elif view.value:
                    await self.db.execute(
                        "DELETE FROM extraowners WHERE guild_id = ?", (guild_id,)
                    )
                    await self.db.commit()
                    await message.edit(
                        view=CV2(
                            f"{TICK} Succès", "Configuration Extra Owner désactivée !"
                        )
                    )
                else:
                    await message.edit(
                        view=CV2(f"{CROSS} Annulerled", "Action annulée.")
                    )

        elif option.lower() == "view":
            async with self.db.execute(
                "SELECT owner_id FROM extraowners WHERE guild_id = ?", (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                await ctx.reply(
                    view=CV2(
                        f"{CROSS} Error",
                        "Aucun extra owner n’est actuellement assigné.",
                    )
                )
            else:
                await ctx.reply(
                    view=CV2("Extra Owner", f"Current Extraowner is <@{row[0]}>")
                )
