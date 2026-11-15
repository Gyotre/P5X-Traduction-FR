#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_extra_card_fixes.py
Ajoute les capacités manquantes identifiées dans les captures d'écran récentes :
- Resolve & Prudence
- Perseverance & Gain
- Perseverance & Sorrow (variante sans 'effect')
- Nativity & Strife
- Acuity & Satiety
- Regex de dégâts continus
"""

import os
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EASY_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")
CARDS_FILE = os.path.join(EASY_DIR, "08_Equipements_et_Objets", "02_Cartes_Revelation_et_Sets.json")
UI_FILE = os.path.join(EASY_DIR, "09_Interface_et_Menus", "01_UI_Steam_Officiel.json")
SYNC_SCRIPT = os.path.join(BASE_DIR, "02_Outils_Traduction", "synchroniser_steam_cartes.py")

NEW_OVERRIDES = {
    # 1. Resolve & Prudence
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color\\=#2899ff>24%/30%</color>.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>.",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by <color=#2899ff>24%/30%</color>.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de <color\\=#2899ff>24%/30%</color>.",
    "At the start of battle, if the user is the 3rd/4th ally in the turn order, increase Attack by 24%/30%.":
        "Au début du combat, si le lanceur est le 3e ou 4e allié dans l'ordre du tour, augmente l'ATQ de 24%/30%.",

    # 2. Perseverance & Gain (avec lost HP et missing HP)
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

    # 3. Perseverance & Sorrow (sans 'effect')
    "Increase continuous damage by <color\\=#2899ff>16%</color>.":
        "Augmente les dégâts continus de <color\\=#2899ff>16%</color>.",
    "Increase continuous damage by <color=#2899ff>16%</color>.":
        "Augmente les dégâts continus de <color\\=#2899ff>16%</color>.",
    "Increase continuous damage by 16%.":
        "Augmente les dégâts continus de 16%.",

    # 4. Nativity & Strife
    "At the start of battle or at the start of an extra action, increase party's critical damage by <color\\=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by <color=#2899ff>10%</color>. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de <color\\=#2899ff>10%</color>. Cet effet est permanent et cumulable jusqu'à 2 fois.",
    "At the start of battle or at the start of an extra action, increase party's critical damage by 10%. This effect is permanent and stacks up to 2 times.":
        "Au début du combat ou au début d'une action supplémentaire, augmente les dégâts critiques de l'équipe de 10%. Cet effet est permanent et cumulable jusqu'à 2 fois.",

    # 5. Acuity & Satiety
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

    # 6. Titres de combos (garde en anglais avec taille anti-chevauchement)
    "Perseverance & Gain": "Perseverance & Gain",
    "Acuity & Satiety": "Acuity & Satiety",
    "Nativity & Strife": "Nativity & Strife",
    "Resolve & Prudence": "<size=85%>Resolve & Prudence</size>"
}

# 1. Mise à jour de 02_Cartes_Revelation_et_Sets.json
print("1. Mise à jour de 02_Cartes_Revelation_et_Sets.json...")
with open(CARDS_FILE, "r", encoding="utf-8") as f:
    cards_data = json.load(f)

c_added = 0
for k, v in NEW_OVERRIDES.items():
    if k not in cards_data or not cards_data[k].strip() or cards_data[k] != v:
        cards_data[k] = v
        c_added += 1

with open(CARDS_FILE, "w", encoding="utf-8") as f:
    json.dump(cards_data, f, ensure_ascii=False, indent=2)
print(f"  • {c_added} entrée(s) ajoutée(s)/mise(s) à jour dans Cartes.")

# 2. Mise à jour de 01_UI_Steam_Officiel.json
print("\n2. Mise à jour de 01_UI_Steam_Officiel.json...")
with open(UI_FILE, "r", encoding="utf-8") as f:
    ui_data = json.load(f)

ui_mods = 0
for k, v in NEW_OVERRIDES.items():
    if k in ui_data and ui_data[k] != v:
        ui_data[k] = v
        ui_mods += 1
    # Check escaped variants
    k_esc = k.replace("=", r"\=")
    if k_esc in ui_data and ui_data[k_esc] != v:
        ui_data[k_esc] = v
        ui_mods += 1

# Regex de dégâts continus
regex_key = r'r:"^Increase continuous damage by <color\=#2899ff>([\d\.]+)%</color>\.$"'
regex_val = r'"Augmente les dégâts continus de <color\=#2899ff>$1%</color>."'
if regex_key in ui_data:
    ui_data[regex_key] = regex_val
    ui_mods += 1

with open(UI_FILE, "w", encoding="utf-8") as f:
    json.dump(ui_data, f, ensure_ascii=False, indent=2)
print(f"  • {ui_mods} entrée(s) mise(s) à jour dans UI Steam.")

# 3. Mise à jour de synchroniser_steam_cartes.py
print("\n3. Mise à jour de synchroniser_steam_cartes.py...")
with open(SYNC_SCRIPT, "r", encoding="utf-8") as f:
    sync_code = f.read()

# Ajouter les nouvelles entrées dans CARD_ABILITY_OVERRIDES
for k, v in NEW_OVERRIDES.items():
    if k not in sync_code:
        # Insérer après CARD_ABILITY_OVERRIDES = {
        idx = sync_code.find("CARD_ABILITY_OVERRIDES = {")
        if idx != -1:
            end_brace = sync_code.find("}", idx)
            entry_str = f'    "{k}":\n        "{v}",\n'
            sync_code = sync_code[:end_brace] + entry_str + sync_code[end_brace:]

with open(SYNC_SCRIPT, "w", encoding="utf-8") as f:
    f.write(sync_code)
print("  • synchroniser_steam_cartes.py mis à jour.")

# 4. Mise à jour des fichiers Steam dans TRADUCTION_FACILE/11_Textes_Generaux_Steam
print("\n4. Synchronisation des fichiers Steam...")
import glob
for sf in sorted(glob.glob(os.path.join(EASY_DIR, "11_Textes_Generaux_Steam", "*.json"))):
    with open(sf, "r", encoding="utf-8") as f:
        sdata = json.load(f)
    smods = 0
    for k, v in NEW_OVERRIDES.items():
        if k in sdata and sdata[k] != v:
            sdata[k] = v
            smods += 1
        k_esc = k.replace("=", r"\=")
        if k_esc in sdata and sdata[k_esc] != v:
            sdata[k_esc] = v
            smods += 1
    if smods > 0:
        with open(sf, "w", encoding="utf-8") as f:
            json.dump(sdata, f, ensure_ascii=False, indent=2)
        print(f"  • {os.path.basename(sf)} : {smods} mise(s) à jour.")

print("\nToutes les capacités supplémentaires ont été appliquées avec succès.")
