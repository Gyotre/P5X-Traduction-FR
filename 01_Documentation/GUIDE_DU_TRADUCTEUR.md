# Guide Pratique du Traducteur P5X

Ce guide t'explique pas à pas comment modifier, tester et valider les traductions pour les équipements et les kits de personnages dans Persona 5: The Phantom X.

---

## 1. La Règle Fondamentale : Le Format "Original": "Traduction"

Tout se traduit dans les fichiers JSON de `TRADUCTION_FACILE/` (ou via l'éditeur visuel) :
```json
{
  "Rarity": "Rareté",
  "Weapon Case": "Caisse d'arme",
  "Online Shopping": ""
}
```
- **À gauche** : le texte exact affiché par le jeu (en anglais). **Ne jamais le modifier.**
- **À droite** : ta traduction en français. Laisse `""` si ce n'est pas encore traduit.
- Le compilateur (`convertisseur_json.py`) transforme ça au format XUnity `Original=Traduction`.
- Si une même phrase existe dans plusieurs fichiers, la première trouvée (ordre des dossiers) est utilisée : `valider_traductions.py` signale les conflits.

### Les substitutions (`00_Configuration_et_Substitutions`, `*Substitutions*.json`)
Ce sont des noms propres. XUnity les remplace par `{{A}}`, `{{B}}`… avant de chercher la phrase : c'est pour ça que beaucoup de clés contiennent `{{A}}`.
- Laisse vide pour garder le nom tel quel (le compilateur écrit alors `Nom=Nom`).
- Ne mets une valeur que si le nom doit vraiment changer en français : elle s'appliquera **partout** dans le jeu.
- Dans tes traductions, garde les `{{A}}` aux bons endroits.

---

## 2. Gérer les Balises Visuelles (Unity Rich Text)

Le jeu utilise des balises pour styliser le texte. **Tu dois conserver les balises identiques** et ne traduire que le texte à l'intérieur :

| Balise | Rôle | Exemple de Traduction |
| :--- | :--- | :--- |
| `<color=#FFFC40>...</color>` | Couleur jaune/or | `<color=#FFFC40>Bonus ATQ +10%</color>` |
| `<size=26>...</size>` | Taille de police | `<size=26>Rang d'Élévation</size>` |
| `<b>...</b>` | Texte en gras | `<b>DÉG Critiques accrus</b>` |
| `\n` | Saut de ligne | `Attaque puissante.\nAugmente la défense.` |

> [!CAUTION]
> **Ne remplace jamais `\n` par la touche "Entrée" !**
> Chaque entrée de traduction doit rester sur **une seule et même ligne**. Si tu fais un retour à la ligne physique, XUnity ne reconnaîtra plus la ligne et affichera une erreur.

---

## 3. Gérer les Compétences et Chiffres Dynamiques (Regex)

Les compétences ont souvent des chiffres qui changent avec le niveau (ex : 12.5%, 3 tours). Pour éviter de devoir écrire une ligne pour chaque niveau, on utilise des **expressions régulières (Regex)** :

```text
r:"^Inflige (\d+)% de dégâts pendant (\d+) tours$"="Inflige $1% de dégâts pendant $2 tours"
```
- `(\d+)` capture un nombre.
- `$1` réinjecte le premier nombre capturé.
- `$2` réinjecte le deuxième nombre capturé.

---

## 4. Les Outils à ta Disposition

Dans le dossier `02_Outils_Traduction/`, tu disposes de plusieurs scripts pratiques :

### 📊 1. Voir l'avancement :
```powershell
python 02_Outils_Traduction/statistiques_avancement.py
```
Affiche le nombre de textes traduits par catégorie (`--fichiers` pour le détail par fichier).

### 🔍 2. Chercher un mot ou une arme :
```powershell
python 02_Outils_Traduction/chercher_texte.py "Deus Xiphos"
```
Recherche instantanément dans tous les fichiers pour savoir où se trouve un terme.

### ✅ 3. Vérifier qu'il n'y a pas d'erreur de syntaxe :
```powershell
python 02_Outils_Traduction/valider_traductions.py
```
Vérifie les balises, les variables (`$1`, `{{A}}`…) et les conflits entre fichiers avant de tester en jeu (`--tout` pour tout afficher).

### 📦 4. Créer un pack à distribuer à tes amis :
```powershell
python 02_Outils_Traduction/generer_pack_release.py 1.0.0
```
Génère dans `06_Releases/` un ZIP avec BepInEx, XUnity configuré en français et les traductions compilées, à copier dans le dossier du jeu.
