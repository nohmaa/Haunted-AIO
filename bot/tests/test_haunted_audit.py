"""Tests de non-regression pour les points audites du bot Haunted.

Lancement (aucune dependance supplementaire, unittest est dans la stdlib) :

    cd bot && python -m unittest discover -s tests -v

Ce que ces tests couvrent :
1. `_text_of` : la reconstruction en texte brut utilisee par le repli
   anti-50006 (« Cannot send an empty message ») de `core.Context`.
2. `_lavalink_uri` : normalisation des .env Lavalink imprecis et refus des
   noeuds non configures (cause des `InvalidNodeException` en production).
3. Unicite des routes FastAPI : deux handlers identiques se masquent en
   silence (le second devient inatteignable).
4. Coherence dashboard -> bot : chaque appel de `dashboard/lib/api.ts` doit
   correspondre a une route reellement exposee.
5. Contrat de la route admin `/stats` : les champs existent et l'etat des
   noeuds est derive de mesures, jamais code en dur.
"""

import asyncio
import io
import os
import pathlib
import sys
import types
import unittest
from collections import defaultdict

BOT_DIR = pathlib.Path(__file__).resolve().parent.parent
REPO_DIR = BOT_DIR.parent

if str(BOT_DIR) not in sys.path:
    sys.path.insert(0, str(BOT_DIR))
os.chdir(BOT_DIR)
os.makedirs("db", exist_ok=True)


class TextOfTests(unittest.TestCase):
    """Repli texte brut : le contenu doit survivre au rejet de Discord."""

    def setUp(self):
        from core.Context import _text_of

        self._text_of = _text_of

    def test_plain_text_is_returned_as_is(self):
        self.assertEqual(self._text_of("Bonjour le manoir"), "Bonjour le manoir")

    def test_none_and_empty_values_are_safe(self):
        self.assertEqual(self._text_of(None), "")
        self.assertEqual(self._text_of(""), "")

    def test_embed_keeps_title_description_fields_and_footer(self):
        import discord

        embed = discord.Embed(title="Hall d'entree", description="Un courant d'air froid.")
        embed.add_field(name="Portes", value="3", inline=True)
        embed.set_footer(text="Haunted")

        text = self._text_of(embed)

        self.assertIn("Hall d'entree", text)
        self.assertIn("Un courant d'air froid.", text)
        self.assertIn("Portes", text)
        self.assertIn("3", text)
        self.assertIn("Haunted", text)

    def test_real_cv2_view_is_flattened(self):
        # Cas reel le plus frequent du bot : CV2("Titre", "corps").
        from utils.cv2 import CV2

        text = self._text_of(CV2("Le manoir", "Une porte grince au premier etage."))

        self.assertIn("Le manoir", text)
        self.assertIn("Une porte grince au premier etage.", text)

    def test_real_cv2embed_keeps_fields_and_footer(self):
        from utils.cv2 import CV2Embed

        embed = CV2Embed("Presence", "Des pas au-dessus de ta chambre.")
        embed._fields = [("Etage", "Grenier")]
        embed._footer = "Haunted"

        text = self._text_of(embed)

        self.assertIn("Presence", text)
        self.assertIn("Des pas au-dessus de ta chambre.", text)
        self.assertIn("Grenier", text)
        self.assertIn("Haunted", text)

    def test_standalone_text_display_keeps_its_content(self):
        import discord

        self.assertEqual(
            self._text_of(discord.ui.TextDisplay("Des pas au-dessus de ta chambre.")),
            "Des pas au-dessus de ta chambre.",
        )


class LavalinkUriTests(unittest.TestCase):
    """`play` echouait sur un noeud injoignable : l'URI doit etre previsible."""

    ENV_KEYS = ("LAVALINK_HOST", "LAVALINK_PORT", "LAVALINK_SECURE")

    def setUp(self):
        from cogs.commands.music import Music

        self.uri = Music._lavalink_uri
        self.saved = {key: os.environ.get(key) for key in self.ENV_KEYS}

    def tearDown(self):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def _build(self, host=None, port=None, secure=None):
        for key, value in (("LAVALINK_HOST", host), ("LAVALINK_PORT", port), ("LAVALINK_SECURE", secure)):
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        return self.uri(object())

    def test_bare_host_uses_https_by_default(self):
        self.assertEqual(self._build(host="lava.exemple.fr"), "https://lava.exemple.fr")

    def test_scheme_in_host_is_not_duplicated(self):
        # L'ancien code produisait « https://https://... » -> connexion refusee.
        self.assertEqual(self._build(host="https://lava.exemple.fr"), "https://lava.exemple.fr")
        self.assertEqual(self._build(host="http://lava.exemple.fr"), "http://lava.exemple.fr")

    def test_insecure_node_uses_http_and_port(self):
        self.assertEqual(
            self._build(host="lava.exemple.fr", port="2333", secure="false"),
            "http://lava.exemple.fr:2333",
        )

    def test_port_is_not_appended_twice(self):
        self.assertEqual(
            self._build(host="lava.exemple.fr:2333", port="2333", secure="false"),
            "http://lava.exemple.fr:2333",
        )

    def test_ws_scheme_is_normalised(self):
        self.assertEqual(self._build(host="wss://lava.exemple.fr"), "https://lava.exemple.fr")

    def test_trailing_slash_is_removed(self):
        self.assertEqual(self._build(host="lava.exemple.fr/"), "https://lava.exemple.fr")

    def test_missing_host_is_reported(self):
        with self.assertRaises(RuntimeError):
            self._build(host=None)

    def test_blank_host_is_reported(self):
        with self.assertRaises(RuntimeError):
            self._build(host="   ")


