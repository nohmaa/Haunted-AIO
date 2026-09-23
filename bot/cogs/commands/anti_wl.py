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
from utils.emoji import ARROWRED, CROSS, DISABLE, ENABLE, MANAGER, TICK
from discord.ext import commands
from discord.ui import LayoutView, TextDisplay, Separator, Container
import aiosqlite
from utils.Tools import *
from utils.cv2 import CV2, build_container


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize_db())

    # @commands.Cog.listener()
    async def initialize_db(self):
        self.db = await aiosqlite.connect("db/anti.db")
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS whitelisted_users (
                guild_id INTEGER,
                user_id INTEGER,
                ban BOOLEAN DEFAULT FALSE,
                kick BOOLEAN DEFAULT FALSE,
                prune BOOLEAN DEFAULT FALSE,
                botadd BOOLEAN DEFAULT FALSE,
                serverup BOOLEAN DEFAULT FALSE,
                memup BOOLEAN DEFAULT FALSE,
                chcr BOOLEAN DEFAULT FALSE,
                chdl BOOLEAN DEFAULT FALSE,
                chup BOOLEAN DEFAULT FALSE,
                rlcr BOOLEAN DEFAULT FALSE,
                rlup BOOLEAN DEFAULT FALSE,
                rldl BOOLEAN DEFAULT FALSE,
                meneve BOOLEAN DEFAULT FALSE,
                mngweb BOOLEAN DEFAULT FALSE,
                mngstemo BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (guild_id, user_id)
            )
        """)
        await self.db.commit()

    @commands.hybrid_command(
        name="whitelist",
        aliases=["wl"],
        help="Whiteliste un utilisateur de l’antinuke pour une action précise.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, member: discord.Member = None):
        if ctx.guild.member_count < 2:
            view = CV2(
                f"{CROSS} Error",
                "Votre serveur ne remplit pas mon critère de 30 membres",
            )
            return await ctx.send(view=view)

        prefix = ctx.prefix

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id),
        ) as cursor:
            check = await cursor.fetchone()

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            antinuke = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            view = CV2(
                f"{CROSS} Accès refusé",
                "Seul le propriétaire du serveur ou un Extra Owner peut exécuter cette commande !",
            )
            return await ctx.send(view=view)

        if not antinuke or not antinuke[0]:
            view = CV2(
                f"{ctx.guild.name} Security Settings {MANAGER}",
                f"Ohh Non! looks like your server doesn't enabled Antinuke\n\nCurrent Status : {CROSS}\n\nTo enable use `{prefix}antinuke enable`",
            )
            return await ctx.send(view=view)

        if not member:
            view = CV2(
                "__Commandes Whitelist__",
                "**Ajouter un utilisateur à la whitelist signifie qu’aucune action ne sera prise contre lui s’il déclenche le module Anti-Nuke.**",
                f"**Usage**\n{ARROWRED} `{prefix}whitelist @user/id`\n{ARROWRED} `{prefix}wl @user`",
            )
            return await ctx.send(view=view)

        async with self.db.execute(
            "SELECT * FROM whitelisted_users WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id),
        ) as cursor:
            data = await cursor.fetchone()

        if data:
            view = CV2(
                f"{CROSS} Error",
                f"<@{member.id}> est déjà un membre whitelisté, **unwhiteliste** l’utilisateur puis réessaie.",
            )
            return await ctx.send(view=view)

        await self.db.execute(
            "INSERT INTO whitelisted_users (guild_id, user_id) VALUES (?, ?)",
            (ctx.guild.id, member.id),
        )
        await self.db.commit()

        options = [
            discord.SelectOption(
                label="Bannissement",
                description="Whitelister un membre pour le bannissement",
                value="ban",
            ),
            discord.SelectOption(
                label="Expulsion",
                description="Whitelister un membre pour l’expulsion",
                value="kick",
            ),
            discord.SelectOption(
                label="Prune",
                description="Whitelister un membre pour le prune",
                value="prune",
            ),
            discord.SelectOption(
                label="Ajout de bots",
                description="Whitelister un membre pour l’ajout de bots",
                value="botadd",
            ),
            discord.SelectOption(
                label="Modif. serveur",
                description="Whitelister un membre pour la modification du serveur",
                value="serverup",
            ),
            discord.SelectOption(
                label="Modif. membres",
                description="Whitelister un membre pour la modification des membres",
                value="memup",
            ),
            discord.SelectOption(
                label="Création salon",
                description="Whitelister un membre pour la création de salons",
                value="chcr",
            ),
            discord.SelectOption(
                label="Suppression salon",
                description="Whitelister un membre pour la suppression de salons",
                value="chdl",
            ),
            discord.SelectOption(
                label="Modif. salon",
                description="Whitelister un membre pour la modification de salons",
                value="chup",
            ),
            discord.SelectOption(
                label="Création rôle",
                description="Whitelister un membre pour la création de rôles",
                value="rlcr",
            ),
            discord.SelectOption(
                label="Modif. rôle",
                description="Whitelister un membre pour la modification de rôles",
                value="rlup",
            ),
            discord.SelectOption(
                label="Suppression rôle",
                description="Whitelister un membre pour la suppression de rôles",
                value="rldl",
            ),
            discord.SelectOption(
                label="Mention everyone",
                description="Whitelister un membre pour la mention everyone",
                value="meneve",
            ),
            discord.SelectOption(
                label="Gestion webhooks",
                description="Whitelister un membre pour la gestion des webhooks",
                value="mngweb",
            ),
        ]

        select = discord.ui.Select(
            placeholder="Choisis tes options",
            min_values=1,
            max_values=len(options),
            options=options,
            custom_id="wl",
        )
        button = discord.ui.Button(
            label="Ajouter cet utilisateur à toutes les catégories",
            style=discord.ButtonStyle.primary,
            custom_id="catWl",
        )

        action_view = discord.ui.View()
        action_view.add_item(select)
        action_view.add_item(button)

        disabled_list = (
            f"{DISABLE} : **Ban**\n"
            f"{DISABLE} : **Kick**\n"
            f"{DISABLE} : **Prune**\n"
            f"{DISABLE} : **Bot Add**\n"
            f"{DISABLE} : **Server Update**\n"
            f"{DISABLE} : **Member Update**\n"
            f"{DISABLE} : **Channel Create**\n"
            f"{DISABLE} : **Channel Delete**\n"
            f"{DISABLE} : **Channel Update**\n"
            f"{DISABLE} : **Role Create**\n"
            f"{DISABLE} : **Role Delete**\n"
            f"{DISABLE} : **Role Update**\n"
            f"{DISABLE} : **Mention** @everyone\n"
            f"{DISABLE} : **Webhook Management**"
        )

        wl_view = CV2(
            ctx.guild.name,
            disabled_list,
            f"**Executor:** <@!{ctx.author.id}> │ **Target:** <@!{member.id}>",
        )

        msg = await ctx.send(view=action_view)

        def check(interaction):
            return (
                interaction.user.id == ctx.author.id
                and interaction.message.id == msg.id
            )

        try:
            interaction = await self.bot.wait_for(
                "interaction", check=check, timeout=60.0
            )
            if interaction.data["custom_id"] == "catWl":

                await self.db.execute(
                    "UPDATE whitelisted_users SET ban = ?, kick = ?, prune = ?, botadd = ?, serverup = ?, memup = ?, chcr = ?, chdl = ?, chup = ?, rlcr = ?, rldl = ?, rlup = ?, meneve = ?, mngweb = ?, mngstemo = ? WHERE guild_id = ? AND user_id = ?",
                    (
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        ctx.guild.id,
                        member.id,
                    ),
                )
                await self.db.commit()

                enabled_list = (
                    f"{ENABLE} : **Ban**\n"
                    f"{ENABLE} : **Kick**\n"
                    f"{ENABLE} : **Prune**\n"
                    f"{ENABLE} : **Bot Add**\n"
                    f"{ENABLE} : **Server Update**\n"
                    f"{ENABLE} : **Member Update**\n"
                    f"{ENABLE} : **Channel Create**\n"
                    f"{ENABLE} : **Channel Delete**\n"
                    f"{ENABLE} : **Channel Update**\n"
                    f"{ENABLE} : **Role Create**\n"
                    f"{ENABLE} : **Role Delete**\n"
                    f"{ENABLE} : **Role Update**\n"
                    f"{ENABLE} : **Mention** @everyone\n"
                    f"{ENABLE} : **Webhook Management**"
                )

                result = CV2(
                    ctx.guild.name,
                    enabled_list,
                    f"**Executor:** <@!{ctx.author.id}> │ **Target:** <@!{member.id}>",
                )
                await interaction.response.edit_message(view=result)
            else:

                fields = {
                    "ban": "Ban",
                    "kick": "Kick",
                    "prune": "Prune",
                    "botadd": "Bot Add",
                    "serverup": "Server Update",
                    "memup": "Member Update",
                    "chcr": "Channel Create",
                    "chdl": "Channel Delete",
                    "chup": "Channel Update",
                    "rlcr": "Role Create",
                    "rldl": "Role Delete",
                    "rlup": "Role Update",
                    "meneve": "Mention Everyone",
                    "mngweb": "Manage Webhooks",
                }

                status_lines = []
                selected_values = interaction.data["values"]
                for key, name in fields.items():
                    if key in selected_values:
                        status_lines.append(f"{ENABLE} : **{name}**")
                    else:
                        status_lines.append(f"{DISABLE} : **{name}**")

                for value in selected_values:
                    await self.db.execute(
                        f"UPDATE whitelisted_users SET {value} = ? WHERE guild_id = ? AND user_id = ?",
                        (True, ctx.guild.id, member.id),
                    )

                await self.db.commit()

                result = CV2(
                    ctx.guild.name,
                    "\n".join(status_lines),
                    f"**Executor:** <@!{ctx.author.id}> │ **Target:** <@!{member.id}>",
                )
                await interaction.response.edit_message(view=result)
        except TimeoutError:
            await msg.edit(view=None)

    @commands.hybrid_command(
        name="whitelisted",
        aliases=["wlist"],
        help="Affiche la liste des utilisateurs whitelistés.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelisted(self, ctx):
        if ctx.guild.member_count < 2:
            view = CV2(
                f"{CROSS} Error",
                "Votre serveur ne remplit pas mon critère de 30 membres",
            )
            return await ctx.send(view=view)

        pre = ctx.prefix

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id),
        ) as cursor:
            check = await cursor.fetchone()

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            antinuke = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            view = CV2(
                f"{CROSS} Accès refusé",
                "Seul le propriétaire du serveur ou un Extra Owner peut exécuter cette commande !",
            )
            return await ctx.send(view=view)

        if not antinuke or not antinuke[0]:
            view = CV2(
                f"{ctx.guild.name} Security Settings {MANAGER}",
                f"Ohh NO! looks like your server doesn't enabled security\n\nCurrent Status : {CROSS}\n\nTo enable use `{pre}antinuke enable`",
            )
            return await ctx.send(view=view)

        async with self.db.execute(
            "SELECT user_id FROM whitelisted_users WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            data = await cursor.fetchall()

        if not data:
            view = CV2(f"{CROSS} Error", "Aucun utilisateur whitelisté trouvé.")
            return await ctx.send(view=view)

        whitelisted_users = [self.bot.get_user(user_id[0]) for user_id in data]
        whitelisted_users_str = ", ".join(
            f"<@!{user.id}>" for user in whitelisted_users if user
        )

        view = CV2(
            f"__Utilisateurs whitelistés pour {ctx.guild.name}__", whitelisted_users_str
        )
        await ctx.send(view=view)

    @commands.hybrid_command(
        name="whitelistreset",
        aliases=["wlreset"],
        help="Réinitialise les utilisateurs whitelistés.",
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelistreset(self, ctx):
        if ctx.guild.member_count < 2:
            view = CV2(
                f"{CROSS} Error",
                "Votre serveur ne remplit pas mon critère de 30 membres",
            )
            return await ctx.send(view=view)

        pre = ctx.prefix

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id),
        ) as cursor:
            check = await cursor.fetchone()

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            antinuke = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            view = CV2(
                f"{CROSS} Accès refusé",
                "Seul le propriétaire du serveur ou un Extra Owner peut exécuter cette commande !",
            )
            return await ctx.send(view=view)

        if not antinuke or not antinuke[0]:
            view = CV2(
                f"{ctx.guild.name} Security Settings {MANAGER}",
                f"Ohh NO! looks like your server doesn't enabled security\n\nCurrent Status : {CROSS}\n\nTo enable use `{pre}antinuke enable`",
            )
            return await ctx.send(view=view)

        async with self.db.execute(
            "SELECT user_id FROM whitelisted_users WHERE guild_id = ?", (ctx.guild.id,)
        ) as cursor:
            data = await cursor.fetchall()

        if not data:
            view = CV2(f"{CROSS} Error", "Aucun utilisateur whitelisté trouvé.")
            return await ctx.send(view=view)

        await self.db.execute(
            "DELETE FROM whitelisted_users WHERE guild_id = ?", (ctx.guild.id,)
        )
        await self.db.commit()
        view = CV2(
            f"{TICK} Succès",
            f"Tous les membres whitelistés ont été retirés de {ctx.guild.name}",
        )
        await ctx.send(view=view)
