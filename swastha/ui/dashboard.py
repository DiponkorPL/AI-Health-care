# ui/dashboard.py

import tkinter as tk
from tkinter import messagebox
import sys
import os
from datetime import datetime
import importlib

# IMPORTANT: project root path fix
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ui.theme import COLORS, FONTS, HEADER_HEIGHT
from ui.sidebar import Sidebar
from config import APP_CONFIG, DASHBOARD_WIDTH, DASHBOARD_HEIGHT
from utils.helpers import center_window


# ── FEATURE LOADER ─────────────────────────────────────────────
def _load_feature(key, parent, user):

    mapping = {
        "home": ("features.home_panel", "HomePanel"),
        "disease_prediction": ("features.disease_prediction", "DiseasePrediction"),
        "chatbot": ("features.chatbot", "Chatbot"),
        "medicine_reminder": ("features.medicine_reminder", "MedicineReminder"),
        "lab_analyzer": ("features.lab_analyzer", "LabAnalyzer"),
        "diet_guide": ("features.diet_guide", "DietGuide"),
        "mental_health": ("features.mental_health", "MentalHealth"),
        "image_analyzer": ("features.image_analyzer", "ImageAnalyzer"),
        "first_aid": ("features.first_aid", "FirstAid"),
        "disease_info": ("features.disease_info", "DiseaseInfo"),
    }

    if key not in mapping:
        print("[ERROR] Invalid key:", key)
        return None

    try:
        module_path, class_name = mapping[key]

        # 🔥 FIX: add swastha prefix
        full_module = f"swastha.{module_path}"

        print(f"[LOAD] {full_module}.{class_name}")

        module = importlib.import_module(full_module)
        cls = getattr(module, class_name)

        return cls(parent, user)

    except Exception as e:
        print(f"[FEATURE LOAD ERROR] {key} → {e}")
        return None


# ── MAIN DASHBOARD ─────────────────────────────────────────────
class Dashboard(tk.Tk):

    def __init__(self, user: dict):
        super().__init__()

        self.user = user
        self.title(APP_CONFIG)
        self.configure(bg=COLORS["bg_dark"])

        center_window(self, DASHBOARD_WIDTH, DASHBOARD_HEIGHT)
        self.minsize(900, 600)

        self._current_panel = None

        self._build_ui()

        # default page
        self._navigate("home")

    # ── UI ─────────────────────────────────────────────
    def _build_ui(self):

        self._sidebar = Sidebar(
            self,
            user=self.user,
            on_navigate=self._navigate,
            on_logout=self._logout,
        )
        self._sidebar.pack(side="left", fill="y")

        right = tk.Frame(self, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        self._build_header(right)

        self._content = tk.Frame(right, bg=COLORS["bg_dark"])
        self._content.pack(fill="both", expand=True)

    def _build_header(self, parent):

        header = tk.Frame(parent, bg=COLORS["bg_medium"], height=HEADER_HEIGHT)
        header.pack(fill="x")
        header.pack_propagate(False)

        self._header_title = tk.Label(
            header,
            text="Dashboard",
            font=FONTS["heading_lg"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_primary"],
            padx=20,
        )
        self._header_title.pack(side="left", pady=12)

        info_frame = tk.Frame(header, bg=COLORS["bg_medium"])
        info_frame.pack(side="right", padx=20)

        today = datetime.now().strftime("%A, %B %d %Y")

        tk.Label(
            info_frame,
            text=today,
            font=FONTS["body_sm"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_secondary"],
        ).pack(anchor="e")

        tk.Label(
            info_frame,
            text=f"Hello, {self.user.get('username','User')} 👋",
            font=FONTS["heading_sm"],
            bg=COLORS["bg_medium"],
            fg=COLORS["primary"],
        ).pack(anchor="e")

        tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x")

    # ── NAVIGATION ─────────────────────────────────────────────
    def _navigate(self, key: str):

        print(f"[NAVIGATE] {key}")

        titles = {
            "home": "Dashboard — Home",
            "disease_prediction": "Disease Prediction",
            "chatbot": "AI Health Chatbot",
            "medicine_reminder": "Medicine Reminder",
            "lab_analyzer": "Lab Report Analyzer",
            "diet_guide": "Diet & Nutrition Guide",
            "mental_health": "Mental Health Support",
            "image_analyzer": "Medical Image Analyzer",
            "first_aid": "First Aid Guide",
            "disease_info": "Disease Information",
        }

        self._header_title.config(
            text=titles.get(key, key.replace("_", " ").title())
        )

        # clear previous
        if self._current_panel:
            self._current_panel.destroy()
            self._current_panel = None

        # load new
        panel = _load_feature(key, self._content, self.user)

        if panel:
            panel.pack(fill="both", expand=True)
            self._current_panel = panel
        else:
            # 🔥 fallback UI (blank না দেখানোর জন্য)
            error_label = tk.Label(
                self._content,
                text="⚠ Feature failed to load",
                fg="red",
                bg=COLORS["bg_dark"],
                font=("Arial", 16)
            )
            error_label.pack(pady=50)
            self._current_panel = error_label

    # ── LOGOUT ─────────────────────────────────────────────
    def _logout(self):

        if messagebox.askyesno("Logout", "Are you sure?"):
            from auth.login import LoginPage

            self.destroy()

            root = tk.Tk()
            LoginPage(root)
            root.mainloop()