"""
Script d'extraction exhaustif de tous les textes de Persona 5: The Phantom X (P5X).
Organise l'ensemble du jeu en 10 catégories modulaires, limpides et précises dans TRADUCTION_FACILE.
Toutes les valeurs sont initialisées à vide ("") pour un départ propre à 100%.
"""

import os
import re
import sys
import json
import shutil
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TW_DIR = os.path.join(BASE_DIR, "02_References_Originales", "TW")
KR_DIR = os.path.join(BASE_DIR, "02_References_Originales", "KR")
EN_DIR = os.path.join(BASE_DIR, "ORIGINAL_ANGLAIS")
OUT_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    name = re.sub(r'\s+', '_', name).strip('_')
    return name

def clean_key(text):
    text = text.strip()
    if text.startswith('"') and text.endswith('"') and len(text) >= 2:
        text = text[1:-1]
    # Unescape escaped equals and quotes
    text = text.replace(r'\=', '=').replace(r'\"', '"')
    return text

def parse_txt_file(filepath):
    if not os.path.exists(filepath):
        return []
    
    entries = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('/*') or line.startswith('#'):
            continue
        if line.startswith('----------') or line.startswith('==========') or line.startswith('----------------'):
            continue
            
        m_reg = re.match(r'^(?:s?r:)?\"(?:.+)\"=\"(.+)\"$', line)
        if m_reg:
            val = clean_key(m_reg.group(1))
            if val and len(val) > 0:
                entries.append(val)
            continue
            
        if '=' in line:
            parts = re.split(r'(?<!\\)=', line, maxsplit=1)
            if len(parts) == 2:
                k = clean_key(parts[0])
                v = clean_key(parts[1])
                chosen = v if v else k
                if chosen and len(chosen) > 0 and chosen not in ['----------', '==========']:
                    entries.append(chosen)
                
    return entries

def parse_sections_from_file(filepath):
    if not os.path.exists(filepath):
        return {}
        
    sections = {}
    current_section = "GENERAL"
    sections[current_section] = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if (line.startswith('---') or line.startswith('===') or line.startswith('+++')) and i + 1 < n:
            next_line = lines[i+1].strip()
            if next_line and not next_line.startswith('-') and not next_line.startswith('=') and not next_line.startswith('+'):
                if i + 2 < n and (lines[i+2].strip().startswith('-') or lines[i+2].strip().startswith('=') or lines[i+2].strip().startswith('+')):
                    current_section = next_line
                    if current_section not in sections:
                        sections[current_section] = []
                    i += 3
                    continue
                else:
                    current_section = next_line
                    if current_section not in sections:
                        sections[current_section] = []
                    i += 2
                    continue
        
        # En-tête entre tirets / plus / crochets
        m_sec = re.search(r'[-+= ]{3,}([a-zA-Z0-9_\(\)\'/][a-zA-Z0-9_\(\)\s/\'\.]{2,})[-+= ]{3,}', line)
        if m_sec:
            current_section = m_sec.group(1).strip()
            if current_section not in sections:
                sections[current_section] = []
            i += 1
            continue

        if line.startswith('[') and line.endswith(']') and len(line) < 60:
            current_section = line[1:-1].strip()
            if current_section not in sections:
                sections[current_section] = []
            i += 1
            continue
            
        if line and not line.startswith('//') and not line.startswith('/*') and not line.startswith('#'):
            m_reg = re.match(r'^(?:s?r:)?\"(?:.+)\"=\"(.+)\"$', line)
            if m_reg:
                val = clean_key(m_reg.group(1))
                if val:
                    sections[current_section].append(val)
                i += 1
                continue
            if '=' in line:
                parts = re.split(r'(?<!\\)=', line, maxsplit=1)
                if len(parts) == 2:
                    k = clean_key(parts[0])
                    v = clean_key(parts[1])
                    chosen = v if v else k
                    if chosen:
                        sections[current_section].append(chosen)
                    
        i += 1
        
    return sections

def write_json(rel_category, filename, items_list):
    target_dir = os.path.join(OUT_DIR, rel_category)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, filename if filename.endswith('.json') else f"{filename}.json")
    
    unique_keys = []
    seen = set()
    for item in items_list:
        if not item or item in seen or item.startswith('---'):
            continue
        if item in ['Meta', 'OG P5', 'P5X', '']:
            continue
        seen.add(item)
        unique_keys.append(item)
        
    data = {k: "" for k in unique_keys}
    
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    return len(data)

