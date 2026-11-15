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
│   ├── 🐍 synchroniser_steam_cartes.py (Synchronise les textes Steam avec 02_Cartes_Revelation_et_Sets.json)
│   ├── 🐍 valider_traductions.py      (Balises, variables $1/{{A}}, conflits entre fichiers)
│   ├── 🐍 statistiques_avancement.py  (Avancement par catégorie)
│   ├── 🐍 chercher_texte.py           (Recherche un mot, en anglais ou en français)
│   ├── 🐍 generer_pack_release.py     (ZIP prêt à partager dans 06_Releases/)
│   └── 🐍 extraire_tout_le_jeu.py / adapter_p5xtes_en_json.py (régénèrent les JSON, sources requises)
│
├── 📂 03_Atelier_Traduction/        <- Application de Traduction (code source)
│   └── 🐍 traducteur_p5x.py           (Interface graphique complète de traduction)
│
├── 🎨 Application pour traduire - Facultatif.bat  <- Lanceur 1-clic de l'application visuelle
└── 📤 Pousser_Sur_GitHub.bat                      <- Envoie automatiquement les changements sur votre repo GitHub
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

> ⚠️ **IMPORTANT : Ne modifiez pas les fichiers JSON directement à la main dans le navigateur !**  
> Une traduction manuelle directe sans passer par l'application pose plusieurs problèmes majeurs :
> 1. **Conflits de doublons :** De nombreuses phrases existent dans plusieurs fichiers à la fois. L'application les synchronise automatiquement partout ; une édition manuelle crée des versions divergentes et bloque le compilateur.
> 2. **Désynchronisation Steam :** Les Cartes de Révélation doivent être synchronisées avec les fichiers Steam (`11_Textes_Generaux_Steam/`) via le bouton dédié de l'application pour être effectives en jeu.
> 3. **Risque de corruption syntaxique :** Oublier d'échapper un guillemet ou casser une balise (`<color>`, `$1`, `{{A}}`) rend le fichier JSON illisible pour le jeu.
> 
> 👉 **Pour traduire proprement et sans risque d'erreur, utilisez impérativement l'application dédiée !**

#### 💻 Comment contribuer étape par étape avec l'Application :
1. **Forkez et clonez** le dépôt sur votre ordinateur (`git clone https://github.com/Gyotre/P5X-Traduction-FR.git`).
2. Double-cliquez sur **`Application pour traduire - Facultatif.bat`** pour ouvrir l'Atelier visuel.
3. **Traduisez en toute sécurité :**
   * Choisissez votre catégorie à gauche (*Personnages*, *Cartes de Révélation*, *Histoire*, *Menus*...).
   * L'anglais apparaît en haut, votre case française en dessous (`Tab` passe au texte suivant).
   * L'option **« Recopier dans les fichiers identiques »** (activée par défaut) garantit qu'aucun doublon n'entre en conflit.
   * Si vous modifiez les Cartes, cliquez sur **`🔄 Sync Steam (Cartes)`** pour propager instantanément les textes dans la version Steam.
   * Cliquez sur **`⚡ INJECTER DANS LE JEU`** pour compiler et tester vos textes en direct en jeu avec **`Alt + R`**.
4. Une fois vos modifications terminées et testées, faites un commit et ouvrez une **Pull Request** sur GitHub !

