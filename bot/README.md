<div align="center">

```
██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
```

<h3>Haunted Bot — Bot Discord Python + Backend FastAPI</h3>

<p>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/></a>
  <a href="https://discordpy.readthedocs.io"><img src="https://img.shields.io/badge/Discord.py-v2-5865F2?style=for-the-badge&logo=discord&logoColor=white"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-MIT-red?style=for-the-badge"/></a>
</p>

</div>

---

## ✦ Aperçu

Ce dossier contient le bot Discord **Haunted** construit avec `discord.py v2`, accompagné d'un backend `FastAPI` qui alimente le dashboard web. Tout tourne avec une seule commande : `python haunted.py`. Les messages sont en **français** (avec repli anglais) et chaque **module peut être activé/désactivé depuis le dashboard**.

```
bot/
├── api/                   Backend FastAPI (routes, schémas, gestionnaire BDD)
│   ├── modules_registry.py  Registre central des modules on/off
│   └── routes/            /bot  /guilds  /admin  /guilds/{id}/modules
├── cogs/
│   ├── antinuke/          Écouteurs d'événements de protection anti-nuke
│   ├── automod/           Écouteurs d'application de l'auto-modération
│   ├── commands/          Tous les modules de commandes slash & préfixe
│   ├── events/            Écouteurs d'événements Discord généraux
│   ├── moderation/        Modules d'actions de modération
│   └── zyrox/             Cogs des fonctionnalités cœur
├── core/                  Client du bot, contexte, classes Cog de base
├── games/                 Logique de jeux + vues à boutons
├── lang/                  Traductions (lang.en.json, lang.fr.json)
├── utils/                 Emojis, outils, sync, tunnel Cloudflare
│   ├── i18n.py              Helper de traduction FR/EN
│   └── modules.py           État on/off des modules (SQLite)
├── assets/                Polices, fonds, GIFs
└── haunted.py             Point d'entrée
```

---

## ✦ Fonctionnalités

<table>
<tr>
<td width="50%">

**🛡️ Anti-nuke**
- Détection de bans/kicks massifs, flood de salons & rôles
- Abus de webhooks, ajout de bots, protection prune
- Anti-modification de membres
- Système de whitelist / unwhitelist
- Mode verrouillage d'urgence

</td>
<td width="50%">

**🤖 Auto-modération**
- Anti-spam, anti-majuscules, anti-liens
- Anti-invitations, mentions de masse, spam d'emojis
- Entièrement configurable par serveur
- Compatible avec l'automod native de Discord

</td>
</tr>
<tr>
<td>

**🎵 Musique**
- Lecture via Lavalink v4
- Support YouTube, SoundCloud, JioSaavn
- File d'attente, boucle, mélange, lecture auto
- Contrôles avancer/reculer/position

</td>
<td>

**⚙️ Modération**
- Ban, kick, muet, avertissement, verrouillage, prison
- Snipe, gestion des messages
- Système complet de journaux
- Rôles à réactions, rôles vanity, suivi d'invitations

</td>
</tr>
<tr>
<td>

**🎉 Engagement**
- Niveaux & XP avec classement
- Suivi des anniversaires
- Counting, AFK, rôles auto, réponses auto
- Messages épinglés, avantages boosters, giveaways

</td>
<td>

**🎮 Jeux**
- Échecs, bataille navale, puissance 4
- Wordle, Typeracer, 2048, Memory
- Test de réaction, pierre-papier-ciseaux, morpion
- Devine-pays, taquin numérique, Lights out

</td>
</tr>
<tr>
<td>

**🌐 Backend API**
- FastAPI avec authentification par clé API
- Limitation de débit (SlowAPI)
- Journaux de requêtes JSON structurés
- CORS configuré pour le domaine du dashboard
- Variable `CORS_ORIGINS` pour les domaines supplémentaires
- Endpoints de modules : `GET/PATCH /guilds/{id}/modules`

</td>
<td>

