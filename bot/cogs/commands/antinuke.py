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
from utils.emoji import CROSS, EMOTE, TICK, ZSAFE, ZSETTINGS
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, Container, Button, ActionRow
import aiosqlite
import asyncio
from utils.Tools import *
from utils.cv2 import CV2, build_container
from utils.config import *


class Antinuke(commands.Cog):

    module_key = "antinuke"

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize_db())

    async def initialize_db(self):
        self.db = await aiosqlite.connect("db/anti.db")
        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS antinuke (
            guild_id INTEGER PRIMARY KEY,
            status BOOLEAN
        )
    """)
        await self.db.commit()

    async def enable_limit_settings(self, guild_id):
        default_limits = DEFAULT_LIMITS
        for action, limit in default_limits.items():
            await self.db.execute(
                "INSERT OR REPLACE INTO limit_settings (guild_id, action_type, action_limit, time_window) VALUES (?, ?, ?, ?)",
                (guild_id, action, limit, TIME_WINDOW),
            )
            await self.db.commit()

    async def disable_limit_settings(self, guild_id):
        await self.db.execute(
            "DELETE FROM limit_settings WHERE guild_id = ?", (guild_id,)
        )
        await self.db.commit()

    @commands.hybrid_command(
        name="antinuke",
        aliases=["antiwizz", "anti"],
        help="Active/Désactive le module Anti-Nuke sur le serveur",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx, option: str = None):
        guild_id = ctx.guild.id
        pre = ctx.prefix

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?", (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id),
        ) as cursor:
            check = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            view = CV2(
                f"{CROSS} Accès refusé",
                "Seul le propriétaire du serveur ou un Extra Owner peut exécuter cette commande !",
            )
            return await ctx.send(view=view)

        is_activated = row[0] if row else False

        if option is None:
            view = CV2(
                f"{ZSAFE} Sécurité {BRAND_NAME}",
                "**Mode de défense Antinuke** — Protège ton serveur contre les actions admin nuisibles avec des protocoles de sécurité automatiques.",
                "**Core Functionalities**\n"
                "• Bannit automatiquement les activités admin malveillantes.\n"
                "• Protection par whitelist pour les utilisateurs de confiance.\n"
                "• Surveillance en direct des actions admin.\n"
                "• Détection et neutralisation rapides des menaces.",
                "**Configuration Panel**\n"
                f"{TICK} Activer la protection : `antinuke enable`\n"
                f"{CROSS} Désactiver la protection : `antinuke disable`",
            )
            await ctx.send(view=view)

        elif option.lower() == "enable":
            if is_activated:
                view = CV2(
                    f"Paramètres de sécurité pour {ctx.guild.name}",
                    f"Your server __**already has Antinuke enabled.**__\n\nCurrent Status: {TICK} Enabled\nTo Disable use `antinuke disable`",
                )
                await ctx.send(view=view)
            else:

                setup_view = CV2(
                    f"Antinuke Setup {EMOTE}", f"{TICK} | Initialisation rapide !"
                )
                setup_message = await ctx.send(view=setup_view)

                if not ctx.guild.me.guild_permissions.administrator:
                    view = CV2(
                        f"Antinuke Setup {EMOTE}",
                        f"{TICK} | Initialisation rapide !\n"
                        f"{CROSS} | **Oups ! Il semble que je n’ai pas la permission Administrateur pour activer l’antinuke**.",
                    )
                    await setup_message.edit(view=view)
                    return

                await asyncio.sleep(1)
                view = CV2(
                    f"Antinuke Setup {EMOTE}",
                    f"{TICK} | Initialisation rapide !\n"
                    f"{TICK} Vérification de la position du rôle {BRAND_NAME} pour une configuration optimale...",
                )
                await setup_message.edit(view=view)

                await asyncio.sleep(1)
                view = CV2(
                    f"Antinuke Setup {EMOTE}",
                    f"{TICK} | Initialisation rapide !\n"
                    f"{TICK} Vérification de la position du rôle {BRAND_NAME} pour une configuration optimale...\n"
                    f"{TICK} | Création et configuration du rôle {BRAND_NAME} Supreme...",
                )
                await setup_message.edit(view=view)

                try:
                    role = await ctx.guild.create_role(
                        name=f"{BRAND_NAME} Supreme™",
                        color=0xFF0000,
                        permissions=discord.Permissions(administrator=True),
                        hoist=False,
                        mentionable=False,
                        reason="Antinuke setup Role Creation",
                    )
                    await ctx.guild.me.add_roles(role)
                except discord.Forbidden:
                    view = CV2(
                        "Antinuke Setup",
                        f"{CROSS} | **Oups ! Je n’ai pas les permissions pour activer l’antinuke**.",
                    )
                    await setup_message.edit(view=view)
                    return
                except discord.HTTPException as e:
                    view = CV2(
                        "Antinuke Setup",
                        f"{CROSS} | **Uh: HTTPException: {e}\nCheck Guild Audit Logs**.",
                    )
                    await setup_message.edit(view=view)
                    return

                await asyncio.sleep(1)
                view = CV2(
                    f"Antinuke Setup {EMOTE}",
                    f"{TICK} | Initialisation rapide !\n"
                    f"{TICK} Vérification de la position du rôle {BRAND_NAME}...\n"
                    f"{TICK} | Création du rôle {BRAND_NAME} Supreme...\n"
                    f"{TICK} | Placement précis du rôle {BRAND_NAME} Supreme™...",
                )
                await setup_message.edit(view=view)

                try:
                    await ctx.guild.edit_role_positions(positions={role: 1})
                except discord.Forbidden:
                    view = CV2(
                        "Antinuke Setup",
                        f"{CROSS} | Oups ! Je n’ai pas les permissions suffisantes pour déplacer le rôle.",
                    )
                    await setup_message.edit(view=view)
                    return
                except discord.HTTPException as e:
                    view = CV2(
                        "Antinuke Setup",
                        f"{CROSS} | Échec de l’installation : HTTPException : {e}.",
                    )
                    await setup_message.edit(view=view)
                    return

                await asyncio.sleep(1)
                await asyncio.sleep(1)

                await self.db.execute(
                    "INSERT OR REPLACE INTO antinuke (guild_id, status) VALUES (?, ?)",
                    (guild_id, True),
                )
                await self.db.commit()

                await asyncio.sleep(1)
                await setup_message.delete()

                modules = (
                    f"{TICK} **Anti Ban**\n"
                    f"{TICK} **Anti Kick**\n"
                    f"{TICK} **Anti Bot**\n"
                    f"{TICK} **Anti Channel Create**\n"
                    f"{TICK} **Anti Channel Delete**\n"
                    f"{TICK} **Anti Channel Update**\n"
                    f"{TICK} **Anti Everyone/Here**\n"
                    f"{TICK} **Anti Role Create**\n"
                    f"{TICK} **Anti Role Delete**\n"
                    f"{TICK} **Anti Role Update**\n"
                    f"{TICK} **Anti Member Update**\n"
                    f"{TICK} **Anti Guild Update**\n"
                    f"{TICK} **Anti Integration**\n"
                    f"{TICK} **Anti Webhook Create**\n"
                    f"{TICK} **Anti Webhook Delete**\n"
                    f"{TICK} **Anti Webhook Update**\n"
                    f"{TICK} **Anti Prune**\n"
                    f"{TICK} **Auto Recovery**"
                )

                punishment_btn = Button(
                    label="Afficher le type de sanction",
                    style=discord.ButtonStyle.secondary,
                )
                punishment_btn.callback = self._show_punishment

                result_view = LayoutView(timeout=None)
                result_view.add_item(
                    build_container(
                        TextDisplay(
                            f"**{ZSETTINGS} Paramètres de sécurité pour {ctx.guild.name}**"
                        ),
                        Separator(visible=True),
                        TextDisplay(
                            "Astuce : pour un fonctionnement optimal, assure-toi que mon rôle a la permission **Administrateur** et est placé en **haut** de la liste des rôles."
                        ),
                        Separator(visible=True),
                        TextDisplay(f"**Modules Enabled**\n{modules}"),
                        Separator(visible=True),
                        TextDisplay(
                            f"Antinuke activé avec succès | Propulsé par {BRAND_NAME} Development™"
                        ),
                        ActionRow(punishment_btn),
                    )
                )

                await ctx.send(view=result_view)

        elif option.lower() == "disable":
            if not is_activated:
                view = CV2(
                    f"Paramètres de sécurité pour {ctx.guild.name}",
                    f"Uhh, looks like your server hasn't enabled Antinuke.\n\nCurrent Status: {CROSS} Disabled\n\nTo Enable use `antinuke enable`",
                )
            else:
                await self.db.execute(
                    "DELETE FROM antinuke WHERE guild_id = ?", (guild_id,)
                )
                await self.db.commit()
                view = CV2(
                    f"Paramètres de sécurité pour {ctx.guild.name}",
                    f"Antinuke désactivé avec succès pour ce serveur.\n\nStatut actuel : {CROSS} Désactivé\n\nPour activer : `antinuke enable`",
                )
            await ctx.send(view=view)
        else:
            view = CV2(
                f"{CROSS} Error", "Option invalide. Utilise `enable` ou `disable`."
            )
            await ctx.send(view=view)

    async def _show_punishment(self, interaction: discord.Interaction):
        view = CV2(
            "Types de sanctions pour les admins/modos non whitelistés",
            "**Anti Ban:** Ban\n"
            "**Anti Kick:** Ban\n"
            "**Anti Bot:** Ban the bot Inviter\n"
            "**Anti Channel Create/Delete/Update:** Ban\n"
            "**Anti Everyone/Here:** Remove the message & 1 hour timeout\n"
            "**Anti Role Create/Delete/Update:** Ban\n"
            "**Anti Member Update:** Ban\n"
            "**Anti Guild Update:** Ban\n"
            "**Anti Integration:** Ban\n"
            "**Anti Webhook Create/Delete/Update:** Ban\n"
            "**Anti Prune:** Ban\n"
            "**Auto Recovery:** Automatically recover damaged channels, roles, and settings",
            "Note : En cas de mise à jour de membres, une action est prise uniquement si le rôle contient des permissions dangereuses comme Bannir des membres, Administrateur, Gérer le serveur, Gérer les salons, Gérer les rôles, Gérer les webhooks ou Mentionner Everyone",
        )
        await interaction.response.send_message(view=view, ephemeral=True)
