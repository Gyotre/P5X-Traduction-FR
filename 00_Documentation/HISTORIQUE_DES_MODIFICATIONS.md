# Rapport Récapitulatif Complet des Modifications — Projet Traduction P5X FR

Ce document récapitule l'ensemble des travaux, corrections d'ingénierie, créations d'outils, restructurations et mises en ligne réalisés sur le projet de fan-traduction française de **Persona 5: The Phantom X (P5X)**.

---

## 1. Résolution des Problèmes Techniques & Mécaniques XUnity

* **Problème des noms d'Arcanes ("Lutte" vs nom d'origine) :**
  * Identification de la règle de priorité et des correspondances parasites dans les dictionnaires globaux.
  * Verrouillage du nom officiel des Arcanes / Cartes de Révélation via des clés isolées pour empêcher que le terme d'origine ne soit écrasé par inadvertance.
* **Problème de description Strife non traduite :**
  * Découverte du comportement **LIFO (Last In, First Out)** du moteur XUnity AutoTranslator : les fichiers regex sont évalués dans l'ordre alphabétique inverse (`99_...` est prioritaire sur `00_...`).
  * Détection du texte de bas de page masqué dans les infobulles TextMeshPro du jeu, qui faussait les regex strictes avec fins de ligne `$` ou `\n`.
  * Configuration impérative de `ForceSplitTextByNewline=False` dans `AutoTranslatorConfig.ini` pour permettre la capture de blocs de compétences multilignes complexes.
  * Prise en compte du système `TemplatedOriginal_Text` (remplacement dynamique des variables de jeu par `{{A}}`, `{{B}}` et `$1`, `$2`).

---

## 2. Création de l'Atelier de Traduction & des Outils

* **Atelier Graphique Tkinter (`04_Launcher_P5X_FR/traducteur_p5x.py`) :**
  * Interface ergonomique sombre/rouge Persona 5, classant les 168 fichiers JSON en 14 sections thématiques.
  * Système de badges visuels pour repérer instantanément les variables calculées (`[$1]`, `[$2]`, etc.).
  * Synchronisation et propagation automatique des traductions identiques sur l'ensemble des fichiers du projet (évite les conflits entre doublons).
  * Bouton **« ⚡ INJECTER DANS LE JEU »** avec validation syntaxique des balises et compilation à chaud.
* **Lanceur d'Atelier (`Atelier_Traduction.bat`) :** Raccourci 1-clic à la racine pour ouvrir l'Atelier visuel.
* **Compilateur Modulaire (`03_Outils_Traduction/convertisseur_json.py`) :**
  * Compilation des 168 JSONs vers les 6 modules texte du jeu en une fraction de seconde.
  * Gestion automatique et vérification de `AutoTranslatorConfig.ini` (`FromLanguage=en`, `Language=fr`).
  * Déploiement direct dans `BepInEx/Translation/fr/Text/` avec rechargement en jeu via `Alt + R`.
* **Générateur de Release (`03_Outils_Traduction/generer_pack_release.py`) :**
  * Empaquette automatiquement `translation.zip` selon la structure exacte attendue par l'updater du launcher.
  * Calcule et affiche l'empreinte de sécurité **SHA-256**.
* **Script de Synchronisation GitHub (`Pousser_Sur_GitHub.bat`) :**
  * Prise en compte automatique de tous les ajouts (`git add -A`), commit avec message au choix et push vers GitHub en 1 double-clic.

---

## 3. Nettoyage et Réorganisation Complète des Dossiers (~70 Mo libérés)

* **Éléments obsolètes supprimés :**
  * Suppression de 3 archives ZIP brutes redondantes dans `05_Paquet_BepInEx_Preconfigure/` (~69 Mo libérés), le dossier extrait `A_COPIER_DANS_LE_JEU/` étant déjà complet et prêt à l'emploi.
  * Suppression de l'ancien dossier `03_Outils_Traduction/_obsoletes/` contenant des scripts morts ciblant des répertoires disparus.
  * Suppression de l'ancien prototype `04_Launcher_P5X_FR/editeur_traduction.py` et des raccourcis doublons.
  * Élimination des brouillons Word temporaires au profit de la version finale consolidée.
* **Nouvelle Arborescence Claire :**
  * **`00_Documentation/`** : Centralisation de tous les guides (`DOCUMENTATION_TECHNIQUE_P5X_TRADUCTION.docx`, `GUIDE_DU_TRADUCTEUR.md`, `Glossaire_Officiel_P5_FR.md`).
  * **`TRADUCTION_FACILE/`** : Les 168 fichiers JSON sources organisés par catégorie.
  * **`TRADUCTION_FR/`** : Les textes compilés et glossaires de référence.
  * **`03_Outils_Traduction/`** : Les scripts d'ingénierie et de compilation actifs.
  * **`04_Launcher_P5X_FR/`** : L'Atelier graphique de traduction.
  * **`05_Paquet_BepInEx_Preconfigure/`** : Le pack BepInEx + XUnity prêt à l'emploi.
  * **`_Sauvegardes/`** : Stockage isolé des anciennes sauvegardes (`BACKUP_TRADUCTIONS_MIKU`).

