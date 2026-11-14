# Projet de Traduction Française — Persona 5: The Phantom X (P5X)

Bienvenue dans l'environnement complet de traduction française pour **Persona 5: The Phantom X**.
Ce dossier contient l'ensemble des fichiers de textes, les outils de développement, le package BepInEx préconfiguré et un **Launcher dédié** permettant de basculer en un clic entre le jeu d'origine (Vanilla) et le jeu moddé en français.

---

## 📁 Structure du Projet

```text
_Traduction-P5X/
│
├── 📂 TRADUCTION_FACILE/            <- LA SOURCE : fichiers JSON {"Texte anglais": "Traduction"}
│   ├── 📂 00_Configuration_et_Substitutions/ (noms propres, voir GUIDE)
│   ├── 📂 01_Personnages/ ... 📂 11_Textes_Generaux_Steam/
│
├── 📂 TRADUCTION_FR/                <- Généré / références (ne pas éditer à la main)
│   ├── 📂 00_Compiles_Modulaires/     (copie de ce qui est envoyé au jeu)
│   ├── 📄 01_Kits_Personnages/00_Regex_Dynamiques.txt (regex écrites à la main, compilées aussi)
│   └── 📄 Glossaire_Officiel_P5_FR.md (termes officiels Persona)
│
├── 📂 03_Outils_Traduction/         <- Scripts
│   ├── 🐍 convertisseur_json.py       (Compile TRADUCTION_FACILE -> jeu + configure XUnity)
│   ├── 🐍 valider_traductions.py      (Balises, variables $1/{{A}}, conflits entre fichiers)
│   ├── 🐍 statistiques_avancement.py  (Avancement par catégorie)
│   ├── 🐍 chercher_texte.py           (Recherche un mot, en anglais ou en français)
│   ├── 🐍 generer_pack_release.py     (ZIP prêt à partager dans 06_Releases/)
│   ├── 🐍 extraire_tout_le_jeu.py / adapter_p5xtes_en_json.py (régénèrent les JSON, sources requises)
│   └── 📂 _obsoletes/                 (anciens scripts gardés pour mémoire)
│
├── 📂 04_Launcher_P5X_FR/           <- Launcher + Éditeur visuel (Python/Tkinter)
├── 📂 05_Paquet_BepInEx_Preconfigure/ <- BepInEx + XUnity.AutoTranslator (A_COPIER_DANS_LE_JEU/)
├── 📂 BACKUP_TRADUCTIONS_MIKU/      <- Sauvegarde manuelle
│
├── 🚀 Lancer_Launcher.bat           <- Le launcher
├── ✏️ Ouvrir_Editeur_Traduction.bat <- L'éditeur visuel
├── 🔄 Mettre_A_Jour_Le_Jeu.bat      <- Compile et envoie la traduction dans le jeu
└── 📄 GUIDE_DU_TRADUCTEUR.md        <- Guide pratique pas à pas pour traduire
```

> La synchronisation écrit uniquement dans `BepInEx/Translation/fr/Text/` et `BepInEx/config/AutoTranslatorConfig.ini`.
> Les anciens `.txt` trouvés dans `Text/` sont déplacés dans `BepInEx/Translation/fr/_anciens_fichiers_<date>/` (sinon ils doublonnent).

---

## ⚡ Démarrage Rapide

### 1. Lancer le Launcher P5X FR
Double-clique sur **`Lancer_Launcher.bat`** :
1. Clique sur **"Parcourir..."** et indique l'emplacement de ton jeu (`P5X.exe`, situé généralement dans `P5X/client/pc`).
2. Clique sur **"SYNCHRONISER LA TRADUCTION FR"** pour copier automatiquement tes fichiers de traduction dans le jeu.
3. Clique sur **"LANCER LE JEU"**.

### 2. Basculer entre Mode Moddé et Mode Officiel (Vanilla)
- Le bouton **"BASCULER MODS ON / OFF"** dans le launcher permet d'activer ou désactiver instantanément BepInEx (`winhttp.dll` <-> `winhttp.dll.disabled`).
- Quand les mods sont désactivés, le jeu est 100 % officiel sans aucune injection mémoire, ce qui est parfait avant une mise à jour du jeu.

### 3. Traduire tes premiers équipements ou kits
1. Double-clique sur **`Ouvrir_Editeur_Traduction.bat`** (ou bouton **"ÉDITEUR FACILE"** du launcher), choisis une fiche et remplis les champs.
   Tu peux aussi éditer directement un JSON de `TRADUCTION_FACILE/` (VS Code, Notepad++…) : `"Texte anglais": "Ta traduction"`.
2. Lance `python 03_Outils_Traduction/valider_traductions.py` pour t'assurer qu'aucune balise ou variable n'est cassée.
3. Clique sur **"ENREGISTRER & APPLIQUER AU JEU"** (éditeur) ou **"SYNCHRONISER LA TRADUCTION FR"** (launcher), puis teste en jeu (Alt + R recharge à chaud).

---

## 🛡️ Rappel Important sur les Risques de Ban
P5X étant un jeu-service en ligne géré par Perfect World / SEGA :
- **BepInEx injecte du code en mémoire (`winhttp.dll`).** L'anti-cheat du jeu peut théoriquement détecter ce comportement.
- Bien que le patch anglais soit très largement utilisé par la communauté sans bans massifs pour le moment, **le risque zéro n'existe pas**.
- Ne dépense pas d'argent réel sur un compte où tu utilises des mods et désactive toujours les mods via le launcher avant une mise à jour majeure du jeu.
