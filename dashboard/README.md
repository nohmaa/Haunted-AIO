<div align="center">

```
██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
```

<h3>Haunted Dashboard — Interface web Next.js</h3>

<p>
  <a href="https://nextjs.org"><img src="https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/></a>
  <a href="https://typescriptlang.org"><img src="https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white"/></a>
  <a href="https://tailwindcss.com"><img src="https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-MIT-red?style=for-the-badge"/></a>
</p>

</div>

---

## ✦ Aperçu

Ce dossier contient le dashboard web **Haunted** construit avec `Next.js 14` (App Router), `TypeScript` et `Tailwind CSS`. Il se connecte au backend FastAPI du bot via une URL HTTPS permanente (tunnel Cloudflare) et permet aux administrateurs de gérer tous les paramètres du bot depuis une interface élégante, **en français** — dont **l'activation/désactivation des modules par serveur**.

```
dashboard/
├── app/                       Pages App Router & routes API
│   ├── api/auth/              Callback OAuth NextAuth
│   ├── dashboard/             Zone principale du dashboard
│   │   ├── admin/             Panneau réservé aux admins
│   │   ├── guilds/            Sélection du serveur
│   │   └── guild/[guildId]/   Pages de paramètres par serveur
│   │       ├── modules/       Activation/désactivation des modules
│   │       ├── antinuke/
│   │       ├── automod/
│   │       ├── leveling/
│   │       ├── logging/
│   │       ├── tickets/
│   │       ├── welcome/
│   │       └── …autres
│   ├── docs/                  Page de documentation
│   ├── privacy/               Politique de confidentialité
│   └── terms/                 Conditions d'utilisation
├── components/
│   ├── dashboard/             Formulaires par fonctionnalité (dont modules-manager)
│   └── ui/                    Composants UI de base (button, card, input…)
├── hooks/                     Hooks React personnalisés
├── lib/                       Client API, config auth, utilitaires
└── types/                     Définitions de types TypeScript
```

---

## ✦ Fonctionnalités

- **Connexion Discord OAuth2** — authentification sécurisée, session gérée par NextAuth
- **Gestion par serveur** — antinuke, automod, leveling, logging, tickets, bienvenue, etc.
- **Modules on/off** — interrupteurs par serveur sur la page Modules (`getModules` / `setModule` dans `lib/api.ts`)
- **Stats du bot en direct** — métriques temps réel depuis le backend FastAPI
- **Panneau admin** — configuration et annonces réservées aux propriétaires
- **Entièrement personnalisable** — nom et abréviation via variables d'environnement
- **Prêt pour HTTPS** — se connecte à l'URL permanente du tunnel Cloudflare du bot
- **Prêt pour la production** — `npm run build` puis `npm start` sur toute machine avec Node.js 22+

---

## ✦ Prérequis

