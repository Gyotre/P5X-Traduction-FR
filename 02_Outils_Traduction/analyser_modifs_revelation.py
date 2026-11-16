# -*- coding: utf-8 -*-
import subprocess, re

diff = subprocess.check_output(['git', 'diff', 'TRADUCTION_FACILE/08_Equipements_et_Objets/02_Cartes_Revelation_et_Sets.json'], encoding='utf-8')

lines = diff.splitlines()
diff_pairs = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('-  "') and i + 1 < len(lines) and lines[i+1].startswith('+  "'):
        old_line = line[1:].strip()
        new_line = lines[i+1][1:].strip()
        diff_pairs.append((old_line, new_line))
        i += 2
        continue
    i += 1

print(f"Total direct replaced lines: {len(diff_pairs)}")

categories = {
    'Theurgy (gardé en Theurgy au lieu de HIGHLIGHT)': [],
    'Highlight (casse: Highlight au lieu de HIGHLIGHT)': [],
    'Elucidator (au lieu de Élucidateur)': [],
    'Type (au lieu de attribut principal)': [],
    'Non cumulable (au lieu de ne se cumule pas / pas actif si cumulé)': [],
    'Taux CRIT / Stats (Harmonisation des majuscules Taux CRIT)': [],
    'Commentaires de section [VÉRIFIÉ - glossaire]': [],
    'Autres': []
}

for old, new in diff_pairs:
    categorized = False
    if 'Theurgy' in new or ('Theurgy' in old and 'HIGHLIGHT' in old):
        categories['Theurgy (gardé en Theurgy au lieu de HIGHLIGHT)'].append((old, new))
        categorized = True
    if ('Highlight' in new and 'HIGHLIGHT' in old) or ('Highlight' in old and 'HIGHLIGHT' in new):
        categories['Highlight (casse: Highlight au lieu de HIGHLIGHT)'].append((old, new))
        categorized = True
    if 'Elucidator' in new or 'Élucidateur' in old:
        categories['Elucidator (au lieu de Élucidateur)'].append((old, new))
        categorized = True
    if 'Type' in new and 'attribut' in old:
        categories['Type (au lieu de attribut principal)'].append((old, new))
        categorized = True
    if 'Non cumulable' in new:
        categories['Non cumulable (au lieu de ne se cumule pas / pas actif si cumulé)'].append((old, new))
        categorized = True
    if 'Taux CRIT' in new and 'taux CRIT' in old:
        categories['Taux CRIT / Stats (Harmonisation des majuscules Taux CRIT)'].append((old, new))
        categorized = True
    if not categorized:
        categories['Autres'].append((old, new))

for cat, items in categories.items():
    print(f"\n=== {cat} ({len(items)} entrées) ===")
    for old, new in items[:3]:
        print("  AVANT:", old[:110])
        print("  APRÈS:", new[:110])