**🔧 Développeur**
- Support d'évaluation Jishaku
- Sync auto des emojis d'application
- Commandes slash + préfixe
- Tunnel Cloudflare via pycloudflared — zéro installation, trafic illimité
- Une seule variable `OWNER_IDS` contrôle toutes les permissions
- Traductions FR/EN via `utils/i18n.py` (`BOT_LANG=fr` par défaut)

</td>
</tr>
</table>

---

## ✦ Prérequis

| Prérequis | Notes |
|---|---|
| Python 3.13 | image Pterodactyl `ghcr.io/ptero-eggs/yolks:python_3.13` |
| Nœud Lavalink v4 | pour la musique |
| Token du bot Discord | depuis le portail développeur |
| Compte Cloudflare (gratuit) | pour le tunnel HTTPS — config navigateur uniquement |

---

## ✦ Installation

> Version guidée (où trouver chaque valeur) : voir « Installation du bot » dans le `README.md` racine. Ici la version courte.

### 1 — Remplir le `.env` en premier

Créez un fichier `.env` (copié depuis `.env.example`) et remplissez **d'abord** les 4 valeurs obligatoires : `TOKEN` (onglet Bot du portail Discord), `OWNER_IDS` (votre ID Discord), `DASHBOARD_API_KEY` (secret inventé, à recopier côté dashboard), puis le tunnel Cloudflare (`CF_TUNNEL_TOKEN`, `CF_TUNNEL_URL`). Laissez le reste par défaut (voir le modèle annoté dans le README racine) :

```env
# ── Cœur ────────────────────────────────────────────────────────────
TOKEN              = votre_token_discord
brand_name         = 'Haunted'

# ── IDs propriétaires (séparés par des virgules, sans toucher au code)
OWNER_IDS          = 870179991462236170,767979794411028491

# ── Lavalink ────────────────────────────────────────────────────────
LAVALINK_HOST      = "votre-hote-lavalink"
LAVALINK_PASSWORD  = "votre_mot_de_passe"
LAVALINK_SECURE    = "true"
LAVALINK_PORT      = ""

# ── Sync des emojis ─────────────────────────────────────────────────
EMOJI_SYNC         = "false"

# ── API / Backend dashboard ─────────────────────────────────────────
API_ENABLED        = "true"
API_PORT           = "8000"
DASHBOARD_API_KEY  = "changez_ce_secret_robuste"
CORS_ORIGINS       = ""

# ── Tunnel Cloudflare ───────────────────────────────────────────────
TUNNEL_ENABLED     = "true"
CF_TUNNEL_TOKEN    = "votre_token_tunnel"
CF_TUNNEL_URL      = "https://api.votredomaine.com"

# ── Webhooks ────────────────────────────────────────────────────────
WEBHOOK_URL        = "https://discord.com/api/webhooks/..."

# ── Langue (fr ou en) ───────────────────────────────────────────────
BOT_LANG           = "fr"
```

### 2 — Installer les dépendances

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3 — Lancer

```bash
python haunted.py
```

✅ Vérifiez `Loaded & Online!` dans la console et copiez la ligne `NEXT_PUBLIC_API_URL` pour le dashboard.

---

## ✦ Référence des variables

