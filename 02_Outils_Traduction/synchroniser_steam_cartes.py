#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synchroniser_steam_cartes.py
Synchronise les fichiers 11_Textes_Generaux_Steam/ (Steam Part01 à Part06)
avec les traductions officielles créées dans :
TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json

- Met à jour les statistiques (SP Recovery, Gun Mult. +, Shield, etc.)
- Met à jour les effets 2 pièces et 4 pièces
- Met à jour les descriptions d'effets de cartes avec dimensionnement anti-chevauchement
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

# Descriptions spécifiques des combinaisons de cartes (optimisées anti-chevauchement UI)
CARD_ABILITY_OVERRIDES = {
    "After defeating a foe, increase user's Attack by 30% for 3 turns.":
        "Augmente l'ATQ de 30% pendant 3 tours après avoir tué un ennemi.",

    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color\\=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "<size=20>Augmente l'ATQ de <color\\=#2899ff>9%</color> à chaque coup sur ennemi avec malus (1 tour). Max 3 cumuls.</size>",

    "Whenever dealing damage to a foe with a debuff, increase user's Attack by 9% for 1 turn. Stacks up to 3 times.":
        "<size=20>Augmente l'ATQ de 9% à chaque coup sur ennemi avec malus (1 tour). Max 3 cumuls.</size>",

    "Increase party's Fire damage by <color\\=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color\\=#2899ff>6%</color> more for 2 turns.":
        "<size=20>Augmente les dégâts Feu de l'équipe de <color\\=#2899ff>6%</color> (+<color\\=#2899ff>6%</color> si ennemi Brûlé, 2 tours).</size>",

    "Increase damage dealt to foes with elemental ailments by <color\\=#2899ff>12%</color>. Stacks up to 2 times.":
        "<size=20>Augmente les dégâts aux ennemis avec altération de <color\\=#2899ff>12%</color>. Max 2 cumuls.</size>",

    "During battle, when SP reaches 100%/150%/200%, increase critical damage by <color\\=#2899ff>15%/30%/45%</color>.":
        "<size=20>En combat, quand les PC atteignent 100%/150%/200%, dégâts critiques +<color\\=#2899ff>15%/30%/45%</color>.</size>",

    "During battle, when SP reaches 100%/150%/200%, increase critical damage by 15%/30%/45%.":
        "<size=20>En combat, quand les PC atteignent 100%/150%/200%, dégâts critiques +15%/30%/45%.</size>",

    "At the start of battle, increase damage of the ally with the lowest Speed by <color\\=#2899ff>12%</color>. This effect won't activate if stacked.":
        "<size=20>Au début du combat, augmente les dégâts de l'allié à plus faible Vitesse de <color\\=#2899ff>12%</color>. Non cumulable.</size>",

    "After attacking a foe, increase party's damage by <color\\=#2899ff>8%</color> for 1 turn.":
        "<size=20>Après avoir attaqué un ennemi, augmente les dégâts de l'équipe de <color\\=#2899ff>8%</color> pendant 1 tour.</size>",

    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color\\=#2899ff>10%</color> for 2 turns.":
        "<size=20>Voleur Élucidateur : en infligeant un malus, réduit la Défense de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.</size>",

    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color\\=#2899ff>10%/20%/30%</color>.":
        "<size=20>En combat, quand les PV atteignent 6000/9000/12000, augmente les dégâts de <color\\=#2899ff>10%/20%/30%</color>.</size>",

    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color\\=#2899ff>24%/30%</color>.":
        "<size=20>Au début du combat, si 3e/4e dans l'ordre du tour, augmente l'Attaque de <color\\=#2899ff>24%/30%</color>.</size>"
}


def normalize_key(s):
    return s.replace('：', ':').replace(r'\=', '=').replace(r'\\=', '=').strip()


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

            # 2. Correspondance exacte dans les cartes
            if k in cards_non_empty:
                target_val = cards_non_empty[k]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 3. Correspondance avec égal échappé (\=)
            k_esc = k.replace("=", r"\=")
            if k_esc in cards_non_empty:
                target_val = cards_non_empty[k_esc]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 4. Correspondance normalisée (deux-points pleine chasse, etc.)
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
