#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chercher_texte.py
Recherche un terme (nom de compétence, arme, personnage, texte d'origine ou traduit)
dans tous les fichiers de TRADUCTION_FACILE.
Usage: python chercher_texte.py <mot_cle>
"""

import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_EASY = os.path.join(BASE_DIR, 'TRADUCTION_FACILE')

def search_text(keyword, search_dir):
    keyword_lower = keyword.lower()
    matches = []

    for root, dirs, files in os.walk(search_dir):
        dirs.sort()
        for file in sorted(files):
            if not file.endswith('.json'):
                continue
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                continue
            for k, v in data.items():
                if keyword_lower in k.lower() or keyword_lower in str(v).lower():
                    matches.append((path, k, str(v)))
    return matches

def main():
    if len(sys.argv) < 2:
        print("Usage: python chercher_texte.py <terme_a_chercher>")
        print("Exemple: python chercher_texte.py Agi")
        sys.exit(1)

    term = " ".join(sys.argv[1:])
    print(f"Recherche de '{term}' dans TRADUCTION_FACILE...\n")
    results = search_text(term, DIR_EASY)

    if not results:
        print("Aucun résultat trouvé.")
    else:
        print(f"{len(results)} occurrences trouvées :\n")
        for filepath, key, val in results[:30]:
            rel_path = os.path.relpath(filepath, DIR_EASY)
            print(f"[{rel_path}]")
            print(f"   EN : {key[:120]}")
            print(f"   FR : {val[:120] if val.strip() else '(pas encore traduit)'}")
        if len(results) > 30:
            print(f"\n... et {len(results) - 30} autre(s) occurrence(s).")

if __name__ == '__main__':
    main()
