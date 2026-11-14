#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_pack_release.py
Empaquette le patch français dans une archive ZIP prête à être distribuée :
BepInEx + XUnity préconfigurés, traductions compilées depuis TRADUCTION_FACILE
et AutoTranslatorConfig.ini réglé sur le français.
Le nom du héros et le mode Streameur du launcher ne sont PAS inclus (réglages personnels).
Usage: python generer_pack_release.py [version] [EN|JP|TW|KR|CN]
"""

import os
import sys
import zipfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convertisseur_json as conv

LISEZMOI = """PATCH FRANÇAIS - PERSONA 5: THE PHANTOM X (v{version})

INSTALLATION
1. Ouvre le dossier du jeu (celui qui contient P5X.exe, en général ...\\P5X\\client\\pc).
2. Copie TOUT le contenu du dossier "Fichiers_Jeu" dedans (accepte de remplacer).
3. Lance le jeu. Le premier démarrage avec BepInEx peut prendre plusieurs minutes.

DÉSINSTALLER / JOUER EN VERSION OFFICIELLE
Renomme winhttp.dll en winhttp.dll.disabled (et inversement pour réactiver).

AVERTISSEMENT
BepInEx injecte du code dans le jeu : le risque de sanction n'est jamais nul.
Ne dépense pas d'argent réel sur un compte moddé et désactive le patch avant une mise à jour.
"""

def make_release(version="1.0.0", region="EN"):
    base_dir = conv.BASE_DIR
    out_dir = os.path.join(base_dir, "06_Releases")
    os.makedirs(out_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    zip_name = f"P5X_Patch_FR_{region}_v{version}_{date_str}.zip"
    zip_path = os.path.join(out_dir, zip_name)

    pack_dir = os.path.join(base_dir, "05_Paquet_BepInEx_Preconfigure", "A_COPIER_DANS_LE_JEU")
    if not os.path.exists(pack_dir):
        print(f"[ERREUR] Pack BepInEx introuvable : {pack_dir}")
        sys.exit(1)

    modules, stats = conv.build_modules()
    print(f"Création de l'archive de distribution : {zip_name} ({stats['entries']} entrées)...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # 1. BepInEx + XUnity préconfigurés
        for root, _, files in os.walk(pack_dir):
            for f in files:
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, pack_dir)
                z.write(full_p, os.path.join("Fichiers_Jeu", rel_p))

        # 2. Traductions compilées
        text_dir = os.path.join("Fichiers_Jeu", "BepInEx", "Translation", "fr", "Text")
        for mod_name, lines in modules.items():
            if lines:
                z.writestr(os.path.join(text_dir, mod_name), "".join(lines))

        # 3. Configuration XUnity en français
        from_lang = conv.REGION_LANG_MAP.get(region, "en")
        z.writestr(os.path.join("Fichiers_Jeu", "BepInEx", "config", "AutoTranslatorConfig.ini"),
                   conv.DEFAULT_INI.format(from_lang=from_lang))

        z.writestr("LISEZMOI.txt", LISEZMOI.format(version=version))

    print(f"\n[SUCCÈS] Archive générée avec succès dans :")
    print(f"         {zip_path}")
    print(f"         Taille : {os.path.getsize(zip_path) / (1024*1024):.2f} Mo")

if __name__ == '__main__':
    ver = sys.argv[1] if len(sys.argv) > 1 else "1.0.0"
    reg = sys.argv[2].upper() if len(sys.argv) > 2 else "EN"
    make_release(ver, reg)
