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

from __future__ import annotations

from typing import Optional
import random

import discord
from utils.emoji import WARNING_ALT
from discord.ext import commands

from ..rps import RockPaperScissors
from ..utils import DiscordColor, DEFAULT_COLOR, BaseView


class RPSButton(discord.ui.Button["RPSView"]):
    def __init__(self, emoji: str, *, style: discord.ButtonStyle) -> None:
        super().__init__(
            label="\u200b",
            emoji=emoji,
            style=style,
        )

    def get_choice(self, user: discord.User, other: bool = False) -> Optional[str]:
        game = self.view.game
        if other:
            return game.player2_choice if user == game.player2 else game.player1_choice
        else:
            return game.player1_choice if user == game.player1 else game.player2_choice

    async def callback(self, interaction: discord.Interaction) -> None:
        game = self.view.game
        players = (game.player1, game.player2) if game.player2 else (game.player1,)

        if interaction.user not in players:
            return await interaction.response.send_message(
                "Ce n’est pas ta partie !", ephemeral=True
            )
        else:
            if not game.player2:
                bot_choice = random.choice(game.OPTIONS)
                user_choice = self.emoji.name

                if user_choice == bot_choice:
                    game.embed.description = (
                        f"**Égalité !**\nOn a tous les deux choisi {user_choice}"
                    )
                else:
                    if game.check_win(bot_choice, user_choice):
                        game.embed.description = f"**Tu as gagné !**\nTu as choisi {user_choice} et j’ai choisi {bot_choice}."
                    else:
                        game.embed.description = f"**Tu as perdu !**\nJ’ai choisi {bot_choice} et tu as choisi {user_choice}."

                self.view.disable_all()
                self.view.stop()

            else:
                if self.get_choice(interaction.user):
                    return await interaction.response.send_message(
                        "Tu as déjà choisi !", ephemeral=True
                    )

                other_player_choice = self.get_choice(interaction.user, other=True)

                if interaction.user == game.player1:
                    game.player1_choice = self.emoji.name

                    if not other_player_choice:
                        game.embed.description += f"\n\n{game.player1.mention} a choisi...\n*En attente du choix de {game.player2.mention}...*"
                else:
                    game.player2_choice = self.emoji.name

                    if not other_player_choice:
                        game.embed.description += f"\n\n{game.player2.mention} a choisi...\n*En attente du choix de {game.player1.mention}...*"

                if game.player1_choice and game.player2_choice:
                    if game.player1_choice == game.player2_choice:
                        game.embed.description = f"**Égalité !**\n{game.player1.mention} et {game.player2.mention} ont tous les deux choisi {game.player1_choice}."
                    else:
                        who_won = (
                            game.player1
                            if game.check_win(game.player2_choice, game.player1_choice)
                            else game.player2
                        )

                        game.embed.description = (
                            f"**{who_won.mention} a gagné !**"
                            f"\n\n{game.player1.mention} a choisi {game.player1_choice}."
                            f"\n{game.player2.mention} a choisi {game.player2_choice}."
                        )

                    self.view.disable_all()
                    self.view.stop()

            return await interaction.response.edit_message(
                embed=game.embed, view=self.view
            )


class RPSView(BaseView):
    game: BetaRockPaperScissors

    def __init__(
        self,
        game: BetaRockPaperScissors,
        *,
        button_style: discord.ButtonStyle,
        timeout: float,
    ) -> None:

        super().__init__(timeout=timeout)

        self.button_style = button_style
        self.game = game

        for option in self.game.OPTIONS:
            self.add_item(RPSButton(option, style=self.button_style))


class BetaRockPaperScissors(RockPaperScissors):
    """
    RockPaperScissors(buttons) game
    """

    player1: discord.User
    embed: discord.Embed

    def __init__(self, other_player: Optional[discord.User] = None) -> None:
        self.player2 = other_player

        if self.player2:
            self.player1_choice: Optional[str] = None
            self.player2_choice: Optional[str] = None

    async def start(
        self,
        ctx: commands.Context[commands.Bot],
        *,
        button_style: discord.ButtonStyle = discord.ButtonStyle.blurple,
        embed_color: DiscordColor = DEFAULT_COLOR,
        timeout: Optional[float] = None,
    ) -> discord.Message:
        if ctx.author == self.player2:
            embed = discord.Embed(
                title=f"{WARNING_ALT}   Accès refusé",
                description="Tu ne peux pas jouer contre toi-même !",
                color=0x000000,
            )
            return await ctx.reply(embed=embed)

        """
        Starts the Rock Paper Scissors (buttons) game.

        Parameters
        ----------
        ctx : commands.Context
            The context of the invoking command.
        button_style : discord.ButtonStyle, optional
            The primary button style to use, by default discord.ButtonStyle.blurple.
        embed_color : DiscordColor, optional
            The color of the game embed, by default DEFAULT_COLOR.
        timeout : Optional[float], optional
            The timeout for the view, by default None.

        Returns
        -------
        discord.Message
            Returns the game message.
        """
        self.player1 = ctx.author

        self.embed = discord.Embed(
            title="Pierre Feuille Ciseaux",
            description="Choisis un bouton pour jouer !",
            color=discord.Color.random(),
        )

        self.view = RPSView(self, button_style=button_style, timeout=timeout)
        self.message = await ctx.send(embed=self.embed, view=self.view)

        await self.view.wait()
        return self.message
