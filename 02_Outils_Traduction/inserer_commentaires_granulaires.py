# -*- coding: utf-8 -*-
"""
Annotate 02_Cartes_Revelation_et_Sets.json with granular, prominent comments
for every single AI-translated card ability and set effect, using both 'A REVOIR'
and 'À REVOIR' so that any search query (with or without accent) hits them immediately.
"""
import json, os

path = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Supprimer tous les anciens commentaires //
clean = {k: v for k, v in data.items() if not k.startswith('//')}

result = {}

# 1. EN-TÊTE PRINCIPAL
result["// =========================================================================================="] = ""
result["// [A REVOIR / À REVOIR] - GUIDE DES TRADUCTIONS TEMPORAIRES DE L'IA POUR GYOTRE"] = ""
result["// =========================================================================================="] = ""
result["// Ce fichier contient deux types de contenus :"] = ""
result["// 1. Les textes traduits et validés par Gyotre (Stats, UI, menus, forge, Voleur Élucidateur)."] = ""
result["// 2. Les descriptions d'effets traduites par l'IA (temporaires) pour assurer le 100% en jeu."] = ""
result["// "] = ""
result["// RECHERCHE RAPIDE DANS VOTRE ÉDITEUR (VS Code / Bloc-notes / Notepad++) :"] = ""
result["// Faites Ctrl+F et tapez : 'A REVOIR' ou 'REVOIR' pour sauter directement aux cartes à peaufiner !"] = ""
result["// Les lignes '//' sont de vrais commentaires ignorés à la compilation (aucun impact en jeu)."] = ""
result["// =========================================================================================="] = ""

# 2. Section Gyotre (Stats, UI, Cartes Departure/Awareness, Forge)
result["// =========================================================================================="] = ""
result["// --- SECTION 1 : [TRADUIT PAR GYOTRE] STATS, FORGE & UI (VALIDÉ PAR TOI) ---"] = ""
result["// =========================================================================================="] = ""

# Séparation des clés
user_keys = {}
combo_abilities = {}
detailed_4set = {}
detailed_2set = {}
size23_sets = {}
puces_variants = {}
fire_initial = {}

for k, v in clean.items():
    if k.startswith('✦ '):
        puces_variants[k] = v
    elif k.startswith('<size=23>') or k.startswith('<size=20>') or k.startswith('<size=8'):
        size23_sets[k] = v
    elif any(k.startswith(prefix) for prefix in ['2 Set Effect: Increase Fire', '4 Set Effect: Increase Attack by 15%', '2 Set Effect：Increase Fire', '4 Set Effect：Increase Attack by 15%']):
        fire_initial[k] = v
    elif k.startswith('2 Set Effect') or k.startswith('2 Set Effect：') or k.startswith('2 Set Effect:'):
        detailed_2set[k] = v
    elif k.startswith('4 Set Effect') or k.startswith('4 Set Effect：') or k.startswith('4 Set Effect:'):
        detailed_4set[k] = v
    elif any(w in k for w in ['When Malice', 'During battle', 'After using a Highlight', 'At the start of battle, if', 'Increase Attack based on', 'Increase continuous damage', 'At the start of battle or at', 'Increase All-Out Attack', 'After activating a Theurgy', 'When equipped by an Elucidator', 'When current HP is over', 'When activating a Resonance', 'All allies deal', 'Increase Resonance', 'After using a skill, gain 1 Glory', 'After dealing a critical hit']):
        combo_abilities[k] = v
    else:
        user_keys[k] = v

result.update(user_keys)

# 3. Combinaisons d'arcanes spécifiques (Wisdom, Resolve, Perseverance, Nativity, Acuity...)
result["// =========================================================================================="] = ""
result["// --- SECTION 2 : [A REVOIR / À REVOIR - IA] CAPACITÉS DES COMBINAISONS D'ARCANES ---"] = ""
result["// =========================================================================================="] = ""

# Regroupement intelligent par arcane
grouped_combos = {
    "Wisdom & Oppression / Pleasure / Virtue": [],
    "Resolve & Prudence": [],
    "Perseverance & Gain / Change / Sorrow": [],
    "Nativity & Strife / Power": [],
    "Acuity & Satiety (Assaut Général & HIGHLIGHT)": [],
    "Voleur Élucidateur & Passifs Spécifiques (Motoha, Soins, etc.)": []
}

