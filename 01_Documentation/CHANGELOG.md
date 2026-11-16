# Journal des Modifications (Changelog) — P5X Traduction FR

## [v1.1.2] - 2026-11-16

### 🔄 Mise à jour :

* **Ajustements de traductions :**
  * Modification et révision de certaines traductions.

---

## [v1.1.1] - 2026-11-15

### 🐛 Correction de bug :

* **Cartes de Révélation :**
  * Correction et ajout de la traduction française manquante pour l'effet 4 pièces du set **[Gain]** (*Perseverance & Gain*) :
    > *« Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois. »*
  * Ajout des variantes textuelles complètes (avec/sans balises de couleur, espaces) et renforcement de la règle regex dynamique pour intercepter automatiquement l'affichage en jeu.

---

## [v1.1.0] - 2026-11-15

### 🚀 Release v1.1.0 — Traduction Intégrale des Cartes de Révélation, Arcanes & Statistiques :

* **Traduction intégrale du fichier des Arcanes (`02_Cartes_Revelation_et_Sets.json`) :**
  * **100% du fichier traduit :** L'intégralité des Cartes de Révélation, des effets de sets (2 pièces et 4 pièces), des combinaisons d'arcanes et des interfaces associées a été traduite en français.
  * **Statistiques d'équipement :** Traduction et harmonisation complète des statistiques principales et secondaires (`ATQ`, `DEF`, `PV`, `Récup. PC`, `Dégâts Arme +`, `Dégâts Bonus`, `Dégâts Crit.`, `Taux Crit.`, `Préc. Altération`, `Pénétration`, `Bouclier`...).
  * **Interface & Forge de Révélation :** Menus de personnalisation, dépenses de cartes d'arcanes (*Soleil, Lune, Étoile, Monde*), avertissements de confirmation, démantèlement de cartes en matériaux et gestion des cartes marquées.
* **Descriptions temporaires & Évolutions futures :**
  * ⚠️ *Note importante :* Certaines descriptions de cartes utilisent pour l'instant une formulation temporaire/provisoire afin de garantir que 100% des cartes soient immédiatement compréhensibles en jeu. Des modifications et affinements stylistiques seront apportés dans les prochaines mises à jour pour parfaire le rendu.
* **Technique & Robustesse (Moteur XUnity) :**
  * Déploiement de la **double couche de détection** (Regex Dynamiques universelles `(?s)` + Clés statiques exhaustives avec puces `✦ ` et balises Unity) assurant une disparition totale des textes anglais résiduels sur Steam.
  * Harmonisation terminologique sur **`Voleur Élucidateur`** (0 conflit lors de la compilation).
  * Activation du rechargement à chaud automatique (`ReloadTranslationsOnFileChange = True`).
* **Volume :** 2 467 entrées actives compilées et déployées dans le jeu.

---

## [v1.0.4] - 2026-11-15

### 🌟 Mise à jour v1.0.4 — Double Couche Cartes de Révélation (Regex Dynamiques + Variantes Statiques avec Puces) & Déploiement :

* **Intégration des modifications utilisateur (`02_Cartes_Revelation_et_Sets.json`) :**
  * Dialogue de fabrication et personnalisation de Révélation (`Dépenser $1 cartes...`, `Toutes les $1 cartes Soleil, Lune...`, `Impossible de modifier...`, `Révélation personnalisée actuelle...`).
  * Harmonisation des statistiques d'équipement : `SP Recovery` ➔ `Récup. PC`, `Gun Mult. +` ➔ `Dégâts Arme +`.
  * Textes de démantèlement et rappels de cartes marqués.
