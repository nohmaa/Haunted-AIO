"""Petit helper i18n FR/EN pour Haunted.

Utilisation :
    from utils.i18n import t
    await ctx.send(t("ping_msg") + "...")
"""

import json
import os
from functools import lru_cache

_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lang")
DEFAULT_LANG = os.getenv("BOT_LANG", "fr").lower()


@lru_cache(maxsize=4)
def _load(lang: str) -> dict:
    path = os.path.join(_BASE, f"lang.{lang}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """Retourne la chaîne traduite, avec repli vers l'anglais puis vers la clé."""
    lang = (lang or DEFAULT_LANG).lower()
    text = _load(lang).get(key)
    if text is None and lang != "en":
        text = _load("en").get(key)
    if text is None:
        return key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
