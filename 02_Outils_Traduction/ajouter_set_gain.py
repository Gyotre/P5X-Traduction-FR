# -*- coding: utf-8 -*-
"""
Ajoute la traduction de l'effet 4 pièces du set [Gain] dans 02_Cartes_Revelation_et_Sets.json
et dans 00_Regex_Dynamiques.txt avec toutes les variantes possibles.
"""
import json, os

json_path = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
regex_path = os.path.join('TRADUCTION_FR', '01_Kits_Personnages', '00_Regex_Dynamiques.txt')

# 1. Mise à jour JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

gain_entries = {
    "// >>> [A REVOIR / À REVOIR] 4P : Gain (Dépense de PV pour activer compétence) <<<": "",
    # 1 espace to activate
    "4 Set Effect: After spending HP to activate a skill, increase damage by <color\\=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect: After spending HP to activate a skill, increase damage by <color=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect:After spending HP to activate a skill, increase damage by <color\\=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect:After spending HP to activate a skill, increase damage by <color=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect：After spending HP to activate a skill, increase damage by <color\\=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect：After spending HP to activate a skill, increase damage by <color=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect: After spending HP to activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect:After spending HP to activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect：After spending HP to activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "✦ 4 Set Effect: After spending HP to activate a skill, increase damage by <color=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "✦ Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "✦ 4 Set Effect: After spending HP to activate a skill, increase damage by <color\\=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "✦ Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "✦ 4 Set Effect: After spending HP to activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "✦ Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",

    # 2 espaces to  activate (visibles sur certaines résolutions / fontes du jeu)
    "4 Set Effect: After spending HP to  activate a skill, increase damage by <color\\=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect: After spending HP to  activate a skill, increase damage by <color=#2899ff>12%</color> for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de <color\\=#2899ff>12%</color> pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect: After spending HP to  activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "4 Set Effect：After spending HP to  activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois.",
    "✦ 4 Set Effect: After spending HP to  activate a skill, increase damage by 12% for 2 turns. Stacks up to 2 times.":
        "✦ Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de 12% pendant 2 tours. Cumulable jusqu'à 2 fois."
}

data.update(gain_entries)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Entrées [Gain] ajoutées dans 02_Cartes_Revelation_et_Sets.json !")

# 2. Mise à jour Regex
with open(regex_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
found = False
new_gain_regex = 'r:"(?s)(?:✦\\s*)?4 Set Effect[：:]\\s*After\\s+spending\\s+HP\\s+to\\s+(?:activate|use)\\s+a\\s+skill,?\\s*increase\\s+damage\\s+by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\s*for\\s+(\\d+)\\s+turns\\.?\\s*Stacks\\s+up\\s+to\\s+(\\d+)\\s+times\\.?"="Effet 4 pièces : Après avoir dépensé des PV pour activer une compétence, augmente les dégâts de $1% pendant $2 tours. Cumulable jusqu\'à $3 fois."\n'

for line in lines:
    if "After spending HP" in line:
        new_lines.append(new_gain_regex)
        found = True
    else:
        new_lines.append(line)

if not found:
    new_lines.append('\n' + new_gain_regex)

with open(regex_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Regex [Gain] mise à jour dans 00_Regex_Dynamiques.txt !")
