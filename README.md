# Projet de Traduction Française — Persona 5: The Phantom X (P5X)

Bienvenue dans l'environnement complet de fan-traduction française pour **Persona 5: The Phantom X** sur PC.
Ce dépôt regroupe l'intégralité des 168 modules de textes JSON, l'**Atelier de traduction interactif**, les outils d'ingénierie et le modpack BepInEx préconfiguré.

> 📢 **Note sur le Launcher :**  
> Le launcher officiel et recommandé pour jouer au jeu et gérer les mises à jour automatiques est **[P5XfrLauncher](https://github.com/Garloulou/P5XfrLauncher)** développé par **Garloulou**.  
> Ce dépôt est dédié à la production, la maintenance et la mise à disposition des fichiers de traduction française. Pour jouer au quotidien, utilisez exclusivement le launcher de Garloulou !

> 🧪 **État d'avancement actuel (Phase de Test) :**  
> Pour le moment, **seul le kit complet de Hatsune Miku** (compétences en combat et dans les menus, passifs d'Awareness/Conscience 0-2, Piste, Miku's Stage, etc.) a été traduit afin de tester et valider l'ensemble du projet. Le reste du jeu sera traduit progressivement.  
>  
> 🐛 **Signalement de bugs :**  
> Si vous constatez un bug, un texte qui déborde, une coquille ou un problème d'injection, n'hésitez pas à ouvrir un ticket dans l'onglet **[Issues](https://github.com/Gyotre/P5X-Traduction-FR/issues)** !

---

## 📁 Structure du Projet

```text
_Traduction-P5X/
│
├── 📂 01_Documentation/              <- Guides et documentation de référence
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
├── 📂 02_Outils_Traduction/         <- Scripts d'ingénierie et de compilation
│   ├── 🐍 convertisseur_json.py       (Compile TRADUCTION_FACILE -> jeu + configure XUnity)
│   ├── 🐍 valider_traductions.py      (Balises, variables $1/{{A}}, conflits entre fichiers)
│   ├── 🐍 statistiques_avancement.py  (Avancement par catégorie)
│   ├── 🐍 chercher_texte.py           (Recherche un mot, en anglais ou en français)
│   ├── 🐍 generer_pack_release.py     (ZIP prêt à partager dans 06_Releases/)
│   └── 🐍 extraire_tout_le_jeu.py / adapter_p5xtes_en_json.py (régénèrent les JSON, sources requises)
│
├── 📂 03_Atelier_Traduction/        <- Atelier de Traduction
│   └── 🐍 traducteur_p5x.py           (Atelier graphique complet de traduction)
│
├── 🎨 Atelier_Traduction.bat        <- L'atelier visuel complet pour traduire
└── 📤 Pousser_Sur_GitHub.bat        <- Envoie automatiquement les changements sur votre repo GitHub
```

> La synchronisation écrit uniquement dans `BepInEx/Translation/fr/Text/` et `BepInEx/config/AutoTranslatorConfig.ini`.
> Les anciens `.txt` trouvés dans `Text/` sont déplacés dans `BepInEx/Translation/fr/_anciens_fichiers_<date>/` (sinon ils doublonnent).

---

## ⚡ Démarrage Rapide

### 1. Pour Jouer au Jeu en Français
Téléchargez et utilisez le launcher moderne officiel développé par Garloulou :  
👉 **[P5XfrLauncher de Garloulou sur GitHub](https://github.com/Garloulou/P5XfrLauncher)**  
*Ce launcher installe BepInEx en 1 clic, gère la bascule Vanilla/Moddé et télécharge automatiquement les nouvelles versions de cette traduction depuis GitHub.*

### 2. 🤝 Vous voulez contribuer ou modifier une traduction ?

**Où devez-vous aller ?**  
👉 **Rendez-vous dans le dossier [`TRADUCTION_FACILE/`](https://github.com/Gyotre/P5X-Traduction-FR/tree/main/TRADUCTION_FACILE)**  
C'est le **seul et unique endroit** où se font les traductions du projet. Il regroupe 168 fichiers `.json` simples classés par catégorie (ex: `01_Personnages/Joker.json`, `07_Cartes_Revelation_et_Sets.json`, `09_Interface_et_Menus/`, etc.).  
*(⚠️ Ne modifiez jamais les fichiers dans `TRADUCTION_FR/` ni les archives zip : ils sont compilés automatiquement par le système).*

#### 🌐 Méthode 1 : Traduire directement depuis GitHub (100% dans le navigateur, sans logiciel)
1. Naviguez dans le dossier **[`TRADUCTION_FACILE/`](https://github.com/Gyotre/P5X-Traduction-FR/tree/main/TRADUCTION_FACILE)**.
2. Ouvrez le fichier JSON que vous souhaitez traduire ou corriger (ex: votre Phantom Thief favori).
3. Cliquez sur l'icône de crayon **✏️ (« Edit this file »)** en haut à droite.
4. Renseignez la traduction française entre les guillemets de droite :
   ```json
   "Original English Text": "Votre traduction française ici"
   ```
5. En bas de page, cliquez sur **« Propose changes »** puis sur **« Create pull request »**.
6. Dès validation de votre proposition, elle sera fusionnée et incluse dans la prochaine version du launcher !

#### 💻 Méthode 2 : Traduire en local avec l'Atelier Visuel P5X
Si vous préférez cloner le dépôt et utiliser l'interface graphique dédiée :
1. Forkez et clonez le dépôt sur votre PC.
2. Double-cliquez sur **`Atelier_Traduction.bat`** :
   * À gauche, choisissez une section : **Personnages**, **Cartes de Révélation**, **Armes**, **Personas**, **Interface**, **Combat**, **Histoire**…
   * Pour chaque texte : l'anglais apparaît en haut, votre traduction dans la case en dessous. `Tab` passe au texte suivant.
   * Le bouton **Chercher partout** permet de retrouver un mot dans tout le projet ; le filtre **Non traduits** n'affiche que ce qui reste à faire.
   * Bouton **⚡ INJECTER DANS LE JEU** : valide la syntaxe, compile automatiquement et envoie directement dans votre jeu. Rechargement immédiat en jeu via **Alt + R**.
3. Poussez vos modifications sur votre branche et ouvrez une **Pull Request**.

#### ⚠️ Règles impératives pour les traducteurs :
1. **Consulter le [Glossaire Officiel](https://github.com/Gyotre/P5X-Traduction-FR/blob/main/01_Documentation/Glossaire_Officiel_P5_FR.md) :** Respectez impérativement le vocabulaire officiel Persona 5 (*Ennemi Principal*, *Attaque de Suivi*, *PV*, *PC*, *Cartes de Révélation*, *Absolue*, etc.).
2. **Respecter scrupuleusement les balises techniques :** Les balises visuelles (`<color=#FFFC40>`, `<size=...>`, `<b>`) et les variables du moteur de jeu (`$1`, `$2`, `{{A}}`) doivent rester **strictement intactes**. Ne traduisez que le texte autour.
3. Pour plus de détails sur les conventions, consultez le **[Guide Pratique du Traducteur](https://github.com/Gyotre/P5X-Traduction-FR/blob/main/01_Documentation/GUIDE_DU_TRADUCTEUR.md)**.

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
- Si vous postez des images en ligne avec le mod, n'oubliez pas de **cacher** votre ID pour éviter de vous faire bannir.
- Bien que le patch anglais soit très largement utilisé par la communauté sans bans massifs pour le moment, **le risque zéro n'existe pas**.
- Ne dépense pas d'argent réel sur un compte où tu utilises des mods et désactive toujours les mods via le launcher avant une mise à jour majeure du jeu.
- Dans AUCUN CAS, nous ne serons responsables de votre bannissement.
