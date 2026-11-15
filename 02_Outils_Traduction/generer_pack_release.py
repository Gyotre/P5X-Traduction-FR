#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_pack_release.py
Génère les archives de publication compatibles avec le P5XfrLauncher de Garloulou :
- translation.zip : Pack léger contenant BepInEx/Translation/fr/Text et BepInEx/config/AutoTranslatorConfig.ini
                   directement extrait par le launcher dans le dossier du jeu.
- Calcul automatique du hash SHA-256 requis pour la vérification d'intégrité du launcher.
- Génération de 06_Releases/RELEASE_NOTES.md à partir de 01_Documentation/CHANGELOG.md.
Usage: python generer_pack_release.py [version] [region]
"""

import os
import re
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

def extract_changelog(version, changelog_path):
    """Extrait la section correspondant à la version dans CHANGELOG.md."""
    if not os.path.exists(changelog_path):
        return ""
    v_clean = version.lstrip('v')
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Chercher la section ## [vX.Y.Z] ou ## [X.Y.Z]
    pattern = rf"##\s*\[v?{re.escape(v_clean)}\][^\n]*\n(.*?)(?=\n---\s*\n|\n##\s*\[|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def make_launcher_release(version="1.0.2.3", region="EN"):
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

    # Génération de RELEASE_NOTES.md
    v_tag = f"v{version.lstrip('v')}"
    changelog_file = os.path.join(base_dir, "01_Documentation", "CHANGELOG.md")
    notes_body = extract_changelog(version, changelog_file)
    if not notes_body:
        notes_body = f"Mise à jour de la traduction française pour Persona 5: The Phantom X ({v_tag})."

    release_notes_content = f"""## Traduction Française — Persona 5: The Phantom X ({v_tag})

Cette version est entièrement compatible avec **[P5XfrLauncher de Garloulou](https://github.com/Garloulou/P5XfrLauncher)**.

{notes_body}

---

### Empreinte de vérification (SHA-256)
translation.zip: {sha256}

---
*Mise à jour automatique par GitHub Actions pour P5XfrLauncher.*
"""

    notes_path = os.path.join(out_dir, "RELEASE_NOTES.md")
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(release_notes_content)

    print(f"[3/3] Empreinte de sécurité calculée et notes de release générées.")
    print("\n" + "=" * 65)
    print("  SUCCÈS : PACK LAUNCHER PRÊT POUR GITHUB RELEASE")
    print("=" * 65)
    print(f"Version  : {v_tag}")
    print(f"Fichier  : {zip_path}")
    print(f"Taille   : {file_size_kb:.1f} Ko")
    print(f"SHA-256  : {sha256}")
    print("\nÀ coller dans le corps de votre Release GitHub pour le launcher :")
    print("-" * 65)
    print(f"translation.zip: {sha256}")
    print("-" * 65)

    return zip_path, sha256

if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else "1.0.2.3"
    reg = sys.argv[2].upper() if len(sys.argv) > 2 else "EN"
    make_launcher_release(ver, reg)