---

## 4. Intégration & Compatibilité avec P5XfrLauncher (Garloulou)

* **Audit du code source C# du launcher de Garloulou :**
  * Analyse de `GitHubUpdateService.cs` : l'updater interroge l'API GitHub Releases, compare les tags SemVer, cherche un asset `(?i)translation.*\.zip` et vérifie le hash SHA-256 dans le corps de la release.
  * L'archive `translation.zip` a été structurée pour s'extraire directement à la racine du jeu (`BepInEx/Translation/fr/Text/...` et `BepInEx/config/AutoTranslatorConfig.ini`).
* **Automatisation par GitHub Actions (`.github/workflows/release.yml`) :**
  * Dès qu'un tag de version (ex: `v1.0.1`) est envoyé sur GitHub, le serveur compile le projet, génère `translation.zip`, calcule le SHA-256 et publie la Release officielle.
* **Mise au point sur le Launcher dans le README :**
  * Clarification officielle indiquant que **P5XfrLauncher de Garloulou** est le launcher recommandé pour jouer, et que le script python local était un prototype de test.
* **Publications en ligne réussies :**
  * Release **v1.0.0** et Release **v1.0.1** publiées avec succès sur GitHub.

---

## 5. Enrichissement du Glossaire Officiel (`Glossaire_Officiel_P5_FR.md`)

* **Intégration des choix de l'équipe :**
  * `Extra Action / Extra Turn` ➔ **Action Supplémentaire / Tour Supplémentaire**
  * `Set Effect` ➔ **Effet d'Arcane**
  * Éléments et stats ajustés (*Absolue*, *Arme*, *Électriques*, *Psy*, etc.).
* **Ajout de 4 nouvelles sections majeures (+55 termes récurrents) :**
  * **Déclencheurs (Triggers) :** *Au début du combat*, *Au début/fin du tour*, *Tué / En éliminant*, *En subissant des dégâts*, *Temps de recharge*, *Dure $1 tours*, etc.
  * **Cibles (Targets) :** *Ennemi Principal*, *Tous les ennemis*, *1 ennemi*, *Ennemis adjacents*, *L'équipe*, *Soi-même*, etc.
  * **Actions & Effets :** *Attaque de Suivi*, *Cumulable jusqu'à*, *Obtient*, *Confère aux alliés*, *Bouclier*, *Vol de vie*, *Dégâts infligés/subis*, etc.
  * **Menus & Métavers :** *Carte de Révélation*, *Caisse d'arme*, *Ombre errante*, *Mémentos*, *Signature de Contrat*, etc.

---

## 6. Avancement des Textes & Traductions Actives

* **Hatsune Miku / Teto :** Kit complet traduit (compétences combat & menu, passifs Conscience 0-2, Piste, Stage) avec adaptation textuelle et passif « La préféré de toute ».
* **Harmonisations générales :**
  * Traduction de *Basic* en **Simple** (Phoebe, mini-jeux, interface).
  * Traduction de *Revelation Card* en **Carte de Revelation**.
  * Traduction de *Cost:* en **Coût:** et *Mark:* en **Symbole:**.
* **Total des textes actifs injectés :** Passé de 1 521 à **1 706 entrées compilées** dans le jeu.

---

## 7. Configuration Git & Attribution des Commits

* **Identité officielle configurée :**  
  * `user.name` = **Gyotre**  
  * `user.email` = **tyogre232@gmail.com**
* **Réécriture de l'historique :** 100 % des commits passés (depuis le premier commit) ont été réécrits pour être attribués à `Gyotre`.
* **Dépôt officiel en ligne :** [https://github.com/Gyotre/P5X-Traduction-FR](https://github.com/Gyotre/P5X-Traduction-FR) (synchronisé, public et à jour).

---

## 8. Déploiement de la Release v1.0.2 & Compatibilité P5XfrLauncher

* **Release GitHub officielle :** [Release v1.0.2](https://github.com/Gyotre/P5X-Traduction-FR/releases/tag/v1.0.2)
* **Tag Git :** `v1.0.2`
* **Intégration P5XfrLauncher validée :**
  * Archive générée : `translation.zip` (25,7 Ko).
  * Structure interne conforme : `BepInEx/config/AutoTranslatorConfig.ini` et `BepInEx/Translation/fr/Text/*.txt`.
  * Hash SHA-256 calculé et inséré dans le corps de la release GitHub pour la vérification d'intégrité automatique du launcher.
  * Détection automatique comme `latest release` via l'API GitHub.
