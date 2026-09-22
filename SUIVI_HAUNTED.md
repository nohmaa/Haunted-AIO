# Suivi des modifications — Projet Haunted (ex-ZyroX)

> Fichier de liaison pour tout agent IA / humain qui intervient sur le projet.
> Objectifs actuels : (1) traduction en français, (2) nouvelle identité **Haunted**, (3) activation/désactivation des modules depuis le dashboard.
> Mettre à jour ce fichier à chaque changement (date + fichiers + comportement).

## 2026-09-23 — Renommage `CodeX.py` → `haunted.py`
- `git mv bot/CodeX.py bot/haunted.py` (historique conservé).
- Docstrings mises à jour : `bot/api/dependencies.py`, `bot/api/server.py` (+ « Haunted Bot Dashboard »), `bot/utils/tunnel.py`.
- Docs : `README.md`, `bot/README.md` (`python haunted.py`, arborescence, `PY_FILE=haunted.py` pour Pterodactyl).
- Vérification : `compileall` OK sur `haunted.py`, plus aucune référence fonctionnelle à `CodeX.py` (les mentions ci-dessous sont historiques ; filigranes d'attribution CodeX Devs conservés).
- ⚠️ Serveurs Pterodactyl existants : mettre `PY_FILE` à `haunted.py` dans l'onglet Startup.

## 2026-09-22 — Déploiement Pterodactyl unique + dépendances à jour
- Déploiement documenté **uniquement** pour Pterodactyl (egg *python generic*, image `ghcr.io/ptero-eggs/yolks:python_3.13`) : `README.md`, `bot/README.md` (upload du contenu de `bot/` à la racine, `PY_FILE=haunted.py`, `USER_UPLOAD=1`, `done` = `Loaded & Online!`, `.env` via Files). Mentions Render/Railway/Fly.io/Vercel/NexioHost supprimées des sections déploiement.
- `dashboard/README.md` : section Vercel remplacée par « Mise en production » générique Node 22+ (`npm run build` + `npm start`) ; le dashboard ne tourne pas sur l'image Python.
- `bot/requirements.txt` réécrit : que des dépendances réellement importées, versions épinglées vérifiées sur PyPI (ex. `discord.py==2.7.1`, `fastapi==0.141.1`, `uvicorn==0.53.0`, `wavelink==3.5.2`, `Pillow==12.3.0`, `numpy==2.5.3`, `openai==3.18.0`, `mcstatus==14.2.0`). Exception : `duckduckgo-search==6.3.7` (dernière ligne avec `AsyncDDGS` requis par `utils/ai_utils.py`, supprimé en 7+/8).
- `dashboard/package.json` : `next 16.3.6`, `react 19.3.0`, `tailwindcss 4.3.3` (+ `@tailwindcss/postcss`), `lucide-react 1.47.0`, `next-auth 4.24.15`, `sonner 2.0.8`, `tailwind-merge 3.7.0`, radix à jour, `typescript 5.9.3` (TS 7 testé : build OK mais `typescript-eslint` incompatible → 5.9.3, dernière 5.x), `eslint 9.39.5` (dernier 9.x : les plugins de `eslint-config-next` ne supportent pas ESLint 10).
- Migration Next 16 : 22 fichiers `params` → `Promise` + `await`/`use()` (script `params_codemod.py`), `postcss.config.mjs` → plugin v4, `app/globals.css` → `@import "tailwindcss"` + `@config`, `eslint.config.mjs` (flat config, `next lint` n'existe plus en v16), `next.config.js` en double supprimé, `tsconfig.json`/`next-env.d.ts` régénérés par le build.
- Prérequis docs : Python 3.13, Node.js 22 LTS. Badges et `dashboard/.env.example` alignés.
- Vérifications : `npm run build` → **succès** (toutes les routes dont `/modules`) ; `pip install -r requirements.txt` en venv vierge → **OK** + imports critiques testés (`discord 2.7.1`, `wavelink 3.5.2`, `JavaServer`, `AsyncDDGS`, `AsyncOpenAI`, `GoogleTranslator`…).
- Dette signalée : `npm run lint` rapporte ~100 erreurs pré-existantes (`no-explicit-any`, `set-state-in-effect` des nouvelles règles react-hooks v7) — le build n'en dépend pas, à traiter par module. Bouton `Website` placeholder `https://.vercel.app` dans `bot/cogs/events/auto.py:40` laissé tel quel (URL du site à renseigner).

## 2026-09-22 — READMEs (FR + Haunted + modules)
- `README.md` (racine), `bot/README.md`, `dashboard/README.md` réécrits en français : identité **Haunted**, exemples `.env` alignés (`brand_name='Haunted'`, `BOT_LANG`, `Haunted`/`H`), nouvelle section « Modules — activation/désactivation » (table des 19 clés + endpoints), dépannage FR (+ ligne modules), footer Haunted avec crédit d'origine.
- Vérification : relecture des trois fichiers (pas de code touché, pas de tests requis).

## 2026-09-22 — Session initiale (état des lieux + fondations)
Repo d'origine : https://github.com/nohmaa/ZyroX-CV2-AIO-With-Dashboard

### Décisions
- Nom du bot : **Haunted** (abréviation dashboard : **H**). Piloté par variables d'environnement :
  - Bot : `brand_name` dans `bot/.env` (défaut `Haunted` dans `bot/utils/config.py`).
  - Dashboard : `NEXT_PUBLIC_BRAND_NAME` / `NEXT_PUBLIC_BRAND_NAME_WORD` (défaut `Haunted` / `H`).
- Langue cible : **français**. Anglais conservé en fallback (`bot/lang/lang.en.json`, `bot/lang/lang.fr.json` + `bot/utils/i18n.py`).
- Modules : un seul registre de vérité `bot/api/modules_registry.py`, état par serveur en SQLite `db/modules.db`, API `GET/PATCH /api/v1/guilds/{guild_id}/modules`, page dashboard `dashboard/.../modules/page.tsx` + composant `components/dashboard/modules-manager.tsx`.

### Registre des modules (clés stables)
| Clé | Label FR | Route dashboard | Cogs Discord visés |
|---|---|---|---|
| `antinuke` | Anti-Nuke | `antinuke` | `Antinuke`, `_antinuke`, `AntiBan`, `AntiKick`, … (dossier `cogs/antinuke/`) |
| `automod` | Auto-modération | `automod` | `Automod`, `_automod`, `AntiSpam`, `AntiCaps`, `AntiLink`, `AntiInvite`, `AntiMassMention`, `AntiEmojiSpam` |
| `tickets` | Tickets | `tickets` | `TicketCog`, `_ticket` |
| `verification` | Vérification | `verification` | `Verification`, `_verify` |
| `welcome` | Bienvenue | `welcome` | `Welcomer`, `_welcome`, `FastGreet`, `greet` |
| `invites` | Invitations | `invites` | `inviteTracker`, `Tracking` |
| `autorole` | Rôles automatiques | `autorole` | `AutoRole` (commands), `Autorole`, `Autorole2` (events) |
| `reactionroles` | Rôles à réactions | `reactionroles` | `ReactionRoles` |
| `j2c` | Salons temporaires (Join-to-Create) | `j2c` | `JoinToCreate`, `_J2C` |
| `invcrole` | Rôle vocal | `invcrole` | `Invcrole` |
| `vanityroles` | Rôles vanity | `vanityroles` | `VanityRoles`, `_vanity` |
| `autoreact` | Réactions auto | `autoreact` | `AutoReaction`, `AutoReactListener` |
| `customroles` | Rôles personnalisés | `customroles` | `Customrole` |
| `joindm` | MP de bienvenue | `joindm` | `joindm`, `_joindm` |
| `leveling` | Niveaux & XP | `leveling` | `Leveling`, `_leveling` |
| `logging` | Journaux | `logging` | `Logging`, `_logging` |
| `games` | Jeux & fun | (pas de page dédiée) | `Games`, `_games`, `Blackjack`, `Slots`, `Counting`, `_Counting`, `Fun`, `_fun` |
| `music` | Musique | (pas de page dédiée) | `Music`, `_music` |
| `moderation` | Modération | (via commandes) | `Moderation`, `_moderation`, `Ban`, `Kick`, `Mute`, … |

### Fichiers créés cette session
- `bot/lang/lang.fr.json` — traduction FR des clés existantes de `lang.en.json`.
- `bot/utils/i18n.py` — helper `t(key, lang="fr")` avec fallback EN.
- `bot/api/modules_registry.py` — registre `MODULES` + `MODULE_KEYS` + `COG_MODULE_MAP`.
- `bot/utils/modules.py` — lecture/écriture SQLite `db/modules.db` (`get_modules_state`, `set_module_state`, `set_modules_bulk`, `is_module_enabled`).
- `bot/api/routes/modules.py` — `GET /{guild_id}/modules`, `PATCH /{guild_id}/modules`, `PATCH /{guild_id}/modules/{module_key}`.
- `dashboard/components/dashboard/modules-manager.tsx` — liste des modules avec interrupteurs (client, FR).
- `dashboard/app/dashboard/guild/[guildId]/modules/page.tsx` — page « Modules » par serveur (FR).

### Fichiers modifiés cette session
- `bot/utils/config.py` — défaut `BRAND_NAME = "Haunted"`.
- `bot/.env.example` — `brand_name='Haunted'`, `NEXT_PUBLIC_BRAND_NAME='Haunted'`, clé exemple `HAUNTED_SECURE_API_KEY_...`, tunnel `haunted-api`.
- `dashboard/.env.example` — marque `Haunted` / `H`, clé exemple alignée, secret nextauth renommé.
- `dashboard/package.json` — `name: "haunted-dashboard"`.
- `dashboard/app/layout.tsx`, `dashboard/app/dashboard/layout.tsx`, `dashboard/app/page.tsx`, `dashboard/app/privacy/page.tsx` — fallbacks `Haunted` / `H` au lieu de `ZyroX` / `ZX`.
- `dashboard/components/dashboard/antinuke-form.tsx`, `autorole-form.tsx`, `customroles-form.tsx`, `verification-form.tsx` — mentions visibles « ZyroX » → « Haunted ».
- `bot/api/schemas.py` — ajout `ModuleState`, `ModulesConfig`, `ModulesUpdate`, `ModuleKeyUpdate`.
- `bot/api/server.py` — enregistre le routeur `modules` sous `/api/v1/guilds` + fix `root()` qui renvoyait `{BRAND_NAME}` (un `set`) au lieu de la chaîne.
- `bot/core/zyrox.py` — `invoke()` bloque les commandes dont le cog porte un `module_key` désactivé pour le serveur (message d'erreur en français).
- Cogs : ajout d'un attribut `module_key` (sans changer la logique) sur `Leveling`/`_leveling` (`leveling`), `Automod`/`_automod` + automod listeners (`automod`), `Antinuke`/`_antinuke` + antinuke listeners (`antinuke`), `Verification`/`_verify` (`verification`), `TicketCog`/`_ticket` (`tickets`), `Logging`/`_logging` (`logging`), `JoinToCreate`/`_J2C` (`j2c`), `Music`/`_music` (`music`), `Games`/`_games` (`games`).
- `dashboard/types/api.ts`, `dashboard/lib/api.ts` — types + appels `getModules` / `updateModules` / `setModule`.
- `dashboard/components/guild-tabs.tsx` — onglets traduits en FR + nouvel onglet « Modules ».
- `dashboard/app/dashboard/guild/[guildId]/layout.tsx` — textes FR (retour, rôles, salons, membres, actualiser, paramètres, accès refusé).
- `dashboard/app/dashboard/guild/[guildId]/page.tsx` — section « Modules actifs » en FR + lien vers la page Modules.
- `dashboard/app/dashboard/guild/[guildId]/settings/page.tsx` — titre/description en FR.

### Traduction FR — état
- Fait : shell dashboard (onglets, layout serveur, vue d'ensemble, paramètres, page Modules), `lang.fr.json` (clés existantes), message de blocage module désactivé en FR.
- Reste à faire (pour un prochain agent) : chaque `page.tsx` de module, chaque `*-form.tsx`, chaque cog (des centaines de chaînes EN). Stratégie : traduire par module en suivant le registre ci-dessus, brancher `t()` côté bot au fil de l'eau, cocher ici.

### Rebranding Haunted — reste à faire
- Remplacer les occurrences visibles restantes de « ZyroX/CodeX » (textes marketing `app/page.tsx`, `app/docs`, README, ASCII art `CodeX.py`, `config.yml`, webhooks/footers). Garder les fallbacks env déjà faits.
- ~~Choisir : renommer `bot/CodeX.py` → `bot/Haunted.py` (avec alias) ou garder le nom de fichier.~~ Fait le 2026-09-23 : `bot/haunted.py` (minuscules, convention Python).
- Mettre à jour `README.md` (nom, captures, `.env`).

### Modules on/off — comment ça marche
- Dashboard : page **Modules** → interrupteur → `PATCH /guilds/{id}/modules/{clé}` (`{enabled: bool}`).
- Bot : `zyrox.invoke()` refuse les commandes des modules désactivés (FR : « Le module X est désactivé sur ce serveur… »). Les écouteurs d'événements (`on_message`, antinuke, automod…) doivent appeler `is_module_enabled(guild_id, key)` — câblé pour l'instant uniquement au niveau commandes ; voir « reste à faire ».
- Reste à faire : ajouter le garde `is_module_enabled` dans les listeners (`leveling on_message`, `AutoReactListener`, `StickyMessageListener`, antinuke `on_audit_log`, automod checks, `Autorole`, `greet`/`welcome`), afficher l'état réel sur la vue d'ensemble (actuellement statique), gérer `games`/`music`/`moderation` sans page dédiée (page Modules suffit).

### Vérifications
- Backend : `python -m compileall` OK sur tous les fichiers touchés (dont `core/zyrox.py`, `api/*`, `utils/*`, cogs marqués).
- Backend : script de test `test_modules2.py` → **ALL TESTS PASSED** (registre 19 modules, schémas pydantic, `get/set/is_module_enabled` + bulk + clé inconnue rejetée, `i18n.t` FR/EN/fallback). Nécessite `aiosqlite`, `pydantic`, `python-dotenv` (installés dans le Python système pour le test ; le bot utilise son `requirements.txt`).
- Dashboard : `npx tsc --noEmit` **impossible dans cette session** — `node_modules/` absent du checkout (`Cannot find module 'react'` sur tout le projet, pré-existant, non lié à ces changements). À valider avec `npm install` puis `npm run dev` (`NEXT_PUBLIC_API_URL` → tunnel/serveur local).
- Bot live non testé : à valider avec `python haunted.py` (commande d'un module désactivé doit répondre le message FR).
