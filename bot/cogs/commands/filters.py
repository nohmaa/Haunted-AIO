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
from typing import Union
import wavelink
from utils.Tools import *


class FilterCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_filters = {}

    async def apply_filter(self, ctx: commands.Context, filter_name: str):
        player: Union[wavelink.Player, None] = ctx.voice_client
        if not player or not player.playing:
            await ctx.send("Je ne joue rien actuellement.")
            return

        if ctx.author.voice is None or ctx.author.voice.channel != player.channel:
            await ctx.send("Tu dois être dans le même salon vocal que moi.")
            return

        filters = wavelink.Filters()

        if filter_name == "nightcore":
            filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
        elif filter_name == "bassboost":
            filters.equalizer.set(
                bands=[
                    {"band": 0, "gain": 0.5},
                    {"band": 1, "gain": 0.5},
                    {"band": 2, "gain": 0.5},
                ]
            )
        elif filter_name == "vaporwave":
            filters.timescale.set(rate=0.85, pitch=0.85)
        elif filter_name == "karaoke":
            filters.karaoke.set(
                level=1.0, mono_level=1.0, filter_band=220.0, filter_width=100.0
            )
        elif filter_name == "tremolo":
            filters.tremolo.set(depth=0.5, frequency=14.0)
        elif filter_name == "vibrato":
            filters.vibrato.set(depth=0.5, frequency=14.0)
        elif filter_name == "rotation":
            filters.rotation.set(rotation_hz=5.0)
        elif filter_name == "distortion":
            filters.distortion.set(
                sin_offset=0.0,
                sin_scale=1.0,
                cos_offset=0.0,
                cos_scale=1.0,
                tan_offset=0.0,
                tan_scale=1.0,
                offset=0.0,
                scale=1.0,
            )
        elif filter_name == "channelmix":
            filters.channel_mix.set(
                left_to_left=0.5,
                left_to_right=0.5,
                right_to_left=0.5,
                right_to_right=0.5,
            )

        await player.set_filters(filters)
        self.active_filters[ctx.guild.id] = filter_name
        await ctx.send(
            embed=discord.Embed(
                description=f"Filtre défini sur **{filter_name}**.",
                color=discord.Color.green(),
            )
        )

    @commands.hybrid_group(invoke_without_command=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def filter(self, ctx: commands.Context):
        await ctx.send(
            "Utilise `filter enable` pour activer un filtre ou `filter disable` pour désactiver le filtre actuel."
        )

    @filter.command(help="Activer un filtre.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def enable(self, ctx: commands.Context):
        player: Union[wavelink.Player, None] = ctx.voice_client
        if not player or not player.playing:
            await ctx.send("Je ne suis pas connecté à un salon vocal.")
            return

        if ctx.author.voice is None or ctx.author.voice.channel != player.channel:
            await ctx.send("Tu dois être dans le même salon vocal que moi.")
            return

        filter_options = [
            discord.SelectOption(
                label="Vaporwave", description="Appliquer l’effet vaporwave"
            ),
            discord.SelectOption(
                label="Nightcore", description="Appliquer l’effet nightcore"
            ),
            discord.SelectOption(
                label="Vibrato", description="Appliquer l’effet vibrato"
            ),
            discord.SelectOption(
                label="Tremolo", description="Appliquer l’effet tremolo"
            ),
            discord.SelectOption(
                label="Bassboost", description="Appliquer l’effet bass boost"
            ),
            discord.SelectOption(
                label="Karaoke", description="Appliquer l’effet karaoké"
            ),
            discord.SelectOption(
                label="Rotation", description="Appliquer l’effet rotation"
            ),
            discord.SelectOption(
                label="Distortion", description="Appliquer l’effet distorsion"
            ),
            discord.SelectOption(
                label="Channelmix", description="Appliquer l’effet channel mix"
            ),
        ]

        class FilterSelect(discord.ui.View):
            @discord.ui.select(
                placeholder="Choisis un filtre...", options=filter_options
            )
            async def select_filter(
                self, interaction: discord.Interaction, select: discord.ui.Select
            ):
                await interaction.response.defer()
                selected_filter = select.values[0].lower()
                await self.cog.apply_filter(ctx, selected_filter)
                # await interaction.message.delete()
                self.disable_all()

            @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
            async def cancel(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                await interaction.message.delete()
                self.disable_all()

            def disable_all(self):
                for child in self.children:
                    child.disabled = True
                self.stop()

        view = FilterSelect()
        view.cog = self

        current_filter = self.active_filters.get(ctx.guild.id, "None")
        embed = discord.Embed(
            title="Activer le filtre",
            description="Choisis un filtre à appliquer :",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Filtre actuel", value=current_filter, inline=False)
        await ctx.send(embed=embed, view=view)

    @filter.command(help="Désactiver le filtre actuel.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def disable(self, ctx: commands.Context):
        player: Union[wavelink.Player, None] = ctx.voice_client
        if not player or not player.playing:
            await ctx.send("Je ne suis pas connecté à un salon vocal.")
            return

        if ctx.author.voice is None or ctx.author.voice.channel != player.channel:
            await ctx.send("Tu dois être dans le même salon vocal que moi.")
            return

        filters = wavelink.Filters()
        await player.set_filters(filters)
        self.active_filters.pop(ctx.guild.id, None)
        await ctx.send(
            embed=discord.Embed(
                description="Filtre désactivé.", color=discord.Color.red()
            )
        )
