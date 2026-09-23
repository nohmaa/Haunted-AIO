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

from discord.ext import commands
import discord
import functools
from typing import Optional, Any
import asyncio

__all__ = ("Context", )


# ── Filet de sécurité d'envoi ───────────────────────────────────────────────
# Discord répond 50006 ("Cannot send an empty message") ou 50035 ("Invalid
# Form Body") lorsqu'il rejette / élague tout le contenu d'un message :
#   • permission « Intégrer des liens » (Embed Links) absente pour le bot dans
#     le salon → Discord supprime l'embed, il ne reste rien à envoyer ;
#   • embed, emoji ou composant invalide, contenu hors limites ;
#   • version de discord.py trop ancienne pour les composants v2.
# Dans ces cas on renvoie la même information en texte brut : la commande
# fonctionne quand même, et la console explique la cause.
_FALLBACK_CODES = (50006, 50035)
_warned_codes: set = set()


def _embed_text(embed) -> str:
    """Texte lisible d'un discord.Embed (via son dict public)."""
    data = embed.to_dict()
    parts = []
    author = data.get("author") or {}
    if author.get("name"):
        parts.append(f"**{author['name']}**")
    if data.get("title"):
        parts.append(f"**{data['title']}**")
    if data.get("description"):
        parts.append(data["description"])
    for field in data.get("fields") or []:
        name = field.get("name") or ""
        value = field.get("value") or ""
        parts.append(f"**{name}**\n{value}" if name else str(value))
    footer = (data.get("footer") or {}).get("text")
    if footer:
        parts.append(f"*{footer}*")
    return "\n\n".join(part for part in parts if part and part.strip())


def _text_of(value) -> str:
    """Texte lisible d'un embed, d'une vue CV2/Components v2 ou d'un composant."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, discord.Embed):
        return _embed_text(value)

    parts = []
    content = getattr(value, "content", None)
    title = getattr(value, "_title", None) or getattr(value, "title", None)
    if isinstance(title, str) and title.strip("* \t\n"):
        parts.append(f"**{title}**")
    description = getattr(value, "_description", None)
    if description is None:
        description = getattr(value, "description", None)
    if isinstance(description, str) and description.strip():
        parts.append(description)

    fields = getattr(value, "_fields", None)
    if fields is None:
        fields = getattr(value, "fields", None)
    for field in fields or []:
        if isinstance(field, dict):
            name, val = field.get("name"), field.get("value")
        else:
            name = getattr(field, "name", None)
            val = getattr(field, "value", None)
            if name is None and isinstance(field, (tuple, list)) and len(field) == 2:
                name, val = field
        if name or val:
            parts.append(f"**{name}**\n{val}" if name else str(val))

    footer = getattr(value, "_footer", None)
    if not isinstance(footer, str):
        # discord.Embed garde un dict dans _footer, CV2Embed une str.
        footer_src = footer or getattr(value, "footer", None)
        footer = (
            footer_src.get("text")
            if isinstance(footer_src, dict)
            else getattr(footer_src, "text", None)
        )
    if isinstance(footer, str) and footer.strip():
        parts.append(f"*{footer}*")

    if not parts and isinstance(content, str) and content.strip():
        parts.append(content)

    if not parts:
        for child in getattr(value, "children", None) or []:
            child_text = _text_of(child)
            if child_text:
                parts.append(child_text)

    return "\n\n".join(part for part in parts if part and part.strip())


def _payload_text(content, kwargs) -> str:
    """Reconstitue le texte d'un envoi dont Discord a rejeté le contenu riche."""
    chunks = []
    if isinstance(content, str) and content.strip():
        chunks.append(content)
    for key in ("embed", "embeds", "view"):
        value = kwargs.get(key)
        if isinstance(value, (list, tuple)):
            for item in value:
                text = _text_of(item)
                if text:
                    chunks.append(text)
        else:
            text = _text_of(value)
            if text:
                chunks.append(text)
    return "\n\n".join(chunks).strip()


def _warn_rejected(exc) -> None:
    code = getattr(exc, "code", None)
    if code in _warned_codes:
        return
    _warned_codes.add(code)
    print(
        f"[WARN] Discord a rejeté un message (code {code}: "
        f"{getattr(exc, 'text', exc)}) → envoi en texte brut à la place.\n"
        "       Causes usuelles : permission « Intégrer des liens » (Embed Links)\n"
        "       manquante pour le bot dans ce salon, embed/emoji invalide, ou\n"
        "       discord.py trop ancien pour les composants v2 (pip install -U discord.py)."
    )


class Context(commands.Context):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<core.Context>"

    @property
    async def session(self):
        return self.bot.session

    @discord.utils.cached_property
    def replied_reference(self) -> Optional[discord.Message]:
        ref = self.message.reference
        if ref and isinstance(ref.resolved, discord.Message):
            return ref.resolved.to_reference()
        return None

    def with_type(func):

        @functools.wraps(func)
        async def wrapped(self, *args, **kwargs):
            context = args[0] if isinstance(args[0],
                                            commands.Context) else args[1]
            try:
                async with context.typing():
                    await func(*args, **kwargs)
            except discord.Forbidden:  
                await func(*args, **kwargs)

        return wrapped

    async def show_help(self, command: str = None) -> Any:
        cmd = self.bot.get_command('help')
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)

    async def send(self,
                   content: Optional[str] = None,
                   **kwargs) -> Optional[discord.Message]:
        if not (self.channel.permissions_for(self.me)).send_messages:
            try:
                await self.author.send(
                    "bot dont have perms to send msg in that channel")
            except discord.Forbidden:  
                pass
            return
        return await self._deliver(super().send, content, kwargs)

    async def reply(self,
                    content: Optional[str] = None,
                    **kwargs) -> Optional[discord.Message]:
        if not (self.channel.permissions_for(self.me)).send_messages:
            try:
                await self.author.send(
                    "bot dont have perms to send msg in that channel")
            except discord.Forbidden:  
                pass
            return
        return await self._deliver(super().reply, content, kwargs)

    async def _deliver(self, sender, content, kwargs):
        """Envoie via `sender` ; si Discord rejette le contenu (50006/50035),
        renvoie la même information en texte brut au lieu d'échouer."""
        try:
            return await sender(content, **kwargs)
        except discord.HTTPException as exc:
            text = _payload_text(content, kwargs)
            if getattr(exc, "code", None) not in _FALLBACK_CODES or not text:
                raise
            _warn_rejected(exc)
            retry = {
                key: value
                for key, value in kwargs.items()
                if key not in ("embed", "embeds", "view", "components")
            }
            try:
                return await sender(text[:1990], **retry)
            except discord.HTTPException:
                retry.pop("reference", None)
                retry.pop("mention_author", None)
                return await self.channel.send(text[:1990], **retry)

    async def release(self, delay: Optional[int] = None) -> None:
        delay = delay or 0
        await asyncio.sleep(delay)
