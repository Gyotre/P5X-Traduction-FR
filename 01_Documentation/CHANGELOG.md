# Journal des Modifications (Changelog) — P5X Traduction FR

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
