# auth/login.py
# Clean & Fixed Login Screen for Swastha Healthcare System

import tkinter as tk
from tkinter import messagebox
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.theme import COLORS, FONTS
from ui.component import LabeledEntry, PrimaryButton, SecondaryButton, StatusLabel
from utils.helpers import verify_password, center_window
from utils.validation import validate_login
from db.db_connection import get_db
from config import APP_NAME, LOGIN_WIDTH, LOGIN_HEIGHT


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)

        self.root.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}")
        self.root.resizable(True, True)

        self._build_ui()

    def _build_ui(self):
        
        outer = tk.Frame(self.root, bg=COLORS["bg_dark"])
        outer.pack(fill="both", expand=True, padx=0, pady=0)

        logo_frame = tk.Frame(outer, bg=COLORS["bg_dark"])
        logo_frame.pack(fill="x", pady=(10, 0))

        tk.Label(
            logo_frame,
            text="🏥",
            font=("Segoe UI Emoji", 36),
            bg=COLORS["bg_dark"],
            fg=COLORS["primary"],
        ).pack()

        tk.Label(
            logo_frame,
            text="Swastha",
            font=FONTS["logo"],
            bg=COLORS["bg_dark"],
            fg=COLORS["primary"],
        ).pack()

        tk.Label(
            logo_frame,
            text="AI Smart Healthcare System",
            font=FONTS["tagline"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(2, 16))

        card = tk.Frame(outer, bg=COLORS["bg_card"], padx=28, pady=28)
        card.pack(fill="both", expand=True)

        tk.Frame(card, bg=COLORS["primary"], height=3).pack(fill="x", pady=(0, 18))

        tk.Label(
            card,
            text="Sign In to Your Account",
            font=FONTS["heading_md"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 16))

        self.username_field = LabeledEntry(card, "Username", bg=COLORS["bg_card"])
        self.username_field.pack(fill="x", pady=(0, 12))

        self.password_field = LabeledEntry(card, "Password", show="•", bg=COLORS["bg_card"])
        self.password_field.pack(fill="x", pady=(0, 6))

        forgot = tk.Label(
            card,
            text="Forgot password?",
            font=FONTS["body_sm"],
            bg=COLORS["bg_card"],
            fg=COLORS["secondary"],
            cursor="hand2",
        )
        forgot.pack(anchor="e", pady=(0, 18))
        forgot.bind("<Button-1>", lambda e: self._open_reset())

        self.status = StatusLabel(card, bg=COLORS["bg_card"])
        self.status.pack(fill="x", pady=(0, 10))

        PrimaryButton(
            card,
            "Sign In",
            command=self._attempt_login
        ).pack(fill="x", pady=(0, 8))

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=8)

        tk.Label(
            card,
            text="Don't have an account?",
            font=FONTS["body_sm"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        ).pack()

        SecondaryButton(
            card,
            "Create Account",
            command=self._open_signup
        ).pack(fill="x", pady=(6, 0))

        self.root.bind("<Return>", lambda e: self._attempt_login())

        self.username_field.focus()

    # ───────────────────────── LOGIN ─────────────────────────
    def _attempt_login(self):

        username = self.username_field.get().strip()
        password = self.password_field.get()

        ok, msg = validate_login(username, password)
        if not ok:
            self.status.show_error(msg)
            return

        conn = get_db()
        if not conn:
            self.status.show_error("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()

            cursor.close()

        except Exception as e:
            self.status.show_error(f"DB Error: {e}")
            return

        if not user or not verify_password(password, user["password"]):
            self.status.show_error("Invalid username or password.")
            return

        # ✅ FIX: pass full user object to dashboard
        self._launch_dashboard(user)

    # ───────────────────────── DASHBOARD CONNECT ─────────────────────────
    def _launch_dashboard(self, user):

        from ui.dashboard import Dashboard

        self.root.destroy()

        app = Dashboard(user)   # 🔥 THIS is the KEY connection
        app.mainloop()

    # ───────────────────────── OTHER WINDOWS ─────────────────────────
    def _open_signup(self):
        from auth.signup import SignupWindow
        SignupWindow(self.root)

    def _open_reset(self):
        from auth.reset_password import ResetPasswordWindow
        ResetPasswordWindow(self.root)