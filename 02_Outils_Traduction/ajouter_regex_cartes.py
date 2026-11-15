# -*- coding: utf-8 -*-
"""
Ajoute des règles regex ultra-robustes dans TRADUCTION_FR/01_Kits_Personnages/00_Regex_Dynamiques.txt
pour tous les effets de sets 4 pièces et combinaisons d'arcanes de Révélation.
"""
import os

path = os.path.join('TRADUCTION_FR', '01_Kits_Personnages', '00_Regex_Dynamiques.txt')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_rules = """
// --- EFFETS DE SET 4 PIÈCES (RÈGLES UNIVERSELLES) ---
r:"(?s)4 Set Effect[：:].*?At the start of battle,\\s*fill\\s*(?:the\\s*)?Highlight gauge by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.\\s*This effect won't activate if stacked\\.?"="Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de $1%. Non cumulable."
r:"(?s)4 Set Effect[：:].*?When dealing damage with a skill,\\s*gain Malice\\.\\s*Malice[：:]\\s*Increase Attack by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? for (\\d+) turns\\.\\s*Stacks up to (\\d+) times\\.?"="Effet 4 pièces : En infligeant des dégâts avec une compétence, gagne [Malice]. Malice : augmente l'ATQ de $1% pendant $2 tours. Cumulable jusqu'à $3 fois."
r:"(?s)4 Set Effect[：:].*?Increase ailment accuracy by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? for (\\d+) turns\\.\\s*Reapply effect after dealing a Technical\\.?"="Effet 4 pièces : Augmente la Préc. Altération de $1% pendant $2 tours. Réapplique l'effet après avoir infligé une Technique."
r:"(?s)4 Set Effect[：:].*?When equipped by an Elucidator Phantom Thief[：:]\\s*During battle,\\s*increase party's max HP,\\s*Attack,\\s*and Defense by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Effet 4 pièces : Si équipé par un Voleur Fantôme Élucidateur : pendant le combat, augmente les PV max, l'ATQ et la DEF de l'équipe de $1%."
r:"(?s)4 Set Effect[：:].*?When dealing skill damage,\\s*if the attribute is different to the damage of the last used skill,\\s*increase the skill's damage dealt by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Effet 4 pièces : En infligeant des dégâts de compétence, si l'attribut est différent de celui de la dernière compétence utilisée, augmente les dégâts infligés par la compétence de $1%."

// --- COMBINAISONS D'ARCANES (WISDOM, RESOLVE, PERSEVERANCE, NATIVITY, ACUITY) ---
r:"(?s)When Malice reaches (\\d+) or more stacks,\\s*increase Physical damage and ailment accuracy by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Quand [Malice] atteint $1 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de $2%."
r:"(?s)During battle,\\s*increase damage by (\\d+)% of user's ailment accuracy \\(max\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? increase\\)\\.?"="Pendant le combat, augmente les dégâts de $1% de la Préc. Altération de l'utilisateur, augmentation max de $2%."
r:"(?s)After using a (?:Highlight|HIGHLIGHT),\\s*increase Attack by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? and damage by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de $1% et les dégâts de $2%."
r:"(?s)At the start of battle,\\s*if the? user is the? 3rd/4th ally in the turn order,\\s*increase Attack by\\s*(?:<color[^>]*>)?([\\d%/]+)(?:</color>)?\\.?"="Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de $1."
r:"(?s)Increase Attack based on (?:lost|missing) HP\\.\\s*Increase Attack by a maximum of\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? when HP is down to\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de $1% quand les PV descendent à $2%."
r:"(?s)Increase continuous damage(?: effect)? by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Augmente les dégâts continus de $1%."
r:"(?s)At the start of battle or at the start of an extra action,\\s*increase party's critical damage by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.\\s*This effect is permanent and stacks up to\\s*(?:<color[^>]*>)?(\\d+)(?:</color>)? times\\.?"="Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de $1%. Cet effet est permanent et cumulable jusqu'à $2 fois."
r:"(?s)Increase All-Out Attack damage by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Augmente les dégâts de l'Assaut Général de $1%."
r:"(?s)After activating a Theurgy,\\s*increase party's damage by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? for (\\d+) turns\\.?"="Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de $1% pendant $2 tours."
"""

if 'When Malice reaches' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + new_rules)
    print('Regexes successfully added to 00_Regex_Dynamiques.txt!')
else:
    print('Regexes already present.')