for k, v in combo_abilities.items():
    if any(w in k for w in ['Malice', 'ailment accuracy', 'After using a Highlight']):
        grouped_combos["Wisdom & Oppression / Pleasure / Virtue"].append((k, v))
    elif '3rd/4th ally in the turn order' in k or '3rd/4th turn order' in k:
        grouped_combos["Resolve & Prudence"].append((k, v))
    elif any(w in k for w in ['lost HP', 'missing HP', 'continuous damage', 'Electric damage by']):
        grouped_combos["Perseverance & Gain / Change / Sorrow"].append((k, v))
    elif 'extra action' in k or 'critical damage by 10%' in k or 'Desire Level' in k:
        grouped_combos["Nativity & Strife / Power"].append((k, v))
    elif any(w in k for w in ['All-Out Attack', 'After activating a Theurgy', 'Theurgy damage is increased']):
        grouped_combos["Acuity & Satiety (Assaut Général & HIGHLIGHT)"].append((k, v))
    else:
        grouped_combos["Voleur Élucidateur & Passifs Spécifiques (Motoha, Soins, etc.)"].append((k, v))

for title, entries in grouped_combos.items():
    if entries:
        result[f"// >>> [A REVOIR / À REVOIR] {title} <<<"] = ""
        for k, v in entries:
            result[k] = v

# 4. Effets de Set 4 Pièces
result["// =========================================================================================="] = ""
result["// --- SECTION 3 : [A REVOIR / À REVOIR - IA] EFFETS DE SET 4 PIÈCES (DÉTAILLÉS) ---"] = ""
result["// =========================================================================================="] = ""

grouped_4sets = {
    "Worry (Remplissage Jauge HIGHLIGHT 25%)": [],
    "Fire / Feu (Attaque +15% si cible faible Feu)": [],
    "Electric / Électrique (Dégâts Élec après compétence)": [],
    "Malice / Attaque cumulable": [],
    "Soins & Buffs Alliés (Healing)": [],
    "Autres Effets 4 Pièces (Stats, Coups Critiques, Attributs)": []
}

for k, v in detailed_4set.items():
    if 'Highlight gauge' in k or 'HIGHLIGHT Energy' in k:
        grouped_4sets["Worry (Remplissage Jauge HIGHLIGHT 25%)"].append((k, v))
    elif 'weak to Fire' in k or 'Fire DMG' in k:
        grouped_4sets["Fire / Feu (Attaque +15% si cible faible Feu)"].append((k, v))
    elif 'Electric' in k or 'Elec' in k:
        grouped_4sets["Electric / Électrique (Dégâts Élec après compétence)"].append((k, v))
    elif 'Malice' in k:
        grouped_4sets["Malice / Attaque cumulable"].append((k, v))
    elif 'healing' in k or 'Healing' in k or 'Soins' in v:
        grouped_4sets["Soins & Buffs Alliés (Healing)"].append((k, v))
    else:
        grouped_4sets["Autres Effets 4 Pièces (Stats, Coups Critiques, Attributs)"].append((k, v))

for title, entries in grouped_4sets.items():
    if entries:
        result[f"// >>> [A REVOIR / À REVOIR] 4P : {title} <<<"] = ""
        for k, v in entries:
            result[k] = v

# 5. Effets de Set 2 Pièces
result["// =========================================================================================="] = ""
result["// --- SECTION 4 : [A REVOIR / À REVOIR - IA] EFFETS DE SET 2 PIÈCES (TOUS ÉLÉMENTS & STATS) ---"] = ""
result["// =========================================================================================="] = ""
result["// >>> [A REVOIR / À REVOIR] 2P : Bonus élémentaires et statistiques directes <<<"] = ""
result.update(detailed_2set)

# 6. Sets multilinges et size=23
result["// =========================================================================================="] = ""
result["// --- SECTION 5 : [A REVOIR / À REVOIR - IA] FORMATS MOBILES & MULTILIGNES ANCIENS (<size=23>) ---"] = ""
result["// =========================================================================================="] = ""
result.update(fire_initial)
result.update(size23_sets)

# 7. Variantes Steam avec puces ✦
result["// =========================================================================================="] = ""
result["// --- SECTION 6 : [A REVOIR / À REVOIR - IA] VARIANTES AVEC PUCES '✦ ' DU CLIENT STEAM ---"] = ""
result["// =========================================================================================="] = ""
result["// >>> [A REVOIR / À REVOIR] Variantes avec puce ✦ et balises de couleurs exactes <<<"] = ""
result.update(puces_variants)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Terminé ! Fichier structuré avec {len(result)} entrées au total.")
