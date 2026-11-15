# -*- coding: utf-8 -*-
"""
Applique les modifications textuelles demandées par l'utilisateur pour les cartes de Révélation,
ajoute les variantes avec et sans '✦ ' et balises, et met à jour les regex dynamiques.
"""
import json, os

path_json = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
with open(path_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Paires demandées par l'utilisateur
user_updates = {
    # 1. Debuff DEF par Voleur Élucidateur
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color\\=#2899ff>10%</color> for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color=#2899ff>10%</color> for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief：After using a skill to inflict a debuff on a foe, decrease target's Defense by <color\\=#2899ff>10%</color> for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief：After using a skill to inflict a debuff on a foe, decrease target's Defense by <color=#2899ff>10%</color> for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by 10% for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de 10% pendant 2 tours.",
    "When equipped by an Elucidator Phantom Thief：After using a skill to inflict a debuff on a foe, decrease target's Defense by 10% for 2 turns.":
        "Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de 10% pendant 2 tours.",

    # Variantes avec puce ✦
    "✦ When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by <color=#2899ff>10%</color> for 2 turns.":
        "✦ Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de <color\\=#2899ff>10%</color> pendant 2 tours.",
    "✦ When equipped by an Elucidator Phantom Thief: After using a skill to inflict a debuff on a foe, decrease target's Defense by 10% for 2 turns.":
        "✦ Si équipé par un Voleur Élucidateur : après avoir utilisé une compétence infligeant un malus à un ennemi, réduit la DEF de la cible de 10% pendant 2 tours.",

    # 2. PV 6000/9000/12000
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color\\=#2899ff>10%/20%/30%</color>.":
        "Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de <color\\=#2899ff>10%, 20% ou 30%</color>.",
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by <color=#2899ff>10%/20%/30%</color>.":
        "Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de <color\\=#2899ff>10%, 20% ou 30%</color>.",
    "During battle, when user's HP reaches 6000/9000/12000, increase damage by 10%/20%/30%.":
        "Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de 10%, 20% ou 30%.",
    "✦ During battle, when user's HP reaches 6000/9000/12000, increase damage by <color=#2899ff>10%/20%/30%</color>.":
        "✦ Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de <color\\=#2899ff>10%, 20% ou 30%</color>.",
    "✦ During battle, when user's HP reaches 6000/9000/12000, increase damage by 10%/20%/30%.":
        "✦ Pendant le combat, lorsque les PV du lanceur atteignent 6000, 9000 ou 12000, augmente les dégâts de 10%, 20% ou 30%.",

    # 3. ATQ de Motoha
    "During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to <color\\=#FFFC40>1280</color>.":
        "Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à <color\\=#FFFC40>1280</color>.",
    "During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to <color=#FFFC40>1280</color>.":
        "Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à <color\\=#FFFC40>1280</color>.",
    "During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to 1280.":
        "Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à 1280.",
    "✦ During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to <color=#FFFC40>1280</color>.":
        "✦ Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à <color\\=#FFFC40>1280</color>.",
    "✦ During battle, increase Motoha's Attack by 24 points for every 100 points of max HP above 8000, up to 1280.":
        "✦ Pendant le combat, augmente l'ATQ de Motoha de 24 points par tranche de 100 points de PV max au-delà de 8000, jusqu'à 1280.",

    # 4. PV actuels > 50%
    "When current HP is over 50%, increase critical rate of Bless skills by 12%.":
        "Quand les PV actuels sont supérieurs à 50%, augmente le taux CRIT des compétences Bénies de 12%.",
    "✦ When current HP is over 50%, increase critical rate of Bless skills by 12%.":
        "✦ Quand les PV actuels sont supérieurs à 50%, augmente le taux CRIT des compétences Bénies de 12%.",

    # 5. Voleur Élucidateur : attribut assorti
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color\\=#2899ff>2%</color> more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color=#2899ff>2%</color> more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "When equipped by an Elucidator Phantom Thief：At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color\\=#2899ff>2%</color> more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "When equipped by an Elucidator Phantom Thief：At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color=#2899ff>2%</color> more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by 2% more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de 2% supplémentaires.",
    "When equipped by an Elucidator Phantom Thief：At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by 2% more.":
        "Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de 2% supplémentaires.",
    "✦ When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by <color=#2899ff>2%</color> more.":
        "✦ Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de <color\\=#2899ff>2%</color> supplémentaires.",
    "✦ When equipped by an Elucidator Phantom Thief: At the start of battle, for each ally with a matching main attribute, increase party's max HP, Attack, and Defense by 2% more.":
        "✦ Si équipé par un Voleur Élucidateur : au début du combat, pour chaque allié ayant le même attribut principal, augmente les PV max, l'ATQ et la DEF de l'équipe de 2% supplémentaires."
}

for k, v in user_updates.items():
    data[k] = v

with open(path_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Mis à jour {len(user_updates)} clés dans 02_Cartes_Revelation_et_Sets.json !")
