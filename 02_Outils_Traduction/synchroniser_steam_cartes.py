#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synchroniser_steam_cartes.py
Synchronise les fichiers 11_Textes_Generaux_Steam/ (Steam Part01 à Part06)
avec les traductions officielles créées dans :
TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json

- Met à jour les statistiques (SP Recovery, Gun Mult. +, Shield, etc.)
- Met à jour les effets 2 pièces et 4 pièces (toutes variantes de deux-points et balises)
- Met à jour les titres de combinaisons (ex: Departure & Control) avec taille anti-chevauchement <size=13>
- Met à jour les descriptions d'effets de cartes avec dimensionnement et glossaire officiel
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

# Dictionnaire complet des capacités de cartes et effets de sets
CARD_ABILITY_OVERRIDES = {
    # --- RÈGLES GÉNÉRALES & MENUS ---
    "Equip the same type of Revelation Cards to activate Set Effects.":
        "Équipez des Cartes de Révélation du même type pour activer les Effets d'Arcane.",
    "[Set Effects]":
        "[Effets d'Arcane]",
    "Activate a 4-piece Revelation Set Effect 5 times.":
        "Activer un effet d'Arcane de Révélation 4 pièces 5 fois.",
    "Activate a 4-piece Revelation Set Effect once.":
        "Activer un effet d'Arcane de Révélation 4 pièces une fois.",

    # --- EFFETS 4 PIÈCES & 2 PIÈCES ---
    "4 Set Effect：At the start of battle, fill Highlight gauge by <color\\=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect: At the start of battle, fill Highlight gauge by <color\\=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect：At the start of battle, fill Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect: At the start of battle, fill Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect：At the start of battle, fill Highlight gauge by 25%. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable.",
    "4 Set Effect: At the start of battle, fill Highlight gauge by 25%. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable.",

    "4 Set Effect：At the start of battle, fill the Highlight gauge by <color\\=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect: At the start of battle, fill the Highlight gauge by <color\\=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect：At the start of battle, fill the Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect: At the start of battle, fill the Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect：At the start of battle, fill the Highlight gauge by 25%. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable.",
    "4 Set Effect: At the start of battle, fill the Highlight gauge by 25%. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable.",

    "4 Set Effect：From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 turns. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> tous les 6 tours. Cumulable jusqu'à 3 fois.",
    "4 Set Effect: From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 turns. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> tous les 6 tours. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：Increase Curse damage to foes with debuffs by <color\\=#2899ff>20%</color>.":
        "Effet 4 pièces : Augmente les dégâts Maudits infligés aux ennemis avec un malus de <color\\=#2899ff>20%</color>.",
    "4 Set Effect: Increase Curse damage to foes with debuffs by <color\\=#2899ff>20%</color>.":
        "Effet 4 pièces : Augmente les dégâts Maudits infligés aux ennemis avec un malus de <color\\=#2899ff>20%</color>.",
    "4 Set Effect：After allies use Electric skills, increase own Electric damage by <color\\=#2899ff>9%</color>. Stacks up to 3 times.":
        "Effet 4 pièces : Après que les alliés ont utilisé des compétences Électriques, augmente ses propres dégâts Électriques de <color\\=#2899ff>9%</color>. Cumulable jusqu'à 3 fois.",
    "4 Set Effect: After allies use Electric skills, increase own Electric damage by <color\\=#2899ff>9%</color>. Stacks up to 3 times.":
        "Effet 4 pièces : Après que les alliés ont utilisé des compétences Électriques, augmente ses propres dégâts Électriques de <color\\=#2899ff>9%</color>. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：When attacking, 25% chance to deal <color\\=#2899ff>20%</color> of the user's Attack as bonus damage.":
        "Effet 4 pièces : Lors d'une attaque, 25% de chances d'infliger <color\\=#2899ff>20%</color> de l'ATQ du lanceur en dégâts bonus.",
    "4 Set Effect: When attacking, 25% chance to deal <color\\=#2899ff>20%</color> of the user's Attack as bonus damage.":
        "Effet 4 pièces : Lors d'une attaque, 25% de chances d'infliger <color\\=#2899ff>20%</color> de l'ATQ du lanceur en dégâts bonus.",
    "4 Set Effect：Increase healing to allies with less than 50% HP by <color\\=#2899ff>23%</color>.":
        "Effet 4 pièces : Augmente les soins prodigués aux alliés ayant moins de 50% de PV de <color\\=#2899ff>23%</color>.",
    "4 Set Effect: Increase healing to allies with less than 50% HP by <color\\=#2899ff>23%</color>.":
        "Effet 4 pièces : Augmente les soins prodigués aux alliés ayant moins de 50% de PV de <color\\=#2899ff>23%</color>.",
    "4 Set Effect：When attacking with a skill, deal <color\\=#2899ff>8%</color> of own HP as bonus damage to the target.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige à la cible des dégâts bonus équivalents à <color\\=#2899ff>8%</color> de ses propres PV.",
    "4 Set Effect: When attacking with a skill, deal <color\\=#2899ff>8%</color> of own HP as bonus damage to the target.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige à la cible des dégâts bonus équivalents à <color\\=#2899ff>8%</color> de ses propres PV.",
    "4 Set Effect：When attacking with a skill, deal <color\\=#2899ff>30%</color> of user's Attack as damage if the target has an elemental ailment.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige <color\\=#2899ff>30%</color> de l'ATQ du lanceur en dégâts si la cible subit une altération élémentaire.",
    "4 Set Effect: When attacking with a skill, deal <color\\=#2899ff>30%</color> of user's Attack as damage if the target has an elemental ailment.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige <color\\=#2899ff>30%</color> de l'ATQ du lanceur en dégâts si la cible subit une altération élémentaire.",
    "4 Set Effect：When equipped by an Elucidator Phantom Thief: During battle, increase party's max HP, Attack, and Defense by <color\\=#2899ff>8%</color>.":
        "Effet 4 pièces : Si équipé par un Voleur Fantôme Élucidateur : pendant le combat, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>8%</color>.",
    "4 Set Effect: When equipped by an Elucidator Phantom Thief: During battle, increase party's max HP, Attack, and Defense by <color\\=#2899ff>8%</color>.":
        "Effet 4 pièces : Si équipé par un Voleur Fantôme Élucidateur : pendant le combat, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>8%</color>.",
    "4 Set Effect：When dealing Psychokinesis damage, increase Attack by 15%. If more than 3 foes are on the field, increase Attack by <color\\=#2899ff>15%</color> more.":
        "Effet 4 pièces : En infligeant des dégâts Psy, augmente l'ATQ de 15%. S'il y a plus de 3 ennemis sur le terrain, augmente l'ATQ de <color\\=#2899ff>15%</color> supplémentaires.",
    "4 Set Effect: When dealing Psychokinesis damage, increase Attack by 15%. If more than 3 foes are on the field, increase Attack by <color\\=#2899ff>15%</color> more.":
        "Effet 4 pièces : En infligeant des dégâts Psy, augmente l'ATQ de 15%. S'il y a plus de 3 ennemis sur le terrain, augmente l'ATQ de <color\\=#2899ff>15%</color> supplémentaires.",
    "4 Set Effect：When current HP is 50% or more, increase critical rate of Bless skills by <color\\=#2899ff>12%</color>.":
        "Effet 4 pièces : Quand les PV actuels sont à 50% ou plus, augmente le taux CRIT des compétences Bénies de <color\\=#2899ff>12%</color>.",
    "4 Set Effect: When current HP is 50% or more, increase critical rate of Bless skills by <color\\=#2899ff>12%</color>.":
        "Effet 4 pièces : Quand les PV actuels sont à 50% ou plus, augmente le taux CRIT des compétences Bénies de <color\\=#2899ff>12%</color>.",
    "4 Set Effect：When dealing damage with a skill, gain Malice. Malice: Increase Attack by <color\\=#2899ff>5%</color> for 2 turns. Stacks up to 6 times.":
        "Effet 4 pièces : En infligeant des dégâts avec une compétence, gagne [Malice]. Malice : augmente l'ATQ de <color\\=#2899ff>5%</color> pendant 2 tours. Cumulable jusqu'à 6 fois.",
    "4 Set Effect: When dealing damage with a skill, gain Malice. Malice: Increase Attack by <color\\=#2899ff>5%</color> for 2 turns. Stacks up to 6 times.":
        "Effet 4 pièces : En infligeant des dégâts avec une compétence, gagne [Malice]. Malice : augmente l'ATQ de <color\\=#2899ff>5%</color> pendant 2 tours. Cumulable jusqu'à 6 fois.",
    "4 Set Effect：During battle, increase own max HP, Attack, and Defense by <color\\=#2899ff>15%</color>.":
        "Effet 4 pièces : Pendant le combat, augmente ses propres PV max, son ATQ et sa DEF de <color\\=#2899ff>15%</color>.",
    "4 Set Effect: During battle, increase own max HP, Attack, and Defense by <color\\=#2899ff>15%</color>.":
        "Effet 4 pièces : Pendant le combat, augmente ses propres PV max, son ATQ et sa DEF de <color\\=#2899ff>15%</color>.",
    "4 Set Effect：When dealing skill damage, if the attribute is different to the damage of the last used skill, increase the skill's damage dealt by <color\\=#2899ff>25%</color>.":
        "Effet 4 pièces : En infligeant des dégâts de compétence, si l'attribut est différent de celui de la dernière compétence utilisée, augmente les dégâts infligés par la compétence de <color\\=#2899ff>25%</color>.",
    "4 Set Effect: When dealing skill damage, if the attribute is different to the damage of the last used skill, increase the skill's damage dealt by <color\\=#2899ff>25%</color>.":
        "Effet 4 pièces : En infligeant des dégâts de compétence, si l'attribut est différent de celui de la dernière compétence utilisée, augmente les dégâts infligés par la compétence de <color\\=#2899ff>25%</color>.",
    "4 Set Effect：Increase ailment accuracy by <color\\=#2899ff>30%</color> for 2 turns. Reapply effect after dealing a Technical.":
        "Effet 4 pièces : Augmente la Préc. Altération de <color\\=#2899ff>30%</color> pendant 2 tours. Réapplique l'effet après avoir infligé une Technique.",
    "4 Set Effect: Increase ailment accuracy by <color\\=#2899ff>30%</color> for 2 turns. Reapply effect after dealing a Technical.":
        "Effet 4 pièces : Augmente la Préc. Altération de <color\\=#2899ff>30%</color> pendant 2 tours. Réapplique l'effet après avoir infligé une Technique.",
    "4 Set Effect：From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 actions. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> toutes les 6 actions. Cumulable jusqu'à 3 fois.",
    "4 Set Effect: From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 actions. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> toutes les 6 actions. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：Increase Attack by <color\\=#2899ff>25%</color> for 3 turns. After using a Theurgy, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 3 tours. Après avoir utilisé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect: Increase Attack by <color\\=#2899ff>25%</color> for 3 turns. After using a Theurgy, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 3 tours. Après avoir utilisé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect：Increase damage by 16%.":
        "Effet 4 pièces : Augmente les dégâts de 16%.",
    "4 Set Effect: Increase damage by 16%.":
        "Effet 4 pièces : Augmente les dégâts de 16%.",
    "4 Set Effect：Increase damage by <color\\=#2899ff>20%</color> for 3 turns. After activating a Highlight, gain the same effect again.":
        "Effet 4 pièces : Augmente les dégâts de <color\\=#2899ff>20%</color> pendant 3 tours. Après avoir activé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect: Increase damage by <color\\=#2899ff>20%</color> for 3 turns. After activating a Highlight, gain the same effect again.":
        "Effet 4 pièces : Augmente les dégâts de <color\\=#2899ff>20%</color> pendant 3 tours. Après avoir activé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect：Increase Attack by <color\\=#2899ff>25%</color> for 2 turns. After activating a critical, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 2 tours. Après avoir infligé un coup critique, réapplique le même effet.",
    "4 Set Effect: Increase Attack by <color\\=#2899ff>25%</color> for 2 turns. After activating a critical, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 2 tours. Après avoir infligé un coup critique, réapplique le même effet.",
    "2 Set Effect：Decrease Speed by <color\\=#2899ff>3</color>, but increase Attack by <color\\=#2899ff>18%</color>.":
        "Effet 2 pièces : Réduit la Vitesse de <color\\=#2899ff>3</color>, mais augmente l'ATQ de <color\\=#2899ff>18%</color>.",
    "2 Set Effect: Decrease Speed by <color\\=#2899ff>3</color>, but increase Attack by <color\\=#2899ff>18%</color>.":
        "Effet 2 pièces : Réduit la Vitesse de <color\\=#2899ff>3</color>, mais augmente l'ATQ de <color\\=#2899ff>18%</color>.",

    # --- CAPACITÉS SPÉCIFIQUES DES CARTES ---
    # Wisdom
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color\\=#2899ff>20%</color>.":
        "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de <color\\=#2899ff>20%</color>.",
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color=#2899ff>20%</color>.":
        "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de <color=#2899ff>20%</color>.",
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by 20%.":
        "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de 20%.",

    "After using a Highlight, increase Attack by <color\\=#2899ff>30%</color> and damage by <color\\=#2899ff>25%</color>.":
        "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de <color\\=#2899ff>30%</color> et les dégâts de <color\\=#2899ff>25%</color>.",
    "After using a Highlight, increase Attack by <color=#2899ff>30%</color> and damage by <color=#2899ff>25%</color>.":
        "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de <color=#2899ff>30%</color> et les dégâts de <color=#2899ff>25%</color>.",
    "After using a Highlight, increase Attack by 30% and damage by 25%.":
        "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de 30% et les dégâts de 25%.",

    "During battle, increase damage by 50% of user's ailment accuracy (max <color\\=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>.",
    "During battle, increase damage by 50% of user's ailment accuracy (max <color=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de <color=#2899ff>30%</color>.",
    "During battle, increase damage by 50% of user's ailment accuracy (max 30% increase).":
        "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de 30%.",

    "During battle, increase damage by 80% of user's healing effect (max <color\\=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 80% de l'effet de soin de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>.",
    "During battle, increase damage by 80% of user's healing effect (max <color=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 80% de l'effet de soin de l'utilisateur, augmentation max de <color=#2899ff>30%</color>.",
    "During battle, increase damage by 80% of user's healing effect (max 30% increase).":
        "Pendant le combat, augmente les dégâts de 80% de l'effet de soin de l'utilisateur, augmentation max de 30%.",

    # Departure
    "When attacking with a skill, decrease main target's Defense by <color\\=#2899ff>23%</color> for 2 turns.":
        "Réduit la DEF de l'ennemi principal de <color\\=#2899ff>23%</color> pendant 2 tours après l'avoir attaqué avec une compétence.",
    "When attacking with a skill, decrease main target's Defense by <color=#2899ff>23%</color> for 2 turns.":
        "Réduit la DEF de l'ennemi principal de <color=#2899ff>23%</color> pendant 2 tours après l'avoir attaqué avec une compétence.",
    "When attacking with a skill, decrease main target's Defense by 23% for 2 turns.":
        "Réduit la DEF de l'ennemi principal de 23% pendant 2 tours après l'avoir attaqué avec une compétence.",

    "After attacking a foe, increase party's damage by <color\\=#2899ff>8%</color> for 1 turn.":
        "Augmente les Dégâts infligés de l'équipe de <color\\=#2899ff>8%</color> pendant 1 tour lorsqu'un ennemi est attaqué.",
    "After attacking a foe, increase party's damage by <color=#2899ff>8%</color> for 1 turn.":
        "Augmente les Dégâts infligés de l'équipe de <color=#2899ff>8%</color> pendant 1 tour lorsqu'un ennemi est attaqué.",
    "After attacking a foe, increase party's damage by 8% for 1 turn.":
        "Augmente les Dégâts infligés de l'équipe de 8% pendant 1 tour lorsqu'un ennemi est attaqué.",

    "After defeating a foe, increase user's Attack by <color\\=#2899ff>30%</color> for 3 turns.":
        "Augmente l'ATQ de <color\\=#2899ff>30%</color> pendant 3 tours après avoir tué un ennemi.",
    "After defeating a foe, increase user's Attack by <color=#2899ff>30%</color> for 3 turns.":
        "Augmente l'ATQ de <color=#2899ff>30%</color> pendant 3 tours après avoir tué un ennemi.",
    "After defeating a foe, increase user's Attack by 30% for 3 turns.":
        "Augmente l'ATQ de 30% pendant 3 tours après avoir tué un ennemi.",

    # Awareness
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color\\=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de <color\\=#2899ff>9%</color> pour chaque coup infligé sur un ennemi avec un malus pendant 1 tour, jusqu'à 3 cumuls.",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de <color=#2899ff>9%</color> pour chaque coup infligé sur un ennemi avec un malus pendant 1 tour, jusqu'à 3 cumuls.",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by 9% for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de 9% pour chaque coup infligé sur un ennemi avec un malus pendant 1 tour, jusqu'à 3 cumuls.",

    "Increase party's Fire damage by <color\\=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color\\=#2899ff>6%</color> more for 2 turns.":
        "Augmente les Dégâts de Feu des alliés de <color\\=#2899ff>6%</color>. Augmente les Dégâts de Feu des alliés de <color\\=#2899ff>6%</color> supplémentaires pendant 2 tours quand on inflige Brûlure.",
    "Increase party's Fire damage by <color=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color=#2899ff>6%</color> more for 2 turns.":
        "Augmente les Dégâts de Feu des alliés de <color=#2899ff>6%</color>. Augmente les Dégâts de Feu des alliés de <color=#2899ff>6%</color> supplémentaires pendant 2 tours quand on inflige Brûlure.",
    "Increase party's Fire damage by 6%. When a foe is Burning, increase party's Fire damage by 6% more for 2 turns.":
        "Augmente les Dégâts de Feu des alliés de 6%. Augmente les Dégâts de Feu des alliés de 6% supplémentaires pendant 2 tours quand on inflige Brûlure.",

    "Increase damage dealt to foes with elemental ailments by <color\\=#2899ff>12%</color>. Stacks up to 2 times.":
        "Augmente les Dégâts infligés de <color\\=#2899ff>12%</color> lors d'une attaque sur un ennemi sous altération, jusqu'à 2 cumuls.",
    "Increase damage dealt to foes with elemental ailments by <color=#2899ff>12%</color>. Stacks up to 2 times.":
        "Augmente les Dégâts infligés de <color=#2899ff>12%</color> lors d'une attaque sur un ennemi sous altération, jusqu'à 2 cumuls.",
    "Increase damage dealt to foes with elemental ailments by 12%. Stacks up to 2 times.":
        "Augmente les Dégâts infligés de 12% lors d'une attaque sur un ennemi sous altération, jusqu'à 2 cumuls.",

    # Trust & Growth & Harmony & Meditation & Faith
    "At the start of battle, increase other allies' Attack by <color\\=#2899ff>10%</color>. This effect won't activate if stacked.":
        "Au début du combat, augmente l'ATQ des autres alliés de <color\\=#2899ff>10%</color>. Non cumulable.",
    "After using a skill on an ally, increase party's damage by <color\\=#2899ff>8%</color> for 2 turns.":
        "Après avoir utilisé une compétence sur un allié, augmente les dégâts de l'équipe de <color\\=#2899ff>8%</color> pendant 2 tours.",
    "When 3 Electric damage buffs are stacked, increase party's Electric damage by <color\\=#2899ff>12%</color>. This effect won't activate if stacked.":
        "Quand 3 améliorations de dégâts Électriques sont cumulées, augmente les dégâts Électriques de l'équipe de <color\\=#2899ff>12%</color>. Non cumulable.",
    "For each foe on the field, increase Attack by <color\\=#2899ff>8%</color>. Maximum of <color\\=#2899ff>40%</color>.":
        "Pour chaque ennemi sur le terrain, augmente l'ATQ de <color\\=#2899ff>8%</color>, jusqu'à un maximum de <color\\=#2899ff>40%</color>.",
    "Increase Physical and Electric damage by <color\\=#2899ff>12%</color>. If there is only 1 foe on the field, increase by <color\\=#2899ff>24%</color> more.":
        "Augmente les dégâts Physiques et Électriques de <color\\=#2899ff>12%</color>. S'il n'y a qu'un seul ennemi sur le terrain, augmente de <color\\=#2899ff>24%</color> supplémentaires.",
    "When activating a Revelation set effect's bonus damage, increase target's damage taken by <color\\=#2899ff>12%</color> for 2 turns.":
        "Lors de l'activation des dégâts bonus d'un effet d'Arcane, augmente les dégâts subis par la cible de <color\\=#2899ff>12%</color> pendant 2 tours.",
    "After taking damage, increase Defense by <color\\=#2899ff>40%</color> for 2 turns.":
        "Après avoir subi des dégâts, augmente la DEF de <color\\=#2899ff>40%</color> pendant 2 tours.",
    "Each time a shield is granted, increase target's Defense by <color\\=#2899ff>7%</color> for 2 turns. Stacks up to 3 times.":
        "Chaque fois qu'un bouclier est octroyé, augmente la DEF de la cible de <color\\=#2899ff>7%</color> pendant 2 tours. Cumulable jusqu'à 3 fois.",
    "After using a healing skill, increase user's Attack by <color\\=#2899ff>25%</color>.":
        "Après avoir utilisé une compétence de soin, augmente l'ATQ du lanceur de <color\\=#2899ff>25%</color>.",
    "When activating Resonance, increase critical damage by <color\\=#2899ff>50%</color>.":
        "Lors de l'activation d'une Attaque de Suivi, augmente les dégâts critiques de <color\\=#2899ff>50%</color>.",
    "Increase critical damage of Resonance by <color\\=#2899ff>50%</color>.":
        "Augmente les dégâts critiques de l'Attaque de Suivi de <color\\=#2899ff>50%</color>.",
    "When activating Resonance, increase own Ice damage by <color\\=#2899ff>10%</color> for 2 turns. Stacks up to 3 times.":
        "Lors de l'activation d'une Attaque de Suivi, augmente ses propres dégâts de Glace de <color\\=#2899ff>10%</color> pendant 2 tours. Cumulable jusqu'à 3 fois.",
    "Increase maximum number of Attack buff stacks to <color\\=#2899ff>5</color>.":
        "Augmente le nombre maximum de cumuls du bonus d'ATQ à <color\\=#2899ff>5</color>.",
    "For each elemental ailment inflicted, increase party's Nuclear damage by <color\\=#2899ff>5%</color> for 2 turns.":
        "Pour chaque altération élémentaire infligée, augmente les dégâts Nucléaires de l'équipe de <color\\=#2899ff>5%</color> pendant 2 tours.",
    "After dealing a critical hit, increase user's healing effect by <color\\=#2899ff>28%</color> for 2 turns.":
        "Après avoir infligé un coup critique, augmente l'effet de soin du lanceur de <color\\=#2899ff>28%</color> pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color\\=#2899ff>10%</color> for 2 turns.":
        "Si équipé par un Voleur Fantôme Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color\\=#2899ff>10%/20%/30%</color>.":
        "Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de <color\\=#2899ff>10%, 20% ou 30%</color>.",
    "During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to <color\\=#FFFC40>1280</color>.":
        "Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à <color\\=#FFFC40>1280</color>.",
    "When current HP is over 50%, increase critical rate of Bless skills by 12%.":
        "Quand les PV actuels sont supérieurs à 50%, augmente le taux CRIT des compétences Bénies de 12%.",
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color\\=#2899ff>2%</color> more.":
        "Si équipé par un Voleur Fantôme Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "When activating a Resonance, increase critical damage by <color\\=#2899ff>50%</color>.":
        "Lors de l'activation d'une Attaque de Suivi, augmente les dégâts critiques de <color\\=#2899ff>50%</color>.",
    "All allies deal <color\\=#2899ff>8%</color> bonus damage to enemies with debuffs. This effect won't activate if stacked.":
        "Tous les alliés infligent <color\\=#2899ff>8%</color> de dégâts bonus aux ennemis ayant un malus. Non cumulable.",
    "Increase Resonance critical damage by <color\\=#2899ff>50%</color>.":
        "Augmente les dégâts critiques de l'Attaque de Suivi de <color\\=#2899ff>50%</color>.",
    "When activating a Resonance, increase own Ice damage by <color\\=#2899ff>10%</color> for 2 turns. Stacks up to 3 times.":
        "Lors de l'activation d'une Attaque de Suivi, augmente ses propres dégâts de Glace de <color\\=#2899ff>10%</color> pendant 2 tours. Cumulable jusqu'à 3 fois.",
    "After using a skill, gain 1 Glory stack. When a Resonance is activated, spend all Glory stacks and increase pierce rate by <color\\=#2899ff>8%</color> for each stack. Stacks up to 2 times.":
        "Après avoir utilisé une compétence, gagne 1 cumul de Gloire. Lors de l'activation d'une Attaque de Suivi, dépense tous les cumuls de Gloire et augmente le taux de perforation de <color\\=#2899ff>8%</color> par cumul. Cumulable jusqu'à 2 fois.",
    "During battle, when SP reaches 100%/150%/200%, increase critical damage by <color\\=#2899ff>15%/30%/45%</color>.":
        "Pendant le combat, lorsque les PC atteignent 100%, 150% ou 200%, augmente les dégâts critiques de <color\\=#2899ff>15%, 30% ou 45%</color>.",
    "When dealing Almighty damage, increase Attack by <color\\=#2899ff>35%</color> and critical rate by <color\\=#2899ff>12%</color>.":
        "En infligeant des dégâts d'Affinité Absolue, augmente l'ATQ de <color\\=#2899ff>35%</color> et le taux CRIT de <color\\=#2899ff>12%</color>.",
    "Increase damage dealt by allies to foes inflicted with <link\\=\"s|232\"><u>technical ailments</u></link> by <color\\=#2899ff>10%</color>. This effect won't activate if stacked.":
        "Augmente les dégâts infligés par les alliés aux ennemis sous <link\\=\"s|232\"><u>altération Technique</u></link> de <color\\=#2899ff>10%</color>. Non cumulable.",
    "At the start of battle, increase damage of the ally with the lowest Speed by <color\\=#2899ff>12%</color>. This effect won't activate if stacked.":
        "Au début du combat, augmente les dégâts de l'allié ayant la plus basse Vitesse de <color\\=#2899ff>12%</color>. Non cumulable.",
    "Increase damage of allies with the same main attribute by <color\\=#2899ff>10%</color>. This effect won't activate if stacked.":
        "Augmente les dégâts des alliés ayant le même attribut principal de <color\\=#2899ff>10%</color>. Non cumulable.",
    "Increase all allies' damage to enemies with <link\\=\"s|232\"><u>technical ailments</u></link> by <color\\=#2899ff>10%</color>. This effect won't activate if stacked.":
        "Augmente les dégâts de tous les alliés aux ennemis sous <link\\=\"s|232\"><u>altération Technique</u></link> de <color\\=#2899ff>10%</color>. Non cumulable.",
    "For every <color\\=#2899ff>800</color> HP, increase user's healing effect by <color\\=#2899ff>1%</color>. Maximum of <color\\=#2899ff>20%</color>.":
        "Par tranche de <color\\=#2899ff>800</color> PV, augmente l'effet de soin du lanceur de <color\\=#2899ff>1%</color>, jusqu'à un maximum de <color\\=#2899ff>20%</color>.",
    "Increase all allies' damage to enemies with debuffs by <color\\=#2899ff>8%</color>. This effect won't activate if stacked.":
        "Augmente les dégâts de tous les alliés aux ennemis ayant un malus de <color\\=#2899ff>8%</color>. Non cumulable.",
    "<nobr>After defeating a foe, inflict (<color\\=#50b50d>3</color>/4) <link\\=\"s|167\"><u>Agony</u></link> stacks on all other foes.</nobr>":
        "<nobr>Après avoir vaincu un ennemi, inflige <color\\=#50b50d>3</color> à 4 cumuls d'<link\\=\"s|167\"><u>Agonie</u></link> à tous les autres ennemis.</nobr>",
    "<nobr>After defeating a foe, inflict (3/<color\\=#c900e4>4</color>) <link\\=\"s|167\"><u>Agony</u></link> stacks on all other foes.</nobr>":
        "<nobr>Après avoir vaincu un ennemi, inflige 3 à <color\\=#c900e4>4</color> cumuls d'<link\\=\"s|167\"><u>Agonie</u></link> à tous les autres ennemis.</nobr>",
    "<nobr>After defeating a foe, inflict 4 <link\\=\"s|167\"><u>Agony</u></link> stacks on all other foes.</nobr>":
        "<nobr>Après avoir vaincu un ennemi, inflige 4 cumuls d'<link\\=\"s|167\"><u>Agonie</u></link> à tous les autres ennemis.</nobr>",
    "<nobr>After defeating a foe, inflict <color\\=#50b50d>3</color>→<color\\=#c900e4>4</color> <link\\=\"s|167\"><u>Agony</u></link> stacks on all other foes.</nobr>":
        "<nobr>Après avoir vaincu un ennemi, inflige <color\\=#50b50d>3</color> à <color\\=#c900e4>4</color> cumuls d'<link\\=\"s|167\"><u>Agonie</u></link> à tous les autres ennemis.</nobr>",
    "After using a Theurgy, increase party's damage by 10% for 3 turns.":
        "Après avoir utilisé un HIGHLIGHT, augmente les dégâts de l'équipe de 10% pendant 3 tours.",
    "When equipped by an Elucidator Phantom Thief: When granting buffs to allies with a skill, increase the main target's pierce rate by <color\\=#2899ff>5%</color> for 1 turn.":
        "Si équipé par un Voleur Fantôme Élucidateur : lors de l'octroi d'améliorations aux alliés avec une compétence, augmente le taux de perforation de la cible principale de <color\\=#2899ff>5%</color> pendant 1 tour.",
    "Allies' <color\\=#FFFC40>Theurgy</color> damage is increased by 30%. After using a Theurgy, user's final damage is increased by 30% more for 3 turns.":
        "Les dégâts de <color\\=#FFFC40>HIGHLIGHT</color> des alliés sont augmentés de 30%. Après avoir utilisé un HIGHLIGHT, les dégâts finaux du lanceur augmentent de 30% supplémentaires pendant 3 tours.",
    "For each foe on the field, increase Electric damage by <color\\=#2899ff>8%</color>. Maximum of <color\\=#2899ff>32%</color>.":
        "Pour chaque ennemi sur le terrain, augmente les dégâts Électriques de <color\\=#2899ff>8%</color>, jusqu'à un maximum de <color\\=#2899ff>32%</color>.",
    "Increase continuous damage effect by <color\\=#2899ff>16%</color>.":
        "Augmente les effets de dégâts continus de <color\\=#2899ff>16%</color>.",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color\\=#2899ff>24%/30%</color>.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>.",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color=#2899ff>24%/30%</color>.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>.",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by 24%/30%.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de 24%/30%.",
    "Increase Attack based on lost HP. Increase Attack by a maximum of <color\\=#2899ff>40%</color> when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%.",
    "Increase Attack based on lost HP. Increase Attack by a maximum of <color=#2899ff>40%</color> when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%.",
    "Increase Attack based on lost HP. Increase Attack by a maximum of 40% when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de 40% quand les PV descendent à 40%.",
    "Increase Attack based on missing HP. Increase Attack by a maximum of <color\\=#2899ff>40%</color> when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%.",
    "Increase Attack based on missing HP. Increase Attack by a maximum of <color=#2899ff>40%</color> when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%.",
    "Increase Attack based on missing HP. Increase Attack by a maximum of 40% when HP is down to 40%.":
        "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de 40% quand les PV descendent à 40%.",
    "Increase continuous damage by <color\\=#2899ff>16%</color>.":
        "Augmente les dégâts continus de <color\\=#2899ff>16%</color>.",
    "Increase continuous damage by <color=#2899ff>16%</color>.":
        "Augmente les dégâts continus de <color\\=#2899ff>16%</color>.",
    "Increase continuous damage by 16%.":
        "Augmente les dégâts continus de 16%.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by <color\\=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to <color=#2899ff>2</color> times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à <color\\=#2899ff>2</color> fois.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by 10%. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de 10%. Cet effet est permanent et cumulable jusqu'à 2 fois.",
    "Increase All-Out Attack damage by <color\\=#2899ff>16%</color>.":
        "Augmente les dégâts de l'Assaut Général de <color\\=#2899ff>16%</color>.",
    "Increase All-Out Attack damage by <color=#2899ff>16%</color>.":
        "Augmente les dégâts de l'Assaut Général de <color\\=#2899ff>16%</color>.",
    "Increase All-Out Attack damage by 16%.":
        "Augmente les dégâts de l'Assaut Général de 16%.",
    "After activating a Theurgy, increase party's damage by <color\\=#2899ff>10%</color> for 3 turns.":
        "Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de <color\\=#2899ff>10%</color> pendant 3 tours.",
    "After activating a Theurgy, increase party's damage by <color=#2899ff>10%</color> for 3 turns.":
        "Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de <color\\=#2899ff>10%</color> pendant 3 tours.",
    "After activating a Theurgy, increase party's damage by 10% for 3 turns.":
        "Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de 10% pendant 3 tours.",
    "Perseverance & Gain":
        "Perseverance & Gain",
    "Acuity & Satiety":
        "Acuity & Satiety",
    "Nativity & Strife":
        "Nativity & Strife",
    "Resolve & Prudence":
        "<size=85%>Resolve & Prudence</size>",
}

