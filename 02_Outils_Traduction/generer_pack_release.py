#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_pack_release.py
Génère les archives de publication compatibles avec le P5XfrLauncher de Garloulou :
- translation.zip : Pack léger contenant BepInEx/Translation/fr/Text et BepInEx/config/AutoTranslatorConfig.ini
                   directement extrait par le launcher dans le dossier du jeu.
- Calcul automatique du hash SHA-256 requis pour la vérification d'intégrité du launcher.
Usage: python generer_pack_release.py [version] [region]
"""

import os
import sys
import zipfile
import hashlib
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convertisseur_json as conv

def compute_sha256(filepath):
    """Calcule le hash SHA-256 d'un fichier."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower()

def make_launcher_release(version="1.0.0", region="EN"):
    """
    Génère translation.zip avec l'arborescence exacte attendue par P5XfrLauncher :
    translation.zip
    └── BepInEx/
        ├── config/
        │   └── AutoTranslatorConfig.ini
        └── Translation/
            └── fr/
                └── Text/
                    ├── 00_Regex_Dynamiques.txt
                    ├── 01_Kits_Personnages.txt
                    ...
    """
    base_dir = conv.BASE_DIR
    out_dir = os.path.join(base_dir, "06_Releases")
    os.makedirs(out_dir, exist_ok=True)

    zip_name = "translation.zip"
    zip_path = os.path.join(out_dir, zip_name)

    modules, stats = conv.build_modules()
    print(f"\n[1/3] Compilation des modules ({stats['entries']} traductions)...")

    print(f"[2/3] Création du pack Launcher : {zip_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Fichiers de traduction texte
        text_dir = os.path.join("BepInEx", "Translation", "fr", "Text")
        for mod_name, lines in modules.items():
            if lines:
                z.writestr(os.path.join(text_dir, mod_name), "".join(lines))

        # Configuration XUnity
        from_lang = conv.REGION_LANG_MAP.get(region, "en")
        z.writestr(os.path.join("BepInEx", "config", "AutoTranslatorConfig.ini"),
                   conv.DEFAULT_INI.format(from_lang=from_lang))

    sha256 = compute_sha256(zip_path)
    file_size_kb = os.path.getsize(zip_path) / 1024

    print(f"[3/3] Empreinte de sécurité calculée.")
    print("\n" + "=" * 65)
    print("  SUCCÈS : PACK LAUNCHER PRÊT POUR GITHUB RELEASE")
    print("=" * 65)
    print(f"Fichier  : {zip_path}")
    print(f"Taille   : {file_size_kb:.1f} Ko")
    print(f"SHA-256  : {sha256}")
    print("\nÀ coller dans le corps de votre Release GitHub pour le launcher :")
    print("-" * 65)
    print(f"translation.zip: {sha256}")
    print("-" * 65)

    return zip_path, sha256

if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else "1.0.0"
    reg = sys.argv[2].upper() if len(sys.argv) > 2 else "EN"
    make_launcher_release(ver, reg)
