#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
traducteur_p5x.py - Atelier de traduction P5X
Texte anglais en haut, case française en dessous, bouton INJECTER pour envoyer dans le jeu.

- Sections : Personnages, Arcanes & Cartes, Armes, Personas, Interface, Combat, Histoire...
- Recherche dans tout le projet, filtre « non traduits »
- Une traduction est recopiée dans tous les fichiers qui contiennent la même phrase
  (le compilateur ne garde qu'une version par phrase : sans ça, une traduction pourrait être ignorée)
- Vérification des balises et variables avant l'injection
"""

import os
import re
import sys
import json
import io
import importlib
import contextlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EASY_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")
TOOLS_DIR = os.path.join(BASE_DIR, "02_Outils_Traduction")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "launcher_config.json")
GLOSSAIRE = os.path.join(BASE_DIR, "01_Documentation", "Glossaire_Officiel_P5_FR.md")

sys.path.insert(0, os.path.dirname(__file__))
try:
    import assistant_traduction as assistant
except Exception:
    assistant = None

PAGE_SIZE = 40

# Couleurs Persona 5
BG_DARK = "#141414"
BG_CARD = "#1F1F1F"
BG_INPUT = "#2B2B2B"
P5_RED = "#D80027"
P5_RED_HOVER = "#FF1F3D"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#AAAAAA"
TEXT_EN = "#66CCFF"
ACCENT_GREEN = "#00D26A"
ACCENT_GOLD = "#FFC000"
ACCENT_PURPLE = "#B07CFF"

# (titre affiché, test sur le chemin relatif du fichier)
SECTIONS = [
    ("Personnages", lambda p: p.startswith("01_Personnages/")),
    ("Arcanes & Cartes de Révélation", lambda p: p.endswith("02_Cartes_Revelation_et_Sets.json")),
    ("Armes", lambda p: p.endswith("01_Armes_et_Effets.json")),
    ("Objets, Boutiques & Artisanat", lambda p: p.startswith("08_Equipements_et_Objets/")),
    ("Personas & Compétences", lambda p: p.startswith("07_Personas_et_Competences/")),
    ("Interface & Menus", lambda p: p.startswith("09_Interface_et_Menus/")),
    ("Combat", lambda p: p.startswith("10_Combat/") and "Substitutions" not in p),
    ("Histoire principale", lambda p: p.startswith("02_Histoire_Principale/")),
    ("Vie quotidienne & Quêtes", lambda p: p.startswith("03_Vie_Quotidienne_et_Quetes/")),
    ("Social Links & Synergies", lambda p: p.startswith("04_Social_Links_et_Synergies/")),
    ("Événements & Collabs", lambda p: p.startswith("05_Evenements_et_Collabs/")),
    ("Donjons, Palais & Métavers", lambda p: p.startswith("06_Donjons_Palais_et_Metavers/")),
    ("Textes généraux (Steam)", lambda p: p.startswith("11_Textes_Generaux_Steam/")),
    ("Noms propres (substitutions)", lambda p: "Substitutions" in p),
]


# ---------------------------------------------------------------- logique (sans interface)

def is_regex(key):
    return key.startswith("r:") or key.startswith("sr:")


def readable_regex(key):
    """Transforme une clé regex en texte lisible : (.*) -> [$1], .* -> …"""
    body = key[2:] if key.startswith("r:") else key[3:]
    body = body.strip('"')
    body = re.sub(r"^\(\?s\)", "", body)
    body = body.lstrip("^").rstrip("$")
    n = [0]

    def group(_m):
        n[0] += 1
        return f"[${n[0]}]"

    body = re.sub(r"\((?!\?)(?:[^()\\]|\\.)*\)", group, body)   # groupes capturants
    body = re.sub(r"\(\?:[^()]*\)\??", "…", body)                 # groupes non capturants
    body = body.replace(".*?", "…").replace(".+?", "…").replace(".*", "…")
    body = re.sub(r"\\(.)", r"\1", body)
    body = re.sub(r"…+", "…", body)
    return body, n[0]


def to_display(s):
    """Texte stocké -> texte affiché (vrais retours à la ligne, = sans antislash)."""
    return s.replace("\\n", "\n").replace("\\=", "=")


def from_display(s):
    """Texte saisi -> texte stocké (le compilateur échappe lui-même les =)."""
    return s.strip().replace("\r\n", "\n").replace("\n", "\\n")


def nice_file_name(rel):
    name = os.path.splitext(os.path.basename(rel))[0]
    name = re.sub(r"^\d+_", "", name)
    return name.replace("_-_", " — ").replace("_", " ")


class Projet:
    """Toutes les traductions de TRADUCTION_FACILE en mémoire, avec suivi des modifications."""

    def __init__(self, easy_dir=EASY_DIR):
        self.easy_dir = easy_dir
        self.files = {}      # chemin relatif -> dict (ordre conservé)
        self.index = {}      # clé -> [chemins relatifs]
        self.dirty = set()   # fichiers modifiés non enregistrés
        self.errors = []
        self.load()

    def load(self):
        self.files.clear()
        self.index.clear()
        self.dirty.clear()
        for root, dirs, files in os.walk(self.easy_dir):
            dirs.sort()
            for f in sorted(files):
                if not f.endswith(".json"):
                    continue
                path = os.path.join(root, f)
                rel = os.path.relpath(path, self.easy_dir).replace("\\", "/")
                try:
                    with open(path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                except Exception as e:
                    self.errors.append(f"{rel} : {e}")
                    continue
                self.files[rel] = data
                for k in data:
                    self.index.setdefault(k, []).append(rel)

    def sections(self):
        """[(titre, [fichiers])] ; un fichier n'apparaît que dans la première section qui le revendique."""
        taken, out = set(), []
        for title, test in SECTIONS:
            fl = [r for r in self.files if r not in taken and test(r)]
            taken.update(fl)
            if fl:
                out.append((title, fl))
        rest = [r for r in self.files if r not in taken]
        if rest:
            out.append(("Autres", rest))
        return out

    def progress(self, rels):
        total = done = 0
        for r in rels:
            d = self.files[r]
            total += len(d)
            done += sum(1 for v in d.values() if str(v).strip())
        return done, total

    def set_value(self, rel, key, value, propagate=True):
        """Modifie une traduction. Recopie la nouvelle valeur dans les autres fichiers ayant la même phrase
        (si leur traduction est vide ou identique à l'ancienne). Renvoie le nombre de fichiers touchés."""
        old = str(self.files[rel].get(key, ""))
        if value == old:
            return 0
        self.files[rel][key] = value
        self.dirty.add(rel)
        touched = 1
        if propagate:
            for other in self.index.get(key, []):
                if other == rel:
                    continue
                ov = str(self.files[other].get(key, ""))
                if not ov.strip() or ov == old:
                    if ov != value:
                        self.files[other][key] = value
                        self.dirty.add(other)
                        touched += 1
        return touched

    def save(self):
        saved = []
        for rel in sorted(self.dirty):
            path = os.path.join(self.easy_dir, rel)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fp:
                json.dump(self.files[rel], fp, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
            saved.append(rel)
        self.dirty.clear()
        return saved

    def search(self, query, limit=2000):
        q = query.lower().strip()
        out = []
        if not q:
            return out
        for rel, data in self.files.items():
            for k, v in data.items():
                if q in k.lower() or q in str(v).lower():
                    out.append((rel, k))
                    if len(out) >= limit:
                        return out
        return out

    def conflicts(self, rel, key):
        """Autres traductions différentes de la même phrase ailleurs."""
        mine = str(self.files[rel].get(key, ""))
        res = []
        for other in self.index.get(key, []):
            if other != rel:
                ov = str(self.files[other].get(key, ""))
                if ov.strip() and ov != mine:
                    res.append((other, ov))
        return res


def check_value(key, value):
    """Contrôles avant injection (balises, variables)."""
    sys.path.insert(0, TOOLS_DIR)
    try:
        import valider_traductions as vt
    finally:
        sys.path.pop(0)
    if is_regex(key):
        # pour une regex : les $n utilisés doivent exister
        _, ngroups = readable_regex(key)
        used = {int(n) for n in re.findall(r"\$(\d+)", value)}
        bad = sorted(n for n in used if n > ngroups)
        return [f"variable ${n} inexistante (le texte en a {ngroups})" for n in bad]
    return vt.check_entry(key, value)


# ---------------------------------------------------------------- interface

class Atelier(tk.Tk):
    def __init__(self, projet=None):
        super().__init__()
        self.title("P5X — Atelier de traduction")
        self.geometry("1280x800")
        self.minsize(980, 600)
        self.configure(bg=BG_DARK)

        self.projet = projet or Projet()
        self.items = []          # [(rel, key)] de la vue courante
        self.page = 0
        self.widgets = {}        # (rel, key) -> Text
        self.view_title = ""
        self.view_rels = []
        self.changed_keys = set()   # (rel, key) modifiés depuis la dernière injection

        self._style()
        self._build()
        self._fill_tree()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind_all("<Control-s>", lambda e: self.save())
        self.bind_all("<Control-f>", lambda e: self.search_entry.focus_set())

        if self.projet.errors:
            messagebox.showwarning("Fichiers illisibles", "\n".join(self.projet.errors[:10]))
        first = next((r for r in self.projet.files if "Miku" in r), next(iter(self.projet.files), None))
        if first:
            self.show_files([first], nice_file_name(first))

    # ---------- construction
    def _style(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD, foreground=TEXT_WHITE,
                     rowheight=24, font=("Segoe UI", 10), borderwidth=0)
        st.configure("Treeview.Heading", background=BG_DARK, foreground=TEXT_MUTED)
        st.map("Treeview", background=[("selected", P5_RED)])
        st.configure("Vertical.TScrollbar", background=BG_CARD, troughcolor=BG_DARK)
        st.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_INPUT, foreground=TEXT_WHITE)

    def _build(self):
        header = tk.Frame(self, bg=P5_RED, height=54)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="P5X — ATELIER DE TRADUCTION", font=("Segoe UI Black", 16, "italic"),
                 fg=TEXT_WHITE, bg=P5_RED).pack(side="left", padx=18)
        self.lbl_global = tk.Label(header, text="", font=("Segoe UI", 10, "bold"), fg=TEXT_WHITE, bg=P5_RED)
        self.lbl_global.pack(side="right", padx=18)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # --- gauche : sections
        left = tk.Frame(body, bg=BG_DARK, width=310)
        left.pack(side="left", fill="y", padx=(10, 0), pady=10)
        left.pack_propagate(False)
        tk.Label(left, text="SECTIONS", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_DARK).pack(anchor="w")
        self.tree = ttk.Treeview(left, show="tree", selectmode="browse")
        sb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree_map = {}

        # --- droite
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        bar = tk.Frame(right, bg=BG_CARD, padx=10, pady=8)
        bar.pack(fill="x")
        tk.Label(bar, text="🔍", fg=TEXT_MUTED, bg=BG_CARD, font=("Segoe UI", 11)).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(bar, textvariable=self.search_var, font=("Segoe UI", 10), width=34,
                                     bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat")
        self.search_entry.pack(side="left", ipady=3, padx=(4, 6))
        self.search_entry.bind("<Return>", lambda e: self.do_search())
        self._button(bar, "Chercher partout", self.do_search, "#444444").pack(side="left")

        tk.Label(bar, text="Afficher :", fg=TEXT_MUTED, bg=BG_CARD, font=("Segoe UI", 9)).pack(side="left", padx=(16, 4))
        self.filter_var = tk.StringVar(value="Tous")
        cb = ttk.Combobox(bar, textvariable=self.filter_var, state="readonly", width=20,
                          values=["Tous", "Non traduits", "Traduits", "Textes à variables"])
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda e: self.refilter())

        self.propagate_var = tk.BooleanVar(value=True)
        tk.Checkbutton(bar, text="Recopier dans les fichiers identiques", variable=self.propagate_var,
                       fg=TEXT_MUTED, bg=BG_CARD, selectcolor=BG_INPUT, activebackground=BG_CARD,
                       activeforeground=TEXT_WHITE, font=("Segoe UI", 9)).pack(side="left", padx=12)
        self._button(bar, "Glossaire", self.open_glossary, "#444444").pack(side="right")

        info = tk.Frame(right, bg=BG_DARK)
        info.pack(fill="x", pady=(8, 4))
        self.lbl_view = tk.Label(info, text="", font=("Segoe UI", 13, "bold"), fg=TEXT_WHITE, bg=BG_DARK)
        self.lbl_view.pack(side="left")
        self.lbl_progress = tk.Label(info, text="", font=("Segoe UI", 10), fg=ACCENT_GOLD, bg=BG_DARK)
        self.lbl_progress.pack(side="left", padx=12)
        nav = tk.Frame(info, bg=BG_DARK)
        nav.pack(side="right")
        self._button(nav, "🪄 Auto-Traduire la page", self.auto_translate_page, "#5E239D").pack(side="left", padx=8)
        self._button(nav, "◀", lambda: self.goto(self.page - 1), "#383838").pack(side="left")
        self.lbl_page = tk.Label(nav, text="", fg=TEXT_MUTED, bg=BG_DARK, font=("Segoe UI", 9), width=16)
        self.lbl_page.pack(side="left")
        self._button(nav, "▶", lambda: self.goto(self.page + 1), "#383838").pack(side="left")

        # zone défilante
        holder = tk.Frame(right, bg=BG_DARK)
        holder.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(holder, bg=BG_DARK, highlightthickness=0)
        vsb = ttk.Scrollbar(holder, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG_DARK)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", self._wheel)

        # barre du bas
        bottom = tk.Frame(self, bg=BG_CARD, padx=12, pady=8)
        bottom.pack(fill="x", side="bottom")
        self.lbl_status = tk.Label(bottom, text="Prêt.", fg=TEXT_MUTED, bg=BG_CARD, font=("Segoe UI", 9), anchor="w")
        self.lbl_status.pack(side="left", fill="x", expand=True)
        self._button(bottom, "💾 ENREGISTRER (Ctrl+S)", self.save, "#2B5B84").pack(side="right", padx=(8, 0))
        self.btn_inject = self._button(bottom, "⚡ INJECTER DANS LE JEU", self.inject, P5_RED, big=True)
        self.btn_inject.pack(side="right")

    def _button(self, parent, text, cmd, bg, big=False):
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=TEXT_WHITE, relief="flat", cursor="hand2",
                         activebackground=P5_RED_HOVER if bg == P5_RED else "#555555", activeforeground=TEXT_WHITE,
                         font=("Segoe UI", 11 if big else 9, "bold"), padx=14 if big else 8, pady=5 if big else 2)

    def _wheel(self, event):
        w = self.winfo_containing(event.x_root, event.y_root)
        while w is not None and w is not self.canvas and w is not self.tree:
            w = w.master
        if w is self.canvas:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------- arbre
    def _fill_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree_map.clear()
        for title, rels in self.projet.sections():
            done, total = self.projet.progress(rels)
            sid = self.tree.insert("", "end", text=f"{title}  ({done}/{total})", open=False)
            self.tree_map[sid] = (rels, title)
            for r in rels:
                d, t = self.projet.progress([r])
                mark = "✓ " if t and d == t else ""
                fid = self.tree.insert(sid, "end", text=f"{mark}{nice_file_name(r)}  {d}/{t}")
                self.tree_map[fid] = ([r], nice_file_name(r))
        done, total = self.projet.progress(list(self.projet.files))
        self.lbl_global.config(text=f"Projet : {done} / {total} textes traduits ({done / total * 100 if total else 0:.1f} %)")

    def on_tree_select(self, _e=None):
        sel = self.tree.selection()
        if sel and sel[0] in self.tree_map:
            rels, title = self.tree_map[sel[0]]
            self.show_files(rels, title)

    # ---------- vues
    def show_files(self, rels, title):
        self.flush()
        self.view_rels = rels
        self.view_title = title
        self.items_all = [(r, k) for r in rels for k in self.projet.files[r]]
        self.refilter()

    def do_search(self):
        q = self.search_var.get().strip()
        if not q:
            return
        self.flush()
        self.view_rels = []
        self.view_title = f"Recherche : « {q} »"
        self.items_all = self.projet.search(q)
        self.refilter()

    def refilter(self):
        self.flush()
        f = self.filter_var.get()
        out = []
        for rel, key in self.items_all:
            v = str(self.projet.files[rel].get(key, "")).strip()
            if f == "Non traduits" and v:
                continue
            if f == "Traduits" and not v:
                continue
            if f == "Textes à variables" and not is_regex(key):
                continue
            out.append((rel, key))
        self.items = out
        self.page = 0
        self.render()

    def goto(self, page):
        last = max(0, (len(self.items) - 1) // PAGE_SIZE)
        page = max(0, min(page, last))
        if page != self.page:
            self.flush()
            self.page = page
            self.render()

    def render(self):
        for w in self.inner.winfo_children():
            w.destroy()
        self.widgets = {}
        start = self.page * PAGE_SIZE
        chunk = self.items[start:start + PAGE_SIZE]
        last = max(0, (len(self.items) - 1) // PAGE_SIZE)
        self.lbl_view.config(text=self.view_title)
        self.lbl_page.config(text=f"page {self.page + 1}/{last + 1}  ({len(self.items)})")
        rels = self.view_rels or sorted({r for r, _ in self.items})
        d, t = self.projet.progress(rels) if rels else (0, 0)
        self.lbl_progress.config(text=f"{d}/{t} traduits" if t else "")
        if not chunk:
            tk.Label(self.inner, text="Aucun texte à afficher avec ce filtre.", fg=TEXT_MUTED, bg=BG_DARK,
                     font=("Segoe UI", 11)).pack(pady=40)
        show_file = not self.view_rels or len(self.view_rels) > 1
        for rel, key in chunk:
            self._card(rel, key, show_file)
        self.canvas.yview_moveto(0)
        first = next(iter(self.widgets.values()), None)
        if first:
            first.focus_set()

    def _card(self, rel, key, show_file):
        value = str(self.projet.files[rel].get(key, ""))
        card = tk.Frame(self.inner, bg=BG_CARD, padx=12, pady=8, highlightthickness=1, highlightbackground="#333333")
        card.pack(fill="x", pady=4, padx=2)

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x")
        regex = is_regex(key)
        if regex:
            shown, n = readable_regex(key)
            badge = f"TEXTE À VARIABLES — écris $1…${n} là où l'anglais montre [$1]…[${n}]" if n else "TEXTE À VARIABLES"
            tk.Label(top, text=badge, fg=ACCENT_PURPLE, bg=BG_CARD, font=("Segoe UI", 8, "bold")).pack(side="left")
        else:
            shown = key
            tk.Label(top, text="ANGLAIS", fg=TEXT_MUTED, bg=BG_CARD, font=("Segoe UI", 8, "bold")).pack(side="left")
        if show_file:
            tk.Label(top, text=nice_file_name(rel), fg=TEXT_MUTED, bg=BG_CARD, font=("Segoe UI", 8)).pack(side="right")
        others = len(self.projet.index.get(key, [])) - 1
        if others > 0:
            tk.Label(top, text=f"présent dans {others} autre(s) fichier(s)", fg="#7F7F7F", bg=BG_CARD,
                     font=("Segoe UI", 8)).pack(side="right", padx=10)

        en = tk.Label(card, text=to_display(shown), fg=TEXT_EN, bg=BG_CARD, font=("Segoe UI", 10),
                      justify="left", anchor="w", wraplength=820)
        en.pack(fill="x", pady=(2, 6))

        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill="x")
        lines = max(1, min(8, len(shown) // 95 + shown.count("\\n") + 1))
        txt = tk.Text(row, height=lines, font=("Segoe UI", 10), bg=BG_INPUT, fg=TEXT_WHITE, wrap="word",
                      insertbackground=TEXT_WHITE, relief="flat", padx=6, pady=4, undo=True)
        txt.insert("1.0", to_display(value))
        txt.pack(side="left", fill="x", expand=True)
        txt.bind("<Tab>", self._focus_next)
        txt.bind("<Shift-Tab>", self._focus_prev)
        txt.bind("<FocusOut>", lambda e, r=rel, k=key: self._commit(r, k))
        side = tk.Frame(row, bg=BG_CARD)
        side.pack(side="right", padx=(6, 0))
        self._button(side, "⚡ Auto", lambda t=txt, s=key, r=rel: self._auto_translate_card(t, s, r), "#5E239D").pack(fill="x", pady=(0, 2))
        self._button(side, "= EN", lambda t=txt, s=key: self._copy_en(t, s), "#383838").pack(fill="x")
        status = tk.Label(side, text="✓" if value.strip() else "✎", fg=ACCENT_GREEN if value.strip() else ACCENT_GOLD,
                          bg=BG_CARD, font=("Segoe UI", 12, "bold"))
        status.pack(pady=(4, 0))
        txt.status = status
        self.widgets[(rel, key)] = txt

        conf = self.projet.conflicts(rel, key)
        if conf:
            tk.Label(card, text=f"⚠ Traduit autrement dans {nice_file_name(conf[0][0])} : « {conf[0][1][:80]} »",
                     fg=ACCENT_GOLD, bg=BG_CARD, font=("Segoe UI", 8), anchor="w").pack(fill="x", pady=(4, 0))

    def _auto_translate_card(self, txt, key, rel):
        if not assistant:
            messagebox.showerror("Assistant", "Module assistant_traduction.py introuvable.")
            return
        shown, _ = readable_regex(key) if is_regex(key) else (key, 0)
        self._status("Traduction intelligente en cours...", ACCENT_GOLD)
        self.update_idletasks()
        try:
            trad = assistant.traduire_en_francais(shown)
            if trad:
                txt.delete("1.0", "end")
                txt.insert("1.0", to_display(trad))
                self._commit(rel, key)
                txt.status.config(text="✓", fg=ACCENT_GREEN)
                self._status(f"Traduit avec le Glossaire : « {shown[:35]}… »", ACCENT_GREEN)
            else:
                self._status("Impossible de traduire ce texte.", ACCENT_GOLD)
        except Exception as e:
            self._status(f"Erreur de traduction : {e}", P5_RED)

    def auto_translate_page(self):
        if not assistant:
            messagebox.showerror("Assistant", "Module assistant_traduction.py introuvable.")
            return
        to_translate = []
        for (rel, key), txt in self.widgets.items():
            val = txt.get("1.0", "end-1c").strip()
            if not val:
                to_translate.append((rel, key, txt))
        if not to_translate:
            messagebox.showinfo("Auto-Traduction", "Tous les textes de cette page sont déjà traduits !")
            return
        if not messagebox.askyesno("Auto-Traduction", f"Traduire automatiquement {len(to_translate)} texte(s) non traduit(s) sur cette page avec le Glossaire officiel ?"):
            return
        self._status(f"Traduction de {len(to_translate)} texte(s) en cours...", ACCENT_GOLD)
        self.update_idletasks()
        count = 0
        for rel, key, txt in to_translate:
            shown, _ = readable_regex(key) if is_regex(key) else (key, 0)
            try:
                trad = assistant.traduire_en_francais(shown)
                if trad:
                    txt.delete("1.0", "end")
                    txt.insert("1.0", to_display(trad))
                    self._commit(rel, key)
                    txt.status.config(text="✓", fg=ACCENT_GREEN)
                    count += 1
            except Exception:
                pass
        self._status(f"Succès : {count} texte(s) traduit(s) avec le Glossaire sur la page !", ACCENT_GREEN)
        self._fill_tree()

    def _copy_en(self, txt, key):
        if is_regex(key):
            messagebox.showinfo("Texte à variables", "Pour un texte à variables, écris la phrase française "
                                "en plaçant $1, $2… là où apparaissent [$1], [$2]… dans l'anglais.")
            return
        txt.delete("1.0", "end")
        txt.insert("1.0", to_display(key))

    def _focus_next(self, e):
        e.widget.tk_focusNext().focus_set()
        self._scroll_to(self.focus_get())
        return "break"

    def _focus_prev(self, e):
        e.widget.tk_focusPrev().focus_set()
        self._scroll_to(self.focus_get())
        return "break"

    def _scroll_to(self, w):
        try:
            self.update_idletasks()
            y = w.winfo_rooty() - self.inner.winfo_rooty()
            h = max(1, self.inner.winfo_height())
            top, bottom = self.canvas.yview()
            frac = y / h
            if not (top <= frac <= bottom - 0.05):
                self.canvas.yview_moveto(max(0, frac - 0.2))
        except Exception:
            pass

    def _commit(self, rel, key):
        txt = self.widgets.get((rel, key))
        if txt is None or not txt.winfo_exists():
            return
        value = from_display(txt.get("1.0", "end-1c"))
        old = str(self.projet.files[rel].get(key, ""))
        if value == from_display(to_display(old)):
            return   # seul l'échappement diffère : pas une vraie modification
        touched = self.projet.set_value(rel, key, value, self.propagate_var.get())
        if touched:
            self.changed_keys.add((rel, key))
            txt.status.config(text="✓" if value else "✎", fg=ACCENT_GREEN if value else ACCENT_GOLD)
            extra = f" (recopié dans {touched - 1} autre(s) fichier(s))" if touched > 1 else ""
            self._status(f"Modifié : {key[:60]}{extra} — {len(self.projet.dirty)} fichier(s) à enregistrer")

    def flush(self):
        for (rel, key) in list(self.widgets):
            self._commit(rel, key)

    def _status(self, text, color=TEXT_MUTED):
        self.lbl_status.config(text=text, fg=color)

    # ---------- actions
    def save(self):
        self.flush()
        saved = self.projet.save()
        self._fill_tree()
        self._status(f"Enregistré : {len(saved)} fichier(s)." if saved else "Rien à enregistrer.", ACCENT_GREEN)
        return saved

    def _game_path(self):
        path = ""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    path = json.load(f).get("game_path", "")
            except Exception:
                pass
        if path and os.path.exists(os.path.join(path, "P5X.exe")):
            return path
        path = filedialog.askdirectory(title="Dossier du jeu (celui qui contient P5X.exe)")
        if not path:
            return ""
        if not os.path.exists(os.path.join(path, "P5X.exe")) and os.path.exists(os.path.join(path, "client", "pc", "P5X.exe")):
            path = os.path.join(path, "client", "pc")
        cfg = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception:
                cfg = {}
        cfg["game_path"] = path
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        return path

    def inject(self):
        self.flush()
        # 1. vérification des textes modifiés
        problems = []
        for rel, key in sorted(self.changed_keys):
            v = str(self.projet.files[rel].get(key, ""))
            if v.strip():
                for msg in check_value(key, v):
                    problems.append(f"• {key[:50]}… : {msg}")
        if problems:
            more = f"\n… et {len(problems) - 12} autre(s)" if len(problems) > 12 else ""
            if not messagebox.askyesno("Vérification", "Problèmes détectés :\n\n" + "\n".join(problems[:12]) + more +
                                       "\n\nInjecter quand même ?"):
                return
        # 2. enregistrement
        self.save()
        # 3. compilation + déploiement
        game = self._game_path()
        if not game:
            self._status("Injection annulée : dossier du jeu non choisi.", ACCENT_GOLD)
            return
        sys.path.insert(0, TOOLS_DIR)
        try:
            import convertisseur_json
            importlib.reload(convertisseur_json)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                total = convertisseur_json.compile_json_to_game(game)
        except Exception as e:
            messagebox.showerror("Injection", f"Erreur pendant la compilation :\n{e}")
            return
        finally:
            sys.path.pop(0)
        log = out.getvalue()
        conflicts = re.search(r"(\d+) clé\(s\) traduite\(s\) différemment", log)
        self.changed_keys.clear()
        self._status(f"Injecté : {total} entrées dans le jeu. Alt + R en jeu pour recharger.", ACCENT_GREEN)
        msg = (f"Traduction injectée dans le jeu !\n\n{total} entrées compilées.\n"
               + (f"{conflicts.group(1)} phrase(s) traduite(s) différemment selon les fichiers (la première est gardée).\n"
                  if conflicts else "")
               + "\nSi le jeu est ouvert : Alt + R pour recharger.")
        messagebox.showinfo("Injection terminée", msg)

    def open_glossary(self):
        if os.path.exists(GLOSSAIRE):
            os.startfile(GLOSSAIRE)
        else:
            messagebox.showinfo("Glossaire", "Glossaire introuvable :\n" + GLOSSAIRE)

    def on_close(self):
        self.flush()
        if self.projet.dirty:
            r = messagebox.askyesnocancel("Quitter", f"{len(self.projet.dirty)} fichier(s) modifié(s) non enregistré(s).\n"
                                                     "Enregistrer avant de quitter ?")
            if r is None:
                return
            if r:
                self.projet.save()
        self.destroy()


if __name__ == "__main__":
    Atelier().mainloop()
