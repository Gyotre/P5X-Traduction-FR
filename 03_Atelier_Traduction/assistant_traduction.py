#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assistant_traduction.py - Moteur de Traduction Assistée et Intelligent pour P5X
- Protection intégrale des balises Unity (<color>, <size>, <link>) et variables ($1, {{A}})
- Harmonisation automatique selon le Glossaire Officiel Persona 5 FR
- Détection et injection automatique de balises anti-chevauchement (<size=80%>)
- Traduction en 1-clic avec fallback local hors-ligne
"""

import re
import json
import urllib.request
import urllib.parse

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
    (r"\bdégâts? infligés?\b", "Dégâts infligés"),
    (r"\bdégâts? subis?\b", "Dégâts subis"),
    (r"\bdégâts? de faiblesse\b", "Dégâts de Faiblesse"),
    (r"\bdégâts? finaux\b", "Dégâts Finaux"),
    (r"\bpénétration\b", "Pénétration"),
    (r"\bvitesse\b", "Vitesse"),
    (r"\bprécision\b", "Précision"),
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

# Dictionnaire hors-ligne des termes et tournures fréquents
DICTIONNAIRE_LOCAL = {
    "Set Effect": "<size=85%>Effet d'Arcane</size>",
    "Revelation Card": "Carte de Révélation",
    "Basic": "Simple",
    "Cost:": "Coût:",
    "Mark:": "Symbole:",
    "Reset": "Réinitialiser",
    "Equip": "Équiper",
    "Unequip All": "Tout déséquiper",
    "Close": "Fermer",
    "Confirm": "Confirmer",
    "Cancel": "Annuler",
    "Level Up": "Améliorer",
    "Details": "Détails",
}


def masquer_balises(texte):
    """Remplace les balises Unity et variables par des jetons neutres [[T0]], [[T1]]..."""
    jetons = {}

    def _remplacer(m):
        cle = f"[[T{len(jetons)}]]"
        jetons[cle] = m.group(0)
        return cle

    # Balises Unity Rich Text, balises XML, variables $1 et {{A}}
    motif = (
        r"<size[^>]*>|<color[^>]*>|</color>|</size>|<link[^>]*>|</link>|"
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
        # Gestion des espaces parasites parfois ajoutés par les moteurs de traduction
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
    Applique la balise <size=80%> si le texte est un titre de set de cartes ou un titre long
    pour éviter tout chevauchement avec la description en jeu.
    """
    # Si déjà balisé avec <size>, on ne touche pas
    if "<size" in texte_francais:
        return texte_francais

    # Détection des combinaisons de cartes de révélation (ex: "Awareness & Hindrance" ou "Resolve & $1")
    if re.match(r"^[A-Za-zÀ-ÿ\-]+\s*&\s*([A-Za-zÀ-ÿ\-]+|\$\d+|\{\{[A-Za-z0-9_]+\}\})$", cle_anglaise.strip()):
        return f"<size=80%>{texte_francais}</size>"

    return texte_francais


def traduire_en_francais(texte_anglais):
    """
    Traduit un texte anglais en français :
    1. Vérification dans le dictionnaire rapide local
    2. Protection des balises Unity et variables
    3. Traduction via service distant
    4. Restauration des balises
    5. Application des règles officielles du Glossaire Persona 5
    6. Vérification anti-chevauchement d'interface
    """
    if not texte_anglais or not texte_anglais.strip():
        return ""

    texte_brut = texte_anglais.strip()

    # 1. Correspondance directe dans le dictionnaire local
    if texte_brut in DICTIONNAIRE_LOCAL:
        return DICTIONNAIRE_LOCAL[texte_brut]

    # 2. Protection des balises
    masque, jetons = masquer_balises(texte_brut)

    # 3. Traduction en ligne
    traduction = ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fr&dt=t&q=" + urllib.parse.quote(masque)
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            donnees = json.loads(reponse.read().decode("utf-8"))
            traduction = "".join([segment[0] for segment in donnees[0] if segment and segment[0]])
    except Exception:
        # Fallback hors-ligne si pas de connexion internet
        traduction = masque

    # 4. Restauration des balises
    texte_restaure = restaurer_balises(traduction, jetons)

    # 5. Harmonisation avec le Glossaire Officiel
    texte_final = appliquer_glossaire(texte_restaure)

    # 6. Protection anti-chevauchement
    texte_securise = verifier_anti_chevauchement(texte_brut, texte_final)

    return texte_securise.strip()
