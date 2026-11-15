#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_revelation_steam_fix.py
Applique l'ensemble des traductions des capacités de cartes de Révélation et des effets de sets
sur les fichiers sources TRADUCTION_FACILE et synchronise le compilateur pour Steam PC.
"""

import os
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EASY_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")
CARDS_FILE = os.path.join(EASY_DIR, "08_Equipements_et_Objets", "02_Cartes_Revelation_et_Sets.json")
SYNC_SCRIPT = os.path.join(BASE_DIR, "02_Outils_Traduction", "synchroniser_steam_cartes.py")

# Dictionnaire de référence complet des capacités de cartes et effets d'arcanes
RAW_OVERRIDES = {
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
    "4 Set Effect：At the start of battle, fill the Highlight gauge by <color\\=#2899ff>25%</color>. This effect won't activate if stacked.":
        "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable.",
    "4 Set Effect：From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 turns. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> tous les 6 tours. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：Increase Curse damage to foes with debuffs by <color\\=#2899ff>20%</color>.":
        "Effet 4 pièces : Augmente les dégâts Maudits infligés aux ennemis avec un malus de <color\\=#2899ff>20%</color>.",
    "4 Set Effect：After allies use Electric skills, increase own Electric damage by <color\\=#2899ff>9%</color>. Stacks up to 3 times.":
        "Effet 4 pièces : Après que les alliés ont utilisé des compétences Électriques, augmente ses propres dégâts Électriques de <color\\=#2899ff>9%</color>. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：When attacking, 25% chance to deal <color\\=#2899ff>20%</color> of the user's Attack as bonus damage.":
        "Effet 4 pièces : Lors d'une attaque, 25% de chances d'infliger <color\\=#2899ff>20%</color> de l'ATQ du lanceur en dégâts bonus.",
    "4 Set Effect：Increase healing to allies with less than 50% HP by <color\\=#2899ff>23%</color>.":
        "Effet 4 pièces : Augmente les soins prodigués aux alliés ayant moins de 50% de PV de <color\\=#2899ff>23%</color>.",
    "4 Set Effect：When attacking with a skill, deal <color\\=#2899ff>8%</color> of own HP as bonus damage to the target.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige à la cible des dégâts bonus équivalents à <color\\=#2899ff>8%</color> de ses propres PV.",
    "4 Set Effect：When attacking with a skill, deal <color\\=#2899ff>30%</color> of user's Attack as damage if the target has an elemental ailment.":
        "Effet 4 pièces : Lors d'une attaque avec une compétence, inflige <color\\=#2899ff>30%</color> de l'ATQ du lanceur en dégâts si la cible subit une altération élémentaire.",
    "4 Set Effect：When equipped by an Elucidator Phantom Thief: During battle, increase party's max HP, Attack, and Defense by <color\\=#2899ff>8%</color>.":
        "Effet 4 pièces : Si équipé par un Voleur Fantôme Élucidateur : pendant le combat, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>8%</color>.",
    "4 Set Effect：When dealing Psychokinesis damage, increase Attack by 15%. If more than 3 foes are on the field, increase Attack by <color\\=#2899ff>15%</color> more.":
        "Effet 4 pièces : En infligeant des dégâts Psy, augmente l'ATQ de 15%. S'il y a plus de 3 ennemis sur le terrain, augmente l'ATQ de <color\\=#2899ff>15%</color> supplémentaires.",
    "4 Set Effect：When current HP is 50% or more, increase critical rate of Bless skills by <color\\=#2899ff>12%</color>.":
        "Effet 4 pièces : Quand les PV actuels sont à 50% ou plus, augmente le taux CRIT des compétences Bénies de <color\\=#2899ff>12%</color>.",
    "4 Set Effect：When dealing damage with a skill, gain Malice. Malice: Increase Attack by <color\\=#2899ff>5%</color> for 2 turns. Stacks up to 6 times.":
        "Effet 4 pièces : En infligeant des dégâts avec une compétence, gagne [Malice]. Malice : augmente l'ATQ de <color\\=#2899ff>5%</color> pendant 2 tours. Cumulable jusqu'à 6 fois.",
    "4 Set Effect：During battle, increase own max HP, Attack, and Defense by <color\\=#2899ff>15%</color>.":
        "Effet 4 pièces : Pendant le combat, augmente ses propres PV max, son ATQ et sa DEF de <color\\=#2899ff>15%</color>.",
    "4 Set Effect：When dealing skill damage, if the attribute is different to the damage of the last used skill, increase the skill's damage dealt by <color\\=#2899ff>25%</color>.":
        "Effet 4 pièces : En infligeant des dégâts de compétence, si l'attribut est différent de celui de la dernière compétence utilisée, augmente les dégâts infligés par la compétence de <color\\=#2899ff>25%</color>.",
    "4 Set Effect：Increase ailment accuracy by <color\\=#2899ff>30%</color> for 2 turns. Reapply effect after dealing a Technical.":
        "Effet 4 pièces : Augmente la Préc. Altération de <color\\=#2899ff>30%</color> pendant 2 tours. Réapplique l'effet après avoir infligé une Technique.",
    "4 Set Effect：From the start of battle, increase Attack by <color\\=#2899ff>10%</color> every 6 actions. Stacks up to 3 times.":
        "Effet 4 pièces : Depuis le début du combat, augmente l'ATQ de <color\\=#2899ff>10%</color> toutes les 6 actions. Cumulable jusqu'à 3 fois.",
    "4 Set Effect：Increase Attack by <color\\=#2899ff>25%</color> for 3 turns. After using a Theurgy, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 3 tours. Après avoir utilisé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect：Increase damage by 16%.":
        "Effet 4 pièces : Augmente les dégâts de 16%.",
    "4 Set Effect：Increase damage by <color\\=#2899ff>20%</color> for 3 turns. After activating a Highlight, gain the same effect again.":
        "Effet 4 pièces : Augmente les dégâts de <color\\=#2899ff>20%</color> pendant 3 tours. Après avoir activé un HIGHLIGHT, réapplique le même effet.",
    "4 Set Effect：Increase Attack by <color\\=#2899ff>25%</color> for 2 turns. After activating a critical, gain the same effect again.":
        "Effet 4 pièces : Augmente l'ATQ de <color\\=#2899ff>25%</color> pendant 2 tours. Après avoir infligé un coup critique, réapplique le même effet.",
    "2 Set Effect：Decrease Speed by <color\\=#2899ff>3</color>, but increase Attack by <color\\=#2899ff>18%</color>.":
        "Effet 2 pièces : Réduit la Vitesse de <color\\=#2899ff>3</color>, mais augmente l'ATQ de <color\\=#2899ff>18%</color>.",

    # --- CAPACITÉS SPÉCIFIQUES DES CARTES (COMBOS & INDIVIDUELLES) ---
    # Wisdom
    "When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color\\=#2899ff>20%</color>.":
        "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de <color\\=#2899ff>20%</color>.",
    "After using a Highlight, increase Attack by <color\\=#2899ff>30%</color> and damage by <color\\=#2899ff>25%</color>.":
        "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de <color\\=#2899ff>30%</color> et les dégâts de <color\\=#2899ff>25%</color>.",
    "During battle, increase damage by 50% of user's ailment accuracy (max <color\\=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>.",
    "During battle, increase damage by 80% of user's healing effect (max <color\\=#2899ff>30%</color> increase).":
        "Pendant le combat, augmente les dégâts de 80% de l'effet de soin de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>.",

    # Departure & Awareness
    "When attacking with a skill, decrease main target's Defense by <color\\=#2899ff>23%</color> for 2 turns.":
        "Réduit la DEF de l'ennemi principal de <color\\=#2899ff>23%</color> pendant 2 tours après l'avoir attaqué avec une compétence.",
    "After attacking a foe, increase party's damage by <color\\=#2899ff>8%</color> for 1 turn.":
        "Augmente les Dégâts infligés de l'équipe de <color\\=#2899ff>8%</color> pendant 1 tour lorsqu'un ennemi est attaqué.",
    "After defeating a foe, increase user's Attack by <color\\=#2899ff>30%</color> for 3 turns.":
        "Augmente l'ATQ de <color\\=#2899ff>30%</color> pendant 3 tours après avoir tué un ennemi.",
    "Whenever dealing damage to a foe with a debuff, increase user's Attack by <color\\=#2899ff>9%</color> for 1 turn. Stacks up to 3 times.":
        "Augmente l'ATQ de <color\\=#2899ff>9%</color> pour chaque coup infligé sur un ennemi avec un malus pendant 1 tour, jusqu'à 3 cumuls.",
    "Increase party's Fire damage by <color\\=#2899ff>6%</color>. When a foe is Burning, increase party's Fire damage by <color\\=#2899ff>6%</color> more for 2 turns.":
        "Augmente les Dégâts de Feu des alliés de <color\\=#2899ff>6%</color>. Augmente les Dégâts de Feu des alliés de <color\\=#2899ff>6%</color> supplémentaires pendant 2 tours quand on inflige Brûlure.",
    "Increase damage dealt to foes with elemental ailments by <color\\=#2899ff>12%</color>. Stacks up to 2 times.":
        "Augmente les Dégâts infligés de <color\\=#2899ff>12%</color> lors d'une attaque sur un ennemi sous altération, jusqu'à 2 cumuls.",

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
        "Augmente les effets de dégâts continus de <color\\=#2899ff>16%</color>."
}

def generate_variants(k, v):
    """Génère automatiquement les déclinaisons (avec :, avec ：, sans balise couleur, avec color=# vs color\=#)."""
    variants = {}
    
    def strip_tags(s):
        return re.sub(r'<[^>]+>', '', s)

    # 1. Base
    variants[k] = v
    
    # 2. Remplacement de = par \= ou inversement
    k_unesc = k.replace(r'\=', '=')
    v_unesc = v.replace(r'\=', '=')
    variants[k_unesc] = v
    
    # 3. Remplacement deux-points standard : <-> deux-points pleine chasse ：
    if '：' in k:
        k_colon = k.replace('：', ': ')
        v_colon = v.replace('：', ': ')
        variants[k_colon] = v_colon
        variants[k_colon.replace('  ', ' ')] = v_colon.replace('  ', ' ')
        variants[k.replace('：', ':')] = v
        variants[k_unesc.replace('：', ': ')] = v
        variants[k_unesc.replace('：', ':')] = v
    if ': ' in k:
        k_full = k.replace(': ', '：')
        variants[k_full] = v
        variants[k_unesc.replace(': ', '：')] = v

    # 4. Version sans balises de couleur (si le jeu envoie du texte brut sans balises)
    k_plain = strip_tags(k)
    v_plain = strip_tags(v)
    if k_plain != k:
        variants[k_plain] = v_plain
        if '：' in k_plain:
            variants[k_plain.replace('：', ': ')] = v_plain.replace('：', ': ')
            variants[k_plain.replace('：', ':')] = v_plain
        if ': ' in k_plain:
            variants[k_plain.replace(': ', '：')] = v_plain

    # 5. Variantes spécifiques de Highlight gauge (avec ou sans "the")
    if 'the Highlight gauge' in k:
        k_nothe = k.replace('the Highlight gauge', 'Highlight gauge')
        variants[k_nothe] = v
        variants[k_nothe.replace(r'\=', '=')] = v
        if '：' in k_nothe:
            variants[k_nothe.replace('：', ': ')] = v
            variants[k_nothe.replace('：', ':')] = v
    elif 'Highlight gauge' in k and 'the Highlight gauge' not in k:
        k_the = k.replace('Highlight gauge', 'the Highlight gauge')
        variants[k_the] = v
        variants[k_the.replace(r'\=', '=')] = v
        if '：' in k_the:
            variants[k_the.replace('：', ': ')] = v
            variants[k_the.replace('：', ':')] = v

    return variants

print("Génération du dictionnaire étendu de capacités de cartes...")
FULL_OVERRIDES = {}
for k, v in RAW_OVERRIDES.items():
    vars_dict = generate_variants(k, v)
    FULL_OVERRIDES.update(vars_dict)

print(f"Total variantes générées : {len(FULL_OVERRIDES)}")

# 1. Mise à jour de TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json
print("\nMise à jour de 02_Cartes_Revelation_et_Sets.json...")
with open(CARDS_FILE, "r", encoding="utf-8") as f:
    cards_data = json.load(f)

cards_added = 0
cards_updated = 0
for k, v in FULL_OVERRIDES.items():
    if k not in cards_data:
        cards_data[k] = v
        cards_added += 1
    elif not cards_data[k].strip() or cards_data[k] != v:
        cards_data[k] = v
        cards_updated += 1

with open(CARDS_FILE, "w", encoding="utf-8") as f:
    json.dump(cards_data, f, ensure_ascii=False, indent=2)

print(f"02_Cartes_Revelation_et_Sets.json mis à jour : {cards_added} ajoutée(s), {cards_updated} modifiée(s).")

# 2. Mise à jour des fichiers Steam (Part01 à Part06)
print("\nMise à jour des fichiers 11_Textes_Generaux_Steam/...")
import glob
steam_files = sorted(glob.glob(os.path.join(EASY_DIR, "11_Textes_Generaux_Steam", "*.json")))
total_steam_updated = 0

for sf in steam_files:
    with open(sf, "r", encoding="utf-8") as f:
        sdata = json.load(f)
    smods = 0
    for k in list(sdata.keys()):
        # Si la clé est dans FULL_OVERRIDES
        if k in FULL_OVERRIDES:
            tval = FULL_OVERRIDES[k]
            if sdata[k] != tval:
                sdata[k] = tval
                smods += 1
        else:
            # Vérifier équivalence = vs \=
            k_esc = k.replace("=", r"\=")
            k_unesc = k.replace(r"\=", "=")
            if k_esc in FULL_OVERRIDES:
                tval = FULL_OVERRIDES[k_esc]
                if sdata[k] != tval:
                    sdata[k] = tval
                    smods += 1
            elif k_unesc in FULL_OVERRIDES:
                tval = FULL_OVERRIDES[k_unesc]
                if sdata[k] != tval:
                    sdata[k] = tval
                    smods += 1

    if smods > 0:
        with open(sf, "w", encoding="utf-8") as f:
            json.dump(sdata, f, ensure_ascii=False, indent=2)
        print(f"  • {os.path.basename(sf)} : {smods} entrée(s) mise(s) à jour.")
        total_steam_updated += smods

print(f"Total textes Steam mis à jour : {total_steam_updated}")
