# **All-jellyfin-media-server**

<div style="text-align: center">
    <img src="image/Isyrr.png" style="margin: 15px 10px;">
</div>


Bienvenue dans le dépôt All-jellyfin-media-server ! Ce dépôt contient tout ce dont vous avez besoin pour créer votre propre serveur média Jellyfin avec Sonarr, Radarr, Jellyseerr, Prowlarr, Jackett, qBittorrent et Gluetun (VPN) dans une configuration Docker Compose. Nous désignerons l’ensemble de ces conteneurs sous le nom **Isyrr** pour simplifier.

> [!NOTE]
> **Ceci est un fork personnalisé.** En plus de la stack d'origine, il ajoute :
> - **Bazarr** – téléchargement automatique de sous-titres pour Radarr/Sonarr
> - **Translatarr** – traduction automatique des sous-titres
> - **Tailscale** – expose Jellyfin / Jellyseerr (et les interfaces livres audio) sur un tailnet privé au lieu de publier les ports sur le LAN
> - **qbit-port-sync** – injecte automatiquement le port forwardé par Gluetun dans qBittorrent
> - **Stack livres audio** – Audiobookshelf (lecteur/bibliothèque), Shelfarr (demandes + import, le Jellyseerr des livres) et Chaptarr (surveillance optionnelle, façon Radarr), en réutilisant le Prowlarr + qBittorrent existants
>
> Voir [**Services ajoutés**](#services-ajoutés-fork) et [**Livres audio**](#livres-audio) plus bas, ainsi que les fichiers compose dans [`compose_files/VPN-Only/`](compose_files/VPN-Only/) (`tailscale-docker-compose.yaml`, `tailscale-docker-compose-audiobooks.yaml`).

![](https://img.shields.io/github/stars/Morzomb/All-jellyfin-media-server.svg)
![](https://img.shields.io/github/forks/Morzomb/All-jellyfin-media-server.svg)
![](https://img.shields.io/github/release/Morzomb/All-jellyfin-media-server.svg) 
![](https://img.shields.io/github/issues/Morzomb/All-jellyfin-media-server.svg)
[![GitHub last commit](https://img.shields.io/github/last-commit/Morzomb/All-jellyfin-media-server.svg)](https://github.com/Morzomb/All-jellyfin-media-server/commits/master)
![GitHub repo size](https://img.shields.io/github/repo-size/Morzomb/All-jellyfin-media-server)
![visitors](https://visitor-badge.laobi.icu/badge?page_id=Morzomb.All-jellyfin-media-server.id)

> [!NOTE] 
> **Access the repository in [English](README.md)**

## **Table des matières**

- [**All-jellyfin-media-server**](#all-jellyfin-media-server)
  - [**Table des matières**](#table-des-matières)
  - [**À quoi sert Isyrr ?**](#à-quoi-sert-isyrr-)
    - [**Jellyfin**](#jellyfin)
    - [**Jellyseerr**](#jellyseerr)
    - [**Sonarr**](#sonarr)
    - [**Radarr**](#radarr)
    - [**Jackett**](#jackett)
    - [**Flaresolverr**](#flaresolverr)
    - [**Prowlarr**](#prowlarr)
    - [**qBittorrent**](#qbittorrent)
    - [**Bazarr**](#bazarr)
    - [**Gluetun (VPN)**](#gluetun-vpn)
  - [**Services ajoutés (fork)**](#services-ajoutés-fork)
    - [**Bazarr**](#bazarr)
    - [**Translatarr**](#translatarr)
    - [**Tailscale**](#tailscale)
    - [**qbit-port-sync**](#qbit-port-sync)
  - [**Livres audio**](#livres-audio)
    - [**Audiobookshelf**](#audiobookshelf)
    - [**Shelfarr**](#shelfarr)
    - [**Chaptarr**](#chaptarr)
- [**Prérequis**](#prérequis)
  - [**Docker**](#docker)
    - [**Utiliser Docker Compose :**](#utiliser-docker-compose-)
  - [**NVIDIA**](#nvidia)
    - [**Première méthode**](#première-méthode)
  - [**Vérification finale**](#vérification-finale)
  - [**Deuxième méthode**](#deuxième-méthode)
- [**VPN**](#vpn)
  - [**NORD**](#nord)
  - [**PROTON**](#proton)
  - [**Dépannage VPN**](#dépannage-vpn)
- [**Installation**](#installation)
  - [**🚀 Installation Automatique (Recommandée)**](#-installation-automatique-recommandée)
    - [**Prérequis**](#prérequis-1)
    - [**Menu du Script d'Installation**](#menu-du-script-dinstallation)
    - [**Ajouter des Services Personnalisés**](#ajouter-des-services-personnalisés)
      - [**Étape 1 : Créer le Modèle YAML du Service**](#étape-1--créer-le-modèle-yaml-du-service)
      - [**Étape 2 : Ajouter la Sélection du Service dans setup-fr.sh**](#étape-2--ajouter-la-sélection-du-service-dans-setup-frsh)
      - [**Étape 3 : Mettre à Jour la Génération de docker-compose**](#étape-3--mettre-à-jour-la-génération-de-docker-compose)
      - [**Étape 4 : Créer le Dossier de Configuration**](#étape-4--créer-le-dossier-de-configuration)
      - [**Étape 5 : Sauvegarder l'État de Configuration**](#étape-5--sauvegarder-létat-de-configuration)
      - [**Étape 6 : Ajouter la Configuration Post-Installation (Optionnel)**](#étape-6--ajouter-la-configuration-post-installation-optionnel)
      - [**Étape 7 : Ajouter à Tous les Fichiers Docker Compose**](#étape-7--ajouter-à-tous-les-fichiers-docker-compose)
      - [**Étape 8 : Mettre à Jour la Documentation README**](#étape-8--mettre-à-jour-la-documentation-readme)
      - [**Étape 9 : Tester l'Intégration**](#étape-9--tester-lintégration)
  - [**Installation Manuelle**](#installation-manuelle)
  - [**1. Installation de base**](#1-installation-de-base)
  - [**2. Installation avec uniquement NVIDIA**](#2-installation-avec-uniquement-nvidia)
  - [**3. Installation avec NVIDIA et VPN**](#3-installation-avec-nvidia-et-vpn)
  - [**4. Installation avec VPN (sans NVIDIA)**](#4-installation-avec-vpn-sans-nvidia)
  - [**5. Installation avec Tailscale (+ Livres audio)**](#5-installation-avec-tailscale--livres-audio)
- [**Accéder aux Applications**](#accéder-aux-applications)
- [**Guide de Configuration pour les Interfaces Web uniquement**](#guide-de-configuration-pour-les-interfaces-web-uniquement)
  - [**qBittorrent**](#qbittorrent-1)
    - [**Configuration des Catégories**](#configuration-des-catégories)
  - [**Radarr**](#radarr-1)
    - [**Gestion des Médias**](#gestion-des-médias)
    - [**Clients de Téléchargement**](#clients-de-téléchargement)
    - [**Indexer Jackett (Optionnelle)**](#indexer-jackett-optionnelle)
  - [**Sonarr**](#sonarr-1)
    - [**Gestion des Médias**](#gestion-des-médias-1)
    - [**Clients de Téléchargement**](#clients-de-téléchargement-1)
    - [**Indexer Jackett (Optionnelle)**](#indexer-jackett-optionnelle-1)
  - [**Prowlarr**](#prowlarr-1)
    - [**Configurer les Indexeurs de Torrents**](#configurer-les-indexeurs-de-torrents)
    - [**Configurer FlareSolverr**](#configurer-flaresolverr)
    - [**Configurer Radarr**](#configurer-radarr)
    - [**Configurer Sonarr**](#configurer-sonarr)
  - [**Jellyfin**](#jellyfin-1)
    - [**Configuration Initiale**](#configuration-initiale)
    - [**Ajouter des utilisateurs à Jellyfin**](#ajouter-des-utilisateurs-à-jellyfin)
  - [**Jellyseerr**](#jellyseerr-1)
    - [**Connexion / Configuration**](#connexion--configuration)
    - [**Intégration avec Radarr**](#intégration-avec-radarr)
    - [**Intégration avec Sonarr**](#intégration-avec-sonarr)
  - [**Bazarr**](#bazarr-1)
    - [**Configuration Initiale**](#configuration-initiale-1)
    - [**Configurer l'Intégration Sonarr**](#configurer-lintégration-sonarr)
    - [**Configurer l'Intégration Radarr**](#configurer-lintégration-radarr)
    - [**Configurer les Fournisseurs de Sous-titres**](#configurer-les-fournisseurs-de-sous-titres)
    - [**Configurer les Langues**](#configurer-les-langues)
    - [**Configurer les Sous-titres**](#configurer-les-sous-titres)
  - [**Tailscale**](#tailscale-1)
  - [**Livres audio (Audiobookshelf / Shelfarr / Chaptarr)**](#livres-audio-audiobookshelf--shelfarr--chaptarr)
- [**Mise à jour des applications**](#mise-à-jour-des-applications)
- [**Avertissement**](#avertissement)

## **À quoi sert Isyrr ?**

Ce dépôt vous permet de créer votre propre serveur média Jellyfin avec tous les outils nécessaires pour gérer vos films, séries TV, musique et eBooks. Il inclut également des outils pour automatiser le téléchargement de nouveaux contenus et protéger votre confidentialité grâce à un VPN.

Isyrr utilise Docker et Docker Compose pour déployer les services. Les fichiers Docker Compose se trouvent dans les répertoires avec-vpn et sans-vpn.

> [!IMPORTANT]  
> Pour utiliser Docker Compose, assurez-vous que Docker est installé sur votre système.

---

### **Jellyfin**

[Jellyfin](https://jellyfin.org/) est un logiciel de serveur multimédia open-source qui vous permet de diffuser vos films, séries TV, musique et eBooks sur tous vos appareils. Il est compatible avec de nombreux types de fichiers multimédia et prend en charge le streaming vers divers appareils.

<div style="text-align: center">
    <img src="https://jellyfin.org/images/logo.svg" width="300" height="100"  style="margin: 15px 10px;">
</div>

### **Jellyseerr**

[Jellyseerr](https://github.com/Fallenbagel/jellyseerr) est une application open-source qui vous permet d'automatiser la gestion de votre serveur multimédia Jellyfin. Elle fonctionne en surveillant votre bibliothèque Jellyfin et en recherchant et téléchargeant automatiquement de nouveaux contenus en fonction de vos préférences. Jellyseerr prend en charge l'intégration avec divers autres outils, tels que Sonarr et Radarr, pour offrir une expérience fluide dans la gestion de votre collection multimédia.

<div style="text-align: center"> 
    <img src="https://raw.githubusercontent.com/Fallenbagel/jellyseerr/develop/public/logo_full.svg" width="300" height="100" style="margin: 15px 10px;"> 
</div>

### **Sonarr**

[Sonarr](https://sonarr.tv/) est un logiciel de gestion de séries TV qui vous permet de rechercher, télécharger et gérer automatiquement vos séries TV préférées. Il fonctionne avec de nombreux types de trackers et de clients torrent et prend en charge le téléchargement automatique de sous-titres.

<div style="text-align: center">
    <img src="image/sonarr/sonarr.png" width="300" height="100" style="margin: 15px 10px;">
</div>

### **Radarr**

[Radarr](https://radarr.video/) est un logiciel de gestion de films qui vous permet de rechercher, télécharger et gérer automatiquement vos films préférés. Il fonctionne avec de nombreux types de trackers et de clients torrent et prend en charge le téléchargement automatique de sous-titres.

<div style="text-align: center">
    <img src="https://warlord0blog.files.wordpress.com/2022/01/radarr_logo-1.png" width="300" height="100" style="margin: 15px 10px;">
</div>

### **Jackett**

[Jackett](https://github.com/Jackett/Jackett) est un logiciel proxy pour les trackers torrent qui vous permet de rechercher des fichiers torrent sur de nombreux trackers depuis un seul endroit. Il fonctionne avec de nombreux types de clients torrent et prend en charge l'authentification ainsi que la recherche avancée.

<div style="text-align: center">
    <img src="https://avatars.githubusercontent.com/u/15383019?s=280&v=4" width="100" height="100" style="margin: 15px 10px;">
</div>

### **Flaresolverr**

[Flaresolverr](https://github.com/FlareSolverr/FlareSolverr) est un logiciel open-source qui vous permet de contourner les restrictions de streaming sur les sites de partage de vidéos. Il fonctionne en résolvant les liens de streaming et en contournant les blocages géographiques et les restrictions de lecture.

<div style="text-align: center">
    <img src="https://avatars.githubusercontent.com/u/75936191?v=4" width="200" height="200" style="margin: 15px 10px;">
</div>

### **Prowlarr**

[Prowlarr](https://github.com/Prowlarr/Prowlarr) est un logiciel de gestion des téléchargements qui vous permet de rechercher et de télécharger automatiquement des fichiers provenant de diverses sources, y compris des trackers torrent, des newsgroups et des sites de téléchargement direct.

<div style="text-align: center">
    <img src="https://prowlarr.com/logo/128.png" width="100" height="100" style="margin: 15px 10px;">
</div>

### **qBittorrent**

[qBittorrent](https://www.qbittorrent.org/) est un logiciel open-source de client BitTorrent qui vous permet de télécharger des fichiers torrent. Il est léger, facile à utiliser et prend en charge de nombreuses fonctionnalités avancées telles que la recherche de torrents intégrée, le chiffrement, la création de torrents et la prise en charge des trackers privés.

<div style="text-align: center">
    <img src="https://a.fsdn.com/allura/p/qbittorrent/icon?1518743661?&w=90" width="100" height="100" style="margin: 15px 10px;">
</div>

### **Bazarr**

[Bazarr](https://www.bazarr.media/) est une application complémentaire à Sonarr et Radarr qui gère et télécharge les sous-titres en fonction de vos préférences. Il utilise les fichiers vidéo stockés par Sonarr et Radarr pour rechercher et télécharger les sous-titres dans la/les langue(s) de votre choix. Bazarr supporte plus de 60 langues et s'intègre parfaitement à votre flux de travail de gestion des médias existant.

<div style="text-align: center">
    <img src="https://www.bazarr.media/assets/img/logo.png" width="200" height="100" style="margin: 15px 10px;">
</div>

### **Gluetun (VPN)**

[Gluetun](https://github.com/qdm12/gluetun) est un logiciel open-source de client VPN qui vous permet de vous connecter à des serveurs VPN. Il est facile à utiliser et prend en charge de nombreuses fonctionnalités avancées telles que le transfert de port, la protection contre les fuites DNS et la prise en charge de plusieurs protocoles VPN.

<div style="text-align: center">
  <img src="https://raw.githubusercontent.com/qdm12/gluetun/master/title.svg" width="300" height="200" style="margin: 15px 10px;">
</div>

<div style="text-align: center">
    <img src="https://m.media-amazon.com/images/I/51gvJaXQh4L.png" width="200" height="200" style="margin-right: 10px;">
    <img src="https://m.media-amazon.com/images/I/31o0QB0R0sL.png" width="200" height="200" style="margin-left: 10px;">
</div>

---

## **Services ajoutés (fork)**

Ces services **ne font pas partie du projet d'origine**. Ils sont câblés dans les fichiers `compose_files/VPN-Only/tailscale-docker-compose.yaml` et `tailscale-docker-compose-audiobooks.yaml`.

### **Bazarr**

[Bazarr](https://www.bazarr.media/) est le compagnon de Sonarr et Radarr : il gère et télécharge les sous-titres selon vos critères. Il surveille les mêmes dossiers `movies` / `tv` et récupère les sous-titres depuis des fournisseurs comme OpenSubtitles.

- Image : `lscr.io/linuxserver/bazarr:latest`
- Interface web : `http://<hôte>:6767`
- Montages : `configs/bazarr:/config`, `radarr/movies:/movies`, `sonarr/tv:/tv`
- `depends_on` : `sonarr`, `radarr`

### **Translatarr**

[Translatarr](https://github.com/aleknomu/translatarr) traduit automatiquement les fichiers de sous-titres (ex. anglais → français) pour les médias déjà importés par Radarr / Sonarr, comblant ce que Bazarr ne trouve pas chez les fournisseurs.

- Image : `aleknomu/translatarr:latest`
- Interface web : `http://<hôte>:6868`
- Montages : `configs/translatarr:/config`, `radarr/movies:/movies`, `sonarr/tv:/tv`

### **Tailscale**

[Tailscale](https://tailscale.com/) crée un maillage WireGuard privé et chiffré (tailnet) entre vos appareils. Dans ce fork, le conteneur `tailscale` sert de **fournisseur réseau** : `jellyfin`, `jellyseerr` et les interfaces livres audio tournent avec `network_mode: service:tailscale` et sont donc accessibles via `http://homeserver:<port>` sur le tailnet, sans publier de ports sur le LAN.

- Image : `tailscale/tailscale:latest`
- Nécessite une clé d'authentification dans `TS_AUTHKEY` (définie dans le fichier compose), `/dev/net/tun`, et les capacités `NET_ADMIN` + `SYS_MODULE`.
- Tout port dont a besoin un conteneur co-réseauté **doit figurer dans le bloc `ports:` du service `tailscale`** (c'est pourquoi `13378` et `5056` y sont ajoutés pour la stack livres audio).
- État : `configs/tailscale:/var/lib/tailscale`

> [!IMPORTANT]
> Ne committez jamais une vraie `TS_AUTHKEY` dans un dépôt public. Utilisez une clé éphémère/réutilisable et faites-la tourner en cas de fuite. Mieux : déplacez-la dans le fichier `.env` (ex. `TS_AUTHKEY=${TS_AUTHKEY}`).

### **qbit-port-sync**

Un petit conteneur utilitaire (`curlimages/curl`) partageant l'espace réseau de Gluetun. Il lit le port que Gluetun fait suivre depuis le fournisseur VPN (`/tmp/gluetun/forwarded_port`) et appelle l'API de qBittorrent pour le définir comme port d'écoute, afin que la connectivité entrante continue de fonctionner quand ce port change. Il s'exécute une seule fois (`restart: "no"`) et s'appuie sur `scripts/qbit-port-sync.sh`.

---

## **Livres audio**

Un pipeline livres audio optionnel qui reprend la logique films/séries et **réutilise le Prowlarr et le qBittorrent existants** :

| Service | Rôle | Équivalent | Réseau | Accès |
|---|---|---|---|---|
| `audiobookshelf` | lecteur / bibliothèque | Jellyfin | `service:tailscale` | `http://homeserver:13378` |
| `shelfarr` | demandes **+ import** | Jellyseerr | `service:tailscale` | `http://homeserver:5056` |
| `chaptarr` | gestionnaire d'acquisition | Radarr | bridge | `http://<hôte>:8789` |

#### **Ports**

| Service | Port hôte | Port conteneur | Déclaré sur | Accessible via |
|---|---|---|---|---|
| `audiobookshelf` | `13378` | `13378` (`PORT=13378`) | le service **`tailscale`** | `http://homeserver:13378` |
| `shelfarr` | `5056` | `5056` (`HTTP_PORT=5056`) | le service **`tailscale`** | `http://homeserver:5056` |
| `chaptarr` | `8789` | `8789` | le service `chaptarr` lui-même | `http://<hôte>:8789` |

#### **Noms d'hôte des conteneurs — à lire avant de remplir le moindre écran de configuration**

> [!CAUTION]
> **`qbittorrent` n'est pas un nom d'hôte valide dans cette stack.** qBittorrent tourne avec `network_mode: service:gluetun` : il n'a donc aucune identité réseau propre et le DNS de Docker n'a aucun enregistrement pour lui. Pire, chez de nombreux FAI le nom fuite vers le DNS public et résout silencieusement vers un serveur public sans rapport (chez Numericable/SFR, `qbittorrent` résout vers `qbittorrent.numericable.fr`). Le test de connexion échoue, ou reste bloqué, pour des raisons qui ne ressemblent en rien à un problème DNS.
>
> **Utilisez `gluetun` à la place.** Idem pour Jellyfin, Jellyseerr, Audiobookshelf et Shelfarr, qui vivent dans l'espace réseau `tailscale` et répondent sur `tailscale`.

La règle : un conteneur déclaré avec `network_mode: service:X` s'adresse via **`X`**, pas via son propre nom.

| Service | `network_mode` | Adresse à utiliser depuis les autres conteneurs | Vérifié |
|---|---|---|---|
| qBittorrent | `service:gluetun` | **`gluetun:8080`** | HTTP 200 |
| Audiobookshelf | `service:tailscale` | **`tailscale:13378`** | HTTP 200 |
| Shelfarr | `service:tailscale` | **`tailscale:5056`** | HTTP 302 |
| Jellyfin | `service:tailscale` | **`tailscale:8096`** | |
| Jellyseerr | `service:tailscale` | **`tailscale:5055`** | |
| Chaptarr | *(bridge)* | `chaptarr:8789` | HTTP 200 |
| Prowlarr | *(bridge)* | `prowlarr:9696` | |
| Sonarr / Radarr / Bazarr | *(bridge)* | `sonarr:8989` / `radarr:7878` / `bazarr:6767` | |
| FlareSolverr | *(bridge)* | `flaresolverr:8191` | |

Donc, les adresses à saisir dans chaque écran de configuration :

| Depuis | Vers | Adresse à saisir |
|---|---|---|
| Chaptarr | qBittorrent | Host `gluetun`, Port `8080` |
| Shelfarr | qBittorrent | `http://gluetun:8080` |
| Shelfarr | Prowlarr | `http://prowlarr:9696` |
| Shelfarr | Audiobookshelf | `http://localhost:13378` *(même espace réseau — `localhost` fonctionne)* |
| Prowlarr | Chaptarr | `http://chaptarr:8789` |
| Radarr / Sonarr / Bazarr | qBittorrent | Host `gluetun`, Port `8080` |

> [!NOTE]
> Ceci corrige les instructions d'origine plus bas, qui indiquent de saisir `qbittorrent` comme Host pour Radarr et Sonarr. Ce conseil est antérieur aux variantes VPN ; avec `network_mode: service:gluetun` il ne peut pas fonctionner. Utilisez `gluetun`.

> [!WARNING]
> `audiobookshelf` et `shelfarr` utilisent `network_mode: service:tailscale` : **leurs ports doivent être déclarés dans le bloc `ports:` du service `tailscale`**, pas sur leur propre service. Si vous changez `13378` ou `5056`, changez-le aux *deux* endroits (la liste `ports:` de `tailscale` et la variable `PORT` de l'application).
>
> Les conteneurs partageant un espace réseau se joignent entre eux via `localhost`. Tout le reste se joint via le nom du propriétaire de l'espace réseau, selon le tableau ci-dessus.

Convention de dossiers sous `${COMMON_PATH}` (`/VOTRE_CHEMIN/Isyrr`) :

```
configs/audiobookshelf      configs/shelfarr      configs/chaptarr
chaptarr/audiobooks         chaptarr/ebooks              audiobookshelf/metadata
```

À créer une fois avant le premier `up` :

```bash
mkdir -p ${COMMON_PATH}/configs/{audiobookshelf,shelfarr,chaptarr} \
         ${COMMON_PATH}/chaptarr/{audiobooks,ebooks} \
         ${COMMON_PATH}/audiobookshelf/metadata
```

### **Audiobookshelf**

[Audiobookshelf](https://www.audiobookshelf.org/) est un serveur auto-hébergé de livres audio et de podcasts : multi-utilisateurs, synchronisation de la progression, applications iOS/Android natives, édition des chapitres et fusion en m4b.

- Image : `ghcr.io/advplyr/audiobookshelf:latest`
- Tourne avec `network_mode: service:tailscale`, `PORT=13378`
- Montages : `configs/audiobookshelf:/config`, `audiobookshelf/metadata:/metadata`, `chaptarr/audiobooks:/audiobooks`, `chaptarr/ebooks:/books`

### **Shelfarr**

[Shelfarr](https://shelfarr.org/) est l'équivalent de Jellyseerr pour les livres : on parcourt, on demande, et le livre arrive dans la bibliothèque. Surtout, il prend en charge **toute** la chaîne — il cherche via Prowlarr, envoie la release à qBittorrent, puis renomme, organise et livre les fichiers finis dans la bibliothèque Audiobookshelf.

C'est cette dernière étape qui le fait préférer ici à une interface de demandes seule : les outils qui s'arrêtent à « torrent téléchargé » vous laissent déplacer et renommer les fichiers à la main, faute d'un *arr derrière eux pour faire l'import.

- Image : **`ghcr.io/pedro-revez-silva/shelfarr:latest`** (épinglez la version avec `SHELFARR_VERSION` dans `.env`)
- Tourne avec `network_mode: service:tailscale`, `HTTP_PORT=5056` — volontairement voisin du `5055` de Jellyseerr
- Montages : `configs/shelfarr:/rails/storage`, `chaptarr/audiobooks:/audiobooks`, `chaptarr/ebooks:/ebooks`, `qbittorrent/downloads:/downloads`
- Une clé secrète est générée au premier démarrage et enregistrée dans `/rails/storage` — aucune configuration manuelle
- Gère aussi des sources directes (Anna's Archive, Z-Library, LibriVox) et un compagnon Libation optionnel pour les sauvegardes Audible, laissé en commentaire dans le fichier compose
- Seule exigence stricte : un moyen de trouver des livres, et un endroit où les mettre

### **Chaptarr**

[Chaptarr](https://github.com/Chaptarr/Chaptarr) est un fork maintenu de Readarr (désormais archivé), gérant ebooks **et** livres audio dans une seule instance, avec organisation tenant compte du narrateur, éditions multiples, support m4b et conversion MP3→M4B.

- Image : **`chaptarr/chaptarr:latest`** (Docker Hub). Projet en **bêta** — pensez à épingler un tag précis (ex. `chaptarr/chaptarr:0.9.333`) une fois une version choisie.
- Interface web : `http://<hôte>:8789`
- Montages : `configs/chaptarr:/config`, `chaptarr/audiobooks:/audiobooks`, `chaptarr/ebooks:/ebooks`, `qbittorrent/downloads:/downloads`
- Alternative : un bloc `lazylibrarian` commenté (`lscr.io/linuxserver/lazylibrarian`) est inclus dans le fichier compose livres audio.

---

# **Prérequis**

> [!NOTE]  
> Ce service nécessite une machine avec au moins 4 cœurs de CPU et 8 Go de RAM. Il est également fortement recommandé d'avoir une carte graphique NVIDIA pour des performances optimales.

La première chose à faire est de mettre à jour votre système :

```bash
sudo apt update && sudo apt upgrade
```

## **Docker**

Pour installer Docker sur votre système, utilisez les commandes suivantes :

Téléchargez le script avec cette commande :
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```

Puis exécutez le script avec cette commande :
```bash
sh get-docker.sh
```

> [!TIP]
> Je recommande de donner les droits d'administration Docker à votre utilisateur :
> ```bash
> usermod -aG docker <user>
> ```
> Après cette commande, déconnectez-vous et reconnectez-vous.



### **Utiliser Docker Compose :**

Pour utiliser Docker Compose avec ce dépôt, vous devez d'abord choisir si vous souhaitez utiliser la version avec VPN ou sans VPN. Ensuite, naviguez vers le répertoire correspondant (avec-vpn ou sans-vpn) et exécutez la commande suivante :

```bash
docker-compose up -d
```

Pour arrêter la stack :

```bash
docker-compose down
```

**[`^        retour au sommaire        ^`](#table-des-matières)**

## **NVIDIA**

> [!WARNING]  
> Veuillez noter qu'en raison des mises à jour récentes de Debian 12 et de Proxmox, les pilotes NVIDIA sont devenus instables. Par conséquent, il existe deux méthodes pour installer les pilotes.

Pour mon serveur, il possède une carte graphique NVIDIA GeForce 1060. Le système d'exploitation installé est Proxmox 8.1.10, basé sur Debian 12. Si vous devez vérifier la compatibilité, consultez le [matrice de support NVIDIA](https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new).

### **Première méthode**

Rendez-vous sur le [site web de NVIDIA](https://www.nvidia.com/en-us/drivers/) et sélectionnez votre carte graphique. Voici un exemple :



<div style="text-align: center">
    <img src="image/nvidia/nv1.png" style="margin: 15px 10px;">
</div>

---

<div style="text-align: center">
    <img src="image/nvidia/nv2.png" style="margin: 15px 10px;">
</div>

Copiez le lien de téléchargement pour le pilote, vous devriez obtenir un lien qui ressemble à ceci :

```text
https://us.download.nvidia.com/XFree86/Linux-x86_64/550.127.05/NVIDIA-Linux-x86_64-550.127.05.run
```

1. Mise à jour et préparation du système

Mettez à jour et améliorez votre système pour vous assurer que tous les paquets sont à jour.

```bash
apt update
apt upgrade
```

2. Téléchargement et préparation du pilote NVIDIA

Téléchargez le pilote NVIDIA requis.


```bash
wget https://us.download.nvidia.com/XFree86/Linux-x86_64/550.127.05/NVIDIA-Linux-x86_64-550.127.05.run
chmod u+x NVIDIA-Linux-x86_64-550.127.05.run
```

3. Installer les clés et le dépôt du NVIDIA Container Toolkit

Ajoutez la clé GPG et configurez le dépôt pour les outils de conteneur NVIDIA.

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

4. Mettre à jour les dépôts et installer les packages nécessaires

Mettez à jour les dépôts et installez les packages nécessaires pour la compilation.

```bash
apt update
apt install pve-headers gcc make
```

5. Installer le pilote NVIDIA

Installez le pilote NVIDIA téléchargé en utilisant le chemin source du noyau.

```bash
./NVIDIA-Linux-x86_64-550.127.05.run --kernel-source-path /usr/src/linux-headers-6.8.12-3-pve/
```

6. Installer et configurer le NVIDIA Container Toolkit

Installez le NVIDIA Container Toolkit et configurez-le pour Docker.

```bash
apt install nvidia-container-toolkit
nvidia-ctk runtime configure --runtime=docker
```

7. Configurer le démon Docker

Éditez le fichier de configuration Docker pour configurer le runtime et le chemin des données.


```bash
nano /etc/docker/daemon.json
```

Ajoutez le contenu suivant :

```json
{
    "data-root": "/<YOUR_PATH>/docker",
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    }
}
```

8. Redémarrer

Votre environnement est maintenant prêt à exécuter des conteneurs Docker avec le support GPU NVIDIA.

## **Vérification finale**

Assurez-vous que le GPU est correctement détecté :

```
root@pve:~#nvidia-smi
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.147.05   Driver Version: 525.147.05   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:01:00.0 Off |                  N/A |
| N/A   47C    P8     9W /  78W |      1MiB /  3072MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

**[`^        retour au sommaire        ^`](#table-des-matières)**

## **Deuxième méthode**

> [!WARNING]  
> Cette méthode est obsolète car elle peut provoquer d'importants conflits si vous mettez fréquemment à jour votre serveur.

1. Votre fichier `/etc/apt/sources.list` doit ressembler à ceci :
```bash
deb http://ftp.debian.org/debian bookworm main contrib
deb http://ftp.debian.org/debian bookworm-updates main contrib

# Proxmox VE pve-no-subscription repository provided by proxmox.com,
# NOT recommended for production use
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription

# security updates
deb http://security.debian.org/debian-security bookworm-security main contrib

# Debian Bookworm
### Add this line
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
```

Et : 

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

2. Mettre à jour les dépôts :

```bash
apt update
```

3. Installer les mises à jour :

```bash
apt upgrade
```

4. Installer les pilotes NVIDIA :

Uniquement pour l'environnement Proxmox :

```bash
apt install pve-headers
```

Ensuite :

```bash
apt install libnvidia-cfg1 nvidia-kernel-source nvidia-kernel-common nvidia-driver nvidia-container-toolkit

nvidia-ctk runtime configure --runtime=docker
```

5. Configurer le démon Docker

Éditez le fichier de configuration Docker pour configurer le runtime et le chemin des données.

```bash
nano /etc/docker/daemon.json
```

Ajoutez le contenu suivant :

```json
{
    "data-root": "/<YOUR_PATH>/docker",
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    }
}
```

6. Redémarrer

7. Ensuite, entrez **nvidia-smi**, ce qui devrait afficher :

```
root@pve:~#nvidia-smi
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.147.05   Driver Version: 525.147.05   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:01:00.0 Off |                  N/A |
| N/A   47C    P8     9W /  78W |      1MiB /  3072MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

Il pourrait y avoir des erreurs pendant l'installation ; il est préférable d'utiliser nvidia-patch :

```bash
git clone https://github.com/keylase/nvidia-patch.git

cd nvidia-patch
./patch.sh
```

> [!CAUTION]  
> Si vous devez redémarrer l'installation, voici comment désinstaller les pilotes NVIDIA :
> 
> ```bash
> apt remove nvidia-driver
> apt purge *nvidia*
> apt autoremove
> apt clean
> apt search nvidia-driver
> apt autoremove glx-alternative-nvidia libegl-nvidia0 libgl1-nvidia-glvnd-glx libgles-nvidia1 libgles-nvidia2 libglx-nvidia0 nvidia-alternative nvidia-detect nvidia-driver nvidia-driver-bin nvidia-driver-libs nvidia-kernel-dkms nvidia-kernel-source nvidia-open-kernel-dkms nvidia-open-kernel-source xserver-xorg-video-nvidia
> ```
> Si des fichiers résiduels restent, recherchez-les en utilisant `apt search nvidia-driver`

**[`^        retour au sommaire        ^`](#table-des-matières)**

# **VPN**

Maintenant, nous allons voir comment configurer le VPN. Personnellement, j'utiliserai ProtonVPN et NordVPN, mais vous pouvez trouver de nombreux autres fournisseurs de VPN [ICI](https://github.com/qdm12/gluetun-wiki/tree/main/setup/providers).

## **NORD**

Tout d'abord, vous devez vous connecter au site Web de Nord VPN.

1. Allez sur les services de Nord VPN :

<div style="text-align: center">
    <img src="image/vpn/vpn1.png" style="margin: 15px 10px;">
</div>

2. Sélectionnez la configuration manuelle de NordVPN :

<div style="text-align: center">
    <img src="image/vpn/vpn2.png" style="margin: 15px 10px;">
</div>

3. Vous pouvez maintenant récupérer votre identifiant et votre mot de passe pour le conteneur Gluetun :

<div style="text-align: center">
    <img src="image/vpn/vpn3.png" style="margin: 15px 10px;">
</div>

---

## **PROTON**

Allez sur le site de [Proton VPN](https://account.protonvpn.com/downloads).

1. Allez dans la section Téléchargement :

<div style="text-align: center">
    <img src="image/vpn/pro1.png" style="margin: 15px 10px;">
</div>

2. Configurez votre VPN manuellement en sélectionnant un nom de système d'exploitation à utiliser, et assurez-vous d'activer NAT-PMP. Enfin, sélectionnez le pays souhaité :

<div style="text-align: center">
    <img src="image/vpn/pro2.png" style="margin: 15px 10px;">
</div>

3. Vous pouvez maintenant rassembler vos informations pour la configuration du conteneur Gluetun :

<div style="text-align: center">
    <img src="image/vpn/pro3.png" style="margin: 15px 10px;">
</div>

> [!CAUTION]  
> Assurez-vous d'avoir soit téléchargé le fichier, soit copié son contenu dans un fichier texte, car certaines informations ne seront plus disponibles après avoir cliqué sur "Fermer".

## **Dépannage VPN** 

Une fois Docker lancé, vous pouvez tester votre VPN avec la commande suivante :

```bash
docker exec qbittorrent curl -s https://api.ipify.org/
# Résultat
94.101.115.63
```

De mon côté, cela m'affiche une adresse IP en Belgique :

<div style="text-align: center">
    <img src="image/vpn/vpn4.png" style="margin: 15px 10px;">
</div>

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

# **Installation**

## **🚀 Installation Automatique (Recommandée)**

 Déplacez-vous dans votre dossier personnel, puis lancez le script d'installation automatique correspondant à la langue souhaitée. NE PAS exécuter en root ; le script demandera `sudo` :

 Installateur français :
 ```bash
 wget https://raw.githubusercontent.com/Morzomb/All-jellyfin-media-server/Main/setup-fr.sh -O setup-fr.sh
 chmod +x setup-fr.sh
 ./setup-fr.sh
 ```

### **Prérequis**

📋 Vous aurez besoin de :

- **Système d'exploitation supporté** : Debian 12+, Ubuntu LTS 22.x ou 24.x, ou Raspbian
- **Matériel** : Minimum 4 cœurs de CPU et 8 Go de RAM (16 Go recommandés pour le transcodage 4K)
- **Réseau** : Ports TCP ouverts 8096 (Jellyfin), 5055 (Jellyseerr), 8989 (Sonarr), 7878 (Radarr), 9696 (Prowlarr), 9117 (Jackett), 8080 (qBittorrent)
- **Logiciels** : Docker & Docker Compose installés, paquets `wget` et `sudo`
- **GPU** (optionnel) : GPU NVIDIA avec pilotes installés pour le transcodage matériel (Offre 3 uniquement)
- **VPN** (optionnel) : Identifiants de compte NordVPN ou ProtonVPN pour les téléchargements sécurisés

### **Menu du Script d'Installation**

🔧 Les installateurs `setupfinale.sh` (français) et `setupfinale-eng.sh` (anglais) guident l'installation complète.

1. **Gestion stateful** - Détecte une installation précédente et propose : Mettre à jour / Désinstaller / Modifier / Quitter
2. **Sélection de la pile** - Choisissez Offre 1 (Standard), 2 (Sécurisée avec VPN) ou 3 (Ultime avec NVIDIA)
3. **Services additionnels** - Activer facultativement Homepage et Bazarr
4. **Variables d'environnement** - Configurer `COMMON_PATH`, `TZ`, `PUID`/`PGID`, `SERVER_IP` (ou conserver `.env` existant)
5. **Configuration VPN** (si choisie) - Saisie des identifiants NordVPN (OpenVPN) ou ProtonVPN (WireGuard)
6. **Préconfiguration** - Déploiement des configs Homepage si demandé
7. **Sauvegarde & Déploiement** - Enregistre la config, crée les dossiers et lance `docker compose up -d`
8. **Post‑install (harvest)** - Option d'automatisation pour lier Jellyfin, qBittorrent, Radarr, Sonarr, Prowlarr, Bazarr

**[`^        retour au sommaire        ^`](#table-des-matières)**

### **Ajouter des Services Personnalisés**

Vous pouvez étendre Isyrr en ajoutant des services Docker personnalisés. Voici comment intégrer un nouveau service dans la configuration automatique :

#### **Étape 1 : Créer le Modèle YAML du Service**

Créez un nouveau fichier YAML dans le répertoire `auto/templates/services/` (ou `auto/templates/vpn/` s'il est lié au VPN) :

```bash
cat > auto/templates/services/monservice.yml << 'EOF'
services:
  monservice:
    image: monimage:latest
    container_name: monservice
    environment:
      - PUID=0
      - PGID=0
      - TZ=${TZ}
    ports:
      - 9999:9999
    volumes:
      - ${COMMON_PATH}/configs/monservice:/config
      - ${COMMON_PATH}:/data
    restart: unless-stopped
EOF
```

#### **Étape 2 : Ajouter la Sélection du Service dans setup-fr.sh**

Dans la section **2.5 Services Additionnels** de `setup-fr.sh` et `setup.sh`, ajoutez votre invite de service :

```bash
echo -e "${BOLD}MonService:${NC}"
echo -e "  Description du service personnalisé"
echo -e "  Fonctionnalités et avantages"
echo ""
while true; do
    read -p "Installer MonService ? (y/n): " monservice_choice
    case $monservice_choice in
        [yY]*) INSTALL_MONSERVICE=true; show_success "MonService activé"; break ;;
        [nN]*) INSTALL_MONSERVICE=false; show_warn "MonService désactivé"; break ;;
        *) show_error "Répondez par y ou n" ;;
    esac
done
```

#### **Étape 3 : Mettre à Jour la Génération de docker-compose**

Dans la fonction `generate_docker_command()`, ajoutez :

```bash
if [ "$INSTALL_MONSERVICE" == "true" ]; then
    curl -sL "$REPO_BASE/templates/services/monservice.yml" -o "$COMPOSE_DL_DIR/monservice.yml"
    CMD_ARGS="$CMD_ARGS -f $COMPOSE_DL_DIR/monservice.yml"
fi
```

#### **Étape 4 : Créer le Dossier de Configuration**

Dans la section création des répertoires, ajoutez :

```bash
[ "$INSTALL_MONSERVICE" == "true" ] && mkdir -p "$CURRENT_PATH/configs/monservice"
```

#### **Étape 5 : Sauvegarder l'État de Configuration**

Mettez à jour la section de sauvegarde `.isyrr_config` pour inclure votre service :

```bash
cat > "$CONFIG_FILE" <<EOF
PACK_TYPE="$PACK_TYPE"
VPN_PROVIDER="$VPN_PROVIDER"
INSTALL_HOMEPAGE="$INSTALL_HOMEPAGE"
INSTALL_BAZARR="$INSTALL_BAZARR"
INSTALL_MONSERVICE="$INSTALL_MONSERVICE"
EOF
```

#### **Étape 6 : Ajouter la Configuration Post-Installation (Optionnel)**

Si votre service a besoin d'extraction de clé API ou de configuration, ajoutez-le dans la **section post-installation** :

```bash
if [[ "$INSTALL_MONSERVICE" == "true" ]]; then
    box_section "Configuration MonService"
    
    MONSERVICE_CONFIG="$DATA_PATH/configs/monservice/config.json"
    
    if [ -f "$MONSERVICE_CONFIG" ]; then
        MONSERVICE_KEY=$(grep 'apikey:' "$MONSERVICE_CONFIG" | awk '{print $2}')
    fi
    
    if [ -z "$MONSERVICE_KEY" ]; then
        echo -e "    ${RED}[-]${NC} Clé API MonService non trouvée"
    else
        echo -e "    ${GREEN}[+]${NC} Clé API MonService : ${YELLOW}${MONSERVICE_KEY:0:8}...${NC}"
    fi
fi
```

#### **Étape 7 : Ajouter à Tous les Fichiers Docker Compose**

Pour la cohérence, ajoutez votre définition de service à tous les fichiers `compose_files/docker-compose*.yaml` pour qu'il puisse être utilisé dans les installations manuelles :

```yaml
  monservice:
    image: monimage:latest
    container_name: monservice
    environment:
      - PUID=0
      - PGID=0
      - TZ=${TZ}
    ports:
      - 9999:9999
    volumes:
      - ${COMMON_PATH}/configs/monservice:/config
      - ${COMMON_PATH}:/data
    restart: unless-stopped
```

#### **Étape 8 : Mettre à Jour la Documentation README**

Ajoutez les informations du service dans le README principal :

```markdown
### **MonService**

[MonService](https://exemple.com) est un service qui fait X, Y et Z. Description...

<div style="text-align: center">
    <img src="url-vers-logo" width="200" height="100" style="margin: 15px 10px;">
</div>
```

#### **Étape 9 : Tester l'Intégration**

1. Testez le script de configuration avec votre nouveau service
2. Vérifiez que les fichiers Docker Compose sont valides : `docker-compose config`
3. Vérifiez que l'extraction de clé API fonctionne correctement
4. Vérifiez la connectivité du service après le déploiement

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Installation Manuelle**

Alternativement, vous pouvez cloner et gérer le dépôt manuellement :

```bash
git clone https://github.com/Morzomb/All-jellyfin-media-server.git
cd All-jellyfin-media-server/
```

Pour l'installation, j'ai créé uniquement trois versions du fichier `docker-compose`.

Avant de procéder, rendez-vous dans le fichier `.env` situé dans le répertoire `compose_files/` et complétez-le avec les informations nécessaires. Ce fichier doit toujours être à la racine du fichier `docker-compose` que vous allez lancer.

```yaml
# BASE
COMMON_PATH=/VOTRE_CHEMIN/Isyrr
TZ=Europe/Paris

# Décommentez les lignes ci-dessous pour activer la configuration VPN correspondante

# NORD VPN
# OPENVPN_USER=nom_utilisateur  # Votre nom d'utilisateur pour NordVPN
# OPENVPN_PASSWORD=mot_de_passe  # Votre mot de passe pour NordVPN
# SERVER_REGIONS=Belgique  # Choisissez la région du serveur (ici la Belgique)

# PROTON VPN
# ENDPOINT_IP=ADRESSE_IP_PEER  # L'adresse IP du serveur VPN
# WIREGUARD_ADDR=Adresse_Interface  # L'adresse de l'interface WireGuard
# ENDPOINT_PORT=51820  # Le port par défaut est 51820, mais confirmez s'il est différent
# DNS_ADDRESS=Interface_DNS  # L'adresse DNS pour ProtonVPN
# PUBLIC_KEY=Clef_Publique_PEER  # La clé publique de l'autre pair
# PRIVATE_KEY=Clef_Privée_Interface  # Votre clé privée
```

> [!WARNING]  
> Assurez-vous de décommenter et de configurer les paramètres en fonction du service VPN que vous utilisez. Cette étape est essentielle pour établir une connexion VPN correcte.

## **1. Installation de base**

Installation standard sans `VPN` ni `NVIDIA` :

Pour commencer l'installation, exécutez :

```bash
cd compose_files/
docker compose -f docker-compose.yaml up -d
```

[Accédez au fichier ici](compose_files/docker-compose.yaml)

## **2. Installation avec uniquement NVIDIA**

Installation standard avec `NVIDIA` mais sans `VPN` :

Pour commencer l'installation, exécutez :

```bash
cd compose_files/
docker compose -f docker-compose-nvidia.yaml up -d
```

[Accédez au fichier ici](compose_files/docker-compose-nvidia.yaml)

## **3. Installation avec NVIDIA et VPN**

> [!WARNING]  
> Si vous utilisez cette méthode, remplissez le fichier `.env` situé dans `compose_files/VPN-Nvidia`.

Installation standard avec à la fois `VPN` et `NVIDIA` :

Pour commencer l'installation, exécutez :

```bash
cd compose_files/VPN-nvidia/
docker compose -f docker-compose-<YOUR_VPN>-vpn.yaml up -d
```

[Aller au fichier ici](compose_files/VPN-Nvidia/)

## **4. Installation avec VPN (sans NVIDIA)**

> [!WARNING]  
> Si vous utilisez cette méthode, remplissez le fichier `.env` situé dans `compose_files/VPN`.
> 
Installation standard avec un `VPN` :

Pour commencer l'installation, exécutez :

```bash
cd compose_files/VPN/
docker compose -f docker-compose-<YOUR_VPN>-vpn.yaml up -d
```
[Aller au fichier ici](compose_files/VPN-Only/)

## **5. Installation avec Tailscale (+ Livres audio)**

> [!WARNING]
> Si vous utilisez cette méthode, remplissez le fichier `.env` situé dans `compose_files/VPN-Only/`. Jellyfin, Jellyseerr et les interfaces livres audio sont servis via le **tailnet** (`http://homeserver:<port>`), pas sur `localhost`. Renseignez une `TS_AUTHKEY` valide (voir la note [Tailscale](#tailscale) sur le fait de la garder hors d'un dépôt public).

Ce fork ajoute deux fichiers compose basés sur Tailscale dans `compose_files/VPN-Only/` :

| Fichier | Contenu |
|---|---|
| `tailscale-docker-compose.yaml` | Tailscale + Jellyfin + Jellyseerr + Gluetun + qBittorrent + qbit-port-sync + FlareSolverr + Prowlarr + Sonarr + Radarr + Bazarr + Translatarr |
| `tailscale-docker-compose-audiobooks.yaml` | Tout ce qui précède **plus** Audiobookshelf + Shelfarr + Chaptarr |

Créez d'abord les dossiers livres audio (voir [Livres audio](#livres-audio)), puis :

```bash
cd compose_files/VPN-Only/
# stack sans livres audio
docker compose -f tailscale-docker-compose.yaml up -d
# ou la stack avec livres audio
docker compose -f tailscale-docker-compose-audiobooks.yaml up -d
```
[Aller aux fichiers ici](compose_files/VPN-Only/)

**[`^        retour au sommaire        ^`](#table-des-matières)**

# **Accéder aux Applications**

Une fois les applications déployées, vous pouvez y accéder via les adresses suivantes :

> [!IMPORTANT]  
> Remplacez `localhost` par l'adresse IP de votre machine ou serveur distant si nécessaire.

* Jellyfin : http://localhost:8096
* Jellyseer : http://localhost:5055
* Sonarr : http://localhost:8989
* Radarr : http://localhost:7878
* Jackett : http://localhost:9117
* Prowlarr : http://localhost:9696
* qBittorrent : http://localhost:8080

Ajoutés par ce fork :

* Bazarr : http://localhost:6767
* Translatarr : http://localhost:6868

Avec un fichier compose **Tailscale**, Jellyfin / Jellyseerr / Audiobookshelf / Shelfarr sont accessibles via le tailnet et non `localhost` :

* Jellyfin : http://homeserver:8096
* Jellyseerr : http://homeserver:5055
* Audiobookshelf : http://homeserver:13378
* Shelfarr : http://homeserver:5056
* Chaptarr : http://localhost:8789 *(LAN uniquement, pas sur le tailnet)*

Gluetun (Nord VPN) sera automatiquement configuré pour être utilisé avec les applications.

# **Guide de Configuration pour les Interfaces Web uniquement**

> [!IMPORTANT]  
> Tous les liens contenant le nom du conteneur peuvent être remplacés par l'IP du serveur ou `localhost`. De plus, remplacez `/COMMON_PATH/` par le chemin que vous avez configuré dans le fichier `.env`.

## **qBittorrent**

1. Ouvrez l'interface Web en cliquant sur l'icône de l'application dans l'onglet **DOCKER** et sélectionnez **WebUI**.
2. Connectez-vous avec les identifiants par défaut :
   - **Nom d'utilisateur** : `admin`
   - **Mot de passe** : `adminadmin`
   
<div style="text-align: center">
    <img src="image/qBittorrent/qbit1.png" style="margin: 15px 10px;">
</div>

   *Remarque : Les identifiants par défaut peuvent avoir changé. Veuillez consulter la documentation pour les mises à jour à ce sujet. Dans la plupart des cas, l'interface Web de qBittorrent générera un mot de passe temporaire au démarrage du conteneur. Pour afficher ce mot de passe, consultez les journaux de ce conteneur avec la commande : `docker logs qbittorrent`*

3. Une fois connecté, cliquez sur l'icône d'engrenage pour accéder aux **Options**.
4. Sous l'onglet **Téléchargements**, configurez les paramètres de sauvegarde comme suit :
   - **Mode de gestion des torrents par défaut** : `Automatique` (nécessaire pour que les chemins de sauvegarde basés sur les catégories fonctionnent)
   - **Lorsque la catégorie de torrent change** : `Relocaliser le torrent`
   - **Lorsque le chemin de sauvegarde par défaut change** : `Relocaliser les torrents affectés`
   - **Lorsque le chemin de sauvegarde de la catégorie change** : `Relocaliser les torrents affectés`
   - **Chemin de sauvegarde par défaut** : `/downloads`
5. Cliquez sur **SAUVEGARDER**.

<div style="text-align: center">
    <img src="image/qBittorrent/qbit2.png" style="margin: 15px 10px;">
</div>

### **Configuration des Catégories**

1. Dans l'interface Web, développez **CATEGORIES** dans le menu de gauche. Faites un clic droit sur **Tous** et sélectionnez **Ajouter une catégorie...**.
2. Dans la fenêtre **Nouvelle catégorie**, configurez comme suit :
   - **Catégorie** : `radarr` (cela correspond à la catégorie que vous configurerez plus tard dans Radarr)
   - **Chemin de sauvegarde** : `/downloads/radarr`
3. Cliquez sur **Ajouter**.
4. Faites un clic droit sur **Tous** à nouveau, puis sélectionnez **Ajouter une catégorie...**.
5. Configurez comme suit :
   - **Catégorie** : `sonarr` (cela doit correspondre à la catégorie configurée plus tard dans Sonarr, par défaut `sonarr-tv`, mais ce guide utilise `sonarr`)
   - **Chemin de sauvegarde** : `/downloads/sonarr`
6. Cliquez sur **Ajouter**.

<div style="text-align: center">
    <img src="image/qBittorrent/qbit3.png" style="margin: 15px 10px;">
</div>

<div style="text-align: center">
    <img src="image/qBittorrent/qbit4.png" style="margin: 15px 10px;">
    <img src="image/qBittorrent/qbit5.png" style="margin: 15px 10px;">
</div>

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Radarr**

### **Gestion des Médias**

1. Ouvrez l'interface Web et allez dans **Paramètres** > **Gestion des Médias**.
2. Cliquez sur **Ajouter un dossier racine**, ajoutez le chemin `/COMMON_PATH/radarr/movies` et cliquez sur **OK**.
3. Cliquez sur **Afficher les options avancées** en haut, faites défiler jusqu'à **Importation**, et assurez-vous que **Utiliser des liens physiques au lieu de copier** est activé.

<div style="text-align: center">
    <img src="image/radarr/rad3.png" style="margin: 15px 10px;">
</div>

### **Clients de Téléchargement**

1. Dans l'interface Web, allez dans **Paramètres** > **Clients de Téléchargement**.
2. Cliquez sur **+** sous **Clients de Téléchargement**, puis sélectionnez **qBittorrent** dans la fenêtre **Ajouter un client de téléchargement**.
3. Remplissez les champs comme suit :
   - **Nom** : `qBittorrent` (ou un autre nom de votre choix)
   - **Hôte** : `qbittorrent`
   - **Nom d'utilisateur** : `admin`
   - **Mot de passe** : `adminadmin` (modifiez-le si vous l'avez changé dans qBittorrent)
   - **Catégorie** : `radarr` (cela doit correspondre à la catégorie définie dans qBittorrent)
4. Cliquez sur **Tester**. Si vous voyez une coche, cela signifie que la connexion fonctionne ; sinon, il y a une erreur.
5. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/radarr/rad5.png" style="margin: 15px 10px;">
</div>

_Note: if entering qbittorrent as the Host does not work, try entering the IP addressinstead (ex: 192.168.x.x)_

>[!WARNING]
>Lors des nouvelles installations, Radarr peut signaler que le répertoire `/downloads/radarr` n'existe pas dans le conteneur (cela est généralement indiqué comme une erreur par Radarr dans **Système** > **Statut**).
>
>Pour corriger cela, accédez simplement au répertoire `/COMMON_PATH/qbittorrent/downloads` et créez manuellement le dossier radarr. Ensuite, supprimez qBittorrent de Radarr et ajoutez-le à nouveau, l'erreur devrait disparaître.
>
### **Indexer Jackett (Optionnelle)**

1. Dans l'interface Web, allez dans **Paramètres** > **Indexeurs**.
2. Cliquez sur **+** sous **Ajouter un Indexeur**, puis sélectionnez **Torznab**.
3. Remplissez les champs comme suit :
   - **Nom** : `Torznab` (ou un autre nom de votre choix)
   - **URL** : `http://Jackett:9117/api/v2.0/indexers/YOUR_INDEXERS/results/torznab/`
   - **Clé API** : Trouvez la clé API dans le menu d'accueil en haut à droite.
4. Cliquez sur **Tester**. Si vous voyez une coche, cela signifie que la connexion fonctionne ; sinon, il y a une erreur.
5. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/sonarr/son3.png" style="margin: 15px 10px;">
</div>

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Sonarr**

### **Gestion des Médias**

1. Ouvrez l'interface Web et allez dans **Paramètres** > **Gestion des Médias**.
2. Cliquez sur **Ajouter un dossier racine**, ajoutez le chemin `/COMMON_PATH/sonarr/tv`, puis cliquez sur **OK**.
3. Cliquez sur **Afficher les options avancées**, faites défiler jusqu'à **Importation**, et activez **Utiliser des liens physiques au lieu de copier**.

<div style="text-align: center">
    <img src="image/sonarr/son1.png" style="margin: 15px 10px;">
</div>

_Remarque : si l'utilisation de `qbittorrent` comme hôte ne fonctionne pas, essayez d'entrer l'adresse IP à la place (ex :`192.168.x.x`)_

### **Clients de Téléchargement**

1. Dans l'interface Web, allez dans **Paramètres** > **Clients de Téléchargement**.
2. Cliquez sur **+** sous **Clients de Téléchargement**, puis sélectionnez **qBittorrent**.
3. Remplissez les champs comme suit :
   - **Nom** : `qBittorrent` (ou un autre nom de votre choix)
   - **Hôte** : `qbittorrent`
   - **Nom d'utilisateur** : `admin`
   - **Mot de passe** : `adminadmin` (modifiez-le si vous l'avez changé dans qBittorrent)
   - **Catégorie** : `sonarr` (cela doit correspondre à la catégorie définie dans qBittorrent)
4. Cliquez sur **Tester**. Si vous voyez une coche, cela signifie que la connexion fonctionne.
5. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/sonarr/son2.png" style="margin: 15px 10px;">
</div>

### **Indexer Jackett (Optionnelle)**

1. Dans l'interface Web, allez dans **Paramètres** > **Indexeurs**.
2. Cliquez sur **+** sous **Ajouter un Indexeur**, puis sélectionnez **Torznab**.
3. Remplissez les champs comme suit :
   - **Nom** : `Torznab` (ou un autre nom de votre choix)
   - **URL** : `http://Jackett:9117/api/v2.0/indexers/YOUR_INDEXERS/results/torznab/`
   - **Clé API** : Trouvez la clé API dans le menu d'accueil en haut à droite.
4. Cliquez sur **Tester**. Si vous voyez une coche, cela signifie que la connexion fonctionne ; sinon, il y a une erreur.
5. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/sonarr/son3.png" style="margin: 15px 10px;">
</div>

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Prowlarr**

### **Configurer les Indexeurs de Torrents**

1. Ouvrez l'interface Web et allez dans **Indexeurs** > **Ajouter un Nouvel Indexeur**.
2. Sélectionnez **1337x** (ou un autre tracker de votre choix).
   - Vous pouvez modifier les paramètres selon vos préférences, mais les valeurs par défaut fonctionnent généralement bien.
   - Le tri par **Seeders** peut être utile pour des téléchargements plus rapides.
3. Cliquez sur **Tester**. Si vous voyez une coche, la connexion fonctionne ; sinon, il y a une erreur.
4. Cliquez sur **Sauvegarder**.

### **Configurer FlareSolverr**

1. Allez dans **Paramètres** et cliquez sur **+** sous **Indexer**.
2. Sélectionnez **FlareSolverr** et remplissez les informations comme suit :
   - **Nom** : `FlareSolverr`
   - **Tags** : `flaresolverr`
   - **Hôte** : `http://flaresolverr:8191/`
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/prowlarr/pro1.png" style="margin: 15px 10px;">
</div>

### **Configurer Radarr**

1. Allez dans **Paramètres** et cliquez sur **Apps**.
2. Sélectionnez **Radarr** et remplissez les informations comme suit :
   - **Niveau de synchronisation** : `Synchronisation complète`
   - **Serveur Prowlarr** : `http://prowlarr:9696`
   - **Serveur Radarr** : `http://radarr:7878`
   - **Clé API** : Trouvez la clé API dans l'interface de Radarr sous **Paramètres** > **Général** > **Clé API**.
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/prowlarr/pro2.png" style="margin: 15px 10px;">
</div>

### **Configurer Sonarr**

1. Allez dans **Paramètres** et cliquez sur **Apps**.
2. Sélectionnez **Sonarr** et remplissez les informations comme suit :
   - **Niveau de synchronisation** : `Synchronisation complète`
   - **Serveur Prowlarr** : `http://prowlarr:9696`
   - **Serveur Sonarr** : `http://sonarr:8989`
   - **Clé API** : Trouvez la clé API dans l'interface de Sonarr sous **Paramètres** > **Général** > **Clé API**.
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **Sauvegarder**.

<div style="text-align: center">
    <img src="image/prowlarr/pro3.png" style="margin: 15px 10px;">
</div>

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Jellyfin**

### **Configuration Initiale**

1. Ouvrez l'interface Web en allant dans l'onglet **DOCKER**, cliquez sur l'icône de l'application Jellyfin et sélectionnez **WebUI**.
2. Sélectionnez une langue d'affichage préférée (ou utilisez l'anglais par défaut). Cliquez sur **Suivant** ➝.
3. Créez un compte administrateur, remplissez les informations d'identification selon vos préférences et cliquez sur **Suivant** ➝.
4. Cliquez sur **Ajouter une bibliothèque multimédia** et remplissez les informations suivantes :
   - **Type de contenu** : Films
   - **Dossiers** : `/COMMON_PATH/radarr/movies`
   - Configurez le reste comme bon vous semble ; les paramètres par défaut conviennent généralement.
5. Cliquez sur **OK**.
6. Cliquez de nouveau sur **Ajouter une bibliothèque multimédia** et remplissez les informations suivantes :
   - **Type de contenu** : Séries
   - **Dossiers** : `/COMMON_PATH/sonarr/tv`
   - Configurez le reste comme bon vous semble ; les paramètres par défaut conviennent généralement.
7. Cliquez sur **OK**.
8. Cliquez sur **Suivant** ➝.
9. Configurez la **Langue de Métadonnées Préférée** (ou utilisez la langue par défaut) et cliquez sur **Suivant** ➝.
10. Dans **Configurer l'accès à distance**, laissez **Autoriser les connexions distantes à ce serveur** coché et **Activer le mappage automatique de port** décoché.
11. Cliquez sur **Suivant** ➝, puis cliquez sur **Terminer**.
12. Connectez-vous avec votre compte administrateur.

Une fois connecté, si vous avez déjà du contenu dans vos dossiers `/COMMON_PATH/*`, il devrait commencer à apparaître dans Jellyfin. Sinon, le contenu sera ajouté au fur et à mesure que les dossiers se remplissent.

### **Ajouter des utilisateurs à Jellyfin**

Si vous souhaitez que d'autres utilisateurs aient accès à votre serveur Jellyfin, vous pouvez créer des comptes utilisateurs supplémentaires. Cette étape est optionnelle si vous êtes le seul utilisateur.

1. Ouvrez le menu à gauche en cliquant sur les trois lignes horizontales (menu hamburger) dans le coin supérieur gauche.
2. Sélectionnez **Utilisateurs** et cliquez sur le bouton **+** à gauche pour ajouter un nouvel utilisateur.
3. Remplissez les informations suivantes pour le nouvel utilisateur :
   - **Nom** : `<nom_utilisateur>`
   - **Mot de passe** : `<mot_de_passe>`
   - Sous **Accès à la bibliothèque**, cochez les cases des bibliothèques (Films, Séries TV, etc.) auxquelles vous voulez que l'utilisateur ait accès.
4. Cliquez sur **Sauvegarder** pour créer l'utilisateur.
5. Répétez ce processus pour tous les utilisateurs que vous souhaitez ajouter au serveur.

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Jellyseerr**

### **Connexion / Configuration**

1. Ouvrez l'interface Web et, dans l'écran **Bienvenue sur Jellyseerr**, sélectionnez **Utiliser votre compte Jellyfin**.
2. Remplissez les informations comme suit :
   - **URL Jellyfin** : `http://jellyfin:8096/`
   - **Adresse Email** : `<votre adresse email>`
   - **Nom d'utilisateur** : `<votre nom d'utilisateur Jellyfin>`
   - **Mot de passe** : `<votre mot de passe Jellyfin>`
3. Sélectionnez **Se connecter**.
4. Allez dans **Synchroniser les bibliothèques** sous **Bibliothèques Jellyfin**, sélectionnez vos bibliothèques Jellyfin, puis cliquez sur **Continuer**.

### **Intégration avec Radarr**

1. Allez dans **Paramètres Radarr**, puis cliquez sur **Ajouter un serveur Radarr**.
2. Remplissez les informations comme suit :
   - **Serveur par défaut** : Cochez cette case
   - **Nom du serveur** : `Radarr`
   - **Nom ou adresse IP** : `http://radarr`
   - **Port** : `7878`
   - **Clé API** : Trouvez la clé API dans l'interface Radarr sous **Paramètres** > **Général** > **Clé API**.
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **Sauvegarder les modifications**.

### **Intégration avec Sonarr**

1. Allez dans **Paramètres Sonarr**, puis cliquez sur **Ajouter un serveur Sonarr**.
2. Remplissez les informations comme suit :
   - **Serveur par défaut** : Cochez cette case
   - **Nom du serveur** : `Sonarr`
   - **Nom ou adresse IP** : `http://sonarr`
   - **Port** : `8989`
   - **Clé API** : Trouvez la clé API dans l'interface Sonarr sous **Paramètres** > **Général** > **Clé API**.
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **Sauvegarder les modifications**.

**[`^        back to top        ^`](#table-of-contents)**

---

## **Bazarr**

### **Configuration Initiale**

1. Ouvrez l'interface Web en naviguant vers `http://localhost:6767` (ou remplacez `localhost` par l'adresse IP de votre serveur).
2. L'assistant de configuration vous guidera dans la configuration initiale :
   - **Langue** : Sélectionnez votre langue préférée et cliquez sur **Suivant**.
   - **Authentification** : Configurez l'authentification si désiré (optionnel pour l'accès local).
   - **Paramètres Généraux** : Configurez vos préférences générales.
3. Cliquez sur **Suivant** puis sur **Enregistrer**.

> [!NOTE]  
> **Configuration des chemins** : Puisque vous utilisez les fichiers Docker Compose fournis, tous les chemins de répertoires et les mappages de volumes sont déjà configurés correctement. Bazarr détectera automatiquement vos bibliothèques Sonarr et Radarr sans avoir besoin de configuration manuelle des chemins.

### **Configurer l'Intégration Sonarr**

1. Allez dans **Paramètres** > **Sonarr**.
2. Cliquez sur **Ajouter** et remplissez les informations suivantes :
   - **Nom** : `Sonarr`
   - **Activé** : Cochez cette case
   - **Adresse** : `http://sonarr`
   - **Port** : `8989`
   - **URL de base** : Laissez vide
   - **Clé API** : Trouvez la clé API dans l'interface Sonarr sous **Paramètres** > **Général** > **Clé API**.
   - **Score minimum** : Configurez selon votre préférence (recommandé : 70-80)
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **OK** pour enregistrer.

### **Configurer l'Intégration Radarr**

1. Allez dans **Paramètres** > **Radarr**.
2. Cliquez sur **Ajouter** et remplissez les informations suivantes :
   - **Nom** : `Radarr`
   - **Activé** : Cochez cette case
   - **Adresse** : `http://radarr`
   - **Port** : `7878`
   - **URL de base** : Laissez vide
   - **Clé API** : Trouvez la clé API dans l'interface Radarr sous **Paramètres** > **Général** > **Clé API**.
   - **Score minimum** : Configurez selon votre préférence (recommandé : 70-80)
3. Cliquez sur **Tester** pour vérifier la connexion.
4. Cliquez sur **OK** pour enregistrer.

### **Configurer les Fournisseurs de Sous-titres**

1. Allez dans **Paramètres** > **Fournisseurs**.
2. Ajoutez vos fournisseurs de sous-titres préférés en cliquant sur **Ajouter** et en sélectionnant parmi les fournisseurs disponibles. Basé sur les recommandations de la communauté, voici les fournisseurs les plus efficaces :

**Fournisseurs Gratuits Recommandés (Pas de compte requis) :**
   - **TVSubtitles** : Excellent pour les séries TV, pas d'inscription nécessaire
   - **YIFYSubtitles** : Excellent pour les films, pas d'inscription nécessaire
   - **SuperSubtitles** : Bon fournisseur général, pas d'inscription nécessaire
   - **EmbeddedSubtitles** : Extrait les sous-titres des fichiers vidéo
   - **AnimeTosho** : Spécialisé pour le contenu anime

**Fournisseurs Recommandés (Compte gratuit requis) :**
   - **OpenSubtitles.com** : Compte gratuit requis, bien meilleur que l'ancienne version .org
   - **Addic7ed** : Compte gratuit requis, excellent pour les séries TV

> [!IMPORTANT]  
> **Note sur OpenSubtitles** : L'ancien opensubtitles.org nécessite maintenant un abonnement VIP et n'est plus recommandé pour les utilisateurs gratuits. Utilisez **opensubtitles.com** à la place, qui offre des comptes gratuits avec de bons plafonds de téléchargement.

3. Pour les fournisseurs nécessitant une authentification :
   - **OpenSubtitles.com** : Inscrivez-vous sur opensubtitles.com et utilisez votre nom d'utilisateur/mot de passe
   - **Addic7ed** : Inscrivez-vous sur addic7ed.com et utilisez votre nom d'utilisateur/mot de passe
4. Configurez chaque fournisseur selon vos préférences et exigences d'authentification.
5. Cliquez sur **Enregistrer**.

> [!TIP]  
> De nombreux utilisateurs rapportent une couverture de 99 % des sous-titres pour les films et 90 % pour les épisodes de télévision en utilisant cette combinaison de fournisseurs. 
> *Recommandations de fournisseurs basées sur les commentaires de la communauté de [r/bazarr](https://www.reddit.com/r/bazarr/comments/1fevojd/the_best_unlimited_provider/)*

### **Configurer les Langues**

1. Allez dans **Paramètres** > **Langues**.
2. Sélectionnez vos langues préférées pour les sous-titres :
   - **Filtre de langues** : Ajoutez les langues pour lesquelles vous voulez des sous-titres
   - **Activé par défaut** : Cochez la case pour les langues que vous voulez activées par défaut
   - **Séries** : Configurez les préférences de langue pour les séries TV
   - **Films** : Configurez les préférences de langue pour les films
3. Cliquez sur **Enregistrer**.

### **Configurer les Sous-titres**

1. Allez dans **Paramètres** > **Sous-titres**.
2. Configurez vos préférences de sous-titres :
   - **Télécharger** : Définissez quand rechercher les sous-titres (recommandé : Manuellement et quand des sous-titres sont voulus)
   - **Dossier des sous-titres** : Configurez comment les sous-titres doivent être stockés (recommandé : À côté du fichier média)
   - **Mettre à niveau les sous-titres** : Activez si vous voulez que Bazarr remplace les sous-titres existants par de meilleurs
3. Cliquez sur **Enregistrer**.

Une fois configuré, Bazarr surveillera automatiquement vos bibliothèques Sonarr et Radarr et téléchargera les sous-titres selon vos préférences configurées.

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

## **Bazarr**

1. Ouvrez l'interface web sur `http://<hôte>:6767`.
2. Allez dans **Settings** > **Languages**, créez un **Languages Profile** avec la ou les langues voulues (ex. français, anglais) et définissez-le par défaut.
3. Allez dans **Settings** > **Sonarr** :
   - **Address** : `sonarr`  **Port** : `8989`  **API Key** : depuis Sonarr **Paramètres** > **Général**
   - **Test** puis **Save**.
4. Allez dans **Settings** > **Radarr** :
   - **Address** : `radarr`  **Port** : `7878`  **API Key** : depuis Radarr **Paramètres** > **Général**
   - **Test** puis **Save**.
5. Allez dans **Settings** > **Providers**, ajoutez au moins un fournisseur de sous-titres (ex. OpenSubtitles.com avec votre compte) puis **Save**.
6. Dans **Movies** / **Series**, assignez le profil de langues et laissez Bazarr scanner.

> Translatarr (`http://<hôte>:6868`) peut pointer vers les mêmes API `radarr` / `sonarr` pour traduire automatiquement les sous-titres qu'aucun fournisseur ne propose.

---

## **Tailscale**

1. Générez une **clé d'authentification** sur <https://login.tailscale.com/admin/settings/keys> (réutilisable ou éphémère ; activez *Ephemeral* si le nœud est jetable).
2. Mettez-la dans le `TS_AUTHKEY=` du fichier compose (ou mieux, dans le `.env` sous le nom `TS_AUTHKEY` et référencez `${TS_AUTHKEY}`).
3. Démarrez la stack :
   ```bash
   cd compose_files/VPN-Only/
   docker compose -f tailscale-docker-compose.yaml up -d
   ```
4. Le nœud s'enregistre sous le nom **`homeserver`** dans votre tailnet. Depuis n'importe quel appareil du tailnet, ouvrez `http://homeserver:8096` (Jellyfin), `http://homeserver:5055` (Jellyseerr), etc.
5. Pour une exposition publique en HTTPS, utilisez plutôt `tailscale serve` / `funnel` depuis l'intérieur du conteneur, ou MagicDNS + un reverse proxy.

> [!IMPORTANT]
> Tout conteneur partageant l'espace réseau tailnet (`network_mode: service:tailscale`) ne peut publier ses ports que via la liste `ports:` du service **`tailscale`**. Ajoutez le port là, pas sur le conteneur applicatif.

---

## **Livres audio (Audiobookshelf / Shelfarr / Chaptarr)**

**0. Créez les dossiers** (voir [Livres audio](#livres-audio)) puis démarrez `tailscale-docker-compose-audiobooks.yaml`.

**1. qBittorrent** – créez d'abord la catégorie de téléchargement

   Sans cela, Chaptarr signalera une erreur « directory does not exist » (même comportement que Radarr).

   - Sur l'hôte : `mkdir -p ${COMMON_PATH}/qbittorrent/downloads/chaptarr`
   - Interface web (`http://localhost:8080`) > dépliez **CATEGORIES** > clic droit sur **All** > **Add category...**
     - **Category** : `chaptarr`
     - **Save path** : `/downloads/chaptarr`
   - Cliquez sur **Add**.

**2. Chaptarr** – `http://<hôte>:8789`

   Créez le compte administrateur au premier lancement, puis :

   | Où | Champ | Valeur |
   |---|---|---|
   | **Settings** > **Media Management** > **Add Root Folder** | Chemin | `/audiobooks` |
   | **Settings** > **Media Management** > **Add Root Folder** | Chemin | `/ebooks` *(seulement si vous gardez des ebooks)* |
   | **Settings** > **Media Management** > *Show Advanced* > **Importing** | Use Hardlinks instead of Copy | **activé** |
   | **Settings** > **Download Clients** > **+** > **qBittorrent** | Host | **`gluetun`** *(pas `qbittorrent` — voir [Noms d'hôte des conteneurs](#noms-dhôte-des-conteneurs--à-lire-avant-de-remplir-le-moindre-écran-de-configuration))* |
   | | Port | `8080` |
   | | Use SSL | désactivé |
   | | Username | `admin` |
   | | Password | votre mot de passe qBittorrent |
   | | Category | `chaptarr` |

   Cliquez sur **Test** (une coche verte doit apparaître), puis **Save**. N'ajoutez **pas** d'indexeurs ici — Prowlarr les pousse à l'étape suivante.

   <details>
   <summary>Retrouver votre mot de passe qBittorrent</summary>

   Par défaut `admin` / `adminadmin`. Les images récentes génèrent plutôt un mot de passe temporaire au premier démarrage — lisez-le avec :

   ```bash
   docker logs qbittorrent 2>&1 | grep -i "temporary password"
   ```

   Définissez-en un permanent dans qBittorrent **Options** > **Web UI** > *Authentification*.
   </details>

   Notez la clé API dans **Settings** > **General** > **API Key**, elle sert plus bas.

**3. Prowlarr** – `http://localhost:9696` – ajoutez les indexeurs livres et synchronisez-les vers Chaptarr

   - **Indexers** > **Add Indexer** : ajoutez des trackers proposant livres audio / ebooks (catégories *Audio > Audiobook* et *Books*). Testez et enregistrez chacun.
   - **Settings** > **Apps** > **+** et choisissez **Readarr**.

     > [!IMPORTANT]
     > Il n'existe **aucun type d'application « Chaptarr »** dans Prowlarr (vérifié en 2.5.2). Chaptarr parle l'API de Readarr : vous l'enregistrez donc *en tant que* Readarr. Nommez l'entrée `Chaptarr` pour les distinguer.

     | Champ | Valeur |
     |---|---|
     | Name | `Chaptarr` |
     | Sync Level | `Full Sync` |
     | Prowlarr Server | `http://prowlarr:9696` |
     | Readarr Server | `http://chaptarr:8789` |
     | API Key | la clé Chaptarr de l'étape 2 |
     | Sync Categories | `3030` (Audiobook), `7000`/`7020` (Books), `8000`/`8010` (Other/Books) |

   - **Test**, puis **Save**. Prowlarr pousse immédiatement tous les indexeurs dont les catégories recoupent celles ci-dessus ; ils apparaissent dans Chaptarr sous **Settings** > **Indexers**, avec la synchronisation RSS déjà activée.
   - Pour forcer manuellement : **Settings** > **Apps** > *Sync App Indexers*.

   > [!NOTE]
   > Seuls les indexeurs annonçant réellement des catégories livres sont synchronisés : attendez-vous donc à **moins** d'indexeurs dans Chaptarr que dans Prowlarr — c'est le comportement normal, pas un échec. Les trackers uniquement anime/séries sont ignorés.

**4. Audiobookshelf** – `http://homeserver:13378`

   - Créez le compte administrateur au premier lancement (compte *serveur*, distinct de Jellyfin).
   - **Settings** > **Libraries** > **Add Library** :

     | Champ | Valeur |
     |---|---|
     | Nom | `Audiobooks` |
     | Type de média | `Books` |
     | Dossier | `/audiobooks` |

   - Ajoutez une seconde bibliothèque pointant sur `/books` si vous gardez des ebooks.
   - **Settings** > **Users** pour ajouter des comptes aux autres auditeurs (chacun a sa propre synchronisation de progression).
   - Applications mobiles (iOS/Android) : ajoutez le serveur `http://homeserver:13378` — l'appareil doit être sur votre tailnet.

**5. Shelfarr** – `http://homeserver:5056`

   Créez le compte administrateur au premier lancement, puis parcourez **Settings** :

   **a. Indexeur** — comment il trouve les livres

   | Paramètre | Valeur |
   |---|---|
   | Type | Prowlarr |
   | Base URL | `http://prowlarr:9696` |
   | Clé API | depuis Prowlarr **Settings** > **General** |
   | Catégories | Audiobook `3030`, Books `7000`/`7020`, Other `8000`/`8010` |

   **b. Client de téléchargement** — comment il les récupère

   | Paramètre | Valeur |
   |---|---|
   | Type | qBittorrent |
   | Host / URL | **`gluetun`** port `8080` — *pas* `qbittorrent`, voir [Noms d'hôte des conteneurs](#noms-dhôte-des-conteneurs--à-lire-avant-de-remplir-le-moindre-écran-de-configuration) |
   | Utilisateur / mot de passe | comme dans l'interface qBittorrent |
   | Catégorie | `shelfarr` (créez-la dans qBittorrent avec le chemin `/downloads/shelfarr`) |

   **c. Chemins de bibliothèque** — où vont les livres terminés

   | Paramètre | Valeur |
   |---|---|
   | Dossier livres audio | `/audiobooks` |
   | Dossier ebooks | `/ebooks` |
   | Dossier téléchargements | `/downloads` |

   **d. Audiobookshelf** *(optionnel mais recommandé)* — enrichissement des métadonnées et scans automatiques

   | Paramètre | Valeur |
   |---|---|
   | URL | `http://localhost:13378` — même espace réseau, `localhost` est donc correct ici |
   | Jeton API | Audiobookshelf **Settings** > **Users** > votre utilisateur > *API Token* |

   **e. Fournisseur de métadonnées — obligatoire, et le premier piège**

   Shelfarr a besoin d'une source de métadonnées fonctionnelle pour pouvoir chercher. Son ordre de priorité est `hardcover, openlibrary, google_books, comic_vine`, et par défaut **aucun ne fonctionne de façon fiable** :

   | Fournisseur | État par défaut | Correctif |
   |---|---|---|
   | Hardcover | Activé mais **sans jeton** → échoue | Inscrivez-vous sur [hardcover.app](https://hardcover.app/), puis **Account Settings** > **API** et collez le jeton. Gratuit, spécialisé livres — **faites celui-ci** |
   | OpenLibrary | Fonctionne, mais une seule mauvaise réponse le marque `degraded` et il n'est plus interrogé ; cet état **survit à un redémarrage** du conteneur | Se rétablit seul après le délai, ou réactivez-le dans les Settings |
   | Google Books | Le quota anonyme est partagé mondialement et est généralement **déjà épuisé** (`HTTP 429`) | Ajoutez une clé API gratuite depuis la [console Google Cloud](https://console.cloud.google.com/) (activez l'API Books) |

   > [!CAUTION]
   > Si vous voyez **« Unable to connect to metadata service. Please try again later. »**, c'est la raison — ce n'est pas un problème réseau. Vérifiez avec `docker logs shelfarr | grep MetadataService` ; vous verrez `Skipping openlibrary: degraded` et `Skipping google_books: rate_limited`. Renseignez un **jeton Hardcover** et cela se règle.

   **f. Accès** — choisissez le mode de connexion et, si vous le souhaitez, OIDC/2FA avant d'ouvrir à d'autres.

> [!NOTE]
> Shelfarr et Chaptarr sont des projets jeunes et leurs écrans de configuration bougent d'une version à l'autre — si un nom de champ ci-dessus ne correspond pas, consultez la documentation du projet. Épinglez des tags d'image explicites (`SHELFARR_VERSION`) et lisez les notes de version avant toute mise à jour. Chaptarr est explicitement en **bêta**.

> [!TIP]
> **Avez-vous besoin de Shelfarr *et* de Chaptarr ?** Probablement pas.
>
> - **Shelfarr seul** — l'expérience Jellyseerr. On parcourt, on demande, c'est fini : il cherche, télécharge, organise et livre dans Audiobookshelf. Le plus simple, et ce que veulent la plupart des gens.
> - **Chaptarr seul** — l'expérience Radarr. Pas d'interface de demandes, mais il *surveille* les auteurs et récupère automatiquement les sorties futures et les montées en qualité.
> - **Les deux** — seulement si vous voulez le flux de demandes de Shelfarr *et* la surveillance continue de Chaptarr. Donnez à chacun sa propre catégorie qBittorrent (`shelfarr` / `chaptarr`) pour qu'ils ne se disputent jamais le même téléchargement.

### **Tutoriel : votre premier livre audio**

Tout ce qui précède, c'est du câblage. Voici la chaîne complète, parcourue une fois de bout en bout.

#### **Étape 0 — vérifier la plomberie (2 min)**

Lancez ces quatre vérifications depuis l'hôte. Les quatre doivent passer avant de chercher.

```bash
# 1. qBittorrent passe bien derrière le VPN — ces deux IP DOIVENT différer
docker exec GlueTun-VPN wget -qO- https://api.ipify.org/   # IP de sortie VPN
curl -s https://api.ipify.org/                             # votre vraie IP

# 2. Un port est bien forwardé (un nombre, pas vide)
cat ${COMMON_PATH}/gluetun/forwarded_port

# 3. Le dossier de téléchargement chaptarr existe dans le conteneur
docker exec qbittorrent ls -ld /downloads/chaptarr

# 4. Chaptarr a des indexeurs, et aucun avertissement de santé
KEY=$(grep -oP '(?<=<ApiKey>)[^<]+' ${COMMON_PATH}/configs/chaptarr/config.xml | head -1)
curl -s -H "X-Api-Key: $KEY" http://localhost:8789/api/v1/indexer | grep -o '"name"' | wc -l
curl -s -H "X-Api-Key: $KEY" http://localhost:8789/api/v1/health
```

La vérification 4 doit afficher un nombre supérieur à `0` puis `[]` (vide = aucun avertissement). Si elle affiche `0`, Chaptarr n'a aucun indexeur — revenez à l'étape 3 du guide de configuration.

> [!IMPORTANT]
> La catégorie `chaptarr` dans qBittorrent doit avoir un **chemin de sauvegarde**. Une catégorie créée avec un chemin vide envoie silencieusement les téléchargements dans le dossier par défaut, et Chaptarr ne les importe jamais. Vérifiez dans **CATEGORIES** > clic droit sur `chaptarr` > **Éditer la catégorie** : *Save path* doit indiquer `/downloads/chaptarr`.

#### **Étape 1 — ajouter le livre dans Chaptarr**

1. Ouvrez `http://<hôte>:8789` > **Library** > **Add New**.
2. Saisissez un auteur ou un titre (ex. `Brandon Sanderson`) et choisissez le résultat voulu.
3. Remplissez la boîte de dialogue :

   | Champ | Valeur |
   |---|---|
   | Root Folder | `/audiobooks` |
   | Monitor | `All Books` — ou `None` si vous ne voulez que ce titre |
   | Quality Profile | `Audiobook` |
   | Metadata Profile | `Audiobook Default` |
   | Search for missing books | ✅ coché |

4. Cliquez sur **Add**. Chaptarr interroge immédiatement tous les indexeurs synchronisés.

> Choisir le profil de qualité `Audiobook` (et non `E-Book`) est ce qui l'empêche de récupérer un EPUB.

#### **Étape 2 — regarder la récupération**

- **Chaptarr** > **Activity** > **Queue** — la release apparaît en quelques secondes.
- **qBittorrent** (`http://localhost:8080`) — le torrent est là sous la catégorie `chaptarr`, enregistré dans `/downloads/chaptarr`.

Si la file reste vide, lancez plutôt une recherche manuelle : ouvrez le livre > cliquez sur la **loupe** > examinez la liste des releases > cliquez sur la **flèche de téléchargement** d'une release bien seedée. Cela vous indique aussi *pourquoi* la récupération automatique a été rejetée — survolez la release pour voir la raison (mauvais format, profil de qualité incompatible, etc.).

#### **Étape 3 — import**

Une fois le torrent terminé, Chaptarr le hardlinke dans `/audiobooks/<Auteur>/<Titre>/` et continue de seeder depuis `/downloads/chaptarr`. Vérifiez :

```bash
ls -R ${COMMON_PATH}/chaptarr/audiobooks | head -20
```

Si le fichier a été téléchargé mais jamais déplacé, c'est presque toujours l'incohérence de chemin de catégorie de l'étape 0.

#### **Étape 4 — écouter**

1. Ouvrez Audiobookshelf : `http://homeserver:13378`.
2. **Settings** > **Libraries** > votre bibliothèque Audiobooks > **Scan** (un scan planifié existe aussi).
3. Le livre apparaît avec sa jaquette et ses chapitres. Ouvrez-le dans le navigateur, ou dans l'application iOS/Android pointée sur `http://homeserver:13378` — la progression se synchronise entre les deux.

> [!TIP]
> **Vous préférez l'expérience Jellyseerr ?** Sautez complètement Chaptarr et utilisez **Shelfarr** (`http://homeserver:5056`) : cherchez, cliquez sur **Request**, et il interroge Prowlarr, télécharge via qBittorrent, organise les fichiers et les dépose seul dans votre bibliothèque Audiobookshelf. Les étapes 1 à 3 ci-dessus se réduisent à un clic.

---

### **Lancer un téléchargement torrent**

Documentation de référence pour les téléchargements suivants.

#### **Liste de vérification préalable**

Parcourez-la avant votre première recherche — un oubli ici est la cause habituelle des « aucun résultat » ou des « bloqué à 0 % » :

| # | Vérification | Comment vérifier |
|---|---|---|
| 1 | Le VPN est actif et qBittorrent passe derrière | `docker exec qbittorrent curl -s https://api.ipify.org/` renvoie l'IP du **VPN**, pas celle de votre FAI |
| 2 | Le port forwardé est appliqué | qBittorrent **Options** > **Connexion** > *Port d'écoute* correspond à `${COMMON_PATH}/gluetun/forwarded_port` (ce que `qbit-port-sync` automatise) |
| 3 | qBittorrent est en mode automatique | **Options** > **Téléchargements** > *Mode de gestion des torrents par défaut* : `Automatique` — sinon les chemins de sauvegarde par catégorie sont ignorés |
| 4 | La catégorie `chaptarr` existe | qBittorrent > **CATEGORIES** > `chaptarr` → `/downloads/chaptarr` |
| 5 | Les indexeurs sont synchronisés | Chaptarr > **Settings** > **Indexers** liste les trackers poussés par Prowlarr |
| 6 | Au moins un indexeur couvre les livres | Prowlarr > **Indexers**, les catégories de l'indexeur incluent *Audio > Audiobook* (`3030`) et/ou *Books* (`7000`, `8000`) |

#### **A. Télécharger via Chaptarr (bibliothèque surveillée)**

1. **Library** > **Add New** et cherchez un auteur ou un titre.
2. Choisissez le résultat, puis réglez :
   - **Root Folder** : `/audiobooks`
   - **Monitor** : `All Books` (ou `Future Books` si vous ne voulez que les nouveautés)
   - **Quality Profile** : un profil incluant les formats voulus (M4B, MP3)
   - **Search for missing books** : coché, pour démarrer immédiatement
3. Cliquez sur **Add**. Chaptarr interroge tous les indexeurs synchronisés et récupère la meilleure correspondance.
4. Suivez la progression dans **Activity** > **Queue**. Le torrent apparaît dans qBittorrent sous la catégorie `chaptarr`.
5. Pour chercher manuellement : ouvrez le livre > **Manual Search** (la loupe), examinez les releases et cliquez sur la flèche de téléchargement de celle que vous voulez.

Une fois le torrent terminé, Chaptarr l'importe dans `/audiobooks` (en hardlink, le seed continue donc), et Audiobookshelf le détecte au scan suivant — ou immédiatement via **Settings** > **Libraries** > *Scan*.

#### **B. Télécharger via Shelfarr (flux de demande)**

> [!IMPORTANT]
> **« Je ne vois que des ebooks — où sont les livres audio ? »**
>
> Il n'y a pas de filtre « livre audio » dans la recherche, et c'est voulu. Le menu déroulant de Shelfarr ne propose que **All**, **Books** et **Comics & Manga**, parce que les fournisseurs de métadonnées (Hardcover, OpenLibrary, Google Books) indexent des *œuvres*, pas des formats — un titre est une seule entrée, qu'il existe en audio ou en texte.
>
> **Le format se choisit à l'étape de la demande, pas à celle de la recherche.** Après avoir cliqué sur **Request**, un bloc **« Select format(s) »** apparaît avec trois cartes — **Audiobook**, **Ebook**, **Comics & Manga**. Cochez **Audiobook** (et décochez Ebook). C'est seulement là que Shelfarr interroge vos indexeurs avec la catégorie livre audio (`3030`) et dirige le résultat vers `/audiobooks`.

1. Cherchez un titre depuis la page d'accueil, avec le type de contenu **All** ou **Books**.
2. Cliquez sur **Request**, puis cochez **Audiobook** dans *Select format(s)*. La demande d'un admin est mise en file de recherche immédiatement ; celle des autres attend une approbation.
3. Shelfarr interroge Prowlarr (plus les sources directes que vous avez activées), note les résultats selon vos préférences de format et de langue, et choisit le meilleur automatiquement ou vous présente la liste.
4. La release est envoyée à qBittorrent sous la catégorie `shelfarr`.
5. Une fois terminée, **Shelfarr renomme et organise les fichiers lui-même** et les livre dans `/audiobooks`, puis déclenche un scan Audiobookshelf si vous l'avez connecté.
6. Le livre apparaît dans Audiobookshelf. Aucun déplacement manuel — cette étape d'import est ce qui distingue Shelfarr des interfaces de demandes seules.

#### **Dépannage**

| Symptôme | Cause probable |
|---|---|
| **« No indexers available with RSS sync enabled, Chaptarr will not grab new releases automatically »** | Chaptarr a **zéro** indexeur, parce qu'il n'a jamais été enregistré dans Prowlarr. Ajoutez-le dans Prowlarr **Settings** > **Apps** en tant qu'application **Readarr** (étape 3), puis *Sync App Indexers*. Vérifiez via **Settings** > **Indexers** dans Chaptarr — la liste ne doit pas être vide. |
| Indexeurs présents mais RSS toujours désactivé | Prowlarr en est propriétaire en Full Sync : basculer RSS depuis Chaptarr est écrasé. Activez RSS sur l'indexeur **dans Prowlarr**, puis resynchronisez. |
| Aucun résultat de recherche | L'indexeur n'a aucune catégorie livre mappée, ou Prowlarr n'a jamais synchronisé — relancez **Settings** > **Apps** > *Sync App Indexers* dans Prowlarr |
| Résultats trouvés, téléchargement jamais lancé | Le test du client de téléchargement échoue — le Host doit être **`gluetun`**, pas `qbittorrent` ; vérifiez ensuite le port `8080` et les identifiants |
| Le test de connexion reste bloqué, ou signale un serveur distant inattendu | Vous avez saisi `qbittorrent` comme Host et le DNS de votre FAI l'a résolu vers une adresse publique — utilisez `gluetun` |
| Torrent ajouté mais 0 pair / 0 % indéfiniment | Le port forwarding VPN est cassé ; revérifiez les points 1–2 ci-dessus et relancez `qbit-port-sync` |
| Téléchargé mais jamais importé | Incohérence de chemin de catégorie : qBittorrent doit écrire dans `/downloads/chaptarr`, qui doit être le même dossier hôte que le `/downloads/chaptarr` vu par Chaptarr |
| Importé mais absent d'Audiobookshelf | Le dossier de bibliothèque est erroné, ou il faut simplement scanner — **Settings** > **Libraries** > *Scan* |
| Tracker protégé par Cloudflare en échec | Ajoutez FlareSolverr dans Prowlarr (**Settings** > **Indexers** > `http://flaresolverr:8191/`) et taguez l'indexeur avec `flaresolverr` |

> [!CAUTION]
> Ne téléchargez que des contenus auxquels vous avez légalement droit. Ce que proposent vos indexeurs, et ce qui est licite là où vous vivez, relève entièrement de votre responsabilité — voir l'[Avertissement](#avertissement).

**[`^        retour au sommaire        ^`](#table-des-matières)**

---

# **Mise à jour des applications**

Pour mettre à jour les applications, vous devez d'abord arrêter les conteneurs en cours d'exécution et supprimer les images Docker existantes. Vous pouvez utiliser les commandes suivantes pour effectuer ces opérations :

```bash
docker-compose down
docker image prune -a
```

Ensuite, vous pouvez exécuter `docker-compose up -d` pour redémarrer les conteneurs avec les dernières versions des applications.

**[`^        retour au sommaire        ^`](#table-des-matières)**

# **Avertissement**

Ce code est fourni à titre informatif uniquement et ne doit pas être utilisé pour des activités illégales. Je ne suis pas responsable des actions effectuées par les utilisateurs de ce code. Ce code est à des fins informatives, et si les gens souhaitent l'utiliser, ils doivent consulter les lois de leurs pays.
