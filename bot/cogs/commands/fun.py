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
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, MediaGallery
import random
import aiohttp
from discord import app_commands
from utils.Tools import blacklist_check, ignore_check
from utils.cv2 import CV2, build_container


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giphy_api_key = "y3KcqQTdiS0RYcpNJrWn8hFGglKqX4is"

    async def fetch_giphy(self, query):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.giphy.com/v1/gifs/search?api_key={self.giphy_api_key}&q={query}&limit=30&rating=pg"
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if data["data"]:
                    return random.choice(data["data"])["images"]["original"]["url"]
                else:
                    return None

    def random_emoji(self):
        return random.choice(["😂", "🤣", "😆", "😳", "🥴", "🙃", "😜"])

    async def action_command(self, ctx, user: discord.Member, action: str):
        gif_url = await self.fetch_giphy(action)
        if not gif_url:
            await ctx.send(
                view=CV2("😒 Erreur", "L’API GIPHY dort. Réessaie plus tard !")
            )
            return
        view = LayoutView(timeout=None)
        gallery = MediaGallery()
        gallery.add_item(media=gif_url)
        view.add_item(
            build_container(
                TextDisplay(
                    f"**{ctx.author.mention} {action}s {user.mention} {self.random_emoji()}**"
                ),
                gallery,
            )
        )
        await ctx.send(view=view)

    async def meter_command(self, ctx, title, user, text):
        await ctx.send(view=CV2(title, text))

    @commands.command(name="shipp")
    @blacklist_check()
    @ignore_check()
    async def shipp(self, ctx, user1: discord.Member, user2: discord.Member):
        percentage = random.randint(0, 100)
        await ctx.send(
            view=CV2(
                f"{self.random_emoji()} Résultat de compatibilité",
                f"**{user1.mention} x {user2.mention} = {percentage}% d’amour**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def hug(self, ctx, user: discord.Member):
        await self.action_command(ctx, user, "hug")

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def kiss(self, ctx, user: discord.Member):
        await self.action_command(ctx, user, "kiss")

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def pat(self, ctx, user: discord.Member):
        await self.action_command(ctx, user, "pat")

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def slap(self, ctx, user: discord.Member):
        await self.action_command(ctx, user, "slap")

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def tickle(self, ctx, user: discord.Member):
        await self.action_command(ctx, user, "tickle")

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def coinflip(self, ctx):
        result = random.choice(["Pile", "Face"])
        await ctx.send(view=CV2("🪙 Pile ou face", f"**Résultat : {result}**"))

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def dice(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(view=CV2("🎲 Lancer de dé", f"**Tu as obtenu {result} !**"))

    @commands.command(name="8ball")
    @blacklist_check()
    @ignore_check()
    async def eight_ball(self, ctx, *, question: str):
        responses = [
            "C’est certain.",
            "Sans aucun doute.",
            "Tu peux y compter.",
            "Redemande plus tard.",
            "Mieux vaut ne pas te le dire maintenant.",
            "N’y compte pas.",
            "Mes sources disent non.",
            "Très douteux.",
        ]
        await ctx.send(
            view=CV2(
                "🎱 Boule magique 8",
                f"**Q:** {question}\n**A:** {random.choice(responses)}",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def roast(self, ctx, user: discord.Member):
        roasts = [
            f"{user.mention} tu es la raison pour laquelle le shampoing a un mode d’emploi !",
            f"{user.mention} tu as quelque chose sur le menton... non, le troisième en partant du haut !",
            f"{user.mention} tes secrets sont en sécurité avec moi. Je n’écoute même jamais quand tu me les racontes.",
        ]
        await ctx.send(view=CV2("🔥 Moment de clash", random.choice(roasts)))

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def iq(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🧠 Test de QI",
                f"**{user.mention} a un QI de {random.randint(50, 200)} !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def dumb(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🤪 Test de bêtise",
                f"**{user.mention} est bête à {random.randint(0, 100)} % !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def simprate(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "😳 Taux de simp",
                f"**{user.mention} est simp à {random.randint(0, 100)} % !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def toxic(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "☠️ Compteur de toxicité",
                f"**{user.mention} est toxique à {random.randint(0, 100)} % !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def intelligence(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🧠 Compteur d’intelligence",
                f"**{user.mention} a {random.randint(0, 200)} points de QI !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def genius(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🤓 Taux de génie",
                f"**{user.mention} est génial à {random.randint(0, 100)} % !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def brainrate(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🧠 Puissance cérébrale",
                f"**{user.mention} utilise {random.randint(0, 100)} % de son cerveau !**",
            )
        )

    @commands.command()
    @blacklist_check()
    @ignore_check()
    async def howhot(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(
            view=CV2(
                "🔥 Compteur de beauté",
                f"**{user.mention} est beau à {random.randint(0, 100)} % !**",
            )
        )


async def setup(bot):
    await bot.add_cog(Fun(bot))
