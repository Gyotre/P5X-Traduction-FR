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

# Descriptions spécifiques des combinaisons de cartes (optimisées anti-débordement UI en 2 lignes max)
CARD_ABILITY_OVERRIDES = {
    # 1. Theurgy / Théurgie
    "After activating a Theurgy, increase party's damage by <color\\=#2899ff>10%</color> for 3 turns.":
        "<size=20>Après avoir activé une Théurgie, augmente les dégâts de l'équipe de <color\\=#2899ff>10%</color> pendant 3 tours.</size>",
    "After activating a Theurgy, increase party's damage by <color=#2899ff>10%</color> for 3 turns.":
        "<size=20>Après avoir activé une Théurgie, augmente les dégâts de l'équipe de <color=#2899ff>10%</color> pendant 3 tours.</size>",
    "After activating a Theurgy, increase party's damage by 10% for 3 turns.":
        "<size=20>Après avoir activé une Théurgie, augmente les dégâts de l'équipe de 10% pendant 3 tours.</size>",
    "After using a Theurgy, increase party's damage by 10% for 3 turns.":
        "<size=20>Après avoir utilisé une Théurgie, augmente les dégâts de l'équipe de 10% pendant 3 tours.</size>",
    "After activating a Theurgy, increase Atk.":
        "<size=20>Après avoir activé une Théurgie, augmente l'Attaque.</size>",

    # 2. Healing effect / Soins
    "During battle, increase damage by 80% of user's healing effect (max <color\\=#2899ff>30%</color> increase).":
        "<size=20>En combat, augmente les dégâts de 80% des soins de l'utilisateur (max <color\\=#2899ff>30%</color>).</size>",
    "During battle, increase damage by 80% of user's healing effect (max <color=#2899ff>30%</color> increase).":
        "<size=20>En combat, augmente les dégâts de 80% des soins de l'utilisateur (max <color=#2899ff>30%</color>).</size>",
    "During battle, increase damage by 80% of user's healing effect (max 30% increase).":
        "<size=20>En combat, augmente les dégâts de 80% des soins de l'utilisateur (max 30%).</size>",

    # 3. Elucidator Thief start / Voleur Élucidateur début
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color\\=#2899ff>2%</color> more.":
        "<size=20>Voleur Élucidateur : au début du combat, +<color\\=#2899ff>2%</color> PV max, ATQ et DEF par allié du même attribut.</size>",
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color=#2899ff>2%</color> more.":
        "<size=20>Voleur Élucidateur : au début du combat, +<color=#2899ff>2%</color> PV max, ATQ et DEF par allié du même attribut.</size>",
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by 2% more.":
        "<size=20>Voleur Élucidateur : au début du combat, +2% PV max, ATQ et DEF par allié du même attribut.</size>",

    # 4. Elucidator Thief debuff / Voleur Élucidateur malus
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color\\=#2899ff>10%</color> for 2 turns.":
        "<size=20>Voleur Élucidateur : en infligeant un malus, réduit la Défense de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.</size>",
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color=#2899ff>10%</color> for 2 turns.":
        "<size=20>Voleur Élucidateur : en infligeant un malus, réduit la Défense de la cible de <color=#2899ff>10%</color> pendant 2 tours.</size>",
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by 10% for 2 turns.":
        "<size=20>Voleur Élucidateur : en infligeant un malus, réduit la Défense de la cible de 10% pendant 2 tours.</size>",

    # 5. HP threshold / Palier PV
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color\\=#2899ff>10%/20%/30%</color>.":
        "<size=20>En combat, quand les PV atteignent 6000/9000/12000, augmente les dégâts de <color\\=#2899ff>10%/20%/30%</color>.</size>",
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color=#2899ff>10%/20%/30%</color>.":
        "<size=20>En combat, quand les PV atteignent 6000/9000/12000, augmente les dégâts de <color=#2899ff>10%/20%/30%</color>.</size>",
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by 10%/20%/30%.":
        "<size=20>En combat, quand les PV atteignent 6000/9000/12000, augmente les dégâts de 10%/20%/30%.</size>",

    # 6. Turn order 3rd/4th / Ordre du tour 3e/4e
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color\\=#2899ff>24%/30%</color>.":
        "<size=20>Au début du combat, si 3e/4e dans l'ordre du tour, augmente l'Attaque de <color\\=#2899ff>24%/30%</color>.</size>",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color=#2899ff>24%/30%</color>.":
        "<size=20>Au début du combat, si 3e/4e dans l'ordre du tour, augmente l'Attaque de <color=#2899ff>24%/30%</color>.</size>",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by 24%/30%.":
        "<size=20>Au début du combat, si 3e/4e dans l'ordre du tour, augmente l'Attaque de 24%/30%.</size>",

    # 7. Physical and Electric / Physique et Électrique
    "Increase Physical and Electric damage by <color\\=#2899ff>12%</color>. If there is only 1 foe on the field, increase by <color\\=#2899ff>24%</color> more.":
        "<size=20>Dégâts Physiques et Électriques +<color\\=#2899ff>12%</color> (+<color\\=#2899ff>24%</color> si 1 seul ennemi).</size>",
    "Increase Physical and Electric damage by <color=#2899ff>12%</color>. If there is only 1 foe on the field, increase by <color=#2899ff>24%</color> more.":
        "<size=20>Dégâts Physiques et Électriques +<color=#2899ff>12%</color> (+<color=#2899ff>24%</color> si 1 seul ennemi).</size>",
    "Increase Physical and Electric damage by 12%. If there is only 1 foe on the field, increase by 24% more.":
        "<size=20>Dégâts Physiques et Électriques +12% (+24% si 1 seul ennemi).</size>",

    # 8. Resonance Crit DMG / Dégâts Crit Résonance
    "When activating a Resonance, increase critical damage by <color\\=#2899ff>50%</color>.":
        "<size=20>En activant une Résonance, augmente les dégâts critiques de <color\\=#2899ff>50%</color>.</size>",
    "When activating a Resonance, increase critical damage by <color=#2899ff>50%</color>.":
        "<size=20>En activant une Résonance, augmente les dégâts critiques de <color=#2899ff>50%</color>.</size>",
    "When activating a Resonance, increase critical damage by 50%.":
        "<size=20>En activant une Résonance, augmente les dégâts critiques de 50%.</size>",

    # 9. Crit hit healing / Soins après coup critique
    "After dealing a critical hit, increase user's healing effect by <color\\=#2899ff>28%</color> for 2 turns.":
        "<size=20>Après un coup critique, augmente les soins de l'utilisateur de <color\\=#2899ff>28%</color> pendant 2 tours.</size>",
    "After dealing a critical hit, increase user's healing effect by <color=#2899ff>28%</color> for 2 turns.":
        "<size=20>Après un coup critique, augmente les soins de l'utilisateur de <color=#2899ff>28%</color> pendant 2 tours.</size>",
    "After dealing a critical hit, increase user's healing effect by 28% for 2 turns.":
        "<size=20>Après un coup critique, augmente les soins de l'utilisateur de 28% pendant 2 tours.</size>",

    # 10. Highlight Attack & Damage / Absolue Attaque & Dégâts
    "After using a Highlight, increase Attack by <color\\=#2899ff>30%</color> and damage by <color\\=#2899ff>25%</color>.":
        "<size=20>Après une Absolue, augmente l'Attaque de <color\\=#2899ff>30%</color> et les dégâts de <color\\=#2899ff>25%</color>.</size>",
    "After using a Highlight, increase Attack by <color=#2899ff>30%</color> and damage by <color=#2899ff>25%</color>.":
        "<size=20>Après une Absolue, augmente l'Attaque de <color=#2899ff>30%</color> et les dégâts de <color=#2899ff>25%</color>.</size>",
    "After using a Highlight, increase Attack by 30% and damage by 25%.":
        "<size=20>Après une Absolue, augmente l'Attaque de 30% et les dégâts de 25%.</size>",

    # 11. Ailment accuracy DMG / Dégâts Précision Altération
    "During battle, increase damage by 50% of user's ailment accuracy (max <color\\=#2899ff>30%</color> increase).":
        "<size=20>En combat, augmente les dégâts de 50% de la précision d'altération (max <color\\=#2899ff>30%</color>).</size>",
    "During battle, increase damage by 50% of user's ailment accuracy (max <color=#2899ff>30%</color> increase).":
        "<size=20>En combat, augmente les dégâts de 50% de la précision d'altération (max <color=#2899ff>30%</color>).</size>",
    "During battle, increase damage by 50% of user's ailment accuracy (max 30% increase).":
        "<size=20>En combat, augmente les dégâts de 50% de la précision d'altération (max 30%).</size>",

    # 12. Malice stacks / Cumuls de Malice
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color\\=#2899ff>20%</color>.":
        "<size=20>À 5 cumuls de Malice ou plus : dégâts Physiques et précision d'altération +<color\\=#2899ff>20%</color>.</size>",
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color=#2899ff>20%</color>.":
        "<size=20>À 5 cumuls de Malice ou plus : dégâts Physiques et précision d'altération +<color=#2899ff>20%</color>.</size>",
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by 20%.":
        "<size=20>À 5 cumuls de Malice ou plus : dégâts Physiques et précision d'altération +20%.</size>",

    # 13. Skill attack DEF debuff / Malus Défense sur attaque compétence
    "When attacking with a skill, decrease main target's Defense by <color\\=#2899ff>23%</color> for 2 turns.":
        "<size=20>En attaquant avec une compétence, réduit la Défense de la cible de <color\\=#2899ff>23%</color> pendant 2 tours.</size>",
    "When attacking with a skill, decrease main target's Defense by <color=#2899ff>23%</color> for 2 turns.":
        "<size=20>En attaquant avec une compétence, réduit la Défense de la cible de <color=#2899ff>23%</color> pendant 2 tours.</size>",
    "When attacking with a skill, decrease main target's Defense by 23% for 2 turns.":
        "<size=20>En attaquant avec une compétence, réduit la Défense de la cible de 23% pendant 2 tours.</size>",

    # 14. Party damage after attack / Dégâts équipe après attaque
    "After attacking a foe, increase party's damage by <color\\=#2899ff>8%</color> for 1 turn.":
        "<size=20>Après avoir attaqué un ennemi, augmente les dégâts de l'équipe de <color\\=#2899ff>8%</color> pendant 1 tour.</size>",
    "After attacking a foe, increase party's damage by <color=#2899ff>8%</color> for 1 turn.":
        "<size=20>Après avoir attaqué un ennemi, augmente les dégâts de l'équipe de <color=#2899ff>8%</color> pendant 1 tour.</size>",
    "After attacking a foe, increase party's damage by 8% for 1 turn.":
        "<size=20>Après avoir attaqué un ennemi, augmente les dégâts de l'équipe de 8% pendant 1 tour.</size>",

    # 15. Attack after defeat / Attaque après victoire sur ennemi
    "After defeating a foe, increase user's Attack by <color\\=#2899ff>30%</color> for 3 turns.":
        "<size=20>Après avoir vaincu un ennemi, augmente l'Attaque de <color\\=#2899ff>30%</color> pendant 3 tours.</size>",
    "After defeating a foe, increase user's Attack by <color=#2899ff>30%</color> for 3 turns.":
        "<size=20>Après avoir vaincu un ennemi, augmente l'Attaque de <color=#2899ff>30%</color> pendant 3 tours.</size>",
    "After defeating a foe, increase user's Attack by 30% for 3 turns.":
        "<size=20>Après avoir vaincu un ennemi, augmente l'Attaque de 30% pendant 3 tours.</size>",

    # 16. Attack on debuffed foe / Attaque sur ennemi avec malus
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color\\=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "<size=20>Augmente l'ATQ de <color\\=#2899ff>9%</color> à chaque coup sur ennemi avec malus (1 tour). Max 3 cumuls.</size>",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "<size=20>Augmente l'ATQ de <color=#2899ff>9%</color> à chaque coup sur ennemi avec malus (1 tour). Max 3 cumuls.</size>",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by 9% for 1 turn. Stacks up to 3 times.":
        "<size=20>Augmente l'ATQ de 9% à chaque coup sur ennemi avec malus (1 tour). Max 3 cumuls.</size>",

    # 17. Fire damage / Dégâts Feu & Brûlé
    "Increase party's Fire damage by <color\\=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color\\=#2899ff>6%</color> more for 2 turns.":
        "<size=20>Augmente les dégâts Feu de l'équipe de <color\\=#2899ff>6%</color> (+<color\\=#2899ff>6%</color> si ennemi Brûlé, 2 tours).</size>",
    "Increase party's Fire damage by <color=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color=#2899ff>6%</color> more for 2 turns.":
        "<size=20>Augmente les dégâts Feu de l'équipe de <color=#2899ff>6%</color> (+<color=#2899ff>6%</color> si ennemi Brûlé, 2 tours).</size>",
    "Increase party's Fire damage by 6%. When a foe is Burning, increase party's Fire damage by 6% more for 2 tours.":
        "<size=20>Augmente les dégâts Feu de l'équipe de 6% (+6% si ennemi Brûlé, 2 tours).</size>",

    # 18. Elemental ailments / Altérations élémentaires
    "Increase damage dealt to foes with elemental ailments by <color\\=#2899ff>12%</color>. Stacks up to 2 times.":
        "<size=20>Augmente les dégâts aux ennemis avec altération de <color\\=#2899ff>12%</color>. Max 2 cumuls.</size>",
    "Increase damage dealt to foes with elemental ailments by <color=#2899ff>12%</color>. Stacks up to 2 times.":
        "<size=20>Augmente les dégâts aux ennemis avec altération de <color=#2899ff>12%</color>. Max 2 cumuls.</size>",
    "Increase damage dealt to foes with elemental ailments by 12%. Stacks up to 2 times.":
        "<size=20>Augmente les dégâts aux ennemis avec altération de 12%. Max 2 cumuls.</size>",

    # 19. SP threshold Crit DMG / Palier PC Dégâts Crit
    "During battle, when SP reaches 100%/150%/200%, increase critical damage by <color\\=#2899ff>15%/30%/45%</color>.":
        "<size=20>En combat, quand les PC atteignent 100%/150%/200%, dégâts critiques +<color\\=#2899ff>15%/30%/45%</color>.</size>",
    "During battle, when SP reaches 100%/150%/200%, increase critical damage by <color=#2899ff>15%/30%/45%</color>.":
        "<size=20>En combat, quand les PC atteignent 100%/150%/200%, dégâts critiques +<color=#2899ff>15%/30%/45%</color>.</size>",
    "During battle, when SP reaches 100%/150%/200%, increase critical damage by 15%/30%/45%.":
        "<size=20>En combat, quand les PC atteignent 100%/150%/200%, dégâts critiques +15%/30%/45%.</size>",

    # 20. Lowest Speed / Plus faible Vitesse
    "At the start of battle, increase damage of the ally with the lowest Speed by <color\\=#2899ff>12%</color>. This effect won't activate if stacked.":
        "<size=20>Au début du combat, augmente les dégâts de l'allié à plus faible Vitesse de <color\\=#2899ff>12%</color>. Non cumulable.</size>",
    "At the start of battle, increase damage of the ally with the lowest Speed by <color=#2899ff>12%</color>. This effect won't activate if stacked.":
        "<size=20>Au début du combat, augmente les dégâts de l'allié à plus faible Vitesse de <color=#2899ff>12%</color>. Non cumulable.</size>",
    "At the start of battle, increase damage of the ally with the lowest Speed by 12%. This effect won't activate if stacked.":
        "<size=20>Au début du combat, augmente les dégâts de l'allié à plus faible Vitesse de 12%. Non cumulable.</size>",

    # Éléments d'interface Cartes
    "How to Get": "Obtention",
    "How to Get:": "Obtention :",
    "Take on Nightmare Catcher": "Affronter le Chasseur de Cauchemars"
}


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

            # 2. Titres de combinaisons de cartes (ex: Departure & Control) -> <size=13> anti-chevauchement
            if is_combo_key(k):
                target_val = f"<size=13>{k.strip()}</size>"
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