LARGEUR_LETTRES = {}
for _lettres, _l in (("iljI|.,:;'!", 0.30), ("ftr()[] ", 0.38), ("sczJ", 0.52),
                     ("abdeghknopquvxyLFSTZPE&", 0.60), ("BCRKXYV", 0.68), ("ADGHNOQU", 0.75), ("mwMW", 0.90)):
    for _c in _lettres:
        LARGEUR_LETTRES[_c] = _l
TITRE_LARGEUR_MAX = 8.3


def largeur_titre(titre):
    titre = re.sub(r"\{\{.\}\}|\$\d+", "Caroline", titre)
    return sum(LARGEUR_LETTRES.get(c, 0.6) for c in titre)


def taille_titre(titre):
    titre = titre.strip()
    largeur = largeur_titre(titre)
    if largeur <= TITRE_LARGEUR_MAX:
        return titre
    pct = max(55, int(TITRE_LARGEUR_MAX * 100 / largeur))
    return f"<size={pct}%>{titre}</size>"


def normalize_key(s):
    return s.replace('：', ':').replace(r'\=', '=').replace(r'\\=', '=').strip()


def is_combo_key(k):
    if ' & ' not in k:
        return False
    parts = k.split(' & ')
    if len(parts) == 2 and parts[0].strip() in REVELATION_CARD_NAMES:
        return True
    return False


def synchroniser(easy_dir=EASY_DIR):
    cards_path = os.path.join(easy_dir, "08_Equipements_et_Objets", "02_Cartes_Revelation_et_Sets.json")
    if not os.path.exists(cards_path):
        raise FileNotFoundError(f"Fichier Cartes introuvable : {cards_path}")

    with open(cards_path, "r", encoding="utf-8") as f:
        cards_data = json.load(f)

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

            # Équivalences d'échappement = vs \=
            k_esc = k.replace("=", r"\=")
            k_unesc = k.replace(r"\=", "=")
            if k_esc in CARD_ABILITY_OVERRIDES:
                target_val = CARD_ABILITY_OVERRIDES[k_esc]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue
            if k_unesc in CARD_ABILITY_OVERRIDES:
                target_val = CARD_ABILITY_OVERRIDES[k_unesc]
                if data[k] != target_val:
                    data[k] = target_val
                    file_mods += 1
                continue

            # 2. Titres de combinaisons de cartes (ex: Departure & Control)
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
