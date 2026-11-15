# Journal des Modifications (Changelog) — P5X Traduction FR

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
