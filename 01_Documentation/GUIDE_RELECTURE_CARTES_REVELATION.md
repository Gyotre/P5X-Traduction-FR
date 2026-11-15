# Guide de Relecture des Cartes de Révélation (À revoir / Temporaire IA)

Ce guide est destiné à **Gyotre** pour repérer et retravailler facilement les textes temporaires générés par l'IA dans :
📁 [`TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json`](file:///d:/Anti-Gravity/_Traduction-P5X/TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json)

---

## 📌 Organisation des Sections dans le JSON

Le fichier JSON est maintenant balisé avec des commentaires `//` bien visibles. Tu peux effectuer une recherche (`Ctrl + F`) sur **`À REVOIR`** dans ton éditeur pour naviguer instantanément entre les sections :

| Section dans le JSON | Description du contenu | Statut |
| :--- | :--- | :--- |
| **Section 1** : `[TRADUIT PAR GYOTRE]` | Stats d'équipements (`Récup. PC`, `Dégâts Arme +`), noms d'Arcanes, dialogues de forge/personnalisation et démantèlement. | ✅ Validé par toi |
| **Section 2** : `[À REVOIR / TEMPORAIRE IA]` | Effets de Set Feu / Strife initiaux (multilignes). | 🟡 Temporaire IA |
| **Section 3** : `[À REVOIR / TEMPORAIRE IA]` | Effets de set format classique `<size=23>` avec variables `$1`, `$2`. | 🟡 Temporaire IA |
| **Section 4** : `[À REVOIR / TEMPORAIRE IA]` | Effets de set 2 pièces détaillés pour chaque élément (Feu, Glace, Élec, etc.) et statistique. | 🟡 Temporaire IA |
| **Section 5** : `[À REVOIR / TEMPORAIRE IA]` | Effets de set 4 pièces détaillés (*Worry*, *Fire*, *Ice*, *Elec*, *Malice*...). | 🟡 Temporaire IA |
| **Section 6** : `[À REVOIR / TEMPORAIRE IA]` | Capacités spécifiques des combinaisons (*Wisdom*, *Resolve*, *Perseverance*, *Nativity*, *Acuity*...). | 🟡 Temporaire IA |
| **Section 7** : `[À REVOIR / TEMPORAIRE IA]` | Variantes techniques avec puces `✦ ` et balises de couleur exactes pour le client Steam. | 🟡 Variantes techniques |

---

## ⚠️ Règles d'or à respecter quand tu retouches ces textes

Lorsque tu modifies les descriptions de ces cartes, garde en mémoire ces 4 règles techniques indispensables :

1. **🚫 Pas de parenthèses `()` :**  
   Les parenthèses dans les descriptions de compétences et d'arcanes peuvent créer des conflits de découpage ou de regex. Remplace-les par une virgule ou une formulation directe (ex: `augmentation max de 30%` au lieu de `(max 30%)`).

2. **🚫 Pas de point-virgule `;` :**  
   Le point-virgule est souvent interprété par les parsers de scripts. Remplace-le par un point ou reformule en deux phrases courtes.

3. **🎨 Échappement des balises de couleur :**  
   Dans les fichiers `.txt` compilés, toute balise de couleur doit avoir son égal échappé sous la forme `<color\=#2899ff>`. Dans le JSON source, écris `<color=#2899ff>` (ou `<color\\=#2899ff>`), le compilateur s'assure de l'échappement automatiquement.

4. **📖 Glossaire Officiel Persona 5 :**  
   * `Attack / ATK` ➔ **`ATQ`**
   * `Defense / DEF` ➔ **`DEF`**
   * `SP / SP Recovery` ➔ **`PC`** / **`Récup. PC`**
   * `HP` ➔ **`PV`**
   * `Highlight / Theurgy` ➔ **`HIGHLIGHT`**
   * `This effect won't activate if stacked.` ➔ **`Non cumulable.`**
   * `Elucidator Phantom Thief` ➔ **`Voleur Élucidateur`**

---

## ⚡ Comment appliquer tes modifications une fois retravaillées ?

1. Ouvre et modifie [02_Cartes_Revelation_et_Sets.json](file:///d:/Anti-Gravity/_Traduction-P5X/TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json).
2. Lance le compilateur :
   ```powershell
   python 02_Outils_Traduction/convertisseur_json.py
   ```
3. Si le jeu est ouvert, fais **`Alt + R`** en jeu pour admirer le résultat en direct !
