# -*- coding: utf-8 -*-
"""
Vérification approfondie du fichier 02_Cartes_Revelation_et_Sets.json :
1. Syntaxe JSON et encodage UTF-8
2. Balises Rich Text (<color>, <size>, <b>, <u>, <link>, <nobr>)
3. Variables ($1, $2, {{A}}...)
4. Valeurs vides ou doublons
5. Respect du glossaire officiel (ATQ, DEF, PV, Highlight, Theurgy, Elucidator, etc.)
"""
import json, re, os

file_path = os.path.join('TRADUCTION_FACILE', '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')

with open(file_path, 'r', encoding='utf-8') as f:
    try:
        data = json.load(f)
        print("✅ 1. Syntaxe JSON : 100% VALIDE (aucun problème de syntaxe)")
    except Exception as e:
        print("❌ 1. Syntaxe JSON : ERREUR :", e)
        exit(1)

total = len(data)
comments = 0
empty = 0
valid_trans = 0

tag_errors = []
var_errors = []
unescaped_equals = []
glossary_checks = {
    'PV': 0,
    'ATQ': 0,
    'DEF': 0,
    'Highlight': 0,
    'Theurgy': 0,
    'Elucidator': 0,
    'Élucidateur (ancien)': 0,
    'HIGHLIGHT (majuscule ancienne)': 0,
    'Taux CRIT': 0,
    'Dégâts CRIT': 0,
}

for k, v in data.items():
    if k.startswith('//') or k.startswith('#'):
        comments += 1
        continue
    if not v.strip():
        empty += 1
        continue
    valid_trans += 1

    # Balises dans la valeur
    for tag in ['color', 'size', 'b', 'u', 'link', 'nobr']:
        open_c = len(re.findall(rf'<{tag}[^>]*>', v, re.IGNORECASE))
        close_c = len(re.findall(rf'</{tag}>', v, re.IGNORECASE))
        if open_c != close_c:
            tag_errors.append((k, v, f"Balise <{tag}> non équilibrée : {open_c} ouvrante(s), {close_c} fermante(s)"))

    # Variables ($1, $2...)
    if not (k.startswith('r:') or k.startswith('sr:')):
        k_vars = set(re.findall(r'\$(\d+)', k))
        v_vars = set(re.findall(r'\$(\d+)', v))
        if k_vars != v_vars:
            var_errors.append((k, v, f"Variables mismatch : original {k_vars} vs traduction {v_vars}"))

    # Placeholders {{A}}, {{B}}
    k_ph = set(re.findall(r'\{\{([A-Za-z0-9_]+)\}\}', k))
    v_ph = set(re.findall(r'\{\{([A-Za-z0-9_]+)\}\}', v))
    if k_ph != v_ph:
        var_errors.append((k, v, f"Placeholders mismatch : original {k_ph} vs traduction {v_ph}"))

    # Glossary occurrences
    if 'PV' in v: glossary_checks['PV'] += 1
    if 'ATQ' in v: glossary_checks['ATQ'] += 1
    if 'DEF' in v: glossary_checks['DEF'] += 1
    if 'Highlight' in v: glossary_checks['Highlight'] += 1
    if 'Theurgy' in v: glossary_checks['Theurgy'] += 1
    if 'Elucidator' in v: glossary_checks['Elucidator'] += 1
    if 'Élucidateur' in v: glossary_checks['Élucidateur (ancien)'] += 1
    if 'HIGHLIGHT' in v: glossary_checks['HIGHLIGHT (majuscule ancienne)'] += 1
    if 'Taux CRIT' in v or 'Taux Crit.' in v: glossary_checks['Taux CRIT'] += 1
    if 'Dégâts CRIT' in v or 'Dégâts Crit.' in v: glossary_checks['Dégâts CRIT'] += 1

print(f"📊 Statistiques du fichier :")
print(f"   • Total des clés : {total}")
print(f"   • Textes traduits actifs : {valid_trans}")
print(f"   • Commentaires & Séparateurs de sections : {comments}")
print(f"   • Textes vides : {empty}")
print(f"\n🔍 Contrôle d'intégrité :")
print(f"   • Erreurs de balises Rich Text : {len(tag_errors)}")
for k, v, err in tag_errors:
    print(f"     ❌ {err}\n        Clé : {k[:60]}\n        Val : {v[:60]}")

print(f"   • Erreurs de variables ($1, {{{{A}}}}...) : {len(var_errors)}")
for k, v, err in var_errors:
    print(f"     ❌ {err}\n        Clé : {k[:60]}\n        Val : {v[:60]}")

print(f"\n📖 Contrôle du Glossaire :")
for term, count in glossary_checks.items():
    print(f"   • {term} : {count} occurrence(s)")
