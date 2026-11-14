#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valider_traductions.py
Vérifie les traductions de TRADUCTION_FACILE avant de les envoyer dans le jeu :
- JSON lisible
- balises Unity Rich Text équilibrées (<color>, <size>, <b>, <i>, <u>, <link>)
- variables conservées ($1, $2... et {{A}}, {{B}}...)
- même clé traduite différemment dans plusieurs fichiers
Usage: python valider_traductions.py [--tout]   (--tout affiche tous les problèmes)
"""

import os
import re
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_EASY = os.path.join(BASE_DIR, 'TRADUCTION_FACILE')

TAGS = ['color', 'size', 'b', 'i', 'u', 'link']
RE_VARS = re.compile(r'\$\d+|\{\{[A-Z]\}\}')

def tag_balance(text, tag):
    open_count = len(re.findall(rf'<{tag}(?:\\?=[^>]*|\s[^>]*)?>', text, re.IGNORECASE))
    close_count = len(re.findall(rf'</{tag}>', text, re.IGNORECASE))
    return open_count, close_count

def check_entry(key, val):
    issues = []
    for tag in TAGS:
        # Certains textes originaux sont eux-mêmes déséquilibrés : on compare à l'original
        o_val, c_val = tag_balance(val, tag)
        o_key, c_key = tag_balance(key, tag)
        if o_val - c_val != o_key - c_key:
            issues.append(f"balise <{tag}> différente de l'original (ouvert: {o_val}, fermé: {c_val} ; "
                          f"original : {o_key}/{c_key})")

    # Pour une regex, les $1, $2... viennent des groupes capturés : pas de comparaison possible
    if key.startswith('r:') or key.startswith('sr:'):
        return issues

    missing = sorted(set(RE_VARS.findall(key)) - set(RE_VARS.findall(val)), key=lambda s: (len(s), s))
    extra = sorted(set(RE_VARS.findall(val)) - set(RE_VARS.findall(key)), key=lambda s: (len(s), s))
    if missing:
        issues.append(f"variable(s) manquante(s) : {' '.join(missing)}")
    if extra:
        issues.append(f"variable(s) inconnue(s) : {' '.join(extra)}")

    if '\n' in val and '\n' not in key:
        issues.append("vrai retour à la ligne dans la traduction (utilise \\n)")
    return issues

def main():
    show_all = '--tout' in sys.argv
    if not os.path.exists(DIR_EASY):
        print(f"Dossier introuvable : {DIR_EASY}")
        sys.exit(1)

    print("=" * 60)
    print("VÉRIFICATION DES TRADUCTIONS (TRADUCTION_FACILE)")
    print("=" * 60)

    total_files = 0
    total_issues = 0
    seen = {}       # clé -> (valeur, fichier)
    conflicts = []

    for root, dirs, files in os.walk(DIR_EASY):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith('.json'):
                continue
            total_files += 1
            path = os.path.join(root, f)
            rel = os.path.relpath(path, DIR_EASY)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
            except Exception as e:
                print(f"\n[ERREUR] {rel} : JSON illisible ({e})")
                total_issues += 1
                continue

            file_issues = []
            for k, v in data.items():
                val = str(v).strip()
                if not val:
                    continue
                key = k.strip()
                for msg in check_entry(key, val):
                    file_issues.append((key, msg))
                if key in seen and seen[key][0] != val:
                    conflicts.append((key, seen[key], (val, rel)))
                elif key not in seen:
                    seen[key] = (val, rel)

            if file_issues:
                print(f"\n[ATTENTION] {rel} ({len(file_issues)} problème(s)) :")
                for key, msg in (file_issues if show_all else file_issues[:10]):
                    print(f"  - {msg}\n      clé : {key[:80]}")
                if not show_all and len(file_issues) > 10:
                    print(f"  ... et {len(file_issues) - 10} autre(s) (--tout pour tout voir).")
                total_issues += len(file_issues)

    if conflicts:
        print(f"\n[CONFLITS] {len(conflicts)} clé(s) traduite(s) différemment selon le fichier "
              "(le compilateur garde la première) :")
        for key, (v1, f1), (v2, f2) in (conflicts if show_all else conflicts[:15]):
            print(f"  - '{key[:70]}'\n      {f1} : {v1[:60]}\n      {f2} : {v2[:60]}")
        if not show_all and len(conflicts) > 15:
            print(f"  ... et {len(conflicts) - 15} autre(s) (--tout pour tout voir).")

    print("\n" + "=" * 60)
    print(f"Terminé : {total_files} fichiers vérifiés. Problèmes : {total_issues}. Conflits : {len(conflicts)}")
    print("=" * 60)
    sys.exit(1 if total_issues else 0)

if __name__ == '__main__':
    main()
