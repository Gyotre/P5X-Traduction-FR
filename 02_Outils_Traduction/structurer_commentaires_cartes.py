# -*- coding: utf-8 -*-
"""
Organise 02_Cartes_Revelation_et_Sets.json avec des bannières de commentaires claires
marquant les sections traduites par l'IA comme [À REVOIR / TEMPORAIRE IA],
afin que Gyotre puisse facilement les repérer et travailler dessus.
"""
import json, os

path = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Supprimer les anciens commentaires s'il y en avait
clean_data = {k: v for k, v in data.items() if not k.startswith('//')}

# Nous allons reconstruire un dictionnaire ordonné avec des commentaires bien placés.
new_data = {}

# 1. En-tête du fichier
new_data["// =========================================================================================="] = ""
new_data["// FICHIER : 02_Cartes_Revelation_et_Sets.json — Persona 5: The Phantom X (Patch FR v1.1.0)"] = ""
new_data["// NOTE POUR GYOTRE :"] = ""
new_data["// Les sections annotées '[À REVOIR / TEMPORAIRE IA]' contiennent les descriptions générées"] = ""
new_data["// par l'IA pour garantir du 100% en jeu. Tu peux les repérer d'un coup d'œil pour les peaufiner !"] = ""
new_data["// Les lignes de commentaires '//' sont automatiquement ignorées par le compilateur convertisseur_json."] = ""
new_data["// =========================================================================================="] = ""

# 2. Catégorisation des entrées
cat_fire_initial = {}
cat_ui_gyotre = {}
cat_size23_sets = {}
cat_2set_detailed = {}
cat_4set_detailed = {}
cat_combos_standalone = {}
cat_puces_variants = {}

for k, v in clean_data.items():
    if k.startswith('✦ '):
        cat_puces_variants[k] = v
    elif k.startswith('<size=23>') or k.startswith('<size=20>') or k.startswith('<size=8'):
        cat_size23_sets[k] = v
    elif any(k.startswith(prefix) for prefix in ['2 Set Effect: Increase Fire', '4 Set Effect: Increase Attack by 15%', '2 Set Effect：Increase Fire', '4 Set Effect：Increase Attack by 15%']):
        cat_fire_initial[k] = v
    elif k.startswith('2 Set Effect') or k.startswith('2 Set Effect：') or k.startswith('2 Set Effect:'):
        cat_2set_detailed[k] = v
    elif k.startswith('4 Set Effect') or k.startswith('4 Set Effect：') or k.startswith('4 Set Effect:'):
        cat_4set_detailed[k] = v
    elif any(word in k for word in ['When Malice', 'During battle', 'After using a Highlight', 'At the start of battle, if', 'Increase Attack based on', 'Increase continuous damage', 'At the start of battle or at', 'Increase All-Out Attack', 'After activating a Theurgy', 'When equipped by an Elucidator', 'When current HP is over', 'When activating a Resonance', 'All allies deal', 'Increase Resonance', 'After using a skill, gain 1 Glory', 'After dealing a critical hit']):
        cat_combos_standalone[k] = v
    else:
        cat_ui_gyotre[k] = v

# Insertion ordonnée avec bannières

new_data["// --- 1. [TRADUIT PAR GYOTRE] STATS, NOMS D'ARCANES & INTERFACE DE PERSONNALISATION ---"] = ""
new_data.update(cat_ui_gyotre)

new_data["// --- 2. [À REVOIR / TEMPORAIRE IA] EFFETS DE SET FEU INITIAUX (COMBINÉS & MULTILIGNES) ---"] = ""
new_data.update(cat_fire_initial)

new_data["// --- 3. [À REVOIR / TEMPORAIRE IA] EFFETS DE SET FORMAT CLASSIQUE (<size=23> AVEC VARIABLES) ---"] = ""
new_data.update(cat_size23_sets)

new_data["// --- 4. [À REVOIR / TEMPORAIRE IA] EFFETS DE SET 2 PIÈCES DÉTAILLÉS (TOUS ÉLÉMENTS & STATS) ---"] = ""
new_data.update(cat_2set_detailed)

new_data["// --- 5. [À REVOIR / TEMPORAIRE IA] EFFETS DE SET 4 PIÈCES DÉTAILLÉS (WORRY, FIRE, ICE, ELEC...) ---"] = ""
new_data.update(cat_4set_detailed)

new_data["// --- 6. [À REVOIR / TEMPORAIRE IA] CAPACITÉS DES COMBINAISONS D'ARCANES (WISDOM, RESOLVE, PERSEVERANCE...) ---"] = ""
new_data.update(cat_combos_standalone)

new_data["// --- 7. [À REVOIR / TEMPORAIRE IA] VARIANTES AVEC PUCES ✦ & BALISES COULEUR EXACTES DU CLIENT STEAM ---"] = ""
new_data.update(cat_puces_variants)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"Structure mise à jour avec succès : {len(new_data)} entrées au total.")
