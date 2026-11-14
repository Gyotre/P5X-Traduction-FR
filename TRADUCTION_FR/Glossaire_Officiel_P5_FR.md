# Glossaire Officiel Persona 5 - Référence pour la Traduction Française (P5X)

Ce document sert de guide de référence pour garantir la cohérence des termes traduits dans les fichiers d'équipements, de kits de personnages et d'interfaces.

---

## 1. Éléments et Attributs

| Terme Anglais | Terme Chinois / Coréen | Terme Officiel Français | Sorts Associés |
| :--- | :--- | :--- | :--- |
| **Physical** | 物理 / 물리 | **Physique** | Frappe, Tranchant, etc. |
| **Gun** | 射擊 / 사격 | **Tir** | Tir puissant, Rafale |
| **Fire** | 火焰 / 화염 | **Feu** | Agi, Agilao, Agidyne, Maragi |
| **Ice** | 冰凍 / 빙결 | **Glace** | Bufu, Bufula, Bufudyne, Mabufu |
| **Electric** | 電擊 / 전격 | **Électricité** | Zio, Zionga, Ziodyne, Mazio |
| **Wind** | 疾風 / 질풍 | **Vent** | Garu, Garula, Garudyne, Magaru |
| **Psy** | 念動 / 염동 | **Psychokinésie (Psy)** | Psi, Psio, Psiodyne, Mapsi |
| **Nuclear** | 核熱 / 핵열 | **Nucléaire** | Frei, Freila, Freidyne, Mafrei |
| **Bless** | 祝福 / 축복 | **Béni** | Kouha, Kouga, Kougaon, Makouha |
| **Curse** | 詛咒 / 주살 | **Maudit** | Eiha, Eiga, Eigaon, Maeiha |
| **Almighty** | 萬能 / 만능 | **Tout-Puissant** | Megido, Megidola, Megidolaon |

---

## 2. Statistiques et Termes de Combat

| Terme Anglais | Français Recommandé | Abréviation Standard |
| :--- | :--- | :--- |
| **HP / Health** | Points de Vie | **PV** |
| **SP / Stamina Points** | Points de Concentration / Énergie | **PC** (ou **SP**) |
| **ATK / Attack** | Attaque | **ATQ** |
| **DEF / Defense** | Défense | **DEF** |
| **CRIT Rate** | Taux de Critique | **Taux CRIT** |
| **CRIT DMG** | Dégâts Critiques | **DÉG CRIT** |
| **Speed** | Vitesse | **VIT** |
| **Accuracy** | Précision | **PRÉC** |
| **Evasion** | Évasion / Esquive | **ESQ** |
| **Penetration** | Pénétration | **PÉN** |
| **Damage Bonus** | Bonus de Dégâts | **Bonus DÉG** |
| **Damage Reduction** | Réduction de Dégâts | **Réduc. DÉG** |

---

## 3. Mécaniques de Jeu Spécifiques à Persona 5 & P5X

| Terme Anglais | Terme Chinois | Traduction Française Recommandée |
| :--- | :--- | :--- |
| **All-Out Attack** | 總攻擊 | **Assaut Général** |
| **1 More** | 1 More / 再動 | **1 More** |
| **Baton Pass / Highlight** | 接力 / HIGHLIGHT | **Passage de Relais / Highlight** |
| **Weak** | 弱點 | **Faiblesse** |
| **Resist** | 耐性 | **Résistance** |
| **Block / Null** | 無效 | **Nul** (Immunité) |
| **Absorb / Drain** | 吸收 | **Absorption** |
| **Repel / Reflect** | 反彈 | **Renvoi** |
| **Technical** | TECHNICAL | **Coup Technique** |
| **Down** | 倒地 | **À terre (Down)** |
| **Awareness / Awakening** | 意識 / 覺醒 | **Conscience / Éveil** (Doublons de gacha) |
| **Revelation Cards** | 啟示卡 | **Cartes de Révélation** (Reliques / Sets) |
| **Persona Trait** | 人格面具特性 | **Trait de Persona** |
| **Weapon Reform** | 武器改造 | **Refonte d'Arme** |
| **Weapon Enhance** | 武器突破 | **Élévation d'Arme** |

---

## 4. Altérations d'État (Ailments)

| Terme Anglais | Français Officiel | Effet en jeu |
| :--- | :--- | :--- |
| **Burn** | **Brûlure** | Dégâts continus de Feu à chaque tour |
| **Freeze** | **Gel** | Empêche d'agir, vulnérable au Physique/Tir |
| **Shock** | **Électrocution** | Empêche d'agir, vulnérable au Physique/Tir |
| **Dizzy** | **Étourdissement** | Réduit fortement la précision |
| **Forget** | **Oubli** | Empêche l'utilisation de compétences de Persona |
| **Sleep** | **Sommeil** | Empêche d'agir, régénère un peu PV/PC, vulnérable aux coups |
| **Confuse** | **Confusion** | Jette de l'argent ou utilise des objets au hasard |
| **Fear** | **Peur** | Risque de fuir ou d'être paralysé de terreur |
| **Despair** | **Désespoir** | Perte de PC par tour, mort au bout de 3 tours |
| **Rage** | **Colère** | Double l'attaque mais réduit la défense à zéro |
| **Brainwash** | **Lavage de cerveau** | Attaque ses propres alliés ou soigne l'ennemi |
| **Hunger** | **Famine** | Réduit considérablement les dégâts infligés |

---

## 5. Règle d'Or pour les Balises et Formats de Textes

Dans les fichiers XUnity, les lignes utilisent souvent des balises Unity Rich Text :
- `<color=#FFFC40>Texte</color>` : **Garder impérativement les balises `<color>` et `</color>` intactes.** Ne traduire que le texte à l'intérieur.
- `<size=24>Texte</size>` : **Garder les balises de taille intactes.**
- `\n` : Représente un saut de ligne. Ne jamais le remplacer par un vrai saut de ligne physique (Entrée) dans le fichier `.txt`, sinon le fichier sera corrompu.
- `$1`, `$2`, `$3` dans les regex : Variables dynamiques (ex: pourcentage de dégâts, nombre de tours). Conservez leur ordre ou adaptez-les selon la grammaire française.
