from fastapi import APIRouter, HTTPException

from api.modules_registry import MODULES, MODULE_KEYS, MODULE_LABELS
from api.schemas import ModulesConfig, ModulesUpdate, ModuleKeyUpdate, ModuleState
from utils.modules import get_modules_state, set_module_state, set_modules_bulk

router = APIRouter()


@router.get("/{guild_id}/modules", response_model=ModulesConfig, summary="État des modules du serveur")
async def get_guild_modules(guild_id: int):
    """Retourne l'état activé/désactivé de chaque module pour ce serveur."""
    state = await get_modules_state(guild_id)
    return ModulesConfig(
        guild_id=guild_id,
        modules=[
            ModuleState(
                key=m["key"],
                label=m["label"],
                description=m["description"],
                route=m["route"],
                enabled=state.get(m["key"], True),
            )
            for m in MODULES
        ],
    )


@router.patch("/{guild_id}/modules", response_model=ModulesConfig, summary="Mettre à jour plusieurs modules")
async def patch_guild_modules(guild_id: int, data: ModulesUpdate):
    """Active/désactive plusieurs modules d'un coup : `{"modules": {"leveling": false}}`."""
    try:
        state = await set_modules_bulk(guild_id, data.modules)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ModulesConfig(
        guild_id=guild_id,
        modules=[
            ModuleState(
                key=m["key"],
                label=m["label"],
                description=m["description"],
                route=m["route"],
                enabled=state.get(m["key"], True),
            )
            for m in MODULES
        ],
    )


@router.patch("/{guild_id}/modules/{module_key}", response_model=ModuleState, summary="Activer/désactiver un module")
async def patch_guild_module(guild_id: int, module_key: str, data: ModuleKeyUpdate):
    """Active/désactive un seul module."""
    if module_key not in MODULE_KEYS:
        raise HTTPException(status_code=404, detail=f"Module inconnu : {module_key}")
    await set_module_state(guild_id, module_key, data.enabled)
    meta = next(m for m in MODULES if m["key"] == module_key)
    return ModuleState(
        key=module_key,
        label=meta["label"],
        description=meta["description"],
        route=meta["route"],
        enabled=data.enabled,
    )


@router.get("/{guild_id}/modules/{module_key}", response_model=ModuleState, summary="État d'un module")
async def get_guild_module(guild_id: int, module_key: str):
    if module_key not in MODULE_KEYS:
        raise HTTPException(status_code=404, detail=f"Module inconnu : {module_key}")
    state = await get_modules_state(guild_id)
    meta = next(m for m in MODULES if m["key"] == module_key)
    return ModuleState(
        key=module_key,
        label=meta["label"],
        description=meta["description"],
        route=meta["route"],
        enabled=state.get(module_key, True),
    )