| Variable | Défaut | Description |
|---|---|---|
| `TOKEN` | — | Token du bot Discord |
| `brand_name` | `Haunted` | Nom affiché du bot |
| `SUPPORT_SERVER` | `https://discord.gg/DvetGPq9q5` | Serveur Discord des liens « Support » (mettez le vôtre) |
| `OWNER_IDS` | — | IDs Discord des propriétaires, séparés par des virgules |
| `LAVALINK_HOST` | — | Hôte du serveur Lavalink (sans protocole) |
| `LAVALINK_PASSWORD` | — | Mot de passe Lavalink |
| `LAVALINK_SECURE` | `true` | `true` = HTTPS, `false` = HTTP |
| `LAVALINK_PORT` | _(vide)_ | Port — uniquement si `LAVALINK_SECURE=false` |
| `EMOJI_SYNC` | `false` | Synchroniser les emojis custom d'application (inutile : les emojis du bot sont Unicode) |
| `API_ENABLED` | `true` | Démarrer le backend FastAPI du dashboard |
| `API_PORT` | `8000` | Port d'écoute du backend |
| `DASHBOARD_API_KEY` | — | Secret partagé entre l'API du bot et le dashboard |
| `CORS_ORIGINS` | _(vide)_ | Origines CORS supplémentaires, séparées par des virgules |
| `WEBHOOK_URL` | — | Webhook Discord pour les journaux de commandes |
| `TUNNEL_ENABLED` | `true` | Exposer l'API en HTTPS via tunnel Cloudflare |
| `CF_TUNNEL_TOKEN` | — | Token depuis le tableau Cloudflare Zero Trust |
| `CF_TUNNEL_URL` | — | Votre URL publique permanente |
| `BOT_LANG` | `fr` | Langue des messages du bot (`fr` ou `en`) |

---

## ✦ Modules — activation / désactivation

Le registre unique `api/modules_registry.py` définit les 19 modules (`antinuke`, `automod`, `tickets`, `verification`, `welcome`, `invites`, `autorole`, `reactionroles`, `j2c`, `invcrole`, `vanityroles`, `autoreact`, `customroles`, `joindm`, `leveling`, `logging`, `games`, `music`, `moderation`).

- État stocké par serveur dans `db/modules.db` (`utils/modules.py`) — tout est **activé par défaut**.
- Endpoints : `GET /api/v1/guilds/{guild_id}/modules`, `PATCH /api/v1/guilds/{guild_id}/modules` (`{"modules": {"leveling": false}}`), `PATCH /api/v1/guilds/{guild_id}/modules/{clé}` (`{"enabled": false}`).
- Garde côté bot : `core/zyrox.py → invoke()` refuse les commandes des modules désactivés (message FR via `utils/i18n.py`). Chaque cog porte un attribut `module_key` ; la correspondance nom de cog → module est dans `COG_MODULE_MAP`.

---

## ✦ Tunnel HTTPS (Cloudflare)

Utilise **pycloudflared** — télécharge le binaire `cloudflared` automatiquement au premier lancement. Aucune installation système, aucune CLI, compatible Pterodactyl et tout hébergeur Python.

| | Tunnel Cloudflare | ngrok gratuit |
|---|---|---|
| Bande passante | Illimitée | 1 Go/mois |
| Requêtes | Illimitées | 10k/mois |
| Stabilité de l'URL | Permanente | Permanente (1 domaine) |
| Installation système | ❌ Inutile | ❌ Inutile |
| Coût | Gratuit | Gratuit |

**Configuration (navigateur uniquement) :**

