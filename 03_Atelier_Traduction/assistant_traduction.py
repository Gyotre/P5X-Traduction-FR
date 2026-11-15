#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assistant_traduction.py - Moteur de Traduction Assistée et Intelligent pour P5X
- Mémoire de traduction prioritaire : réutilise directement les traductions de l'utilisateur
  (notamment 02_Cartes_Revelation_et_Sets.json et les autres fichiers de TRADUCTION_FACILE)
- Intégration dynamique du Glossaire Officiel Persona 5 FR (01_Documentation/Glossaire_Officiel_P5_FR.md)
- Protection intégrale des balises Unity (<color>, <size>, <link>) et variables ($1, {{A}})
- Harmonisation automatique selon le vocabulaire canonique (PC, PV, ATQ, Bonus, Malus, etc.)
- Protection anti-chevauchement d'interface (<nobr><size=70%>...</size></nobr>)
"""

import os
import re
import json
import urllib.request
import urllib.parse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIR_EASY = os.path.join(BASE_DIR, 'TRADUCTION_FACILE')
GLOSSAIRE_FILE = os.path.join(BASE_DIR, '01_Documentation', 'Glossaire_Officiel_P5_FR.md')
PRIORITY_FILE = os.path.join(DIR_EASY, '08_Equipements_et_Objets', '02_Cartes_Revelation_et_Sets.json')

# Cache global en mémoire
_MEMOIRE_TRADUCTION = None
_GLOSSAIRE_TERMES = None

# Règles de post-traitement pour harmoniser avec le Glossaire Officiel P5X FR
GLOSSAIRE_POST_RULES = [
    # Cibles & Combats
    (r"\b(?:l'attaque de l'utilisateur|l'attaque du joueur|son attaque)\b", "l'Attaque du lanceur"),
    (r"\bl'utilisateur\b", "le lanceur"),
    (r"\bennemi(?:e)? principal(?:e)?\b", "Ennemi Principal"),
    (r"\battaque(?:s)? de suivi\b", "Attaque de Suivi"),
    (r"\bassaut(?:s)? général(?:aux)?\b", "Assaut Général"),
    (r"\btransfert(?:s)?\b", "Transfert"),
    (r"\bpassage(?:s)? de relais\b", "Transfert"),
    
    # Stats & Ressources
    (r"\bpoints? de vie\b", "PV"),
    (r"\bpoints? de concentration\b", "PC"),
    (r"\bpoints? de magie\b", "PC"),
    (r"\bpoints? de compétence\b", "PC"),
    (r"\bSP\b", "PC"),
    (r"\bHP\b", "PV"),
    (r"\bATK\b", "ATQ"),
    (r"\bSPD\b", "VIT"),
    (r"\bdégâts? critiques?\b", "Dégâts Crit."),
    (r"\btaux de critique\b", "Taux Crit."),
    (r"\btaux critique\b", "Taux Crit."),
    (r"\bdégâts? bonus\b", "Dégâts Bonus"),
    (r"\bdégâts? infligés?\b", "Dégâts infligés"),
    (r"\bdégâts? subis?\b", "Dégâts subis"),
    (r"\bdégâts? de faiblesse\b", "Dégâts de Faiblesse"),
    (r"\bdégâts? finaux\b", "Dégâts Finaux"),
    (r"\bpénétration\b", "Pénétration"),
    (r"\bvitesse\b", "Vitesse"),
    (r"\bprécision des altérations\b", "Préc. Altération"),
    (r"\btaux d'altération(?:s)?\b", "Préc. Altération"),
    (r"\besquive\b", "Esquive"),
    
    # Altérations, Buffs & Debuffs
    (r"\b(?:débuffs?|debuffs?|affaiblissements?)\b", "malus"),
    (r"\b(?:buffs?|améliorations?)\b", "bonus"),
    (r"\b(?:se cumule|s'accumule|empilable|cumulable) jusqu'à\b", "Cumulable jusqu'à"),
    (r"\b(?:fois|piles|cumuls)\b", "fois"),
    (r"\bune fois par combat\b", "Une fois par combat"),
    (r"\btou(?:rs)? de combat\b", "Tours de combat"),
    (r"\btemps de recharge\b", "Temps de recharge"),
    (r"\baction(?:s)? supplémentaire(?:s)?\b", "Action Supplémentaire"),
    (r"\baction(?:s)? normale(?:s)?\b", "Action normale"),
    
    # Équipements & Métavers
    (r"\bcartes? de révélation\b", "Cartes de Révélation"),
    (r"\beffets? d'arcane\b", "Effet d'Arcane"),
    (r"\bchambre de velours\b", "Chambre de Velours"),
    (r"\bmétavers\b", "Métavers"),
    (r"\bmémentos\b", "Mémentos"),
    (r"\bpalais\b", "Palais"),
    (r"\bvoleurs? fantômes?\b", "Voleurs Fantômes"),
]


def charger_memoire_traduction(forcer=False):
    """
    Charge l'ensemble des traductions déjà existantes dans TRADUCTION_FACILE.
    Donne la priorité absolue au fichier 02_Cartes_Revelation_et_Sets.json
    pour respecter fidèlement les traductions de l'utilisateur.
    """
    global _MEMOIRE_TRADUCTION
    if _MEMOIRE_TRADUCTION is not None and not forcer:
        return _MEMOIRE_TRADUCTION

    memoire = {}

    # 1. Charger tous les fichiers JSON de TRADUCTION_FACILE
    if os.path.exists(DIR_EASY):
        for root, _, files in os.walk(DIR_EASY):
            for f in sorted(files):
                if f.endswith('.json'):
                    p = os.path.join(root, f)
                    if p == PRIORITY_FILE:
                        continue
                    try:
                        with open(p, 'r', encoding='utf-8') as fp:
                            data = json.load(fp)
                            for k, v in data.items():
                                val = str(v).strip()
                                key_str = str(k).strip()
                                if val and key_str and key_str not in memoire:
                                    memoire[key_str] = val
                    except Exception:
                        pass

    # 2. Priorité absolue : 02_Cartes_Revelation_et_Sets.json (écrase tout le reste)
    if os.path.exists(PRIORITY_FILE):
        try:
            with open(PRIORITY_FILE, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                for k, v in data.items():
                    val = str(v).strip()
                    key_str = str(k).strip()
                    if val and key_str:
                        memoire[key_str] = val
        except Exception:
            pass

    _MEMOIRE_TRADUCTION = memoire
    return _MEMOIRE_TRADUCTION


def charger_glossaire_p5(forcer=False):
    """
    Parse dynamiquement le Glossaire Officiel Persona 5 Markdown
    pour en extraire les correspondances de termes officiels.
    """
    global _GLOSSAIRE_TERMES
    if _GLOSSAIRE_TERMES is not None and not forcer:
        return _GLOSSAIRE_TERMES

    termes = {}
    fichiers = [GLOSSAIRE_FILE, os.path.join(BASE_DIR, 'TRADUCTION_FR', 'Glossaire_Officiel_P5_FR.md')]
    fichier_trouve = next((f for f in fichiers if os.path.exists(f)), None)

    if fichier_trouve:
        try:
            with open(fichier_trouve, 'r', encoding='utf-8') as fp:
                for line in fp:
                    line = line.strip()
                    if line.startswith('| **') and line.endswith('|'):
                        cellules = [c.strip() for c in line.split('|')[1:-1]]
                        if len(cellules) >= 3:
                            en = re.sub(r'[*_`]', '', cellules[0]).strip()
                            fr = re.sub(r'[*_`]', '', cellules[2]).strip()
                            if not fr or fr == '-':
                                fr = re.sub(r'[*_`]', '', cellules[1]).strip()
                            fr_propre = re.sub(r'\(.*?\)', '', fr).strip()
                            if en and fr_propre and en.lower() != fr_propre.lower():
                                termes[en] = fr_propre
        except Exception:
            pass

    _GLOSSAIRE_TERMES = termes
    return _GLOSSAIRE_TERMES


def masquer_balises(texte):
    """Remplace les balises Unity et variables par des jetons neutres [[T0]], [[T1]]..."""
    jetons = {}

    def _remplacer(m):
        cle = f"[[T{len(jetons)}]]"
        jetons[cle] = m.group(0)
        return cle

    motif = (
        r"<size[^>]*>|<color[^>]*>|</color>|</size>|<link[^>]*>|</link>|<nobr>|</nobr>|"
        r"<b>|</b>|<i>|</i>|<u>|</u>|<alpha[^>]*>|"
        r"\\n|\n|"
        r"\$+\d+|\[\$\d+\]|\{\{[A-Za-z0-9_]+\}\}"
    )
    masque = re.sub(motif, _remplacer, texte)
    return masque, jetons


def restaurer_balises(texte, jetons):
    """Restaure les balises et variables d'origine à partir des jetons."""
    res = texte
    for cle, val in jetons.items():
        res = re.sub(re.escape(cle).replace(r"\[\[", r"\[\s*\[").replace(r"\]\]", r"\]\s*\]"), val, res)
        res = res.replace(cle, val)
    return res


