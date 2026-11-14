# Projet de Traduction Française — Persona 5: The Phantom X (P5X)

Bienvenue dans l'environnement complet de fan-traduction française pour **Persona 5: The Phantom X** sur PC.
Ce dépôt regroupe l'intégralité des 168 modules de textes JSON, l'**Atelier de traduction interactif**, les outils d'ingénierie et le modpack BepInEx préconfiguré.

> 📢 **Note sur le Launcher :**  
> Le launcher officiel et recommandé pour jouer au jeu et gérer les mises à jour automatiques est **[P5XfrLauncher](https://github.com/Garloulou/P5XfrLauncher)** développé par **Garloulou**.  
> Le script `launcher_p5x.py` présent dans le dossier `04_Launcher_P5X_FR/` n'était qu'un **prototype de test interne** utilisé pour valider les injections. Pour jouer au quotidien, utilisez exclusivement le launcher de Garloulou !

> 🧪 **État d'avancement actuel (Phase de Test) :**  
> Pour le moment, **seul le kit complet de Hatsune Miku** (compétences en combat et dans les menus, passifs d'Awareness/Conscience 0-2, Piste, Miku's Stage, etc.) a été traduit afin de tester et valider l'ensemble du projet. Le reste du jeu sera traduit progressivement.  
>  
> 🐛 **Signalement de bugs :**  
> Si vous constatez un bug, un texte qui déborde, une coquille ou un problème d'injection, n'hésitez pas à ouvrir un ticket dans l'onglet **[Issues](https://github.com/Gyotre/P5X-Traduction-Francaise/issues)** !

---

## 📁 Structure du Projet

```text
_Traduction-P5X/
│
├── 📂 00_Documentation/              <- Guides et documentation de référence
│   ├── 📄 DOCUMENTATION_TECHNIQUE_P5X_TRADUCTION.docx (Documentation A-Z complète)
│   └── 📄 GUIDE_DU_TRADUCTEUR.md        (Guide pratique pas à pas pour traduire)
│
├── 📂 TRADUCTION_FACILE/            <- LA SOURCE : fichiers JSON {"Texte anglais": "Traduction"}
│   ├── 📂 00_Configuration_et_Substitutions/ (noms propres, règles)
│   └── 📂 01_Personnages/ ... 📂 11_Textes_Generaux_Steam/
│
├── 📂 TRADUCTION_FR/                <- Généré / références (ne pas éditer à la main)
│   ├── 📂 00_Compiles_Modulaires/     (copie de ce qui est envoyé au jeu)
│   ├── 📄 01_Kits_Personnages/00_Regex_Dynamiques.txt (regex écrites à la main, compilées aussi)
│   └── 📄 Glossaire_Officiel_P5_FR.md (termes officiels Persona)
│
├── 📂 03_Outils_Traduction/         <- Scripts d'ingénierie et de compilation
│   ├── 🐍 convertisseur_json.py       (Compile TRADUCTION_FACILE -> jeu + configure XUnity)
│   ├── 🐍 valider_traductions.py      (Balises, variables $1/{{A}}, conflits entre fichiers)
│   ├── 🐍 statistiques_avancement.py  (Avancement par catégorie)
│   ├── 🐍 chercher_texte.py           (Recherche un mot, en anglais ou en français)
│   ├── 🐍 generer_pack_release.py     (ZIP prêt à partager dans 06_Releases/)
│   └── 🐍 extraire_tout_le_jeu.py / adapter_p5xtes_en_json.py (régénèrent les JSON, sources requises)
│
├── 📂 04_Launcher_P5X_FR/           <- Atelier de Traduction (+ prototype test)
│   ├── 🐍 traducteur_p5x.py           (Atelier graphique complet de traduction)
│   └── 🐍 launcher_p5x.py             (Prototype de test interne - préférez P5XfrLauncher de Garloulou)
│
├── 📂 05_Paquet_BepInEx_Preconfigure/ <- Modpack BepInEx + XUnity prêt à l'emploi (A_COPIER_DANS_LE_JEU/)
│
├── 📂 _Sauvegardes/                  <- Archives et sauvegardes de sécurité (ex: BACKUP_TRADUCTIONS_MIKU)
│
├── 🎨 Atelier_Traduction.bat        <- L'atelier visuel complet pour traduire
├── 🔄 Mettre_A_Jour_Le_Jeu.bat      <- Compile et envoie la traduction dans le jeu en 1 clic
├── 📤 Pousser_Sur_GitHub.bat        <- Envoie automatiquement les changements sur votre repo GitHub
└── 🚀 Lancer_Launcher.bat           <- Ancien launcher de test (utilisez P5XfrLauncher de Garloulou)
```

> La synchronisation écrit uniquement dans `BepInEx/Translation/fr/Text/` et `BepInEx/config/AutoTranslatorConfig.ini`.
> Les anciens `.txt` trouvés dans `Text/` sont déplacés dans `BepInEx/Translation/fr/_anciens_fichiers_<date>/` (sinon ils doublonnent).

---

## ⚡ Démarrage Rapide

### 1. Pour Jouer au Jeu en Français
Téléchargez et utilisez le launcher moderne officiel développé par Garloulou :  
👉 **[P5XfrLauncher de Garloulou sur GitHub](https://github.com/Garloulou/P5XfrLauncher)**  
*Ce launcher installe BepInEx en 1 clic, gère la bascule Vanilla/Moddé et télécharge automatiquement les nouvelles versions de cette traduction depuis GitHub.*

### 2. Pour Contribuer à la Traduction (Atelier P5X)
Double-cliquez sur **`Atelier_Traduction.bat`** :
1. À gauche, choisis une section : **Personnages** (un fichier par personnage), **Arcanes & Cartes de Révélation**, Armes, Personas, Interface, Combat, Histoire…
2. Pour chaque texte : l'anglais en bleu, ta traduction dans la case en dessous. `Tab` passe à la case suivante, **= EN** recopie l'anglais (pour garder un nom tel quel).
3. **Chercher partout** trouve un mot dans tout le projet ; le filtre **Non traduits** n'affiche que ce qui reste à faire.
4. Les **textes à variables** (violet) : écris `$1`, `$2`… là où l'anglais montre `[$1]`, `[$2]`… (valeurs calculées par le jeu).
5. **⚡ INJECTER DANS LE JEU** : vérifie les balises et variables, enregistre, compile et envoie dans le jeu. En jeu : **Alt + R**.

Bon à savoir : une même phrase peut exister dans plusieurs fichiers ; l'option « Recopier dans les fichiers identiques » (cochée par défaut)
reporte ta traduction partout, sinon le compilateur pourrait garder une autre version.

---

## 🔄 Compatibilité Totale avec P5XfrLauncher (Garloulou)

Le projet intègre un pipeline de publication 100 % automatisé pour alimenter les mises à jour du launcher **[P5XfrLauncher](https://github.com/Garloulou/P5XfrLauncher)** :
* **Génération automatique de `translation.zip`** : Conforme à l'arborescence directe `BepInEx/Translation/fr/Text/` et `BepInEx/config/AutoTranslatorConfig.ini`.
* **Vérification d'intégrité SHA-256** : Le hash SHA-256 est calculé et injecté dans chaque release pour validation automatique par le launcher.
* **Publication GitHub Actions** : Dès qu'un tag de version (ex: `v1.0.0`) est envoyé sur GitHub, la release est générée, empaquetée et publiée automatiquement.

---

## 🛡️ Rappel Important sur les Risques de Ban
P5X étant un jeu-service en ligne géré par Perfect World / SEGA :
- **BepInEx injecte du code en mémoire (`winhttp.dll`).** L'anti-cheat du jeu peut théoriquement détecter ce comportement.
- Bien que le patch anglais soit très largement utilisé par la communauté sans bans massifs pour le moment, **le risque zéro n'existe pas**.
- Ne dépense pas d'argent réel sur un compte où tu utilises des mods et désactive toujours les mods via le launcher avant une mise à jour majeure du jeu.
- Dans AUCUN CAS, nous ne serons responsables de votre bannissement.