*(💡 Si vous avez simplement repéré une coquille ou une faute sans vouloir cloner le projet, ouvrez une [Issue](https://github.com/Gyotre/P5X-Traduction-FR/issues) et nous l'intégrerons proprement pour vous !)*

---

## ✍️ Comment Traduire Proprement (Guide et Règles d'Or)

Pour que la traduction française soit immersive, fidèle à l'univers Persona et parfaitement intégrée au moteur du jeu sans bugs visuels ni crashs, voici les règles indispensables à respecter :

### 1. 📖 Respecter le Glossaire Officiel Persona (Cohérence Globale)
Ne traduisez pas au jugé : utilisez scrupuleusement la terminologie officielle de la version française de **Persona 5 / Persona 5 Royal / Persona 3 Reload** :
* **Points de vie & concentration :** `HP` $\rightarrow$ **`PV`**, `SP` $\rightarrow$ **`PC`** (*Points de Concentration*, jamais `SP` ni `PE`).
* **Statistiques d'équipement :**
  * `Attack` $\rightarrow$ **`Attaque`** (ou `ATQ`)
  * `Defense` $\rightarrow$ **`Défense`** (ou `DEF`)
  * `Speed` $\rightarrow$ **`Vitesse`** (ou `VIT`)
  * `SP Recovery` $\rightarrow$ **`Récupération PC`** (ou `Régénération PC`)
  * `Gun Mult. +` $\rightarrow$ **`Dégâts Tir +`**
  * `Shield` $\rightarrow$ **`Bouclier`**
  * `Crit Mult.` $\rightarrow$ **`Dégâts Crit.`**
  * `Crit Rate` $\rightarrow$ **`Taux Crit.`**
  * `Damage Mult. +` $\rightarrow$ **`Dégâts Bonus`**
  * `Pierce Rate` $\rightarrow$ **`Pénétration`**
  * `Ailment Acc.` $\rightarrow$ **`Préc. Altération`** *(cette abréviation précise est obligatoire : « Précision d'Altération » ou « Taux d'Altération » dépasse la largeur de colonne et tronque en `Taux d'Altérato...`)*
* **Termes de combat & cartes :**
  * `Set Effect` $\rightarrow$ **`Effet d'Arcane`** (sur les Cartes) ou **`Effet de Set`**
  * `Follow Up` $\rightarrow$ **`Attaque de Suivi`**
  * `Highlight` $\rightarrow$ **`Absolue`** (ou Highlight selon contexte P5X)
  * `Debuff` $\rightarrow$ **`Malus`** / `Buff` $\rightarrow$ **`Bonus`**
  * `Stack` $\rightarrow$ **`Cumul`** (*"Stacks up to 3 times"* $\rightarrow$ *"Cumulable 3 fois"* ou *"Jusqu'à 3 cumuls"*)
* 🔗 Référez-vous toujours au [Glossaire Officiel P5 FR](01_Documentation/Glossaire_Officiel_P5_FR.md).

---

### 2. 🏷️ Conserver les Balises et Variables Techniques (Crashs & Affichage)
Le moteur Unity (TextMeshPro) injecte dynamiquement des données dans les textes. Ces éléments techniques doivent **toujours** rester intacts :
* **Balises de couleur :** `<color=#FFFC40>...</color>` ou `<color\=#2899ff>...</color>`. Ne modifiez jamais le code hexadécimal ni la balise fermante `</color>`.
* **Variables dynamiques :** `$1`, `$2`, `$3`... représentent des nombres ou des variables calculées en temps réel par le jeu. Conservez-les dans l'ordre logique de votre phrase française.
* **Substitutions de noms :** `{{A}}`, `{{B}}` représentent le nom du protagoniste ou d'un allié géré par le module de substitution XUnity. Ne les effacez pas.
* **Sauts de ligne et échappements :** `\n` représente un retour à la ligne obligatoire dans l'interface ou les bulles. Les `\=` dans les clés JSON représentent des signes égal échappés.

---

### 3. 📐 Éviter le Bug de Chevauchement UI (Règle des 2 Lignes)
Dans P5X, les cartes de révélation et plusieurs fenêtres d'interface ont été conçues pour le texte chinois d'origine (très condensé). Leurs conteneurs ont des **hauteurs fixes** :
* ⚠️ **Le problème :** Dès qu'une description d'effet fait **3 lignes**, la 3e ligne dépasse du conteneur et chevauche le titre bleu de l'effet suivant !
* 💡 **La méthode pour traduire proprement :**
  1. **Privilégier la concision :** Allez droit au but sans phrases à rallonge.
     - ❌ *Trop long (3 lignes) :* `En combat, quand les Points de Concentration atteignent 100%/150%/200%, augmente les dégâts critiques de 15%/30%/45%.`
     - ✔️ *Parfait (2 lignes) :* `Quand les PC atteignent 100%/150%/200%, dégâts critiques +15%/30%/45%.`
  2. **Utiliser la balise de taille `<size=20>` :** Pour les descriptions denses, entourer le texte de `<size=20>...</size>` réduit légèrement la police et garantit que le texte reste sur 2 lignes sans déborder.
  3. **Titres de sets :** Les titres longs (ex: `Creation & Reconciliation`) sont automatiquement ajustés via `<size=16>` dans les regex pour tenir sur une seule ligne. **Ne jamais utiliser la balise HTML `<nobr>`**, car Unity TextMeshPro ne la reconnaît pas.

---

### 4. 🃏 Cartes de Révélation et Synchronisation Steam
* Le fichier `TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json` est la **source de vérité absolue** pour toutes les cartes et effets de sets.
* Les noms de base des cartes (ex: `Awareness`, `Creation`, `Departure`, `Resolve`) restent dans leur nomenclature reconnue par le jeu pour assurer le déclenchement des combos.
* 🔄 **Synchronisation automatique en 1 clic :** Dès que vous modifiez ou ajoutez des traductions dans `02_Cartes_Revelation_et_Sets.json`, cliquez sur le bouton **`🔄 Sync Steam (Cartes)`** dans l'application visuelle (ou lancez `python 02_Outils_Traduction/synchroniser_steam_cartes.py`). Cela répercute instantanément vos traductions dans les fichiers Steam (`11_Textes_Generaux_Steam/`) et garantit **0 conflit** à la compilation.

---

### 5. 🎭 Ton, Style et Personnalité des Phantom Thieves
* **Tutoiement entre équipiers :** Les membres du groupe (Joker, Ryuji, Morgana, Ann, Yusuke, Makoto, Futaba, Haru, Shun, etc.) se tutoient.
* **Vouvoiement de politesse :** Envers les adultes, les professeurs, les clients, Sojiro (au début) ou la police.
* **Éviter la traduction automatique brute :** Relisez toujours vos textes pour qu'ils sonnent naturels à l'oral en français.

---

### 6. ⚡ Vérifier et Tester en Jeu Avant de Valider
1. **Compiler et injecter :** Cliquez sur **`⚡ INJECTER DANS LE JEU`** dans l'application (ou lancez `python 02_Outils_Traduction/convertisseur_json.py`).
2. **Zéro conflit :** Le compilateur ne doit signaler aucun avertissement de conflit.
3. **Test immédiat en jeu :** En jeu, appuyez sur **`Alt + R`** pour recharger la traduction à chaud et vérifier instantanément le rendu visuel.
4. Pour plus d'exemples pas à pas, consultez également le **[Guide Pratique du Traducteur](01_Documentation/GUIDE_DU_TRADUCTEUR.md)**.

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