def appliquer_glossaire(texte):
    """Harmonise le texte traduit avec les termes officiels de Persona 5."""
    res = texte
    for motif, remplacement in GLOSSAIRE_POST_RULES:
        res = re.sub(motif, remplacement, res, flags=re.IGNORECASE)
    return res


def verifier_anti_chevauchement(cle_anglaise, texte_francais):
    """
    Applique la balise <nobr><size=70%> si le texte est un titre de set de cartes
    pour garantir qu'il tienne sur une seule ligne sans retour à la ligne ni chevauchement.
    """
    cle_str = cle_anglaise.strip()
    # Détection des combinaisons de cartes de révélation (ex: "Creation & Reconciliation")
    if re.match(r"^[A-Za-zÀ-ÿ\-]+\s*&\s*([A-Za-zÀ-ÿ\-]+|\$\d+|\{\{[A-Za-z0-9_]+\}\})$", cle_str):
        if "<nobr>" not in texte_francais:
            return f"<nobr><size=70%>{texte_francais}</size></nobr>"
    return texte_francais


def traduire_en_francais(texte_anglais):
    """
    Traduit un texte anglais en français avec une chaîne de priorité stricte :
    1. Mémoire de Traduction (02_Cartes_Revelation_et_Sets.json et TRADUCTION_FACILE)
    2. Glossaire Officiel Persona 5 FR
    3. Traduction intelligente distante avec protection des balises et variables
    4. Restauration des balises et harmonisation selon le glossaire
    5. Sécurisation anti-chevauchement d'interface
    """
    if not texte_anglais or not str(texte_anglais).strip():
        return ""

    texte_brut = str(texte_anglais).strip()

    # 1. VÉRIFICATION DANS LA MÉMOIRE DE TRADUCTION (PRIORITÉ ABSOLUE AUX FICHIERS DE L'UTILISATEUR)
    memoire = charger_memoire_traduction()
    if texte_brut in memoire and memoire[texte_brut]:
        return memoire[texte_brut]

    # Vérification insensible à la casse dans la mémoire
    texte_lower = texte_brut.lower()
    for k, v in memoire.items():
        if k.lower() == texte_lower and v:
            return v

    # 2. VÉRIFICATION DANS LE GLOSSAIRE OFFICIEL P5 FR
    glossaire = charger_glossaire_p5()
    if texte_brut in glossaire:
        return glossaire[texte_brut]

    # 3. TRADUCTION EN LIGNE AVEC PROTECTION
    masque, jetons = masquer_balises(texte_brut)

    traduction = ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fr&dt=t&q=" + urllib.parse.quote(masque)
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            donnees = json.loads(reponse.read().decode("utf-8"))
            traduction = "".join([segment[0] for segment in donnees[0] if segment and segment[0]])
    except Exception:
        traduction = masque

    # 4. RESTAURATION DES BALISES ET VARIABLES
    texte_restaure = restaurer_balises(traduction, jetons)

    # 5. HARMONISATION AVEC LE GLOSSAIRE PERSONA 5
    texte_final = appliquer_glossaire(texte_restaure)

    # 6. PROTECTION ANTI-CHEVAUCHEMENT
    texte_securise = verifier_anti_chevauchement(texte_brut, texte_final)

    return texte_securise.strip()
