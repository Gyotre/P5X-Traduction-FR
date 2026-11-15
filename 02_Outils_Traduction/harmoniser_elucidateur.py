# -*- coding: utf-8 -*-
import json, glob, os

files = glob.glob(os.path.join('TRADUCTION_FACILE', '11_Textes_Generaux_Steam', '*.json'))

count = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for k, v in list(data.items()):
        if 'Voleur Fantôme Élucidateur' in v:
            data[k] = v.replace('Voleur Fantôme Élucidateur', 'Voleur Élucidateur')
            changed = True
            count += 1
        elif 'Voleur  Élucidateur' in v:
            data[k] = v.replace('Voleur  Élucidateur', 'Voleur Élucidateur')
            changed = True
            count += 1
    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Aussi dans 02_Cartes_Revelation_et_Sets.json (nettoyer double espace s'il y en a)
cart_fp = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
with open(cart_fp, 'r', encoding='utf-8') as f:
    cdata = json.load(f)
c_changed = False
for k, v in list(cdata.items()):
    if 'Voleur  Élucidateur' in v:
        cdata[k] = v.replace('Voleur  Élucidateur', 'Voleur Élucidateur')
        c_changed = True
    elif 'Voleur  Éucidateur' in v:
        cdata[k] = v.replace('Voleur  Éucidateur', 'Voleur Élucidateur')
        c_changed = True
if c_changed:
    with open(cart_fp, 'w', encoding='utf-8') as f:
        json.dump(cdata, f, ensure_ascii=False, indent=2)

print(f"Harmonisé {count} occurrences vers 'Voleur Élucidateur'.")
