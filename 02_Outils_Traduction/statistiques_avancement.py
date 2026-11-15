#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistiques_avancement.py
Affiche l'avancement de la traduction par catégorie et par fichier (TRADUCTION_FACILE).
Usage: python statistiques_avancement.py [--fichiers]   (--fichiers détaille chaque fichier)
"""

import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_EASY = os.path.join(BASE_DIR, 'TRADUCTION_FACILE')

def pct(done, total):
    return (done / total * 100) if total else 0

def main():
    detail = '--fichiers' in sys.argv
    if not os.path.exists(DIR_EASY):
        print(f"Dossier introuvable : {DIR_EASY}")
        sys.exit(1)

    print("=" * 72)
    print("AVANCEMENT DE LA TRADUCTION P5X")
    print("=" * 72)

    categories = {}
    unique_all, unique_done = set(), set()

    for root, dirs, files in os.walk(DIR_EASY):
        dirs.sort()
        rel = os.path.relpath(root, DIR_EASY)
        cat = rel.split(os.sep)[0] if rel != '.' else '(racine)'
        for f in sorted(files):
            if not f.endswith('.json'):
                continue
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
            except Exception as e:
                print(f"[ERREUR] {os.path.join(rel, f)} : {e}")
                continue
            done = sum(1 for v in data.values() if str(v).strip())
            unique_all.update(k.strip() for k in data)
            unique_done.update(k.strip() for k, v in data.items() if str(v).strip())
            c = categories.setdefault(cat, {"total": 0, "done": 0, "files": []})
            c["total"] += len(data)
            c["done"] += done
            c["files"].append((os.path.join(rel, f) if rel != '.' else f, len(data), done))

    for cat, c in categories.items():
        print(f"  {cat:<40} {c['done']:>6} / {c['total']:<6} ({pct(c['done'], c['total']):5.1f} %)")
        if detail:
            for name, total, done in c["files"]:
                print(f"      - {os.path.basename(name):<50} {done:>5} / {total:<5}")

    print("=" * 72)
    print(f"Textes uniques : {len(unique_done)} traduits sur {len(unique_all)} "
          f"({pct(len(unique_done), len(unique_all)):.1f} %)")
    print("(une même phrase peut apparaître dans plusieurs fichiers : le total unique est le vrai chiffre)")
    print("=" * 72)

if __name__ == '__main__':
    main()
