#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_dossiers_langues.py
Crée et structure les dossiers de traduction pour toutes les langues (EN, JP, TW, KR, CN).
"""

import os
import re

def convert_to_en_keys(src_file, dst_file):
    if not os.path.exists(src_file):
        return
    lines_out = []
    with open(src_file, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            raw = line.rstrip('\r\n')
            if not raw or raw.startswith('//') or raw.startswith('#') or raw.startswith(';') or raw.startswith('-') or raw.startswith('='):
                lines_out.append(raw)
                continue
            if re.search(r'(?<!\\)=', raw):
                parts = re.split(r'(?<!\\)=', raw, maxsplit=1)
                orig, eng = parts[0], parts[1]
                if eng.strip():
                    lines_out.append(f"{eng.strip()}={eng.strip()}")
            elif raw.startswith('r:"'):
                lines_out.append(raw)
            else:
                lines_out.append(raw)
    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines_out) + '\n')

def main():
    base_dst = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '01_Traduction_FR'))
    tw_dir = os.path.join(base_dst, 'TW')

    categories = ['01_Kits_Personnages', '02_Equipements_et_Objets', '03_Interface_et_Combat', '04_Configuration_XUnity']

    for lang in ['EN', 'JP']:
        for cat in categories:
            os.makedirs(os.path.join(base_dst, lang, cat), exist_ok=True)

    for cat in os.listdir(tw_dir):
        cat_src = os.path.join(tw_dir, cat)
        if not os.path.isdir(cat_src):
            continue
        cat_en = os.path.join(base_dst, 'EN', cat)
        cat_jp = os.path.join(base_dst, 'JP', cat)
        for fname in os.listdir(cat_src):
            if fname.endswith('.txt'):
                src_f = os.path.join(cat_src, fname)
                en_f = os.path.join(cat_en, fname)
                jp_f = os.path.join(cat_jp, fname)
                convert_to_en_keys(src_f, en_f)
                # Pour JP, on copie également les fichiers avec en-têtes
                convert_to_en_keys(src_f, jp_f)

    print("Dossiers EN et JP initialisés avec succès !")

if __name__ == '__main__':
    main()
