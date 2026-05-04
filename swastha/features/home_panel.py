# features/home_panel.py
# Home/overview panel shown immediately after login

import tkinter as tk
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG


# ── Feature cards shown on the home panel ─────────────────────────────────────
FEATURE_CARDS = [
    ("🩺", "Disease Prediction", "Identify possible conditions\nfrom your symptoms",    "disease_prediction", COLORS["primary"]),
    ("🤖", "AI Chatbot",         "Get instant AI-powered\nhealth guidance",             "chatbot",            COLORS["secondary"]),
    ("💊", "Medicine Reminder",  "Track your medications\nand daily doses",             "medicine_reminder",  "#AB47BC"),
    ("🔬", "Lab Analyzer",       "Upload and interpret\nyour lab reports",              "lab_analyzer",       "#FF7043"),
    ("🥗", "Diet Guide",         "Personalised nutrition\nand meal planning",           "diet_guide",         "#66BB6A"),
    ("🧠", "Mental Health",      "Mood tracking and\nwellness support",                 "mental_health",      "#FFA726"),
    ("🖼️", "Image Analyzer",     "AI-powered medical\nimage analysis",                 "image_analyzer",     "#EC407A"),
    ("🚑", "First Aid",          "Emergency instructions\nfor common situations",       "first_aid",          "#EF5350"),
    ("📋", "Disease Info",       "Search our database of\ndiseases and conditions",    "disease_info",       "#29B6F6"),
]


class HomePanel(tk.Frame):
    """
    Home overview panel.
    Displays greeting, stats strip, and a card grid for quick navigation.
    """

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        # We need a reference to the dashboard to trigger navigation.
        # Dashboard injects itself as parent's master hierarchy; we use a callback
        # approach: dashboard wires _navigate via the sidebar — here we call
        # the sidebar's set_active which triggers the callback.
        self._build_ui()

    def _build_ui(self):
        # Scrollable canvas so cards don't get clipped on small screens
        canvas = tk.Canvas(self, bg=COLORS["bg_dark"], highlightthickness=0)
        scroll = tk.Scrollbar(self, orient="vertical", command=canvas.yview,
                              bg=COLORS["bg_medium"])
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLORS["bg_dark"])
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(canvas_window, width=e.width)

        def _on_frame_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _on_resize)
        inner.bind("<Configure>", _on_frame_config)

        # Mouse-wheel scrolling
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._fill_inner(inner)

    def _fill_inner(self, parent):
        pad = PADDING_LG

        # ── Greeting banner ────────────────────────────────────────────────
        banner = tk.Frame(parent, bg=COLORS["bg_medium"], pady=20)
        banner.pack(fill="x", padx=pad, pady=(pad, 0))
        tk.Frame(banner, bg=COLORS["primary"], width=4).pack(side="left", fill="y")

        text_side = tk.Frame(banner, bg=COLORS["bg_medium"], padx=16)
        text_side.pack(side="left", fill="both", expand=True)

        hour = datetime.now().hour
        greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

        tk.Label(
            text_side,
            text=f"{greeting}, {self.user['username']} 👋",
            font=FONTS["heading_xl"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            text_side,
            text="Welcome back to Swastha — your AI-powered healthcare companion.",
            font=FONTS["body"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x")

        # ── Quick-stats strip ──────────────────────────────────────────────
        stats_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        stats_frame.pack(fill="x", padx=pad, pady=(PADDING_MD, 0))

        stats = [
            ("9", "Health Features",    COLORS["primary"]),
            ("AI", "Powered Insights",  COLORS["secondary"]),
            ("24/7", "Always Available",COLORS["warning"]),
        ]
        for value, label, color in stats:
            card = tk.Frame(stats_frame, bg=COLORS["bg_card"], padx=20, pady=14)
            card.pack(side="left", padx=(0, PADDING_MD), expand=True, fill="x")
            tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 8))
            tk.Label(card, text=value, font=FONTS["heading_xl"],
                     bg=COLORS["bg_card"], fg=color).pack()
            tk.Label(card, text=label, font=FONTS["body_sm"],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack()

        # ── Section title ──────────────────────────────────────────────────
        tk.Label(
            parent,
            text="All Features",
            font=FONTS["heading_md"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", padx=pad, pady=(PADDING_LG, PADDING_MD))

        # ── Feature card grid (3 columns) ──────────────────────────────────
        grid = tk.Frame(parent, bg=COLORS["bg_dark"])
        grid.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

        for col in range(3):
            grid.columnconfigure(col, weight=1)

        for idx, (icon, title, desc, key, color) in enumerate(FEATURE_CARDS):
            row_idx = idx // 3
            col_idx = idx % 3
            self._make_card(grid, icon, title, desc, key, color, row_idx, col_idx)

    def _make_card(self, grid, icon, title, desc, key, color, row, col):
        """Build one clickable feature card."""
        outer = tk.Frame(grid, bg=COLORS["bg_card"], cursor="hand2")
        outer.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # Accent top line
        accent = tk.Frame(outer, bg=color, height=4)
        accent.pack(fill="x")

        inner = tk.Frame(outer, bg=COLORS["bg_card"], padx=16, pady=14)
        inner.pack(fill="both", expand=True)

        icon_lbl = tk.Label(inner, text=icon, font=("Segoe UI Emoji", 26),
                            bg=COLORS["bg_card"], fg=color)
        icon_lbl.pack(anchor="w")

        title_lbl = tk.Label(inner, text=title, font=FONTS["heading_sm"],
                             bg=COLORS["bg_card"], fg=COLORS["text_primary"], anchor="w")
        title_lbl.pack(fill="x", pady=(6, 2))

        desc_lbl = tk.Label(inner, text=desc, font=FONTS["body_sm"],
                            bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                            anchor="w", justify="left")
        desc_lbl.pack(fill="x")

        # Hover effect
        all_widgets = [outer, inner, accent, icon_lbl, title_lbl, desc_lbl]

        def on_enter(e, aw=all_widgets, c=color):
            for w in aw:
                if w is not accent:
                    w.configure(bg=COLORS["bg_hover"])

        def on_leave(e, aw=all_widgets, c=color):
            for w in aw:
                if w is not accent:
                    w.configure(bg=COLORS["bg_card"])

        for w in all_widgets:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        # Navigate on click — we walk up to find the Dashboard and trigger _navigate
        def on_click(e, k=key):
            self._trigger_nav(k)

        for w in all_widgets:
            w.bind("<Button-1>", on_click)

    def _trigger_nav(self, key: str):
        """
        Walk the widget hierarchy to find the Sidebar and call its set_active,
        which in turn calls Dashboard._navigate via the registered callback.
        """
        # The sidebar is packed in the Dashboard (Tk root); find it
        widget = self
        while widget is not None:
            try:
                master = widget.master
            except Exception:
                break
            # Look for Sidebar among master's children
            from ui.sidebar import Sidebar
            for child in master.winfo_children():
                if isinstance(child, Sidebar):
                    child.set_active(key)
                    return
            widget = master