class ApiRouteTests(unittest.TestCase):
    """Deux routes identiques : la seconde est morte sans le moindre message."""

    def _routers(self):
        from api.routes import admin, bot as bot_routes, guilds, modules

        return [guilds, modules, admin, bot_routes]

    def test_no_duplicate_method_and_path(self):
        duplicates = {}
        for module in self._routers():
            seen = defaultdict(list)
            for route in module.router.routes:
                for method in getattr(route, "methods", None) or ():
                    if method in ("HEAD", "OPTIONS"):
                        continue
                    seen[(method, route.path)].append(route.endpoint.__name__)
            for key, handlers in seen.items():
                if len(handlers) > 1:
                    duplicates[f"{module.__name__} {key[0]} {key[1]}"] = handlers

        self.assertEqual(duplicates, {}, f"Routes masquees : {duplicates}")

    def test_prefix_mounted_routers_do_not_collide(self):
        # /guilds et /modules sont montes sous le meme prefixe : une collision de
        # chemin ferait disparaitre une route du dashboard.
        from api.routes import guilds, modules

        def paths(module):
            found = set()
            for route in module.router.routes:
                for method in getattr(route, "methods", None) or ():
                    if method in ("HEAD", "OPTIONS"):
                        continue
                    found.add((method, route.path))
            return found

        collision = paths(guilds) & paths(modules)
        self.assertEqual(collision, set(), f"Collision de routes : {collision}")


class DashboardContractTests(unittest.TestCase):
    """Chaque appel du dashboard doit viser une route qui existe vraiment."""

    def test_every_dashboard_call_has_a_route(self):
        import re

        api_ts = (REPO_DIR / "dashboard" / "lib" / "api.ts").read_text(encoding="utf-8")
        calls = re.findall(r"request<[^>]*>\(\s*`([^`]+)`", api_ts, re.S)
        self.assertGreater(len(calls), 30, "Extraction des appels cassée ?")

        from api.routes import admin, bot as bot_routes, guilds, modules

        # Prefixes de montage reels (api/server.py) : le dashboard appelle
        # l'API complete, pas le chemin relatif des routeurs.
        routes = set()
        for prefix, module in (
            ("/guilds", guilds),
            ("/guilds", modules),
            ("/admin", admin),
            ("/bot", bot_routes),
        ):
            for route in module.router.routes:
                for method in getattr(route, "methods", None) or ():
                    if method in ("HEAD", "OPTIONS"):
                        continue
                    routes.add((method, prefix + re.sub(r"\{[^}]+\}", "{id}", route.path)))

        missing = []
        for raw in calls:
            endpoint = raw.replace("${", "{")
            endpoint = re.sub(r"\{[^}]+\}", "{id}", endpoint)
            if not any(path == endpoint for _, path in routes):
                missing.append(raw)

        self.assertEqual(missing, [], f"Appels du dashboard sans route : {missing}")


class AdminStatsTests(unittest.TestCase):
    """`/admin/stats` doit renvoyer des mesures reelles, jamais des constantes."""

    def _fake_bot(self):
        guild = types.SimpleNamespace(member_count=42)
        other = types.SimpleNamespace(member_count=8)
        bot = types.SimpleNamespace(
            guilds=[guild, other],
            commands={"a": object(), "b": object(), "c": object()},
            cogs={"x": object()},
            latency=0.042,
            shard_count=2,
        )
        bot.is_ready = lambda: True
        return bot

    def test_stats_are_derived_from_the_bot(self):
        from api.routes import admin

        stats = asyncio.run(admin.get_admin_stats(bot=self._fake_bot()))

        self.assertEqual(stats.total_members, "50")
        self.assertEqual(stats.active_servers, "2")
        self.assertTrue(stats.api_latency.endswith("ms"))
        self.assertEqual(len(stats.nodes), 4)

    def test_node_statuses_are_computed_not_hardcoded(self):
        from api.routes import admin

        bot = self._fake_bot()
        bot.is_ready = lambda: False
        bot.latency = 2.5  # > 1 s : la passerelle ne peut pas etre « healthy »

        stats = asyncio.run(admin.get_admin_stats(bot=bot))
        by_name = {node.name: node.status for node in stats.nodes}

        self.assertEqual(by_name["Modules du bot"], "booting")
        self.assertEqual(by_name["Passerelle Discord"], "warning")
        self.assertNotIn("Healthy", by_name.values(), "statut code en dur detecte")


if __name__ == "__main__":
    unittest.main(verbosity=2)