* **Résolution de l'affichage en jeu (Worry, Wisdom, Resolve, Perseverance, Nativity) :**
  * Ajout d'une couche de **regex dynamiques universelles** dans `00_Regex_Dynamiques.txt` : capture tous les effets multi-lignes, indépendamment des balises de couleur (`<color=#2899ff>`), puces graphiques (`✦ `) ou deux-points pleine chasse (`：`).
  * Ajout de **variantes statiques complètes avec et sans puce `✦ `** dans `06_Equipements_Objets_Cartes.txt`.
  * Cas résolus spécifiquement :
    * *Worry (Set 4 pièces)* : Remplissage jauge HIGHLIGHT de 25% au début du combat.
    * *Wisdom & Oppression* : Malice à 5 cumuls ou plus (+20% Dégâts Physiques et Préc. Altération).
    * *Wisdom & Pleasure* : Dégâts basés sur 50% de la Préc. Altération (max 30%).
    * *Wisdom & Virtue* : Après HIGHLIGHT, +30% ATQ et +25% dégâts.
    * *Resolve & Prudence* : Début de combat, 3e/4e allié dans l'ordre du tour (+24%/30% ATQ).
    * *Perseverance & Gain* : ATQ selon PV perdus (max 40% quand PV <= 40%).
    * *Perseverance & Sorrow* : +16% dégâts continus.
    * *Nativity & Strife* : Début de combat ou action supplémentaire (+10% Dégâts Critiques cumulable jusqu'à 2 fois).
    * *Voleur Élucidateur* : Effets de réduction de DEF (-10%), bonus PV/ATQ/DEF d'équipe (+2% par attribut assorti), buff PV Motoha et seuils de PV (6000, 9000 ou 12000).
* **Déploiement direct dans le jeu :**
  * 2 467 entrées actives compilées et déployées dans `E:\SteamLibrary\steamapps\common\P5X\client\pc\BepInEx\Translation\fr\Text\`.

---

## [v1.0.3] - 2026-11-15

### 🌟 Mise à jour Majeure v1.0.3 — Arcanes, Révélations & Moteur de Traduction :

* **Cartes de Révélation & Descriptions d'effets officielles :**
  * **Intégration des descriptions pour Departure et Awareness :** Traduction exacte des descriptions d'effets de cartes avec dimensionnement adapté et balises de couleurs dynamiques (`<color=#2899ff>`) :
    * *Departure & Control* : Réduction de DEF de l'ennemi principal pendant 2 tours après attaque.
    * *Departure & Prosperity* : Augmentation des dégâts de l'équipe pendant 1 tour lorsqu'un ennemi est attaqué.
    * *Departure & Hindrance* : Augmentation d'ATQ pendant 3 tours après avoir vaincu un ennemi.
    * *Awareness & Hindrance* : Augmentation d'ATQ à chaque coup sur un ennemi avec malus (jusqu'à 3 cumuls).
    * *Awareness & Control* : Augmentation des dégâts de Feu de l'équipe (+ bonus sous Brûlure).
    * *Awareness & Truth* : Augmentation des dégâts contre les ennemis sous altération élémentaire (jusqu'à 2 cumuls).
  * **Conservation des noms d'arcanes d'origine :** Les noms de sets et de combinaisons (*Departure*, *Awareness*, *Meditation*, *Wisdom*, *Creation*, *Resolve*, *Integrity*...) restent strictement en anglais pour garantir une cohérence parfaite avec les tier lists, guides et builds communautaires.
  * **Suppression définitive des chevauchements d'arcanes :** Tous les titres de combinaisons sont calibrés dynamiquement selon la largeur typographique réelle des lettres, garantissant qu'ils tiennent sur une seule ligne sans recouvrir les descriptions.

* **Correctif fondamental du compilateur pour XUnity AutoTranslator :**
  * **Échappement universel des `=` en `\=` :** Résolution du bug critique du parseur XUnity (*TextHelper*) qui rejetait en silence toute ligne contenant un `=` non échappé (balises `<size=...>`, `<color=...>`).
  * **207 lignes de traduction débloquées :** Restauration immédiate des balises de mise en page, de taille et de mise en valeur de texte dans tout le jeu.

* **Améliorations de l'Interface & Regex :**
  * **Correction typographique :** Ajout de l'espace manquant sur la description de bonus de Feu (*Awareness & Control*).
  * **Correction de libellé :** Correction de la coquille d'interface : `Weekly` (`Semains` → **`Semaine`**).
  * **Sécurisation des expressions régulières :** Ancrage strict par `$` de 23 règles de libellés courts (*Defense*, etc.) pour prévenir tout remplacement accidentel de phrases commençant par ces mots.

* **Compatibilité Totale Launcher :**
  * Pack optimisé et 100 % automatisé pour **[P5XfrLauncher de Garloulou](https://github.com/Garloulou/P5XfrLauncher)** avec vérification d'intégrité SHA-256.

---

## [v1.0.2.6] - 2026-11-15

### 🛠️ Correctifs et Améliorations de la version 1.0.2.6 :

* **Correction des bugs d'affichage liés aux descriptions et titres des Arcanes :**
  * **Suppression des chevauchements de texte :** Résolution définitive du problème où les titres de combinaisons d'arcanes trop longs (*Integrity & Pleasure*, *Departure & Control*, *Awareness & Hindrance*, etc.) se coupaient sur deux lignes et recouvraient la description des compétences.
  * **Ajustement typographique dynamique :** Tous les titres sont désormais calibrés en fonction de la largeur réelle des lettres pour tenir strictement sur une seule ligne sans aucun débordement.
  * **Descriptions des arcanes d'origine :** Les descriptions des effets de cartes sont conservées dans leur texte d'origine avec une taille uniforme et lisible.
  * **Déblocage complet sous XUnity AutoTranslator :** Échappement universel des caractères `=` assurant que 100 % des balises de taille et de couleur sont bien interprétées par le moteur du jeu.
* **Compatibilité Launcher :** Pack 100 % compatible avec le système de mise à jour automatique de **[P5XfrLauncher de Garloulou](https://github.com/Garloulou/P5XfrLauncher)**.

---

## [v1.0.2.5] - 2026-11-15

### 🛠️ Correctifs et Améliorations de la version 1.0.2.5 :

* **Correctif critique du compilateur pour XUnity AutoTranslator :**
  * Échappement universel de tous les `=` en `\=` (y compris à l'intérieur des balises `<size=...>`, `<color=...>`).
  * Déblocage de **207 lignes de traduction qui étaient silencieusement rejetées** par le parseur de XUnity (*TextHelper*), rétablissant immédiatement l'application de toutes les balises de taille et de couleur.
* **Titres de combinaisons de cartes calibrés sur la largeur réelle des lettres :**
  * Intégration du modèle de largeur typographique réelle (largeur par lettre calée sur 17 titres observés en jeu, seuil critique à 8,3 avec 10% de marge de sécurité).
  * Les titres longs sont ajustés précisément (ex: *Freedom & Disappointment* à 62%, *Creation & Reconciliation* à 66%, *Awareness & Hindrance* à 70%, *Awareness & Control* à 80%, *Harmony & Victory* à 89%, *Freedom & Defeat* à 92%), tandis que les titres courts restent à 100%.
  * Validation confirmée en jeu : **100% des titres tiennent sur une seule ligne sans aucun chevauchement**.
* **Descriptions des effets de cartes :**
  * Descriptions intégralement conservées en version originale anglaise et à taille normale uniforme.
* **Ancrage des expressions régulières ($) :**
  * 23 règles de libellés (dont *Defense*) ancrées avec `$` pour éviter de remplacer les phrases débutant par ces mots.
* **Correction de libellé :**
  * Correction de la coquille d'interface : `Weekly` (`Semains` → **`Semaine`**).

---

## [v1.0.2.4] - 2026-11-15

### 🛠️ Correctifs et Améliorations de la version 1.0.2.4 :

* **Conservation des descriptions originales des Cartes de Révélation :**
  * Rétablissement des descriptions d'effets de cartes dans leur langue originale (anglais), sans altération.
* **Maintien strict du réglage de taille anti-chevauchement :**
  * Tous les titres de combinaisons (56 arcanes telles que *Departure & Control*, *Creation & Reconciliation*, *Awareness & Hindrance*, *Meditation & Courage*, *Wisdom & Oppression*, etc.) et wildcards `$1` restent calibrés à `<size=13>`.
  * Les titres tiennent sur une seule ligne (largeur ~130px), supprimant le retour à la ligne et empêchant tout chevauchement sur les descriptions.
* **Synchronisation Steam & Cartes :**
  * Mise à jour de `synchroniser_steam_cartes.py` qui n'altère plus les descriptions et applique uniquement le formatage de taille sur les titres de cartes.

---

## [v1.0.2.3] - 2026-11-15

### 🛠️ Correctifs et Améliorations de la version 1.0.2.3 :

* **Résolution définitive du bug de chevauchement sur les Cartes de Révélation :**
  * Réduction automatique à `<size=13>` de tous les titres de combinaisons (56 combinaisons de cartes comme *Departure & Control*, *Creation & Reconciliation*, *Awareness & Hindrance*, *Meditation & Courage*, *Wisdom & Oppression*, etc.).
  * Correction du wildcard `$1` qui bloquait la réduction de taille dans le fichier source des cartes.
  * Les titres restent désormais strictement sur une seule ligne (largeur ~130px), éliminant physiquement toute seconde ligne et tout risque de chevauchement sur la description.

* **Traduction intégrale des 20 compétences d'arcanes de cartes :**
  * Traduction complète de tous les effets montrés sur les cartes : Théurgie, Soins, Voleur Élucidateur, seuils de PV/PC, ordre du tour (3e/4e allié), Dégâts Physiques & Électriques, Résonance, Absolue (Highlight), cumuls de Malice, malus de Défense, Dégâts Feu & Brûlure, et altérations élémentaires.
  * Chaque description est dimensionnée (`<size=20>`) pour tenir sur 2 lignes maximum, prévenant tout débordement dans l'interface.

* **Interface & Obtention des Cartes :**
  * Traduction des boutons d'obtention de cartes en bas d'écran : `How to Get` -> **`Obtention`**, `Take on Nightmare Catcher` -> **`Affronter le Chasseur de Cauchemars`**.
  * Correction des libellés de stats recommandées (`Mark: Moon/Star/Sky`) et des préconfigurations de cartes.

* **Synchronisation & Compilateur Modulaire :**
  * Mise à jour de `synchroniser_steam_cartes.py` intégrant l'anti-chevauchement `<size=13>` automatique sur tous les sets de cartes et les 20 effets d'arcanes.
  * 72 entrées synchronisées entre Steam et les Cartes de Révélation.
  * 0 conflit au compilateur modulaire (`valider_traductions.py`).

---

## [v1.0.2.2] - 2026-11-15

### 🛠️ Correctifs et Améliorations de la version 1.0.2.2 :

* **Cartes de Révélation & Correction du Chevauchement UI :**
  * Correction du bug d'affichage sur les Cartes de Révélation où les textes se superposaient.
  * Les titres de combinaisons longs (*Creation & Reconciliation*, *Awareness & Hindrance*, etc.) sont désormais ajustés avec `<size=16>` pour tenir sur une seule ligne.
  * Les descriptions d'effets de cartes sont calibrées (`<size=20>`) pour ne jamais dépasser 2 lignes, supprimant tout débordement sur l'effet suivant.
  * Remplacement de l'intitulé de stat par **`Préc. Altération`** afin d'éliminer définitivement la coupure d'interface (`Taux d'Altérato...`).
  * Harmonisation de `Set Effect` en `<size=18>Effet d'Arcane</size>` (suppression du retour à la ligne forcé).
  * Nettoyage des balises non supportées (`<nobr>`) pour garantir la compatibilité TextMeshPro d'Unity.

* **Synchronisation stricte des textes Steam (`11_Textes_Generaux_Steam/`) :**
  * Synchronisation intégrale de 57 entrées Steam avec la source de vérité `02_Cartes_Revelation_et_Sets.json`.
  * Traduction et correction de toutes les statistiques d'équipement (`SP Recovery` -> **`Récupération PC`**, `Gun Mult. +` -> **`Dégâts Tir +`**, `Shield` -> **`Bouclier`**, `Crit Mult.` -> **`Dégâts Crit.`**, `Damage Mult. +` -> **`Dégâts Bonus`**, `Pierce Rate` -> **`Pénétration`**, `Crit Rate` -> **`Taux Crit.`**).
  * Résolution des 3 conflits résiduels au compilateur (`0` conflit).

* **Nouvel Outil & Bouton de Synchronisation dans l'Application :**
  * Ajout du bouton **`🔄 Sync Steam (Cartes)`** dans l'application visuelle de traduction (`traducteur_p5x.py`).
  * Ajout du script autonome `02_Outils_Traduction/synchroniser_steam_cartes.py` permettant de synchroniser les fichiers Steam en 1 clic.

* **Documentation & Bonnes Pratiques :**
  * Ajout du guide complet *« Comment Traduire Proprement »* dans le `README.md` (règle des 2 lignes, glossaire officiel Persona, conservation des balises).

---

## [v1.0.2] - 2026-11-15
* Restructuration modulaire et documentation des modifications techniques.
* Nettoyage des dossiers et optimisation des paquets BepInEx.

---

## [v1.0.1] - 2026-11-14
* Kit complet Hatsune Miku traduit (compétences, conscience 0-2, piste, stage).
* Intégration du pipeline GitHub Actions compatible P5XfrLauncher.

---

## [v1.0.0] - 2026-11-14
* Release initiale de test du projet de traduction française.
