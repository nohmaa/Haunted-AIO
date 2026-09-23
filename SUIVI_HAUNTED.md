# Suivi des modifications — Projet Haunted (ex-ZyroX)

> Fichier de liaison pour tout agent IA / humain qui intervient sur le projet.
> Objectifs actuels : (1) traduction en français, (2) nouvelle identité **Haunted**, (3) activation/désactivation des modules depuis le dashboard.
> Mettre à jour ce fichier à chaque changement (date + fichiers + comportement).

## 2026-09-23 — Emojis Unicode + backend conservé en anglais
- Règle actée : le **backend reste en anglais** (identifiants, comparaisons logiques, codes d'erreur) — seule l'UI/UX est traduite. Vérifié : aucune comparaison logique (`== "active"`, etc.) n'a été traduite dans le diff de traduction.
- **Problème emojis résolu** : toutes les constantes de `bot/utils/emoji.py` étaient des emojis custom `<:name:ID>` pointant vers l'application de l'ancien bot → invisibles, et l'EmojiSync ne pouvait ni les retélécharger (404 CDN) ni les uploader. Remplacés par des **emojis Unicode classiques** (✅ ⚠️ 🔨 🎵 …) qui s'affichent partout sans upload : 193 constantes, mêmes noms, mêmes dictionnaires/helpers/aliases → aucun import cassé (diff des constantes vs HEAD : aucune perte).
- `EMOJI_SYNC` : doc mise à jour (défaut désormais `false`, utile uniquement si vous ajoutez vos propres emojis custom dans `emoji.py`). `haunted.py` garde l'appel `run_sync` (il s'auto-désactive via la variable d'env).
- En prod : passer `EMOJI_SYNC=false` dans le `.env` du serveur (ou redémarrer — le défaut du code s'applique si la variable est absente) ; plus aucune erreur EmojiSync attendue.
- Vérifications : `compileall` OK, import `emoji.py` OK avec 0 emoji custom restant.

## 2026-09-23 — Traduction des commandes : consolidation, nettoyage et push
- Reprise des 126 fichiers modifiés par les agents de traduction (commands A-M/N-Z, zyrox, events+moderation, antinuke+automod, games+utils) : tout était appliqué mais **non commité**.
- Supprimés : `bot/extract2.py` et `bot/extract_v.py` (scripts temporaires des agents, pointaient vers un dossier Temp hors repo).
- Les scripts de traduction avaient dégradé le style (`from utils .Tools`, `label ="x",style =y`, espaces traînants) : reformatage **Black** sur les 126 fichiers uniquement, puis normalisation des ~5 800 artefacts `\{expr }` → `{expr}` dans les f-strings (regex restreintes aux substitutions simples, jamais aux chaînes ni au code).
- Vérifications : `python -m compileall bot/` **OK** (0 erreur), aucun changement d'URL/emoji/mention d'identifiant dans le diff (0 URL ajoutée, 0 emoji touché), `npm run build` dashboard **OK** (30 routes).
- Notes : (1) les URLs d'avatar de l'ancien bot (`cdn.discordapp.com/avatars/1396114795102470196/…`, 19 occurrences dans `moderation.py` + `blacklist.py`) sont **pré-existantes** dans HEAD, non introduites par la traduction — à remplacer par `ctx.me.display_avatar.url` plus tard ; (2) quelques chaînes EN subsistent (messages internes/erreurs API dans `ai.py`, `imagine.py`, `role.py`, `dms.py`, `automod.py`, `afk.py`, `emergency.py`) — à finir au fil de l'eau.
- Commit + push effectués : la traduction des commandes est en ligne ; le bot en production la récupère au prochain redémarrage (`AUTO_UPDATE=1`).

## 2026-09-23 — Infra prod (domaine haunted-mind.com)
- Domaine : `haunted-mind.com` abandonné au profit de **`haunted-mind.site`** (acheté chez Hostinger). Délégation NS vers Cloudflare **active** (`adi`/`arch.ns.cloudflare.com`, vérifié).
- Dashboard : **domaine custom = apex `haunted-mind.site`** (pas `dashboard.`). Reste à faire côté Cloudflare : A `@` → `76.76.21.21` (actuellement IP de parking `216.198.79.1`).
- Tunnel `api.haunted-mind.site` **live** (vérifié : `/api/v1/bot/info` répond `{"detail":"Not authenticated"}` = FastAPI atteint, auth par clé exigée comme prévu).
- Reste : variables Vercel finales + redeploy + redirect OAuth + `CORS_ORIGINS`.
- Topologie retenue : API bot → `https://api.haunted-mind.site` (tunnel `haunted-api`) ; dashboard → URL Vercel (domaine custom `dashboard.haunted-mind.site` optionnel plus tard).
- Guide détaillé donné en chat (domaine → tunnel → Vercel → OAuth → CORS).

## 2026-09-23 — Derniers « ZyroX » visibles + traduction des commandes lancée
- Corrigés : `admin-content` (administrateurs Haunted), landing (langage Haunted), dashboard home (cœur Haunted), `.env.example` (haunted-api).
- Reste volontaire : identifiants de code (`zyrox`, `cogs/zyrox/`, `ZYROX_*`), noms d'emojis Discord, historique docs.
- Traduction des ~150 fichiers de commandes lancée en 6 agents parallèles (commands A-M / N-Z, zyrox, events+moderation, antinuke+automod, games+utils) avec garde-fous (identifiants, URLs, emojis, placeholders, compileall par fichier).

## 2026-09-23 — Dashboard 100 % français
- 4 agents parallèles (shell, formulaires A/B, pages publiques) + 18 pages serveurs en scripts vérifiés : titres, descriptions, labels, placeholders, boutons, toasts, sidebars, landing, docs, CGU/confidentialité.
- Garde-fous : valeurs API intactes (`panel_type`, `button_style`, `punishments`, `verification_method`, `value="none"`…), comparaisons logiques traduites à l'identique, `process.env` et routes intacts.
- Corrections : message d'accès refusé + tooltip Actif (layout), console simulée, `Documentation ZyroX` → Haunted.
- Vérification : `npm run build` OK (30 routes). Commandes du bot : reportées (choix utilisateur « dashboard d'abord »).

## 2026-09-23 — CORS : origine www bloquée + variantes auto
- Log prod : dashboard sur `https://www.haunted-mind.site` bloqué car seul l'apex était en `CORS_ORIGINS`. Action côté serveur : `CORS_ORIGINS="https://haunted-mind.site,https://www.haunted-mind.site"` + Restart.
- Code : `_expand_cors_origins()` dans `api/server.py` ajoute auto. la variante www/apex (+ ports préservés, `localhost` exclu). Test logique OK.
- Docs : étape CORS précisée (apex + www).

## 2026-09-23 — Déploiement dashboard + Cloudflare détaillés
- `README.md` : section Tunnel réécrite en pas-à-pas (domaine sur Cloudflare, création du tunnel, tableau Public Hostname, correspondance token/URL → `.env`, test navigateur, dépannage). Section Vercel détaillée (tableau des réglages dont Output vide, tableau des variables avec « où trouver », redirect OAuth, `CORS_ORIGINS` côté bot, checklist finale) + schéma d'architecture.
- `dashboard/README.md` : réglages Vercel tabulés + étape CORS.

## 2026-09-23 — Échec Vercel « No Output Directory named public »
- Diagnostic : le build Next réussit (compile + types + 30 routes), les erreurs `Dynamic server usage` au prerender sont bénignes (pages `ƒ` dynamiques, identiques en local). Le vrai échec est le réglage projet : **Output Directory = `public`** (ou Framework Preset ≠ Next.js).
- Correctif côté dashboard Vercel (aucun changement de code) : Settings → General → Root Directory `dashboard`, Framework Preset **Next.js**, Build Command vide (défaut), **Output Directory vide**, Install Command vide → Redeploy.

## 2026-09-23 — Setup Vercel du dashboard dans les docs
- `README.md` (section Déploiement) + `dashboard/README.md` (« Mise en production ») : pas-à-pas Vercel (Root Directory `dashboard`, variables, redirect OAuth, redeploy obligatoire après changement des `NEXT_PUBLIC_*`) + option Node.js manuel conservée.

## 2026-09-23 — Constat prod (bot en ligne, rien à changer)
- Log 23:39 : bot OK (`Loaded & Online!`, tunnel live, 264 commandes + 89 slash synchronisées).
- 4 échecs EmojiSync (`BugHunterLvl2`, `error`, `HypesquadEvents`, `PartneredServerOwner`) : **bénins**. Le sync retélécharge la source depuis `cdn.discordapp.com/emojis/{ancien_ID}.webp` et ces IDs (badges d'autres apps) ne s'y trouvent plus → 404 ignoré, sync marquée complète (140/144 OK). Pour faire taire : `EMOJI_SYNC=false` une fois stable.
- Bannière console encore ancienne sur ce log → simple `Restart` (récupère `AUTO_UPDATE=1` : bannière Haunted + correctifs identité).

## 2026-09-23 — Assets : aucun ZyroX + fix fond leaderboard
- Vérifié visuellement : `background.png` (texture sombre neutre), `leaderboardlevel.gif` (scène anime sans texte), `minecraft.ttf` → aucun nom/logo ZyroX. Grep binaire : rien.
- Bug trouvé au passage : `leveling.py` cherchait le fond en absolu `/home/container/assets/…` (inexistant en méthode git → fond uni silencieux). Nouveau helper `_leaderboard_bg()` : chemin relatif au dossier du bot d'abord, repli historique sinon. Couverture git + upload.
- Vérification : `compileall` + AST OK.

## 2026-09-23 — Licence Arsonist + serveur support
- `LICENSE` (racine, `bot/`, `dashboard`) : `Copyright (c) 2026 Arsonist`.
- Nouveau lien support `https://discord.gg/DvetGPq9q5` : défaut `SUPPORT_SERVER` (`config.py`), `.env.example`, tables des READMEs, `help_footer` (EN+FR), et ligne discord des 268 filigranes (cadres réalignés).
- Le bot en ligne bascule dessus au prochain redémarrage (`AUTO_UPDATE=1`) sans toucher au `.env` (variable non définie = défaut).
- Restent volontaires : crédits historiques « basé sur ZyroX-CV2 par CodeX Devs » (README + SUIVI), `codexdevs.in` (User-Agent map.py), `ch` (config.py).
- Vérification : `compileall` OK.

## 2026-09-23 — Filigranes de crédit → Arsonist
Selon vos réponses : nom `Arsonist`, Discord gardé (`discord.gg/codexdev`), ligne YouTube supprimée, ligne GitHub supprimée.
- Script appliqué sur 268 fichiers (`.py/.tsx/.ts/.mjs/.js`, en-têtes ≤16 lignes) : `© 2026 CodeX Devs` → `© 2026 Arsonist` (largeur de cadre conservée), suppression des lignes YouTube/GitHub.
- Volontairement inchangés : fichiers `LICENSE` (attribution légale d'origine), mentions historiques dans `SUIVI_HAUNTED.md`.
- Vérifications : `compileall` OK, `npm run build` OK.

## 2026-09-23 — Identités restantes dans le bot
Inventaire par script AST (hors filigranes) + corrections :
- Bannière console `on_ready` : art COCX → art HAUNTED (`bot/haunted.py`).
- `"""Zyrox Games"""` → `"""Haunted Games"""`, docstrings `emoji.py`/`tunnel.py` → Haunted/haunted-api.
- **Liens support centralisés** : nouveau `SUPPORT_SERVER` (`.env`, défaut `discord.gg/codexdev`) utilisé par `server`/`serverLink` et 15 endroits (blacklist, bienvenue, invite, help, noprefix, nitro, tracking, mention, musique, on_guild). Pour changer de serveur support : une seule variable.
- **Bug identité critique** : la commande `invite` et le menu `mention` pointaient vers l'ancien `client_id=1396114795102470196` (l'ancien bot !) → URL construite avec l'ID du bot en ligne (`ctx.bot.user.id` / `guild.me.id`).
- **Bug liens musique** : les titres ajoutés en file pointaient vers le serveur support → vraie URI (`track.uri`, `external_urls.spotify` avec replis).
- Prompts IA : nom Haunted + suppression du texte créateur corrompu (« created by . Evil ! Rexy .. »).
- Volontairement inchangés : classe `zyrox`, dossier `cogs/zyrox/`, constantes d'emojis `ZYROX_*`, filigranes de crédit, URLs tierces (codexdevs.in, grainy-gradients).
- Reste : liens `discord.gg/codexdev` par défaut tant que vous ne renseignez pas votre propre `SUPPORT_SERVER` ; mentions créateurs (stats Team Info, mention Developer Info) à mettre à jour avec vos IDs.
- Vérification : `compileall` OK, plus aucune URL support en dur hors valeur par défaut.

## 2026-09-23 — Installation simplifiée (.env d'abord)
- `README.md` : parcours réécrit — prérequis en checklist avec liens, `.env` **avant** l'install, modèle annoté (où trouver chaque valeur), ordre bot → dashboard, et ✅ « ça marche si » avec la ligne `NEXT_PUBLIC_API_URL` à copier.
- `bot/README.md` et `dashboard/README.md` alignés sur le même ordre (`.env` en étape 1, renvoi vers la version guidée du README racine).

## 2026-09-23 — Repo renommé `Haunted-AIO`
- Renommage GitHub `ZyroX-CV2-AIO-With-Dashboard` → `Haunted-AIO` (fait manuellement côté web).
- Remote local mis à jour (`origin` → `https://github.com/nohmaa/Haunted-AIO.git`).
- URLs mises à jour : badge GitHub + `git clone` + `GIT_ADDRESS` (`README.md`, `bot/README.md`).
- Ligne « Repo d'origine » ci-dessous conservée pour l'historique.

## 2026-09-23 — Disque plein sur Pterodactyl (Errno 28)
- Log : `pip install` avorte pendant le téléchargement (`google_api_python_client`, 16 Mo) → rien n'est installé → le garde signale `aiohttp` manquant. Le backtracking pip sur la chaîne Google rallongeait déjà chaque boot.
- `google-generativeai` **retiré** de `bot/requirements.txt` : déprécié, ~100 Mo de dépendances (grpcio, protobuf, google-api-client…), code déjà protégé (`GEMINI_AVAILABLE=False` dans `ai.py`). Gain : downloads ≈ 60 Mo au lieu de plusieurs centaines.
- Garde `haunted.py` enrichi : affiche l'espace disque libre + consigne (< 300 Mo : vider `.cache/pip` via Files ou demander plus de disque).
- Actions côté serveur : Files → supprimer `.cache/pip` (cache du run avorté), vérifier le quota disque du serveur, Restart (requirements allégé récupéré via `AUTO_UPDATE`).

## 2026-09-23 — Dépendances manquantes (audit AST complet)
Crash Pterodactyl `No module named 'pytz'` : l'audit manuel avait raté des imports. Nouvel audit exhaustif par AST de tous les `.py` (`audit_imports.py`, hors stdlib et paquets locaux).
- Ajoutés à `bot/requirements.txt` (dernières versions PyPI vérifiées) : `pytz==2026.3.post1` (giveaways), `aiofiles==25.1.0` (logging), `pydantic==2.13.5` (explicite), `google-generativeai==0.8.6` (Gemini, import gardé en try/except — package déprécié par Google, migrer vers `google.genai` plus tard).
- `imagine.py` (`from prodia… import`) : **code mort**, jamais chargé (`cogs/__init__.py` ne l'importe pas, aucune référence) + aucun paquet `prodia`/`prodia-python` n'existe sur PyPI → rien à installer, à supprimer ou réparer plus tard.
- Supprimé : `bot/cogs/commands/leveling_original.py` (backup corrompu, null bytes, jamais importé).
- Vérifications : install complète en venv vierge OK, `import pytz/aiofiles/google.generativeai/pydantic` OK, `compileall` OK sur tout `bot/`.

## 2026-09-23 — Fix crash Pterodactyl (pip sauté + CWD + BDD suivies)
Cause du crash `ModuleNotFoundError: No module named 'aiohttp'` : avec la méthode git, `REQUIREMENTS_FILE` restait à `requirements.txt` (racine) alors que le fichier est dans `bot/` → le garde `if [[ -f … ]]` de l'egg sautait l'install pip en silence.
- Docs Pterodactyl (`README.md`, `bot/README.md`) : méthode git documentée en premier (`GIT_ADDRESS`+`BRANCH=main`+`AUTO_UPDATE=1`, `PY_FILE=bot/haunted.py`, `REQUIREMENTS_FILE=bot/requirements.txt` + avertissement), upload manuel en alternative.
- `bot/haunted.py` : `os.chdir()` vers son propre dossier au démarrage — les chemins relatifs (`db/`, `jsondb/`, `.env`) fonctionnent quel que soit le CWD (l'egg lance depuis `/home/container`).
- BDD/JSON runtime désuivis de git (`git rm --cached` : `bot/db/*.db`, `bot/*.db`, `bot/db/counting.json`, `bot/jsondb/*.json`) + `.gitignore` : le bot les recrée seul (`CREATE TABLE IF NOT EXISTS`, gardes `os.path.exists`). Sans ça, `AUTO_UPDATE=1` aurait fait échouer les `git pull` futurs (fichiers modifiés localement).
- À faire côté serveur : mettre `REQUIREMENTS_FILE=bot/requirements.txt` dans Startup puis redémarrer (récupère aussi le fix CWD via `AUTO_UPDATE`).

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
