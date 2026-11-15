# -*- coding: utf-8 -*-
import os

path_regex = os.path.join('TRADUCTION_FR', '01_Kits_Personnages', '00_Regex_Dynamiques.txt')
with open(path_regex, 'r', encoding='utf-8') as f:
    content = f.read()

new_regexes = """
r:"(?s)When equipped by an Elucidator Phantom Thief[：:]\\s*After using a skill to inflict a debuff on a foe,\\s*decrease target's Defense by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? for (\\d+) turns\\.?"="Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de $1% pendant $2 tours."
r:"(?s)During battle,\\s*when user's HP reaches 6000/9000/12000,\\s*increase damage by\\s*(?:<color[^>]*>)?([\\d%/]+)(?:</color>)?\\.?"="Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de 10%, 20% ou 30%."
r:"(?s)During battle,\\s*increase Motoha's Attack by (\\d+) points for every (\\d+) points of max HP above (\\d+),\\s*up to\\s*(?:<color[^>]*>)?(\\d+)(?:</color>)?\\.?"="Pendant le combat, augmente l'ATQ de Motoha de $1 points par tranche de $2 points de PV max au-delà de $3, jusqu'à $4."
r:"(?s)When current HP is over (\\d+)%,\\s*increase critical rate of Bless skills by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)?\\.?"="Quand les PV actuels sont supérieurs à $1%, augmente le taux CRIT des compétences Bénies de $2%."
r:"(?s)When equipped by an Elucidator Phantom Thief[：:]\\s*At the start of battle,\\s*for each ally with a matching main attribute,\\s*increase party's max HP,\\s*Attack,\\s*and Defense by\\s*(?:<color[^>]*>)?(\\d+\\.?\\d*)%(?:</color>)? more\\.?"="Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de $1% supplémentaires."
"""

if "decrease target's Defense by" not in content:
    with open(path_regex, 'a', encoding='utf-8') as f:
        f.write('\n' + new_regexes)
    print("Nouvelles regex ajoutées à 00_Regex_Dynamiques.txt !")
else:
    print("Regex déjà présentes.")
