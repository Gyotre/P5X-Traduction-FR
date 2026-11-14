#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapter_p5xtes_en_json.py
Adapte toutes les données et textes officiels Steam de P5XTES vers notre format JSON
dans TRADUCTION_FACILE sans écraser AUCUNE traduction française existante.
"""

import os
import re
import json
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
P5XTES_TEXT_DIR = os.path.join(BASE_DIR, 'P5XTES_Inspect', 'P5XTES-P5XTESv4', 'Translation', 'es', 'Text')
TRAD_FACILE_DIR = os.path.join(BASE_DIR, 'TRADUCTION_FACILE')

# 1. Sauvegarder toutes les traductions existantes dans TRADUCTION_FACILE
def collect_existing_fr():
    existing = {}
    for root, _, files in os.walk(TRAD_FACILE_DIR):
        for f in files:
            if f.endswith('.json'):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fp:
                        d = json.load(fp)
                        for k, v in d.items():
                            val = str(v).strip()
                            if val:
                                existing[k] = val
                except Exception as e:
                    print(f"Erreur lecture {p}: {e}")
    print(f"[PROTECTION] {len(existing)} traductions françaises existantes protégées.")
    return existing

# 2. Parseur de fichier texte P5XTES en conservant les sections
def parse_p5xtes_file(filepath):
    """
    Retourne une liste de tuples: (section_name, key, value_es)
    """
    items = []
    current_sec = "General"
    if not os.path.exists(filepath):
        return items
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith('//') or raw.startswith('#'):
                continue
            if raw.startswith('++') or raw.startswith('+--'):
                current_sec = raw.strip('+- \r\n')
                continue
            if '=' in raw:
                parts = re.split(r'(?<!\\)=', raw, maxsplit=1)
                if len(parts) == 2:
                    k = parts[0].strip()
                    v = parts[1].strip()
                    items.append((current_sec, k, v))
    return items

def save_json(filepath, data, existing_fr):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Si le fichier existe déjà, fusionner
    merged = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                merged = json.load(f)
        except Exception:
            merged = {}

    # Ajouter les nouvelles clés
    for k, default_val in data.items():
        if k in existing_fr:
            merged[k] = existing_fr[k]
        elif k in merged and merged[k].strip():
            # Garder ce qui a été traduit
            pass
        else:
            merged[k] = default_val

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

def main():
    # Sans les fichiers P5XTES, on créerait des JSON vides : on s'arrête
    if not os.path.isdir(P5XTES_TEXT_DIR):
        print(f"[ARRÊT] Dossier P5XTES introuvable : {P5XTES_TEXT_DIR}")
        print("Rien n'a été modifié.")
        raise SystemExit(1)

    existing_fr = collect_existing_fr()
    print("Début de l'adaptation P5XTES -> JSON...")

    # A. Kits de personnages et Consciences (Awareness)
    chars_dir = os.path.join(TRAD_FACILE_DIR, '01_Personnages')
    char_files = [f for f in os.listdir(chars_dir) if f.endswith('.json')]

    # Dictionnaire de correspondance nom de section -> fichier JSON
    def get_target_char_file(sec_name):
        clean_sec = re.sub(r'[^a-zA-Z0-9]', ' ', sec_name).lower().split()
        if 'miku' in clean_sec or 'hatsune' in clean_sec:
            return 'Miku_-_Hatsune_Miku.json'
        if 'makoto' in clean_sec and 'nijima' in clean_sec:
            return 'Queen_-_Makoto_Niijima.json'
        if 'makoto' in clean_sec and 'yuki' in clean_sec:
            return 'Makoto_Yuki.json'
        if 'joker' in clean_sec or 'ren' in clean_sec:
            return 'Joker_-_Ren_Amamiya.json'

        best_file = None
        best_score = 0
        for f in char_files:
            f_words = re.sub(r'[^a-zA-Z0-9]', ' ', f.replace('.json', '')).lower().split()
            score = sum(1 for w in clean_sec if w in f_words and len(w) > 2)
            if score > best_score:
                best_score = score
                best_file = f
        if best_score > 0:
            return best_file
        return '00_Kits_et_Consciences_General.json'

    # Traiter 01_UI Kit personaje.txt et Awareness.txt
    char_updates = {}
    for fn in ['01_UI Kit personaje.txt', 'Awareness.txt', 'Kit Personaje.txt']:
        p = os.path.join(P5XTES_TEXT_DIR, fn)
        items = parse_p5xtes_file(p)
        for sec, k, v in items:
            target_f = get_target_char_file(sec)
            if target_f not in char_updates:
                char_updates[target_f] = {}
            char_updates[target_f][k] = ""

    for target_f, keys in char_updates.items():
        fp = os.path.join(chars_dir, target_f)
        save_json(fp, keys, existing_fr)
    print(f"[OK] Kits et Consciences intégrés dans {len(char_updates)} fichiers personnages.")

    # B. Armes et Effets (UI Armas.txt)
    armas_path = os.path.join(P5XTES_TEXT_DIR, 'UI Armas.txt')
    armas_items = parse_p5xtes_file(armas_path)
    armas_dict = {k: "" for _, k, _ in armas_items}
    save_json(os.path.join(TRAD_FACILE_DIR, '08_Equipements_et_Objets', '01_Armes_et_Effets.json'), armas_dict, existing_fr)
    print(f"[OK] Armes Steam ({len(armas_dict)} entrées) intégrées dans 08_Equipements_et_Objets.")

    # C. Interface et Menus (UI.txt)
    ui_path = os.path.join(P5XTES_TEXT_DIR, 'UI.txt')
    ui_items = parse_p5xtes_file(ui_path)
    ui_dict = {k: "" for _, k, _ in ui_items}
    save_json(os.path.join(TRAD_FACILE_DIR, '09_Interface_et_Menus', '01_UI_Steam_Officiel.json'), ui_dict, existing_fr)
    print(f"[OK] UI Steam ({len(ui_dict)} entrées) intégrées dans 09_Interface_et_Menus.")

    # D. Substitutions et Noms de Personnages (_Substitutions.txt)
    sub_path = os.path.join(P5XTES_TEXT_DIR, '_Substitutions.txt')
    sub_items = parse_p5xtes_file(sub_path)
    sub_dict = {k: "" for _, k, _ in sub_items}
    save_json(os.path.join(TRAD_FACILE_DIR, '00_Configuration_et_Substitutions', '_Substitutions.json'), sub_dict, existing_fr)
    print(f"[OK] Substitutions ({len(sub_dict)} entrées) créées dans 00_Configuration_et_Substitutions.")

    # E. Événements et Collabs (Persona3, Plage, Anniversaire, Bui)
    events_dir = os.path.join(TRAD_FACILE_DIR, '05_Evenements_et_Collabs')
    event_files_map = {
        'Persona3.txt': '01_Persona3_Reload_Collab.json',
        'Arco Playita pt2.txt': '02_Evenement_Plage_Ete.json',
        'Evento 1er Aniversario.txt': '03_Evenement_1er_Anniversaire.json',
        'Evento Bui.txt': '04_Evenement_BUI.json',
        'Message Valentine pt1.txt': '05_Messages_Saint_Valentin.json'
    }
    for src_txt, dst_json in event_files_map.items():
        items = parse_p5xtes_file(os.path.join(P5XTES_TEXT_DIR, src_txt))
        d = {k: "" for _, k, _ in items}
        save_json(os.path.join(events_dir, dst_json), d, existing_fr)
        print(f"[OK] Événement {src_txt} ({len(d)} entrées) -> {dst_json}")

    # F. Donjons et Palais (Palacio 4)
    palaces_dir = os.path.join(TRAD_FACILE_DIR, '06_Donjons_Palais_et_Metavers')
    palace_files_map = {
        'Palacio 4.txt': '04_Palais_4_Histoire_Part1.json',
        'palacio4parte3.txt': '04_Palais_4_Histoire_Part2.json'
    }
    for src_txt, dst_json in palace_files_map.items():
        items = parse_p5xtes_file(os.path.join(P5XTES_TEXT_DIR, src_txt))
        d = {k: "" for _, k, _ in items}
        save_json(os.path.join(palaces_dir, dst_json), d, existing_fr)
        print(f"[OK] Palais {src_txt} ({len(d)} entrées) -> {dst_json}")

    # G. Textes Généraux Steam (General.txt découpé en morceaux gérables de 10 000 entrées)
    gen_path = os.path.join(P5XTES_TEXT_DIR, 'General.txt')
    gen_items = parse_p5xtes_file(gen_path)
    gen_dir = os.path.join(TRAD_FACILE_DIR, '11_Textes_Generaux_Steam')
    chunk_size = 10000
    total_gen = len(gen_items)
    for idx, i in enumerate(range(0, total_gen, chunk_size)):
        chunk = gen_items[i:i + chunk_size]
        chunk_dict = {k: "" for _, k, _ in chunk}
        part_name = f"General_Steam_Part{idx+1:02d}.json"
        save_json(os.path.join(gen_dir, part_name), chunk_dict, existing_fr)
        print(f"[OK] General Steam {part_name} ({len(chunk_dict)} entrées)")

    print("\n--- VÉRIFICATION FINALE DES TRADUCTIONS FR ---")
    verified_fr = collect_existing_fr()
    print(f"Total traductions actives après adaptation : {len(verified_fr)}")
    assert len(verified_fr) >= len(existing_fr), "ATTENTION: Perte de traductions détectée !"
    print("[SUCCÈS TOTAL] Toutes les traductions FR d'origine ont été conservées à 100% !")

if __name__ == '__main__':
    main()
