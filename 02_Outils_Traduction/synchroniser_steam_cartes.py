#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synchroniser_steam_cartes.py
Synchronise les fichiers 11_Textes_Generaux_Steam/ (Steam Part01 à Part06)
avec les traductions officielles créées dans :
TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json

- Met à jour les statistiques (SP Recovery, Gun Mult. +, Shield, etc.)
- Met à jour les effets 2 pièces et 4 pièces
- Met à jour les titres de combinaisons (ex: Departure & Control) avec taille anti-chevauchement <size=13>
- Met à jour les descriptions d'effets de cartes avec dimensionnement anti-débordement <size=20>
- Assure une stricte cohérence et élimine tout conflit au compilateur
"""

import os
import glob
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EASY_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")
CARDS_FILE = os.path.join(EASY_DIR, "08_Equipements_et_Objets", "02_Cartes_Revelation_et_Sets.json")
STEAM_DIR = os.path.join(EASY_DIR, "11_Textes_Generaux_Steam")

REVELATION_CARD_NAMES = {
    "Awareness", "Departure", "Growth", "Meditation", "Faith", "Trust", "Harmony",
    "Acceptance", "Integrity", "Wisdom", "Resolve", "Creation", "Freedom", "Hope",
    "Perseverance", "Acuity", "Nativity", "Purity", "Self", "Determination", "Embrace",
    "Strength"
}

# Descriptions spécifiques des cartes (reprise exacte de vos traductions dans 02_Cartes_Revelation_et_Sets.json)
CARD_ABILITY_OVERRIDES = {
    # --- DEPARTURE ---
    "When attacking with a skill, decrease main target's Defense by <color\\=#2899ff>23%</color> for 2 turns.":
        "Réduit la DEF de l'ennemie principal de <color\\=#2899ff>23%</color> pendant 2 tours aprés l'avoir attaquer avec une compétence.",
    "When attacking with a skill, decrease main target's Defense by <color=#2899ff>23%</color> for 2 turns.":
        "Réduit la DEF de l'ennemie principal de <color=#2899ff>23%</color> pendant 2 tours aprés l'avoir attaquer avec une compétence.",
    "When attacking with a skill, decrease main target's Defense by 23% for 2 turns.":
        "Réduit la DEF de l'ennemie principal de 23% pendant 2 tours aprés l'avoir attaquer avec une compétence.",

    "After attacking a foe, increase party's damage by <color\\=#2899ff>8%</color> for 1 turn.":
        "Augmente les dégats infligés de l'équipe de <color\\=#2899ff>8%</color> pendant 1 tour lorsqu'un ennemie est attaqué.",
    "After attacking a foe, increase party's damage by <color=#2899ff>8%</color> for 1 turn.":
        "Augmente les dégats infligés de l'équipe de <color=#2899ff>8%</color> pendant 1 tour lorsqu'un ennemie est attaqué.",
    "After attacking a foe, increase party's damage by 8% for 1 turn.":
        "Augmente les dégats infligés de l'équipe de 8% pendant 1 tour lorsqu'un ennemie est attaqué.",

    "After defeating a foe, increase user's Attack by <color\\=#2899ff>30%</color> for 3 turns.":
        "Augmente l'ATQ de <color\\=#2899ff>30%</color> pendant 3 tour aprés avoir tué un ennemie.",
    "After defeating a foe, increase user's Attack by <color=#2899ff>30%</color> for 3 turns.":
        "Augmente l'ATQ de <color=#2899ff>30%</color> pendant 3 tour aprés avoir tué un ennemie.",
    "After defeating a foe, increase user's Attack by 30% for 3 turns.":
        "Augmente l'ATQ de 30% pendant 3 tour aprés avoir tué un ennemie.",

    # --- AWARENESS ---
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color\\=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de <color\\=#2899ff>9%</color> pour chaque coup infligés sur un ennemie avec un malus pendant 1 tours, jusqu'à 3 cumuls.",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de <color=#2899ff>9%</color> pour chaque coup infligés sur un ennemie avec un malus pendant 1 tours, jusqu'à 3 cumuls.",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by 9% for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de 9% pour chaque coup infligés sur un ennemie avec un malus pendant 1 tours, jusqu'à 3 cumuls.",

    "Increase party's Fire damage by <color\\=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color\\=#2899ff>6%</color> more for 2 turns.":
        "Augmente chez les alliée les dégats de Feu de <color\\=#2899ff>6%</color>; Augmente chez les alliée les dégats de Feu de <color\\=#2899ff>6%</color> pour 2 tours qu'on on inflige Brûlure.",
    "Increase party's Fire damage by <color=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color=#2899ff>6%</color> more for 2 turns.":
        "Augmente chez les alliée les dégats de Feu de <color=#2899ff>6%</color>; Augmente chez les alliée les dégats de Feu de <color=#2899ff>6%</color> pour 2 tours qu'on on inflige Brûlure.",
    "Increase party's Fire damage by 6%. When a foe is Burning, increase party's Fire damage by 6% more for 2 turns.":
        "Augmente chez les alliée les dégats de Feu de 6%; Augmente chez les alliée les dégats de Feu de 6% pour 2 tours qu'on on inflige Brûlure.",

    "Increase damage dealt to foes with elemental ailments by <color\\=#2899ff>12%</color>. Stacks up to 2 times.":
        "Augmente les dégats infligés de <color\\=#2899ff>12%</color> lors qu'on attaque un ennemie sous altérations , jusqu'à 2 cumuls.",
    "Increase damage dealt to foes with elemental ailments by <color=#2899ff>12%</color>. Stacks up to 2 times.":
        "Augmente les dégats infligés de <color=#2899ff>12%</color> lors qu'on attaque un ennemie sous altérations , jusqu'à 2 cumuls.",
    "Increase damage dealt to foes with elemental ailments by 12%. Stacks up to 2 times.":
        "Augmente les dégats infligés de 12% lors qu'on attaque un ennemie sous altérations , jusqu'à 2 cumuls.",
}


# Largeur relative des lettres (police des titres, en em). Calibrée sur 17 titres observés en jeu :
# tout titre plus large que 9,24 se coupe sur 2 lignes (ex. « Harmony & Victory »), en dessous il tient.
LARGEUR_LETTRES = {}
for _lettres, _l in (("iljI|.,:;'!", 0.30), ("ftr()[] ", 0.38), ("sczJ", 0.52),
                     ("abdeghknopquvxyLFSTZPE&", 0.60), ("BCRKXYV", 0.68), ("ADGHNOQU", 0.75), ("mwMW", 0.90)):
    for _c in _lettres:
        LARGEUR_LETTRES[_c] = _l
TITRE_LARGEUR_MAX = 8.3   # limite observée 9,24, moins ~10 % de marge


def largeur_titre(titre):
    titre = re.sub(r"\{\{.\}\}|\$\d+", "Caroline", titre)   # nom inconnu : le plus long des noms substitués
    return sum(LARGEUR_LETTRES.get(c, 0.6) for c in titre)


def taille_titre(titre):
    """Valeur anti-chevauchement d'un titre de combinaison : inchangé s'il tient sur une ligne,
    sinon réduit juste assez (taille relative en %) pour tenir sur une ligne."""
    titre = titre.strip()
    largeur = largeur_titre(titre)
    if largeur <= TITRE_LARGEUR_MAX:
        return titre
    pct = max(55, int(TITRE_LARGEUR_MAX * 100 / largeur))
    return f"<size={pct}%>{titre}</size>"


def normalize_key(s):
    return s.replace('：', ':').replace(r'\=', '=').replace(r'\\=', '=').strip()


def is_combo_key(k):
    """Détecte si une clé est un titre de combinaison de cartes de Révélation (ex: Departure & Control)."""
    if ' & ' not in k:
        return False
    parts = k.split(' & ')
    if len(parts) == 2 and parts[0].strip() in REVELATION_CARD_NAMES:
        return True
    return False


def synchroniser(easy_dir=EASY_DIR):
    """
    Synchronise les fichiers 11_Textes_Generaux_Steam avec 02_Cartes_Revelation_et_Sets.json.
    Renvoie (total_updates, files_updated, details).
    """
    cards_path = os.path.join(easy_dir, "08_Equipements_et_Objets", "02_Cartes_Revelation_et_Sets.json")
    if not os.path.exists(cards_path):
        raise FileNotFoundError(f"Fichier Cartes introuvable : {cards_path}")

    with open(cards_path, "r", encoding="utf-8") as f:
        cards_data = json.load(f)

    # Récupérer toutes les traductions non vides
    cards_non_empty = {k.strip(): str(v).strip() for k, v in cards_data.items() if str(v).strip()}

    norm_cards = {}
    for k, v in cards_non_empty.items():
        nk = normalize_key(k)
        norm_cards[nk] = v
        norm_cards[nk.lower()] = v

    steam_files = sorted(glob.glob(os.path.join(easy_dir, "11_Textes_Generaux_Steam", "*.json")))
    if not steam_files:
        raise FileNotFoundError("Aucun fichier trouvé dans 11_Textes_Generaux_Steam.")

    total_updates = 0
    files_updated = 0
    details = []

    for sf in steam_files:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)

        file_mods = 0
        for k in list(data.keys()):
            # 1. Vérification des descriptions spécifiques
            if k in CARD_ABILITY_OVERRIDES:
                target_val = CARD_ABILITY_OVERRIDES[k]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 2. Titres de combinaisons de cartes (ex: Departure & Control) -> réduits seulement s'ils sont trop longs
            if is_combo_key(k):
                target_val = taille_titre(k)
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 3. Correspondance exacte dans les cartes
            if k in cards_non_empty:
                target_val = cards_non_empty[k]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 4. Correspondance avec égal échappé (\=)
            k_esc = k.replace("=", r"\=")
            if k_esc in cards_non_empty:
                target_val = cards_non_empty[k_esc]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 5. Correspondance normalisée (deux-points pleine chasse, etc.)
            nk = normalize_key(k)
            if nk in norm_cards:
                target_val = norm_cards[nk]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue
            elif nk.lower() in norm_cards:
                target_val = norm_cards[nk.lower()]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

        if file_mods > 0:
            with open(sf, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            files_updated += 1
            total_updates += file_mods
            details.append(f"{os.path.basename(sf)} : {file_mods} entrée(s)")

    return total_updates, files_updated, details


if __name__ == "__main__":
    print("Synchronisation des textes Steam avec les Cartes de Révélation...")
    nb_updates, nb_files, det = synchroniser()
    print(f"Terminé : {nb_updates} entrée(s) synchronisée(s) dans {nb_files} fichier(s).")
    for d in det:
        print(f"  • {d}")
