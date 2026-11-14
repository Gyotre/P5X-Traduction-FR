#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
editeur_traduction.py - Éditeur Graphique Simplifié de Traduction pour P5X
Permet de traduire facilement chaque personnage, quête, dialogue et menu sans toucher au code.
"""

import os
import sys
import re
import json
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EASY_DIR = os.path.join(BASE_DIR, "TRADUCTION_FACILE")
SCRIPT_CONVERT = os.path.join(BASE_DIR, "03_Outils_Traduction", "convertisseur_json.py")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "launcher_config.json")

# Couleurs Persona 5
BG_DARK = "#141414"
BG_CARD = "#1F1F1F"
BG_INPUT = "#2B2B2B"
P5_RED = "#D80027"
P5_RED_HOVER = "#FF1F3D"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#AAAAAA"
ACCENT_GREEN = "#00D26A"
ACCENT_GOLD = "#FFC000"

class TranslationEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("P5X - Éditeur Visuel de Traduction")
        self.geometry("1020x720")
        self.minsize(850, 550)
        self.configure(bg=BG_DARK)

        self.current_json_path = None
        self.current_data = {}
        self.entries_widgets = {}

        self.load_game_path()
        self.build_ui()
        self.load_categories()

    def load_game_path(self):
        self.game_path = ""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.game_path = cfg.get("game_path", "")
            except Exception:
                pass

    def build_ui(self):
        # Header Persona 5
        header = tk.Frame(self, bg=P5_RED, height=55)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="P5X - ÉDITEUR VISUEL DE TRADUCTION", 
                 font=("Segoe UI Black", 16, "italic"), fg=TEXT_WHITE, bg=P5_RED).pack(side="left", padx=20, pady=10)

        self.lbl_progress = tk.Label(header, text="", font=("Segoe UI", 11, "bold"), fg=TEXT_WHITE, bg=P5_RED)
        self.lbl_progress.pack(side="right", padx=20)

        # Barre supérieure : Sélection de fichier et Filtres
        top_bar = tk.Frame(self, bg=BG_CARD, padx=15, pady=10, bd=1, relief="solid")
        top_bar.pack(fill="x", padx=15, pady=10)

        # Ligne 1: Fichier et Enregistrer
        row1 = tk.Frame(top_bar, bg=BG_CARD)
        row1.pack(fill="x", pady=(0, 8))

        tk.Label(row1, text="Fiche à traduire :", font=("Segoe UI", 10, "bold"), 
                 fg=TEXT_WHITE, bg=BG_CARD).pack(side="left", padx=(0, 8))

        self.combo_files = ttk.Combobox(row1, width=45, state="readonly", font=("Segoe UI", 10))
        self.combo_files.pack(side="left", padx=(0, 20))
        self.combo_files.bind("<<ComboboxSelected>>", self.on_file_selected)

        btn_save = tk.Button(row1, text="💾 ENREGISTRER & APPLIQUER AU JEU", command=self.save_and_apply,
                             font=("Segoe UI", 10, "bold"), bg=P5_RED, fg=TEXT_WHITE, 
                             activebackground=P5_RED_HOVER, relief="flat", padx=15, pady=4, cursor="hand2")
        btn_save.pack(side="right")

        # Ligne 2: Recherche et Filtrage
        row2 = tk.Frame(top_bar, bg=BG_CARD)
        row2.pack(fill="x")

        tk.Label(row2, text="Recherche :", font=("Segoe UI", 9), 
                 fg=TEXT_MUTED, bg=BG_CARD).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_list)
        entry_search = tk.Entry(row2, textvariable=self.search_var, font=("Segoe UI", 10), 
                                bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat", width=25)
        entry_search.pack(side="left", ipady=2, padx=(0, 20))

        tk.Label(row2, text="Filtrer :", font=("Segoe UI", 9), 
                 fg=TEXT_MUTED, bg=BG_CARD).pack(side="left", padx=(0, 6))

        self.filter_var = tk.StringVar(value="Tous")
        self.combo_filter = ttk.Combobox(row2, textvariable=self.filter_var, values=["Tous", "Non traduits uniquement", "Traduits uniquement"],
                                         state="readonly", width=22, font=("Segoe UI", 9))
        self.combo_filter.pack(side="left")
        self.combo_filter.bind("<<ComboboxSelected>>", self.filter_list)

        # Zone centrale défilante (Scrollable frame)
        container = tk.Frame(self, bg=BG_DARK, padx=15)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG_DARK)

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.bind_mouse_scroll()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def bind_mouse_scroll(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.bind_all("<MouseWheel>", _on_mousewheel)

    def load_categories(self):
        self.file_map = {}
        if os.path.exists(EASY_DIR):
            for root, _, files in os.walk(EASY_DIR):
                rel = os.path.relpath(root, EASY_DIR)
                if rel == ".":
                    continue
                cat_clean = rel.replace("\\", "/")
                # Retirer les chiffres préfixes (ex: 01_Personnages -> Personnages)
                cat_clean = "/".join([re.sub(r"^\d+_", "", seg) for seg in cat_clean.split("/")])
                for f in sorted(files):
                    if f.endswith(".json"):
                        item_name = f[:-5].replace("_", " ")
                        label = f"[{cat_clean}] {item_name}"
                        self.file_map[label] = os.path.join(root, f)

        labels = sorted(list(self.file_map.keys()))
        self.combo_files["values"] = labels

        # Sélectionner Miku par défaut si dispo
        miku_label = next((l for l in labels if "Miku" in l), None)
        if miku_label:
            self.combo_files.set(miku_label)
        elif labels:
            self.combo_files.current(0)
        self.on_file_selected()

    def on_file_selected(self, event=None):
        selected_label = self.combo_files.get()
        if not selected_label or selected_label not in self.file_map:
            return

        self.current_json_path = self.file_map[selected_label]
        try:
            with open(self.current_json_path, "r", encoding="utf-8") as f:
                self.current_data = json.load(f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier JSON : {e}")
            return

        self.update_progress()
        self.render_items()

    def update_progress(self):
        total = len(self.current_data)
        done = sum(1 for v in self.current_data.values() if str(v).strip())
        pct = (done / total * 100) if total > 0 else 0
        self.lbl_progress.config(text=f"Progression : {done}/{total} ({pct:.0f}%)")

    def render_items(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.entries_widgets = {}
        query = self.search_var.get().lower().strip()
        filtre = self.filter_var.get()

        count = 0
        for eng_text, fr_text in self.current_data.items():
            is_translated = bool(str(fr_text).strip())

            # Filtre de statut
            if filtre == "Non traduits uniquement" and is_translated:
                continue
            if filtre == "Traduits uniquement" and not is_translated:
                continue

            # Filtre de recherche
            if query and query not in eng_text.lower() and query not in fr_text.lower():
                continue

            count += 1
            card = tk.Frame(self.scroll_frame, bg=BG_CARD, bd=1, relief="solid", padx=12, pady=10)
            card.pack(fill="x", pady=6)

            # Ligne texte anglais (original)
            tk.Label(card, text="Texte Anglais (En jeu) :", font=("Segoe UI", 8, "bold"), 
                     fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")

            lbl_eng = tk.Label(card, text=eng_text, font=("Segoe UI", 10), fg="#66CCFF", 
                               bg=BG_CARD, wraplength=850, justify="left")
            lbl_eng.pack(anchor="w", pady=(2, 8))

            # Champ de saisie pour la traduction française
            status_text = "✓ Traduit :" if is_translated else "✎ À traduire en français :"
            status_color = ACCENT_GREEN if is_translated else ACCENT_GOLD
            tk.Label(card, text=status_text, font=("Segoe UI", 8, "bold"), 
                     fg=status_color, bg=BG_CARD).pack(anchor="w")

            if "\n" in eng_text or len(eng_text) > 80:
                txt_fr = tk.Text(card, height=3, font=("Segoe UI", 10), bg=BG_INPUT, fg=TEXT_WHITE,
                                 insertbackground=TEXT_WHITE, relief="flat", padx=6, pady=4)
                txt_fr.insert("1.0", fr_text)
                txt_fr.pack(fill="x", pady=(2, 0))
                self.entries_widgets[eng_text] = ("text", txt_fr)
            else:
                entry_fr = tk.Entry(card, font=("Segoe UI", 10), bg=BG_INPUT, fg=TEXT_WHITE,
                                    insertbackground=TEXT_WHITE, relief="flat")
                entry_fr.insert(0, fr_text)
                entry_fr.pack(fill="x", pady=(2, 0), ipady=3)
                self.entries_widgets[eng_text] = ("entry", entry_fr)

        if count == 0:
            tk.Label(self.scroll_frame, text="Aucun résultat trouvé pour ce filtre ou cette recherche.", 
                     font=("Segoe UI", 11), fg=TEXT_MUTED, bg=BG_DARK).pack(pady=40)

    def filter_list(self, *args):
        self.render_items()

    def save_and_apply(self):
        if not self.current_json_path:
            return

        # Récupérer les valeurs éditées
        for eng_text, (wtype, widget) in self.entries_widgets.items():
            if wtype == "text":
                val = widget.get("1.0", "end-1c").strip()
            else:
                val = widget.get().strip()
            self.current_data[eng_text] = val

        try:
            with open(self.current_json_path, "w", encoding="utf-8") as f:
                json.dump(self.current_data, f, ensure_ascii=False, indent=2)

            # Compiler automatiquement vers le jeu
            sys.path.append(os.path.dirname(SCRIPT_CONVERT))
            import convertisseur_json
            total = convertisseur_json.compile_json_to_game(self.game_path)

            self.update_progress()
            self.render_items()
            messagebox.showinfo("Succès", 
                                f"Traduction enregistrée !\n\n{total} traductions actives appliquées dans le jeu.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

if __name__ == "__main__":
    app = TranslationEditor()
    app.mainloop()
