# ui/sidebar.py
# Left-side navigation sidebar with menu items

import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.theme import COLORS, FONTS, SIDEBAR_WIDTH


# ── Navigation items (icon, label, module_key) ───────────────────────────────
NAV_ITEMS = [
    ("🏠", "Dashboard", "home"),
    ("🩺", "Disease Prediction", "disease_prediction"),
    ("🤖", "AI Chatbot", "chatbot"),
    ("💊", "Medicine Reminder", "medicine_reminder"),
    ("🔬", "Lab Analyzer", "lab_analyzer"),
    ("🥗", "Diet Guide", "diet_guide"),
    ("🧠", "Mental Health", "mental_health"),
    ("🖼️", "Image Analyzer", "image_analyzer"),
    ("🚑", "First Aid", "first_aid"),
    ("📋", "Disease Info", "disease_info"),
]


class Sidebar(tk.Frame):
    """Vertical navigation sidebar"""

    def __init__(self, parent, user, on_navigate, on_logout, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["bg_medium"],
            width=SIDEBAR_WIDTH,
            **kwargs,
        )

        self.pack_propagate(False)

        self.user = user
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.active_key = "home"

        self._nav_buttons = {}

        self._build_ui()

    # ─────────────────────────────────────────────────────────────
    def _build_ui(self):

        # LOGO
        logo_frame = tk.Frame(self, bg=COLORS["bg_medium"], pady=16)
        logo_frame.pack(fill="x")

        tk.Label(
            logo_frame,
            text="🏥  Swastha",
            font=FONTS["logo"],
            bg=COLORS["bg_medium"],
            fg=COLORS["primary"],
        ).pack()

        tk.Label(
            logo_frame,
            text="AI Healthcare",
            font=FONTS["tagline"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_muted"],
        ).pack()

        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x", padx=12)

        # NAV ITEMS
        nav_container = tk.Frame(self, bg=COLORS["bg_medium"])
        nav_container.pack(fill="both", expand=True, pady=8)

        for icon, label, key in NAV_ITEMS:
            self._add_nav_item(nav_container, icon, label, key)

        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x", padx=12)

        # USER INFO
        user_frame = tk.Frame(self, bg=COLORS["bg_medium"], pady=12)
        user_frame.pack(fill="x")

        tk.Label(
            user_frame,
            text=f"👤  {self.user['username']}",
            font=FONTS["body"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_secondary"],
        ).pack(padx=16, anchor="w")

        tk.Button(
            user_frame,
            text="⏻  Logout",
            font=FONTS["body"],
            bg=COLORS["bg_medium"],
            fg=COLORS["error"],
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["error"],
            relief="flat",
            cursor="hand2",
            bd=0,
            pady=6,
            padx=16,
            anchor="w",
            command=self.on_logout,
        ).pack(fill="x", padx=8, pady=(6, 0))

    # ─────────────────────────────────────────────────────────────
    def _add_nav_item(self, parent, icon, label_text, key):

        is_active = (key == self.active_key)

        row = tk.Frame(
            parent,
            bg=COLORS["primary"] if is_active else COLORS["bg_medium"],
            cursor="hand2",
        )
        row.pack(fill="x", padx=8, pady=2)

        accent = tk.Frame(
            row,
            bg=COLORS["bg_dark"] if is_active else COLORS["bg_medium"],
            width=4,
        )
        accent.pack(side="left", fill="y")

        icon_lbl = tk.Label(
            row,
            text=icon,
            font=("Segoe UI Emoji", 12),
            bg=COLORS["primary"] if is_active else COLORS["bg_medium"],
            fg=COLORS["bg_dark"] if is_active else COLORS["text_secondary"],
            padx=8,
            pady=10,
        )
        icon_lbl.pack(side="left")

        text_lbl = tk.Label(
            row,
            text=label_text,
            font=FONTS["sidebar"],
            bg=COLORS["primary"] if is_active else COLORS["bg_medium"],
            fg=COLORS["bg_dark"] if is_active else COLORS["text_secondary"],
            anchor="w",
        )
        text_lbl.pack(side="left", fill="x", expand=True)

        self._nav_buttons[key] = (row, accent, icon_lbl, text_lbl)

        # ✅ CLICK EVENT (FIXED SAFE)
        def handle_click(event=None, k=key):
            self._navigate(k)

        for widget in (row, accent, icon_lbl, text_lbl):
            widget.bind("<Button-1>", handle_click)

        # HOVER EFFECT
        def on_enter(e, k=key):
            if k != self.active_key:
                row.configure(bg=COLORS["bg_hover"])
                accent.configure(bg=COLORS["bg_hover"])
                icon_lbl.configure(bg=COLORS["bg_hover"])
                text_lbl.configure(bg=COLORS["bg_hover"])

        def on_leave(e, k=key):
            if k != self.active_key:
                row.configure(bg=COLORS["bg_medium"])
                accent.configure(bg=COLORS["bg_medium"])
                icon_lbl.configure(bg=COLORS["bg_medium"])
                text_lbl.configure(bg=COLORS["bg_medium"])

        for widget in (row, accent, icon_lbl, text_lbl):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    # ─────────────────────────────────────────────────────────────
    def _navigate(self, key):

        # DEBUG (important)
        print("Sidebar clicked:", key)

        prev_key = self.active_key
        self.active_key = key

        # RESET OLD
        if prev_key in self._nav_buttons:
            r, a, il, tl = self._nav_buttons[prev_key]
            r.configure(bg=COLORS["bg_medium"])
            a.configure(bg=COLORS["bg_medium"])
            il.configure(bg=COLORS["bg_medium"], fg=COLORS["text_secondary"])
            tl.configure(bg=COLORS["bg_medium"], fg=COLORS["text_secondary"])

        # SET ACTIVE
        if key in self._nav_buttons:
            r, a, il, tl = self._nav_buttons[key]
            r.configure(bg=COLORS["primary"])
            a.configure(bg=COLORS["bg_dark"])
            il.configure(bg=COLORS["primary"], fg=COLORS["bg_dark"])
            tl.configure(bg=COLORS["primary"], fg=COLORS["bg_dark"])

        # CALL DASHBOARD
        if self.on_navigate:
            self.on_navigate(key)

    # ─────────────────────────────────────────────────────────────
    def set_active(self, key):
        self._navigate(key)