1. Allez sur [one.dash.cloudflare.com](https://one.dash.cloudflare.com) → **Networks → Tunnels → Create a tunnel**
2. Choisissez **Cloudflared**, nommez-le (ex. `haunted-api`), enregistrez
3. Sur **Install connector**, copiez le token depuis la commande affichée :
   ```
   cloudflared tunnel run --token <COPIEZ_CE_TOKEN>
   ```
4. Onglet **Public Hostname** → ajoutez un nom d'hôte :
   - Subdomain : `api` · Domain : `votredomaine.com` · Service : `http://localhost:8000`
5. Ajoutez dans `.env` :
   ```env
   CF_TUNNEL_TOKEN = "eyJhIjoiXXXX..."
   CF_TUNNEL_URL   = "https://api.votredomaine.com"
   ```

À chaque démarrage, la console affiche :
```
◈ Tunnel: cloudflared binary ready — starting tunnel on port 8000…
◈ Tunnel: API is live at  https://api.votredomaine.com
  ↳ NEXT_PUBLIC_API_URL = https://api.votredomaine.com/api/v1
```

`TUNNEL_ENABLED=false` pour désactiver.

---

## ✦ Emojis

Tous les emojis du bot sont des **emojis Unicode classiques** : ils s'affichent partout sans upload ni synchronisation. Aucune action nécessaire.

L'utilitaire `EMOJI_SYNC` reste disponible si vous ajoutez vos propres emojis custom dans `bot/utils/emoji.py` : il les upload dans l'application Discord au démarrage et corrige les IDs.

---

## ✦ Déploiement (Pterodactyl)

Le bot se déploie sur un serveur **Pterodactyl** avec l'egg générique **python generic** et l'image **Python 3.13** (`ghcr.io/ptero-eggs/yolks:python_3.13`). C'est la seule méthode documentée.

**1 — Préparer l'egg (côté admin panel)**

- Vérifiez que l'egg *python generic* est importé (Nests → Import Egg → URL `https://eggs.pterodactyl.io/egg/generic-python-generic`).
- Créez un serveur avec cet egg et sélectionnez l'image Docker `Python 3.13`.

**2 — Récupérer les fichiers (méthode git, recommandée)**

- Dans l'onglet **Startup**, laissez `User Uploaded Files` (`USER_UPLOAD`) à `0` et renseignez :
  - `Git Repo Address` (`GIT_ADDRESS`) : `https://github.com/nohmaa/Haunted-AIO`
  - `Git Branch` (`BRANCH`) : `main`
  - `Auto Update` (`AUTO_UPDATE`) : `1`
- Le dépôt est cloné à la racine : le point d'entrée est donc `bot/haunted.py` et les dépendances `bot/requirements.txt`.

*Alternative — upload manuel : mettez `USER_UPLOAD` à `1` et uploadez via **Files** (ou SFTP) le **contenu de ce dossier `bot/`** à la racine du serveur. Dans ce cas `PY_FILE=haunted.py` et `REQUIREMENTS_FILE=requirements.txt`.*

**3 — Régler le démarrage**

| Variable | Valeur |
|---|---|
| `App py file` (`PY_FILE`) | `bot/haunted.py` |
| `Requirements file` (`REQUIREMENTS_FILE`) | `bot/requirements.txt` |

⚠️ Ne laissez pas `REQUIREMENTS_FILE` à `requirements.txt` : sans lui l'installation pip est silencieusement sautée (`ModuleNotFoundError` au démarrage).

L'egg installe les dépendances automatiquement à chaque (re)démarrage (`pip install -U -r bot/requirements.txt`).

**4 — Détection du démarrage**

Dans la **Start Configuration** de l'egg, la condition `done` doit contenir :

```
Loaded & Online!
```

**5 — Configurer et lancer**

- Créez le fichier `.env` (via **Files**) en copiant `.env.example`, puis renseignez au minimum `TOKEN`, `OWNER_IDS`, `DASHBOARD_API_KEY` et le tunnel Cloudflare.
- Onglet **Console** → **Start**.

---

## ✦ Dépannage

| Problème | Solution |
|---|---|
| Le bot ne démarre pas | Vérifiez `TOKEN` et les intents dans le portail développeur |
| Musique hors service | Vérifiez `LAVALINK_HOST`, `LAVALINK_SECURE`, `LAVALINK_PORT` |
| Le dashboard n'atteint pas l'API | Vérifiez `API_ENABLED=true` et `NEXT_PUBLIC_API_URL` côté dashboard |
| Erreurs CORS | Ajoutez l'URL de votre dashboard dans `CORS_ORIGINS` (`.env`) |
| Emojis affichés en texte brut | Les emojis sont désormais des emojis Unicode standards — vérifiez la version de Discord ou ajoutez vos emojis custom avec `EMOJI_SYNC=true` |
| Tunnel ne démarre pas | Vérifiez `CF_TUNNEL_TOKEN` et que `pycloudflared` est installé |
| Ajouter un propriétaire | Ajoutez son ID dans `OWNER_IDS` (`.env`) — sans toucher au code |
| Un module ne répond pas | Vérifiez qu'il est activé sur la page Modules du serveur |

---

<div align="center">

© 2026 Haunted — Licence MIT

</div>
