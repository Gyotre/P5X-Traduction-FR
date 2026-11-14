#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
launcher_p5x.py - Launcher Persona 5: The Phantom X (Français)
Permet de basculer facilement entre le mode Moddé (Traduction FR) et le mode Officiel (Vanilla).
Supporte les versions Global/Steam (EN), Japon (JP), Taïwan (TW), Corée (KR) et Chine (CN).
Intègre la personnalisation du nom du héros et le masquage d'UID (inspiré de P5XTES).
"""

import os
import sys
import json
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "launcher_config.json")

# Couleurs du thème Persona 5
BG_DARK = "#141414"
BG_CARD = "#1F1F1F"
P5_RED = "#D80027"
P5_RED_HOVER = "#FF1F3D"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#999999"
ACCENT_GREEN = "#00D26A"
ACCENT_AMBER = "#FFB020"

AVAILABLE_REGIONS = [
    ("EN", "Global / Steam (EN)"),
    ("JP", "Japon (JP)"),
    ("TW", "Taïwan (TW)"),
    ("KR", "Corée (KR)"),
    ("CN", "Chine (CN)")
]

class P5XLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Persona 5: The Phantom X - Launcher FR")
        self.geometry("900x680")
        self.minsize(820, 600)
        self.configure(bg=BG_DARK)

        self.game_path = tk.StringVar()
        self.selected_region = tk.StringVar(value="EN")
        self.mod_status = tk.StringVar(value="Vérification...")
        self.prota_prenom = tk.StringVar(value="")
        self.prota_nom = tk.StringVar(value="")
        self.masquer_uid = tk.BooleanVar(value=False)

        self.load_config()
        self.build_ui()
        self.update_mod_status()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.game_path.set(data.get("game_path", ""))
                    self.selected_region.set(data.get("region", "EN"))
                    self.prota_prenom.set(data.get("protagoniste_prenom", ""))
                    self.prota_nom.set(data.get("protagoniste_nom", ""))
                    self.masquer_uid.set(data.get("masquer_uid", False))
            except Exception:
                pass

        if not self.game_path.get():
            possible_paths = [
                r"E:\SteamLibrary\steamapps\common\P5X\client\pc",
                r"D:\SteamLibrary\steamapps\common\P5X\client\pc",
                r"C:\Program Files (x86)\Steam\steamapps\common\P5X\client\pc",
                r"C:\Program Files (x86)\Steam\steamapps\common\P5X",
                r"D:\SteamLibrary\steamapps\common\P5X",
                r"E:\SteamLibrary\steamapps\common\P5X",
            ]
            for p in possible_paths:
                if os.path.exists(os.path.join(p, "P5X.exe")):
                    self.game_path.set(p)
                    break

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "game_path": self.game_path.get(),
                    "region": self.selected_region.get(),
                    "protagoniste_prenom": self.prota_prenom.get().strip(),
                    "protagoniste_nom": self.prota_nom.get().strip(),
                    "masquer_uid": self.masquer_uid.get()
                }, f, indent=2)
        except Exception as e:
            self.log(f"Erreur de sauvegarde de configuration : {e}")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def build_ui(self):
        # Header bannière
        header = tk.Frame(self, bg=P5_RED, height=65)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_lbl = tk.Label(header, text="PERSONA 5: THE PHANTOM X", 
                             font=("Segoe UI Black", 17, "italic"), 
                             fg=TEXT_WHITE, bg=P5_RED)
        title_lbl.pack(side="left", padx=20, pady=6)

        sub_lbl = tk.Label(header, text="LAUNCHER & GESTIONNAIRE DE TRADUCTION FR", 
                           font=("Segoe UI", 9, "bold"), 
                           fg="#FFCCCC", bg=P5_RED)
        sub_lbl.pack(side="left", padx=5, pady=10)

        # Conteneur principal
        main_frame = tk.Frame(self, bg=BG_DARK, padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        # 1. Sélection du répertoire de jeu
        dir_frame = tk.LabelFrame(main_frame, text=" EMPLACEMENT DU JEU (P5X.exe) ", 
                                  font=("Segoe UI", 9, "bold"), 
                                  fg=P5_RED, bg=BG_CARD, bd=1, relief="solid")
        dir_frame.pack(fill="x", pady=(0, 8), ipady=3)

        dir_inner = tk.Frame(dir_frame, bg=BG_CARD, padx=10, pady=4)
        dir_inner.pack(fill="x")

        entry_path = tk.Entry(dir_inner, textvariable=self.game_path, 
                              font=("Consolas", 10), bg="#2D2D2D", fg=TEXT_WHITE, 
                              insertbackground=TEXT_WHITE, relief="flat")
        entry_path.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 10))

        btn_browse = tk.Button(dir_inner, text="Parcourir...", command=self.browse_path,
                               font=("Segoe UI", 9, "bold"), bg="#444444", fg=TEXT_WHITE, 
                               relief="flat", activebackground="#555555", activeforeground=TEXT_WHITE,
                               padx=10, pady=2, cursor="hand2")
        btn_browse.pack(side="right")

        # 2. Options Personnalisation & Confort (Inspiré P5XTES)
        opt_frame = tk.LabelFrame(main_frame, text=" PERSONNALISATION DU HÉROS & CONFORT ", 
                                  font=("Segoe UI", 9, "bold"), 
                                  fg="#5599FF", bg=BG_CARD, bd=1, relief="solid")
        opt_frame.pack(fill="x", pady=(0, 8), ipady=4)

        opt_inner = tk.Frame(opt_frame, bg=BG_CARD, padx=10, pady=4)
        opt_inner.pack(fill="x")

        tk.Label(opt_inner, text="Prénom :", font=("Segoe UI", 9, "bold"), 
                 fg=TEXT_WHITE, bg=BG_CARD).pack(side="left", padx=(0, 4))
        e_prenom = tk.Entry(opt_inner, textvariable=self.prota_prenom, font=("Segoe UI", 9), 
                            width=14, bg="#2D2D2D", fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat")
        e_prenom.pack(side="left", padx=(0, 15))

        tk.Label(opt_inner, text="Nom :", font=("Segoe UI", 9, "bold"), 
                 fg=TEXT_WHITE, bg=BG_CARD).pack(side="left", padx=(0, 4))
        e_nom = tk.Entry(opt_inner, textvariable=self.prota_nom, font=("Segoe UI", 9), 
                         width=14, bg="#2D2D2D", fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat")
        e_nom.pack(side="left", padx=(0, 20))

        chk_stream = tk.Checkbutton(opt_inner, text="Masquer l'UID joueur (Mode Streameur)", 
                                    variable=self.masquer_uid, font=("Segoe UI", 9, "bold"), 
                                    fg="#FFDD66", bg=BG_CARD, selectcolor="#333333", 
                                    activebackground=BG_CARD, activeforeground="#FFDD66",
                                    command=self.save_config)
        chk_stream.pack(side="left")

        # 3. Carte État et Actions
        card_frame = tk.Frame(main_frame, bg=BG_CARD, bd=1, relief="solid", padx=15, pady=10)
        card_frame.pack(fill="x", pady=(0, 8))

        # Statut des Mods
        status_row = tk.Frame(card_frame, bg=BG_CARD)
        status_row.pack(fill="x", pady=(0, 8))

        tk.Label(status_row, text="État Actuel :", font=("Segoe UI", 10, "bold"), 
                 fg=TEXT_WHITE, bg=BG_CARD).pack(side="left")

        self.lbl_status = tk.Label(status_row, textvariable=self.mod_status, 
                                   font=("Segoe UI", 10, "bold"), 
                                   fg=ACCENT_AMBER, bg=BG_CARD)
        self.lbl_status.pack(side="left", padx=10)

        # Version du Jeu (Région)
        region_row = tk.Frame(card_frame, bg=BG_CARD)
        region_row.pack(fill="x", pady=(0, 10))
        tk.Label(region_row, text="Version du Jeu :", font=("Segoe UI", 9, "bold"), 
                 fg=TEXT_WHITE, bg=BG_CARD).pack(side="left", padx=(0, 8))

        for code, label in AVAILABLE_REGIONS:
            rb = tk.Radiobutton(region_row, text=label, variable=self.selected_region, 
                                value=code, font=("Segoe UI", 9), fg=TEXT_WHITE, bg=BG_CARD, 
                                selectcolor="#333333", activebackground=BG_CARD, 
                                activeforeground=TEXT_WHITE, command=self.on_region_change)
            rb.pack(side="left", padx=5)

        # Boutons d'action
        btn_row = tk.Frame(card_frame, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(4, 0))

        self.btn_toggle = tk.Button(btn_row, text="BASCULER MODS ON / OFF", command=self.toggle_mods,
                                    font=("Segoe UI", 9, "bold"), bg="#383838", fg=TEXT_WHITE, 
                                    relief="flat", padx=12, pady=6, cursor="hand2")
        self.btn_toggle.pack(side="left", padx=(0, 8))

        btn_deploy = tk.Button(btn_row, text="SYNCHRONISER LA TRADUCTION FR", command=self.sync_translation,
                               font=("Segoe UI", 9, "bold"), bg="#2B5B84", fg=TEXT_WHITE, 
                               relief="flat", padx=12, pady=6, cursor="hand2")
        btn_deploy.pack(side="left", padx=(0, 8))

        btn_editor = tk.Button(btn_row, text="ÉDITEUR FACILE", command=self.open_editor,
                               font=("Segoe UI", 9, "bold"), bg="#5B2B84", fg=TEXT_WHITE, 
                               relief="flat", padx=12, pady=6, cursor="hand2")
        btn_editor.pack(side="left", padx=(0, 8))

        btn_launch = tk.Button(btn_row, text="LANCER LE JEU P5X", command=self.launch_game,
                               font=("Segoe UI", 10, "bold"), bg=P5_RED, fg=TEXT_WHITE, 
                               relief="flat", activebackground=P5_RED_HOVER, padx=18, pady=6, cursor="hand2")
        btn_launch.pack(side="right")

        # 4. Zone de Journal / Logs
        log_frame = tk.LabelFrame(main_frame, text=" JOURNAL D'ACTIVITÉ ", 
                                  font=("Segoe UI", 8, "bold"), 
                                  fg=TEXT_MUTED, bg=BG_DARK, bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame, bg="#0D0D0D", fg="#88FF88", font=("Consolas", 9), 
                                relief="flat", padx=10, pady=6, state="disabled")
        self.log_text.pack(fill="both", expand=True)

        self.log(f"Launcher démarré. Région sélectionnée : {self.selected_region.get()}.")
        if self.prota_prenom.get() or self.prota_nom.get():
            self.log(f"Protagoniste configuré : {self.prota_prenom.get()} {self.prota_nom.get()}".strip())

    def on_region_change(self):
        self.save_config()
        self.log(f"Région active changée pour : {self.selected_region.get()}")

    def browse_path(self):
        selected = filedialog.askdirectory(title="Sélectionnez le dossier où se trouve P5X.exe")
        if selected:
            if not os.path.exists(os.path.join(selected, "P5X.exe")):
                sub_check = os.path.join(selected, "client", "pc")
                if os.path.exists(os.path.join(sub_check, "P5X.exe")):
                    selected = sub_check
                else:
                    messagebox.showwarning("Avertissement", 
                                           "P5X.exe est introuvable dans ce dossier !\nAssurez-vous de sélectionner le dossier exécutable.")
            self.game_path.set(selected)
            self.save_config()
            self.update_mod_status()

    def update_mod_status(self):
        gdir = self.game_path.get()
        if not gdir or not os.path.exists(gdir):
            self.mod_status.set("Dossier du jeu non configuré")
            self.lbl_status.config(fg=TEXT_MUTED)
            return

        winhttp_active = os.path.exists(os.path.join(gdir, "winhttp.dll"))
        winhttp_disabled = os.path.exists(os.path.join(gdir, "winhttp.dll.disabled"))

        if winhttp_active:
            self.mod_status.set("MODS ACTIFS (Traduction Française chargée)")
            self.lbl_status.config(fg=ACCENT_GREEN)
            self.btn_toggle.config(text="DÉSACTIVER LES MODS (Mode Vanilla)", bg="#7A2222")
        elif winhttp_disabled:
            self.mod_status.set("MODS DÉSACTIVÉS (Mode Officiel Vanilla)")
            self.lbl_status.config(fg=TEXT_MUTED)
            self.btn_toggle.config(text="ACTIVER LES MODS (Mode Traduit)", bg="#256B3A")
        else:
            self.mod_status.set("BepInEx non installé dans ce dossier")
            self.lbl_status.config(fg=ACCENT_AMBER)
            self.btn_toggle.config(text="Installer BepInEx & Traduction", bg="#855B14")

    def toggle_mods(self):
        gdir = self.game_path.get()
        if not gdir or not os.path.exists(gdir):
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner le dossier du jeu.")
            return

        active_path = os.path.join(gdir, "winhttp.dll")
        disabled_path = os.path.join(gdir, "winhttp.dll.disabled")

        if os.path.exists(active_path):
            try:
                os.rename(active_path, disabled_path)
                self.log("Mods désactivés avec succès. Le jeu se lancera en version Vanilla officielle.")
            except Exception as e:
                self.log(f"Erreur lors de la désactivation : {e}")
        elif os.path.exists(disabled_path):
            try:
                os.rename(disabled_path, active_path)
                self.log("Mods activés avec succès. La traduction française sera injectée au démarrage.")
            except Exception as e:
                self.log(f"Erreur lors de l'activation : {e}")
        else:
            confirm = messagebox.askyesno("Installation BepInEx", 
                                          "BepInEx n'est pas installé dans le dossier du jeu.\n"
                                          "Voulez-vous installer le pack BepInEx + XUnity préconfiguré ?")
            if confirm:
                self.install_bepinex_pack()

        self.update_mod_status()

    def install_bepinex_pack(self):
        gdir = self.game_path.get()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        pack_dir = os.path.join(base_dir, "05_Paquet_BepInEx_Preconfigure", "A_COPIER_DANS_LE_JEU")

        if not os.path.exists(pack_dir):
            self.log(f"Erreur : Le dossier de préconfiguration est introuvable : {pack_dir}")
            return

        try:
            self.log("Copie des fichiers BepInEx & XUnity dans le dossier du jeu...")
            for item in os.listdir(pack_dir):
                s = os.path.join(pack_dir, item)
                d = os.path.join(gdir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            self.log("Pack BepInEx installé avec succès dans le jeu !")
            self.sync_translation()
        except Exception as e:
            self.log(f"Erreur d'installation BepInEx : {e}")

    def open_editor(self):
        editor_script = os.path.join(os.path.dirname(__file__), "editeur_traduction.py")
        if os.path.exists(editor_script):
            subprocess.Popen([sys.executable, editor_script])
        else:
            messagebox.showerror("Erreur", "Éditeur introuvable.")

    def sync_translation(self):
        gdir = self.game_path.get()
        if not gdir or not os.path.exists(gdir):
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner le dossier du jeu.")
            return

        self.save_config()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Compilation des fichiers JSON faciles vers les modules et le jeu
        try:
            conv_script = os.path.join(base_dir, "03_Outils_Traduction", "convertisseur_json.py")
            sys.path.append(os.path.dirname(conv_script))
            import convertisseur_json
            total = convertisseur_json.compile_json_to_game(gdir)
            self.log(f"Compilation JSON terminée : {total} traductions actives déployées.")
            messagebox.showinfo("Succès", 
                                f"Traduction synchronisée avec succès !\n\n{total} textes actifs appliqués dans le jeu.\n(Rechargement à chaud actif)")
        except Exception as e:
            self.log(f"Compilation JSON : {e}")
            messagebox.showerror("Erreur", f"Erreur pendant la compilation : {e}")

        self.update_mod_status()

    def launch_game(self):
        gdir = self.game_path.get()
        if not gdir or not os.path.exists(gdir):
            messagebox.showerror("Erreur", "Dossier du jeu non configuré !")
            return

        exe_path = os.path.join(gdir, "P5X.exe")
        if not os.path.exists(exe_path):
            messagebox.showerror("Erreur", f"P5X.exe introuvable dans :\n{gdir}")
            return

        self.log(f"Lancement de Persona 5: The Phantom X ({self.mod_status.get()})...")
        try:
            subprocess.Popen([exe_path], cwd=gdir)
            self.log("Jeu démarré avec succès !")
        except Exception as e:
            self.log(f"Impossible de lancer le jeu : {e}")

if __name__ == "__main__":
    app = P5XLauncher()
    app.mainloop()
