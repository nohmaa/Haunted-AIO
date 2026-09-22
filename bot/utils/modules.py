"""État on/off des modules par serveur (SQLite `db/modules.db`).

Par défaut, tous les modules sont activés. Seuls les modules explicitement
désactivés depuis le dashboard sont stockés à `enabled = 0`.
"""

import aiosqlite
import os

from api.modules_registry import MODULE_KEYS

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "modules.db")


async def _ensure_table(db) -> None:
    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS module_state (
            guild_id INTEGER NOT NULL,
            module_key TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (guild_id, module_key)
        )
        """
    )


async def get_modules_state(guild_id: int) -> dict:
    """Retourne {clé: bool} pour tous les modules connus (défaut True)."""
    state = {key: True for key in MODULE_KEYS}
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await _ensure_table(db)
        await db.commit()
        async with db.execute(
            "SELECT module_key, enabled FROM module_state WHERE guild_id = ?",
            (guild_id,),
        ) as cursor:
            async for module_key, enabled in cursor:
                if module_key in state:
                    state[module_key] = bool(enabled)
    return state


async def is_module_enabled(guild_id: int, module_key: str) -> bool:
    """Garde utilisé par les cogs/listeners. Clé inconnue => activé."""
    if module_key not in MODULE_KEYS:
        return True
    state = await get_modules_state(guild_id)
    return state.get(module_key, True)


async def set_module_state(guild_id: int, module_key: str, enabled: bool) -> None:
    if module_key not in MODULE_KEYS:
        raise ValueError(f"Module inconnu : {module_key}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await _ensure_table(db)
        await db.execute(
            "INSERT OR REPLACE INTO module_state (guild_id, module_key, enabled) VALUES (?, ?, ?)",
            (guild_id, module_key, 1 if enabled else 0),
        )
        await db.commit()


async def set_modules_bulk(guild_id: int, modules: dict) -> dict:
    """Met à jour plusieurs modules d'un coup. Retourne l'état complet."""
    for key in modules:
        if key not in MODULE_KEYS:
            raise ValueError(f"Module inconnu : {key}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await _ensure_table(db)
        for key, enabled in modules.items():
            await db.execute(
                "INSERT OR REPLACE INTO module_state (guild_id, module_key, enabled) VALUES (?, ?, ?)",
                (guild_id, key, 1 if enabled else 0),
            )
        await db.commit()
    return await get_modules_state(guild_id)
