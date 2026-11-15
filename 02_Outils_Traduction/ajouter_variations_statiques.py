# -*- coding: utf-8 -*-
"""
Ajoute des variantes statiques avec et sans '✦ ' et avec balises de couleur
pour garantir une couverture à 100% dans 02_Cartes_Revelation_et_Sets.json.
"""
import json, os

path = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

pairs_to_add = [
    # Worry 4 Set Effect
    ("✦ 4 Set Effect: At the start of battle, fill Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.", "✦ Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable."),
    ("✦ 4 Set Effect: At the start of battle, fill Highlight gauge by 25%. This effect won't activate if stacked.", "✦ Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable."),
    ("4 Set Effect: At the start of battle, fill Highlight gauge by <color=#2899ff>25%</color>. This effect won't activate if stacked.", "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de <color\\=#2899ff>25%</color>. Non cumulable."),
    ("4 Set Effect: At the start of battle, fill Highlight gauge by 25%. This effect won't activate if stacked.", "Effet 4 pièces : Au début du combat, remplit la jauge de HIGHLIGHT de 25%. Non cumulable."),

    # Wisdom & Oppression
    ("✦ When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color=#2899ff>20%</color>.", "✦ Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de <color\\=#2899ff>20%</color>."),
    ("✦ When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by 20%.", "✦ Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de 20%."),
    ("When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by <color=#2899ff>20%</color>.", "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de <color\\=#2899ff>20%</color>."),
    ("When Malice reaches 5 or more stacks, increase Physical damage and ailment accuracy by 20%.", "Quand [Malice] atteint 5 cumuls ou plus, augmente les dégâts Physiques et la Préc. Altération de 20%."),

    # Wisdom & Pleasure
    ("✦ During battle, increase damage by 50% of user's ailment accuracy (max <color=#2899ff>30%</color> increase).", "✦ Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>."),
    ("✦ During battle, increase damage by 50% of user's ailment accuracy (max 30% increase).", "✦ Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de 30%."),
    ("During battle, increase damage by 50% of user's ailment accuracy (max <color=#2899ff>30%</color> increase).", "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de <color\\=#2899ff>30%</color>."),
    ("During battle, increase damage by 50% of user's ailment accuracy (max 30% increase).", "Pendant le combat, augmente les dégâts de 50% de la Préc. Altération de l'utilisateur, augmentation max de 30%."),

    # Wisdom & Virtue
    ("✦ After using a Highlight, increase Attack by <color=#2899ff>30%</color> and damage by <color=#2899ff>25%</color>.", "✦ Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de <color\\=#2899ff>30%</color> et les dégâts de <color\\=#2899ff>25%</color>."),
    ("✦ After using a Highlight, increase Attack by 30% and damage by 25%.", "✦ Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de 30% et les dégâts de 25%."),
    ("After using a Highlight, increase Attack by <color=#2899ff>30%</color> and damage by <color=#2899ff>25%</color>.", "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de <color\\=#2899ff>30%</color> et les dégâts de <color\\=#2899ff>25%</color>."),
    ("After using a Highlight, increase Attack by 30% and damage by 25%.", "Après avoir utilisé un HIGHLIGHT, augmente l'ATQ de 30% et les dégâts de 25%."),

    # Resolve & Prudence
    ("✦ At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color=#2899ff>24%/30%</color>.", "✦ Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>."),
    ("✦ At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by 24%/30%.", "✦ Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de 24%/30%."),
    ("At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color=#2899ff>24%/30%</color>.", "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>."),
    ("At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by 24%/30%.", "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de 24%/30%."),

    # Perseverance & Gain
    ("✦ Increase Attack based on lost HP. Increase Attack by a maximum of <color=#2899ff>40%</color> when HP is down to 40%.", "✦ Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%."),
    ("✦ Increase Attack based on lost HP. Increase Attack by a maximum of 40% when HP is down to 40%.", "✦ Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de 40% quand les PV descendent à 40%."),
    ("✦ Increase Attack based on missing HP. Increase Attack by a maximum of <color=#2899ff>40%</color> when HP is down to 40%.", "✦ Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%."),
    ("✦ Increase Attack based on missing HP. Increase Attack by a maximum of 40% when HP is down to 40%.", "✦ Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de 40% quand les PV descendent à 40%."),
    ("Increase Attack based on lost HP. Increase Attack by a maximum of <color=#2899ff>40%</color> when HP is down to 40%.", "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de <color\\=#2899ff>40%</color> quand les PV descendent à 40%."),
    ("Increase Attack based on lost HP. Increase Attack by a maximum of 40% when HP is down to 40%.", "Augmente l'ATQ selon les PV perdus. Augmente l'ATQ jusqu'à un maximum de 40% quand les PV descendent à 40%."),

    # Perseverance & Sorrow
    ("✦ Increase continuous damage by <color=#2899ff>16%</color>.", "✦ Augmente les dégâts continus de <color\\=#2899ff>16%</color>."),
    ("✦ Increase continuous damage by 16%.", "✦ Augmente les dégâts continus de 16%."),
    ("✦ Increase continuous damage effect by <color=#2899ff>16%</color>.", "✦ Augmente les effets de dégâts continus de <color\\=#2899ff>16%</color>."),
    ("✦ Increase continuous damage effect by 16%.", "✦ Augmente les effets de dégâts continus de 16%."),
    ("Increase continuous damage by <color=#2899ff>16%</color>.", "Augmente les dégâts continus de <color\\=#2899ff>16%</color>."),
    ("Increase continuous damage by 16%.", "Augmente les dégâts continus de 16%."),

    # Nativity & Strife
    ("✦ At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to <color=#2899ff>2</color> times.", "✦ Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à <color\\=#2899ff>2</color> fois."),
    ("✦ At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.", "✦ Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois."),
    ("✦ At the start of battle or at the start of an extra action, increase party's critical damage by 10%. This effect is permanent and stacks up to 2 times.", "✦ Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de 10%. Cet effet est permanent et cumulable jusqu'à 2 fois."),
    ("At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to <color=#2899ff>2</color> times.", "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à <color\\=#2899ff>2</color> fois."),
    ("At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.", "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois."),
    ("At the start of battle or at the start of an extra action, increase party's critical damage by 10%. This effect is permanent and stacks up to 2 times.", "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de 10%. Cet effet est permanent et cumulable jusqu'à 2 fois."),

    # Acuity & Satiety
    ("✦ Increase All-Out Attack damage by <color=#2899ff>16%</color>.", "✦ Augmente les dégâts de l'Assaut Général de <color\\=#2899ff>16%</color>."),
    ("✦ Increase All-Out Attack damage by 16%.", "✦ Augmente les dégâts de l'Assaut Général de 16%."),
    ("✦ After activating a Theurgy, increase party's damage by <color=#2899ff>10%</color> for 3 turns.", "✦ Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de <color\\=#2899ff>10%</color> pendant 3 tours."),
    ("✦ After activating a Theurgy, increase party's damage by 10% for 3 turns.", "✦ Après avoir activé un HIGHLIGHT, augmente les dégâts de l'équipe de 10% pendant 3 tours.")
]

added = 0
for k, v in pairs_to_add:
    if k not in data:
        data[k] = v
        added += 1

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Done! Added {added} static variations to 02_Cartes_Revelation_et_Sets.json.')