| Prérequis | Notes |
|---|---|
| Node.js 22+ (LTS) | — |
| Bot Haunted en ligne | avec `API_ENABLED=true` et `TUNNEL_ENABLED=true` |
| Application Discord OAuth | depuis le [portail développeur Discord](https://discord.com/developers/applications) |

---

## ✦ Installation

> Version guidée (où trouver chaque valeur) : voir « Installation du dashboard » dans le `README.md` racine.

### 1 — Remplir le `.env.local` en premier

Créez un fichier `.env.local` dans ce dossier (copié depuis `.env.example`). À remplir **avant** `npm install`, avec l'URL d'API affichée par le bot et la **même** clé API que côté bot :

```env
# ── API du bot ──────────────────────────────────────────────────────
# Utilisez l'URL du tunnel Cloudflare affichée dans la console du bot
NEXT_PUBLIC_API_URL           = https://api.votredomaine.com/api/v1
NEXT_PUBLIC_DASHBOARD_API_KEY = votre_cle_api_partagee   # doit correspondre à DASHBOARD_API_KEY du bot

# ── NextAuth ────────────────────────────────────────────────────────
NEXTAUTH_URL                  = http://localhost:3000
NEXTAUTH_SECRET               = une_chaine_aleatoire_longue   # générer : openssl rand -base64 32

# ── Discord OAuth ───────────────────────────────────────────────────
DISCORD_CLIENT_ID             = votre_client_id_oauth_discord
DISCORD_CLIENT_SECRET         = votre_client_secret_oauth_discord

# ── Personnalisation ────────────────────────────────────────────────
NEXT_PUBLIC_ADMIN_IDS         = votre_id_utilisateur_discord
NEXT_PUBLIC_BRAND_NAME        = "Haunted"
NEXT_PUBLIC_BRAND_NAME_WORD   = "H"
```

### 2 — Installer puis lancer

```bash
npm install
npm run dev
```

Ouvrez [http://localhost:3000](http://localhost:3000) et connectez-vous avec Discord.

---

## ✦ Référence des variables

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | URL complète du backend FastAPI du bot — utilisez l'URL du tunnel Cloudflare |
| `NEXT_PUBLIC_DASHBOARD_API_KEY` | Doit correspondre exactement à `DASHBOARD_API_KEY` dans le `.env` du bot |
| `NEXTAUTH_URL` | URL publique de votre dashboard (ex. `https://dashboard.votredomaine.com`) |
| `NEXTAUTH_SECRET` | Secret aléatoire pour la signature des sessions NextAuth |
| `DISCORD_CLIENT_ID` | ID client Discord OAuth2 |
| `DISCORD_CLIENT_SECRET` | Secret client Discord OAuth2 |
| `NEXT_PUBLIC_ADMIN_IDS` | IDs Discord des admins (panneau admin), séparés par des virgules |
| `NEXT_PUBLIC_BRAND_NAME` | Nom du bot affiché dans le dashboard |
| `NEXT_PUBLIC_BRAND_NAME_WORD` | Abréviation affichée dans le dashboard (ex. `H`) |

---

## ✦ Mise en production

Le dashboard ne tourne pas sur l'image Python de Pterodactyl (réservée au bot).

### Option A — Vercel (recommandé)

1. Sur [vercel.com](https://vercel.com) → **Add New → Project** → importez `Haunted-AIO` → **Root Directory** : `dashboard`.
2. Dans **Settings → Environment Variables**, ajoutez toutes les clés du tableau « Référence des variables » (avec les valeurs de production ci-dessous).
3. **Deploy** → notez l'URL. Si elle diffère de `NEXTAUTH_URL`, mettez à jour puis **Redeploy** (les `NEXT_PUBLIC_*` sont figées au build).
4. Dans Discord → votre application → **OAuth2 → Redirects**, ajoutez `https://votre-app.vercel.app/api/auth/callback/discord`.

### Option B — Node.js manuel

Sur toute machine avec Node.js 22+ :

```bash
npm run build
npm start   # écoute sur http://localhost:3000 par défaut
```

**Étape 1 — Variables d'environnement**

Renseignez les mêmes clés que dans `.env.local`, avec les valeurs de production :

| Variable | Valeur en production |
|---|---|
| `NEXT_PUBLIC_API_URL` | `https://api.votredomaine.com/api/v1` |
| `NEXTAUTH_URL` | `https://dashboard.votredomaine.com` |
| `NEXTAUTH_SECRET` | [générez-en un](https://generate-secret.vercel.app/32) |
| `DISCORD_CLIENT_ID` | depuis le [portail développeur Discord](https://discord.com/developers/applications) |

**Étape 2 — URI de redirection dans Discord**

Dans votre application Discord → **OAuth2 → Redirects** → ajoutez :

```
https://dashboard.votredomaine.com/api/auth/callback/discord
```

**Étape 3 — Lancer**

```bash
npm run build && npm start
```

Pour le dev local, `NEXTAUTH_URL=http://localhost:3000` et l'URI `http://localhost:3000/api/auth/callback/discord`.

---

## ✦ Connexion à l'API du bot

Le dashboard lit l'URL de l'API depuis `NEXT_PUBLIC_API_URL`.

| Environnement | Valeur |
|---|---|
| Dev local | `http://localhost:8000/api/v1` |
| Production | `https://api.votredomaine.com/api/v1` (URL du tunnel Cloudflare) |

Le bot affiche l'URL confirmée à chaque démarrage :
```
◈ Tunnel: API is live at  https://api.votredomaine.com
  ↳ NEXT_PUBLIC_API_URL = https://api.votredomaine.com/api/v1
```

Cette URL est permanente — elle ne change jamais entre les redémarrages tant que le token du tunnel Cloudflare reste le même.

---

## ✦ Dépannage

| Problème | Solution |
|---|---|
| Erreur d'auth à la connexion | Vérifiez l'ID/secret OAuth Discord et l'URI de redirection dans le portail développeur |
| Le dashboard ne charge pas les données | Vérifiez que le bot tourne avec `API_ENABLED=true` et que `NEXT_PUBLIC_API_URL` est correct |
| Erreur CORS dans le navigateur | Ajoutez l'URL de votre dashboard dans `CORS_ORIGINS` (`.env` du bot) |
| Erreur `NEXTAUTH_SECRET` | Vérifiez que `NEXTAUTH_SECRET` est défini et non vide |
| Clé API rejetée (401) | `NEXT_PUBLIC_DASHBOARD_API_KEY` doit correspondre exactement à `DASHBOARD_API_KEY` du bot |
| L'URL du tunnel a changé | Les tunnels nommés Cloudflare gardent la même URL — vérifiez `CF_TUNNEL_TOKEN` |
| Un module ne s'active pas | Vérifiez la réponse de `PATCH /guilds/{id}/modules/{clé}` et les logs de l'API |

---

<div align="center">

© 2026 Haunted — Licence MIT

</div>
