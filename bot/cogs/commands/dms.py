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
from discord.ui import LayoutView, TextDisplay, Separator, Container, Button, ActionRow
from discord.ext import commands
from utils.cv2 import CV2, build_container
from utils.config import STAFF_IDS


class SuccessView(LayoutView):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member

        self.add_item(
            build_container(
                TextDisplay("**Message envoyé**"),
                Separator(visible=True),
                TextDisplay(
                    f"✅ Your message has been successfully sent to **{member.name}**"
                ),
            )
        )


class ErrorView(LayoutView):
    def __init__(self, member):
        super().__init__(timeout=None)
        self.member = member

        self.add_item(
            build_container(
                TextDisplay("**Échec de l’envoi**"),
                Separator(visible=True),
                TextDisplay(
                    f"❌ Could not send the message. **{member.name}** may have their DMs disabled."
                ),
            )
        )


class GenericErrorView(LayoutView):
    def __init__(self, error):
        super().__init__(timeout=None)
        self.error = error

        self.add_item(
            build_container(
                TextDisplay("**Erreur survenue**"),
                Separator(visible=True),
                TextDisplay(f"🤔 Quelque chose a mal tourné. Erreur : {error}"),
            )
        )


class PermissionErrorView(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            build_container(
                TextDisplay("**Permission refusée**"),
                Separator(visible=True),
                TextDisplay("❌ Tu n’as pas la permission d’utiliser cette commande."),
            )
        )


class StaffDMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dmstaff")
    async def dm_staff(self, ctx, member: discord.Member, *, message: str):
        if ctx.author.id not in STAFF_IDS:
            view = PermissionErrorView()
            await ctx.reply(view=view)
            return

        try:
            embed = discord.Embed(
                title="📢 Un message de l’équipe du staff",
                description=message,
                color=0xFF0000,
            )
            embed.set_footer(text=f"Ce message a été envoyé par {ctx.author.name}.")

            await member.send(embed=embed)

            view = SuccessView(member)
            await ctx.reply(view=view)

        except discord.Forbidden:
            view = ErrorView(member)
            await ctx.reply(view=view)
        except Exception as e:
            view = GenericErrorView(str(e))
            await ctx.reply(view=view)
            print(f"Error in dmstaff command: {e}")


async def setup(bot):
    await bot.add_cog(StaffDMCog(bot))
