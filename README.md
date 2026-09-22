<div align="center">

```
██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
```

<h3>Un bot Discord riche en fonctionnalités, piloté depuis un dashboard Next.js élégant</h3>

<p>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="https://nextjs.org"><img src="https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/></a>
  <a href="https://discordpy.readthedocs.io"><img src="https://img.shields.io/badge/Discord.py-v2-5865F2?style=for-the-badge&logo=discord&logoColor=white"/></a>
</p>
<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-MIT-red?style=for-the-badge"/></a>
  <a href="https://github.com/nohmaa/ZyroX-CV2-AIO-With-Dashboard"><img src="https://img.shields.io/badge/GitHub-Haunted-181717?style=for-the-badge&logo=github&logoColor=white"/></a>
</p>

</div>

---

## ✦ Aperçu

**Haunted** est un bot Discord complet, accompagné d'un dashboard web moderne pour tout gérer : de l'anti-nuke à la musique. Construit avec `discord.py v2`, `FastAPI` et `Next.js 14` + Tailwind CSS. L'interface (bot et dashboard) est en **français**, et chaque **module peut être activé ou désactivé depuis le dashboard**, serveur par serveur.

> Basé sur [ZyroX-CV2](https://github.com/RayExo) par CodeX Devs — renommé, traduit et étendu (voir `SUIVI_HAUNTED.md`).

```
Haunted/
├── 🤖  bot/                   Bot Discord Python + backend FastAPI
│   ├── api/                   API REST du dashboard (FastAPI)
│   │   ├── modules_registry.py  Registre central des modules on/off
│   │   └── routes/modules.py    Endpoints GET/PATCH des modules
│   ├── cogs/                  Toutes les fonctionnalités (commandes, events, antinuke, automod…)
│   ├── core/                  Client du bot, contexte, classe Cog de base
│   ├── lang/                  Traductions (lang.en.json, lang.fr.json)
│   ├── utils/                 Utilitaires partagés (emoji, outils, sync, tunnel Cloudflare…)
│   │   ├── i18n.py              Helper de traduction FR/EN
│   │   └── modules.py           État on/off des modules (SQLite)
│   ├── games/                 Modules de jeux autonomes
│   ├── assets/                Polices, fonds, GIFs
│   └── CodeX.py               Point d'entrée
│
├── 🌐  dashboard/             Frontend Next.js (en français)
│   ├── app/                   Pages App Router & routes API
│   │   └── dashboard/guild/[guildId]/modules/  Page d'activation des modules
│   ├── components/            Composants UI réutilisables
│   │   └── dashboard/modules-manager.tsx  Interrupteurs on/off par module
│   ├── hooks/                 Hooks React personnalisés
│   ├── lib/                   Helpers API & utilitaires
│   └── types/                 Définitions TypeScript
│
└── 📝  SUIVI_HAUNTED.md       Journal des modifications (pour les agents IA/humains)
```

---

## ✦ Fonctionnalités

<table>
<tr>
<td width="50%">

**🛡️ Sécurité**
- Anti-nuke — ban, kick, flood de salons & rôles, abus de webhooks, ajouts de bots, prune
- Auto-modération — spam, majuscules, liens, invitations, mentions de masse, spam d'emojis
- Protection contre les modifications de membres
- Système de whitelist / unwhitelist
- Mode verrouillage d'urgence

</td>
<td width="50%">

**🎵 Musique**
- Lecture via Lavalink v4
- Recherche YouTube, SoundCloud, JioSaavn
- File d'attente, boucle, lecture auto, mélange
- Contrôles avancer/reculer/position
- Entièrement configurable via `.env`

</td>
</tr>
<tr>
<td>

**⚙️ Gestion**
- Modération — ban, kick, muet, avertissement, verrouillage, prison, etc.
- Système complet de journaux
- Rôles à réactions, rôles vanity, suivi d'invitations
- Tickets, giveaways, vérification
- Salons vocaux temporaires (Join-to-Create)

</td>
<td>

**🌐 Dashboard**
- Connexion via Discord OAuth2
- Gestion des paramètres par serveur
- **Activation/désactivation des modules par serveur**
- Statistiques du bot en direct
- Entièrement personnalisable (nom, abréviation)
- HTTPS via tunnel Cloudflare (URL permanente)
- Déployable sur Vercel en quelques minutes

</td>
</tr>
<tr>
<td>

**🎉 Engagement**
- Système de niveaux & XP avec classement
- Suivi des anniversaires
- 12+ mini-jeux (échecs, bataille navale, wordle, 2048…)
- AFK, rôles auto, réponses auto, messages épinglés
- Counting, blackjack, slots, avantages boosters

</td>
<td>

**🔧 Développeur**
- Synchronisation auto des emojis d'application au démarrage
- Support d'évaluation Jishaku
- Commandes slash + préfixe
- Backend FastAPI avec clé API + limitation de débit
- Tunnel Cloudflare — bande passante illimitée, URL permanente
- Traductions FR/EN (`bot/lang/`, `bot/utils/i18n.py`)

</td>
</tr>
</table>

---

## ✦ Prérequis

| Prérequis | Version / Notes |
|---|---|
| Python | 3.10 ou supérieur |
| Node.js | 18 ou supérieur |
| Nœud Lavalink | v4 |
| Token du bot Discord | — |
| Application Discord OAuth | pour la connexion au dashboard |
| Compte Cloudflare (gratuit) | pour le tunnel HTTPS |

---

## ✦ Installation du bot

**1 — Cloner le dépôt**

```bash
git clone https://github.com/nohmaa/ZyroX-CV2-AIO-With-Dashboard
cd ZyroX-CV2-AIO-With-Dashboard/bot
```

**2 — Installer les dépendances**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

**3 — Configurer l'environnement**

Copiez `.env.example` vers `.env` et renseignez les valeurs :

```env
# ── Cœur ────────────────────────────────────────────────────────────
TOKEN              = votre_token_discord
brand_name         = 'Haunted'

# ── IDs propriétaires (séparés par des virgules) ────────────────────
OWNER_IDS          = 870179991462236170,767979794411028491

# ── Lavalink ────────────────────────────────────────────────────────
LAVALINK_HOST      = "votre-hote-lavalink"
LAVALINK_PASSWORD  = "votre_mot_de_passe"
LAVALINK_SECURE    = "true"
LAVALINK_PORT      = ""

# ── Sync des emojis ─────────────────────────────────────────────────
EMOJI_SYNC         = "true"

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
```

**4 — Lancer le bot**

```bash
python CodeX.py
```

---

## ✦ Installation du dashboard

**1 — Installer les dépendances**

```bash
cd dashboard
npm install
```

**2 — Configurer l'environnement**

Copiez `.env.example` vers `.env.local` :

```env
NEXT_PUBLIC_API_URL           = https://api.votredomaine.com/api/v1
NEXT_PUBLIC_DASHBOARD_API_KEY = votre_cle_api_partagee

NEXTAUTH_URL                  = http://localhost:3000
NEXTAUTH_SECRET               = une_chaine_aleatoire_longue

DISCORD_CLIENT_ID             = votre_client_id_oauth_discord
DISCORD_CLIENT_SECRET         = votre_client_secret_oauth_discord

NEXT_PUBLIC_ADMIN_IDS         = votre_id_utilisateur_discord
NEXT_PUBLIC_BRAND_NAME        = "Haunted"
NEXT_PUBLIC_BRAND_NAME_WORD   = "H"
```

**3 — Lancer en local**

```bash
npm run dev
```

Ouvrez [http://localhost:3000](http://localhost:3000)

---

## ✦ Référence des variables

### Bot — `bot/.env`

| Variable | Défaut | Description |
|---|---|---|
| `TOKEN` | — | Token du bot Discord |
| `brand_name` | `Haunted` | Nom affiché du bot |
| `OWNER_IDS` | — | IDs Discord des propriétaires, séparés par des virgules |
| `LAVALINK_HOST` | — | Hôte du serveur Lavalink (sans protocole) |
| `LAVALINK_PASSWORD` | — | Mot de passe Lavalink |
| `LAVALINK_SECURE` | `true` | `true` = HTTPS, `false` = HTTP |
| `LAVALINK_PORT` | _(vide)_ | Port — uniquement si `LAVALINK_SECURE=false` |
| `EMOJI_SYNC` | `true` | Synchroniser les emojis d'application au démarrage |
| `API_ENABLED` | `true` | Démarrer le backend FastAPI du dashboard |
| `API_PORT` | `8000` | Port d'écoute du backend |
| `DASHBOARD_API_KEY` | — | Secret partagé entre l'API du bot et le dashboard |
| `CORS_ORIGINS` | _(vide)_ | Origines CORS supplémentaires, séparées par des virgules |
| `WEBHOOK_URL` | — | Webhook Discord pour les journaux de commandes |
| `TUNNEL_ENABLED` | `true` | Exposer l'API en HTTPS via tunnel Cloudflare |
| `CF_TUNNEL_TOKEN` | — | Token depuis le tableau Cloudflare Zero Trust |
| `CF_TUNNEL_URL` | — | Votre URL publique permanente (ex. `https://api.votredomaine.com`) |
| `BOT_LANG` | `fr` | Langue des messages du bot (`fr` ou `en`) |

### Dashboard — `dashboard/.env.local`

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | URL complète du backend FastAPI — utilisez l'URL du tunnel Cloudflare |
| `NEXT_PUBLIC_DASHBOARD_API_KEY` | Doit correspondre à `DASHBOARD_API_KEY` du bot |
| `NEXTAUTH_URL` | URL publique de votre dashboard |
| `NEXTAUTH_SECRET` | Secret aléatoire pour la signature des sessions NextAuth |
| `DISCORD_CLIENT_ID` | ID client Discord OAuth2 |
| `DISCORD_CLIENT_SECRET` | Secret client Discord OAuth2 |
| `NEXT_PUBLIC_ADMIN_IDS` | IDs Discord des administrateurs, séparés par des virgules |
| `NEXT_PUBLIC_BRAND_NAME` | Nom du bot affiché dans le dashboard |
| `NEXT_PUBLIC_BRAND_NAME_WORD` | Abréviation affichée dans le dashboard |

---

## ✦ Modules — activation / désactivation

Depuis le dashboard, page **Modules** d'un serveur : chaque module possède un interrupteur. Un module désactivé ne répond plus aux commandes sur ce serveur (message en français) ; les autres serveurs ne sont pas affectés. Tous les modules sont **activés par défaut**.

| Module | Clé | Page dashboard |
|---|---|---|
| Anti-Nuke | `antinuke` | `antinuke` |
| Auto-modération | `automod` | `automod` |
| Tickets | `tickets` | `tickets` |
| Vérification | `verification` | `verification` |
| Bienvenue | `welcome` | `welcome` |
| Invitations | `invites` | `invites` |
| Rôles automatiques | `autorole` | `autorole` |
| Rôles à réactions | `reactionroles` | `reactionroles` |
| Salons temporaires | `j2c` | `j2c` |
| Rôle vocal | `invcrole` | `invcrole` |
| Rôles vanity | `vanityroles` | `vanityroles` |
| Réactions auto | `autoreact` | `autoreact` |
| Rôles personnalisés | `customroles` | `customroles` |
| MP de bienvenue | `joindm` | `joindm` |
| Niveaux & XP | `leveling` | `leveling` |
| Journaux | `logging` | `logging` |
| Jeux & fun | `games` | (page Modules uniquement) |
| Musique | `music` | (page Modules uniquement) |
| Modération | `moderation` | (page Modules uniquement) |

**Côté technique :**
- Registre unique : `bot/api/modules_registry.py` (`MODULES`, `COG_MODULE_MAP`)
- État par serveur en SQLite : `db/modules.db` (`bot/utils/modules.py`)
- Endpoints : `GET /api/v1/guilds/{guild_id}/modules`, `PATCH /api/v1/guilds/{guild_id}/modules`, `PATCH /api/v1/guilds/{guild_id}/modules/{clé}` avec `{"enabled": true/false}`
- Garde côté bot : `zyrox.invoke()` refuse les commandes des modules désactivés (chaque cog porte un attribut `module_key`)

---

## ✦ Tunnel HTTPS (Cloudflare)

Le bot utilise **pycloudflared** — le binaire `cloudflared` est téléchargé automatiquement au premier lancement. Aucune installation système, aucun paquet — fonctionne sur Pterodactyl et tout hébergeur Python.

**Pourquoi Cloudflare plutôt que ngrok :**
- ✅ Bande passante & requêtes illimitées — sans plafonds mensuels
- ✅ URL permanente qui ne change jamais entre les redémarrages
- ✅ Gratuit — aucun abonnement requis
- ✅ Zéro installation système — binaire téléchargé via Python

**Configuration (navigateur uniquement, pas de CLI) :**

1. Allez sur [one.dash.cloudflare.com](https://one.dash.cloudflare.com) → **Networks → Tunnels → Create a tunnel**
2. Choisissez **Cloudflared**, donnez-lui un nom (ex. `haunted-api`), enregistrez
3. À l'étape **Install connector**, copiez le token depuis la commande affichée :
   ```
   cloudflared tunnel run --token <COPIEZ_CECI>
   ```
4. Onglet **Public Hostname** → ajoutez un nom d'hôte :
   - Subdomain : `api` · Domain : `votredomaine.com` · Service : `http://localhost:8000`
5. Ajoutez dans `bot/.env` :
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

---

## ✦ Déploiement

### 🤖 Bot — tout hébergeur Python

1. Uploadez tout le dossier `bot/` sur votre hébergeur (Pterodactyl, Render, Railway, Fly.io, VPS…)
2. Commande de démarrage : `python CodeX.py`
3. Ajoutez toutes les variables d'environnement
4. `pycloudflared` télécharge le binaire automatiquement au premier lancement — rien d'autre à faire

### 🌐 Dashboard — Vercel

1. Allez sur [vercel.com](https://vercel.com) → **Add New Project** → connectez votre dépôt GitHub
2. Dossier racine : `dashboard/`
3. Ajoutez toutes les variables d'environnement dans **Settings → Environment Variables**
4. Ajoutez l'URI de redirection OAuth dans le portail développeur Discord :
   ```
   https://votre-app.vercel.app/api/auth/callback/discord
   ```
5. Cliquez **Deploy** — terminé ✓

---

## ✦ Sync des emojis

Tourne automatiquement au démarrage quand `EMOJI_SYNC=true` :

```
★ Starting Application Emoji Sync — 144 unique emojis found in emoji.py
◈ Found 144 templates | Application hosts 202 emojis
↑ Uploading: ztick  (not in application emojis)
✔ Uploaded: ztick  [saved as ID: 1234567890]
✔ emoji.py patched in-place to reflect current API state.
★ Restarting bot to load updated emoji IDs...
```

| Événement | Action |
|---|---|
| Nouvel emoji trouvé | Uploadé dans l'application, ID écrit dans `emoji.py` |
| ID obsolète détecté | `emoji.py` corrigé automatiquement |
| Aucun changement | Sync instantanée, pas de redémarrage |
| Après toute correction | Le bot redémarre pour charger les nouveaux IDs |

---

## ✦ Dépannage

| Problème | Solution |
|---|---|
| Le bot ne démarre pas | Vérifiez `TOKEN` et les intents dans le portail développeur |
| Musique hors service | Vérifiez `LAVALINK_HOST`, `LAVALINK_SECURE` et `LAVALINK_PORT` |
| Erreur d'auth du dashboard | Vérifiez l'ID/secret OAuth Discord et l'URI de redirection |
| Le dashboard ne charge pas les données | Vérifiez `API_ENABLED=true`, bot en ligne, `NEXT_PUBLIC_API_URL` correct |
| Un module ne répond pas | Vérifiez qu'il est **activé** sur la page Modules du serveur |
| Emojis affichés en texte brut | Lancez une fois avec `EMOJI_SYNC=true` |
| Erreurs CORS depuis le dashboard | Ajoutez votre URL Vercel dans `CORS_ORIGINS` (`bot/.env`) |
| Tunnel ne démarre pas | Vérifiez `CF_TUNNEL_TOKEN` et que `pycloudflared` est installé |
| URL du tunnel a changé | Renseignez `CF_TUNNEL_URL` — les tunnels nommés gardent la même URL |

---

## ✦ Sécurité

- Ne commitez jamais les fichiers `.env` — `.gitignore` les couvre déjà
- Utilisez un `NEXTAUTH_SECRET` et un `DASHBOARD_API_KEY` forts et uniques
- Regénérez tout secret accidentellement exposé
- L'API du bot est toujours protégée par clé API — ne l'exposez jamais sans elle

---

## ✦ Suivi des modifications

Toutes les modifications (traduction, rebranding, modules) sont journalisées dans [`SUIVI_HAUNTED.md`](SUIVI_HAUNTED.md) — point d'entrée obligatoire pour tout agent IA ou humain qui intervient sur le projet.

---

<div align="center">

## ✦ Haunted

*Conçu pour protéger. Pensé pour durer.*

Basé sur ZyroX-CV2 par CodeX Devs — voir `SUIVI_HAUNTED.md`.

© 2026 Haunted — Licence MIT

</div>