def main():
    print("=== DÉBUT DE L'EXTRACTION GLOBALE ET EXHAUSTIVE DE P5X ===")

    # Sans les fichiers sources, on produirait des JSON vides : on s'arrête
    missing = [d for d in (EN_DIR, TW_DIR, KR_DIR) if not os.path.isdir(d)]
    if missing:
        print("[ARRÊT] Dossier(s) source introuvable(s) :")
        for d in missing:
            print(f"   - {d}")
        print("Rien n'a été modifié.")
        sys.exit(1)

    # Ce script repart de zéro (valeurs vides) : on sauvegarde l'existant au lieu de le supprimer
    if os.path.exists(OUT_DIR):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = os.path.join(BASE_DIR, f"BACKUP_TRADUCTION_FACILE_{stamp}")
        shutil.move(OUT_DIR, backup)
        print(f"[SAUVEGARDE] Ancien TRADUCTION_FACILE déplacé dans : {backup}")
        print("             (relance adapter_p5xtes_en_json.py ensuite pour récupérer les traductions)")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. PERSONNAGES
    cat_persos = "01_Personnages"
    menu_skills = parse_sections_from_file(os.path.join(EN_DIR, "01_Kits_Personnages", "ThievesSkillsInMenuV5.4.2.txt"))
    battle_skills = parse_sections_from_file(os.path.join(EN_DIR, "01_Kits_Personnages", "ThievesSkillsInBattleV5.4.2.txt"))
    
    all_char_sections = set(list(menu_skills.keys()) + list(battle_skills.keys()))
    general_char_keys = []
    
    for sec in sorted(all_char_sections):
        if sec in ["GENERAL", "Character-specific Skill Details", "UPGRADE MENU + Mindscape (MS)"]:
            general_char_keys.extend(menu_skills.get(sec, []))
            general_char_keys.extend(battle_skills.get(sec, []))
            continue
            
        combined = []
        if sec in menu_skills:
            combined.extend(menu_skills[sec])
        if sec in battle_skills:
            combined.extend(battle_skills[sec])
            
        fname = sanitize_filename(sec)
        write_json(cat_persos, fname, combined)
        
    write_json(cat_persos, "General_Personnages", general_char_keys)
    
    # 2. HISTOIRE
    cat_hist = "02_Histoire_Principale"
    dial_sections = parse_sections_from_file(os.path.join(TW_DIR, "Dialogue.txt"))
    
    hist_prologue, hist_ch1_2, hist_ch3, hist_ch4, hist_ch5, hist_ch6, hist_dreams = [], [], [], [], [], [], []
    for sec, lines in dial_sections.items():
        s_low = sec.lower()
        if any(w in s_low for w in ['prologue', 'first velvet', 'first metaverse', 'wonder awakening', 'awakening video', 'met shedim', 'met marthym', 'katayama jumped']):
            hist_prologue.extend(lines)
        elif any(w in s_low for w in ['chapter 1', 'chapter 2', 'motoha awakening', 'shun awakening']):
            hist_ch1_2.extend(lines)
        elif 'chapter 3' in s_low or 'akashi' in s_low or 'katayama bar' in s_low or 'katayama boss' in s_low:
            hist_ch3.extend(lines)
        elif 'chapter 4' in s_low or 'shimotsuna' in s_low or 'daichi' in s_low or 'rehearsal' in s_low or 'festival' in s_low:
            hist_ch4.extend(lines)
        elif 'chapter 5' in s_low or 'aran' in s_low or 'cetus' in s_low or 'studio visit' in s_low:
            hist_ch5.extend(lines)
        elif 'chapter 6' in s_low or 'kokoro' in s_low or 'execution studio' in s_low:
            hist_ch6.extend(lines)
        elif 'dreams' in s_low:
            hist_dreams.extend(lines)
            
    kiuchi_kr = parse_txt_file(os.path.join(KR_DIR, "story_Kiuchi.txt"))
    miyazawa_kr = parse_txt_file(os.path.join(KR_DIR, "story_Miyazawa.txt"))
    hist_ch1_2.extend(kiuchi_kr)
    hist_ch1_2.extend(miyazawa_kr)
    
    write_json(cat_hist, "01_Prologue_et_Eveil", hist_prologue)
    write_json(cat_hist, "02_Chapitre_1_et_2", hist_ch1_2)
    write_json(cat_hist, "03_Chapitre_3_Akashi_et_Katayama", hist_ch3)
    write_json(cat_hist, "04_Chapitre_4_Shimotsuna_et_Festival", hist_ch4)
    write_json(cat_hist, "05_Chapitre_5_Aran_et_Cetus", hist_ch5)
    write_json(cat_hist, "06_Chapitre_6_KOKORO_et_Examens", hist_ch6)
    write_json(cat_hist, "07_Chapitre_des_Songes", hist_dreams)
    
    # 3. VIE QUOTIDIENNE
    cat_daily = "03_Vie_Quotidienne_et_Quetes"
    wonder_choices, short_phrases, school_life, city_explore, leblanc_talks, side_quests, sns_chats = [], [], [], [], [], [], []
    for sec, lines in dial_sections.items():
        s_low = sec.lower()
        if 'wonder prompt' in s_low:
            wonder_choices.extend(lines)
        elif 'short phrases' in s_low:
            short_phrases.extend(lines)
        elif any(w in s_low for w in ['classroom', 'school', 'exam', 'teacher']):
            school_life.extend(lines)
        elif any(w in s_low for w in ['station', 'train', 'walking', 'city activities']):
            city_explore.extend(lines)
        elif 'leblanc' in s_low or 'thieves' in s_low and 'talk' in s_low:
            leblanc_talks.extend(lines)
        elif 'side quest' in s_low:
            side_quests.extend(lines)
            
    side_quests.extend(parse_txt_file(os.path.join(KR_DIR, "side_quests.txt")))
    city_explore.extend(parse_txt_file(os.path.join(KR_DIR, "cityfreetimetasks.txt")))
    city_explore.extend(parse_txt_file(os.path.join(KR_DIR, "npcs_objects_interactables.txt")))
    sns_chats.extend(parse_txt_file(os.path.join(KR_DIR, "snsmessages.txt")))
    
    write_json(cat_daily, "01_Choix_et_Reponses_de_Wonder", wonder_choices)
    write_json(cat_daily, "02_Phrases_Courtes_et_Interactions", short_phrases)
    write_json(cat_daily, "03_Ecole_Cours_et_Examens", school_life)
    write_json(cat_daily, "04_Transports_Gares_et_Rues", city_explore)
    write_json(cat_daily, "05_Cafe_Leblanc_et_Discussions", leblanc_talks)
    write_json(cat_daily, "06_Quetes_Secondaires_Citadines", side_quests)
    write_json(cat_daily, "07_Messages_SNS_et_Chat_Mobile", sns_chats)
    
    # 4. SOCIAL LINKS ET SYNERGIES
    cat_sl = "04_Social_Links_et_Synergies"
    synergy_base = parse_txt_file(os.path.join(TW_DIR, "SynergySympathizer.txt"))
    write_json(cat_sl, "01_Systeme_Synergies_Rangs_et_Aptitudes", synergy_base)
    
    for sec, lines in dial_sections.items():
        if sec.endswith(" SL") or "Synergy" in sec:
            name = sec.replace(" SL", "").strip()
            fname = f"SL_{sanitize_filename(name)}"
            write_json(f"{cat_sl}/Confidents", fname, lines)
            
    kr_confidants = parse_txt_file(os.path.join(KR_DIR, "confidants.txt"))
    write_json(cat_sl, "02_Rendez_Vous_et_Sorties", kr_confidants)
    
    # 5. ÉVÉNEMENTS ET COLLABS
    cat_events = "05_Evenements_et_Collabs"
    p3r_collab, p5r_collab, p3p_collab, seasonal_events, valentine_event = [], [], [], [], []
    for sec, lines in dial_sections.items():
        s_low = sec.lower()
        if 'p3r' in s_low:
            p3r_collab.extend(lines)
        elif 'p5 collab' in s_low or 'p5r' in s_low:
            p5r_collab.extend(lines)
        elif 'p3p' in s_low:
            p3p_collab.extend(lines)
        elif any(w in s_low for w in ['summer', 'sports festival', 'end of year']):
            seasonal_events.extend(lines)
        elif 'valentine' in s_low:
            valentine_event.extend(lines)
            
    p3r_collab.extend(parse_txt_file(os.path.join(KR_DIR, "P3Rcollab.txt")))
    seasonal_events.extend(parse_txt_file(os.path.join(KR_DIR, "events.txt")))
    guild_tycoon = parse_txt_file(os.path.join(TW_DIR, "GuildTycoon.txt"))
    
    write_json(cat_events, "01_Collab_Persona_3_Reload_P3R", p3r_collab)
    write_json(cat_events, "02_Collab_Persona_5_Royal_P5R", p5r_collab)
    write_json(cat_events, "03_Collab_Persona_3_Portable_P3P", p3p_collab)
    write_json(cat_events, "04_Evenements_Saisonniers_Ete_Sport_Fin_Annee", seasonal_events)
    write_json(cat_events, "05_Evenement_Saint_Valentin", valentine_event)
    write_json(cat_events, "06_Mini_Jeux_Send_Em_Flying_et_Guild_Tycoon", guild_tycoon)
    
    # 6. DONJONS ET MÉTAVERS
    cat_dungeons = "06_Donjons_Palais_et_Metavers"
    palaces_sections = parse_sections_from_file(os.path.join(TW_DIR, "PalacesMementosSoSBosses.txt"))
    palace_explore, palace_bosses, mementos_lines = [], [], []
    for sec, lines in palaces_sections.items():
        s_low = sec.lower()
        if 'boss' in s_low or 'elite' in s_low:
            palace_bosses.extend(lines)
        elif 'mementos' in s_low or 'sea of souls' in s_low:
            mementos_lines.extend(lines)
        else:
            palace_explore.extend(lines)
            
    tartarus_tw = parse_txt_file(os.path.join(TW_DIR, "TartarusV8.txt"))
    tartarus_kr = parse_txt_file(os.path.join(KR_DIR, "Tartarus.txt"))
    tartarus_buffs_kr = parse_txt_file(os.path.join(KR_DIR, "Tartarus Arcana buffs.txt"))
    heart_rail = parse_txt_file(os.path.join(TW_DIR, "HeartRailV3.txt"))
    astrolabe = parse_txt_file(os.path.join(TW_DIR, "AstrolabeTrials.txt"))
    my_palace = parse_txt_file(os.path.join(TW_DIR, "MyPalace.txt"))
    wonder_world = parse_txt_file(os.path.join(TW_DIR, "WonderWorld.txt"))
    desire_gallery = parse_txt_file(os.path.join(TW_DIR, "DesireGallery.txt"))
    
    write_json(cat_dungeons, "01_Palais_1_a_7_Exploration_et_Puzzles", palace_explore)
    write_json(cat_dungeons, "02_Boss_de_Palais_et_Ombres_Elites", palace_bosses)
    write_json(cat_dungeons, "03_Tour_du_Tartare", tartarus_tw + tartarus_kr + tartarus_buffs_kr)
    write_json(cat_dungeons, "04_Mementos_et_Ombres_Deviantes", mementos_lines)
    write_json(cat_dungeons, "05_Essais_Velvet_Room_et_Astrolabe", astrolabe)
    write_json(cat_dungeons, "06_Train_Heart_Rail", heart_rail)
    write_json(cat_dungeons, "07_My_Palace_et_Wonder_World", my_palace + wonder_world + desire_gallery)
    
    # 7. PERSONAS ET COMPÉTENCES
    cat_skills = "07_Personas_et_Competences"
    traits = parse_txt_file(os.path.join(EN_DIR, "01_Kits_Personnages", "PersonaTraits.txt"))
    menu_gen = parse_txt_file(os.path.join(EN_DIR, "01_Kits_Personnages", "SkillsInMenu.txt"))
    battle_gen = parse_txt_file(os.path.join(EN_DIR, "01_Kits_Personnages", "SkillsInBattle.txt"))
    
    write_json(cat_skills, "01_Traits_de_Personas", traits)
    write_json(cat_skills, "02_Competences_Generales_Menu", menu_gen)
    write_json(cat_skills, "03_Competences_Generales_Combat", battle_gen)
    
    # 8. ÉQUIPEMENTS ET OBJETS
    cat_equip = "08_Equipements_et_Objets"
    weapons = parse_txt_file(os.path.join(EN_DIR, "02_Equipements_et_Objets", "Weapons.txt"))
    revelations = parse_txt_file(os.path.join(EN_DIR, "02_Equipements_et_Objets", "RevelationCards.txt"))
    craft_shop = parse_txt_file(os.path.join(EN_DIR, "02_Equipements_et_Objets", "CraftingCookingShopItems.txt"))
    kr_items = parse_txt_file(os.path.join(KR_DIR, "items.txt"))
    
    write_json(cat_equip, "01_Armes_et_Effets", weapons)
    write_json(cat_equip, "02_Cartes_Revelation_et_Sets", revelations)
    write_json(cat_equip, "03_Artisanat_Outils_et_Cuisine", craft_shop)
    write_json(cat_equip, "04_Boutiques_et_Consommables", kr_items)
    
    # 9. INTERFACE ET MENUS
    cat_ui = "09_Interface_et_Menus"
    manual_sections = parse_sections_from_file(os.path.join(EN_DIR, "03_Interface_et_Combat", "ManualTranslations.txt"))
    ui_menus_profile, ui_map, ui_gacha, ui_pass, ui_achievements, ui_other = [], [], [], [], [], []
    
    for sec, lines in manual_sections.items():
        s_low = sec.lower()
        if any(w in s_low for w in ['menu / ui', 'profile', 'character screen', 'class/ stats']):
            ui_menus_profile.extend(lines)
        elif 'map' in s_low or 'area names' in s_low or 'city ui' in s_low:
            ui_map.extend(lines)
        elif any(w in s_low for w in ['contract', 'gacha', 'gachapon', 'crane']):
            ui_gacha.extend(lines)
        elif any(w in s_low for w in ['handbook', 'battle pass', 'tasks']):
            ui_pass.extend(lines)
        elif 'achievements' in s_low or 'cosmetics' in s_low:
            ui_achievements.extend(lines)
        elif any(w in s_low for w in ['music club', 'soccer club', 'chihaya', 'kotone sl', 'synergy']):
            write_json("04_Social_Links_et_Synergies", f"Activite_{sanitize_filename(sec)}", lines)
        elif any(w in s_low for w in ['velvet trials', 'mementos']):
            write_json("06_Donjons_Palais_et_Metavers", f"Epreuve_{sanitize_filename(sec)}", lines)
        elif 'velvet room personas' in s_low:
            write_json("07_Personas_et_Competences", "04_Chambre_de_Velours_et_Fusions", lines)
        elif any(w in s_low for w in ['shop items', 'resources']):
            write_json("08_Equipements_et_Objets", "05_Objets_Cles_et_Monnaies", lines)
        elif any(w in s_low for w in ['worldbuilding', 'combat']):
            write_json("10_Combat", "02_Mots_Cles_et_Termes_Combat", lines)
        else:
            ui_other.extend(lines)
            
    kr_ui_sections = parse_sections_from_file(os.path.join(KR_DIR, "ui.txt"))
    ui_system = []
    for sec, lines in kr_ui_sections.items():
        s_low = sec.lower()
        if any(w in s_low for w in ['video', 'audio', 'gameplay', 'keybind', 'settings']):
            ui_system.extend(lines)
        else:
            ui_other.extend(lines)
            
    write_json(cat_ui, "01_Systeme_Options_Audio_Video", ui_system)
    write_json(cat_ui, "02_Menus_Principaux_et_Profil", ui_menus_profile)
    write_json(cat_ui, "03_Carte_de_Tokyo_et_Navigation", ui_map)
    write_json(cat_ui, "04_Gacha_Contrats_et_Tirages", ui_gacha)
    write_json(cat_ui, "05_Missions_Pass_de_Combat_et_Trophees", ui_pass)
    write_json(cat_ui, "06_Succes_Titres_et_Tenues", ui_achievements)
    write_json(cat_ui, "07_Autres_Textes_Interface", ui_other)
    
    # 10. COMBAT
    cat_combat = "10_Combat"
    kr_battle = parse_txt_file(os.path.join(KR_DIR, "battle.txt"))
    subs = parse_txt_file(os.path.join(EN_DIR, "04_Configuration_XUnity", "_Substitutions.txt"))
    
    write_json(cat_combat, "01_Interface_Combat_et_Popups", kr_battle)
    write_json(cat_combat, "03_Substitutions_Noms_et_Termes", subs)
    
    print("=== EXTRACTION TERMINÉE AVEC SUCCÈS ! ===")

if __name__ == "__main__":
    main()
