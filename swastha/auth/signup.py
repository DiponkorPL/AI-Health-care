# auth/signup.py
# Clean & Fixed Signup / Registration Screen

import tkinter as tk
from tkinter import messagebox
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.theme import COLORS, FONTS
from ui.component import LabeledEntry, PrimaryButton, SecondaryButton, StatusLabel
from utils.helpers import hash_password, center_window
from utils.validation import validate_signup
from db.db_connection import get_db
from config import WINDOW_CONFIG


class SignupWindow(tk.Toplevel):
    """Signup form as a modal window."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Swastha — Create Account")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_dark"])

        # Window config
        config = WINDOW_CONFIG["signup"]
        width = config["width"]
        height = config["height"]

        self.geometry(f"{width}x{height}")
        center_window(self, width, height)

        self.grab_set()  # Modal behavior

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self, bg=COLORS["bg_dark"])
        outer.pack(fill="both", expand=True, padx=40, pady=24)

        # Header
        tk.Label(
            outer,
            text="🏥  Create Your Account",
            font=FONTS["heading_xl"],
            bg=COLORS["bg_dark"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 4))

        tk.Label(
            outer,
            text="Join Swastha and take control of your health",
            font=FONTS["body"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(0, 18))

        # Card
        card = tk.Frame(outer, bg=COLORS["bg_card"], padx=28, pady=24)
        card.pack(fill="x")

        tk.Frame(card, bg=COLORS["primary"], height=3).pack(fill="x", pady=(0, 16))

        # Fields
        self.username_f = LabeledEntry(card, "Username", bg=COLORS["bg_card"])
        self.username_f.pack(fill="x", pady=(0, 10))

        self.email_f = LabeledEntry(card, "Email Address", bg=COLORS["bg_card"])
        self.email_f.pack(fill="x", pady=(0, 10))

        self.password_f = LabeledEntry(card, "Password", show="•", bg=COLORS["bg_card"])
        self.password_f.pack(fill="x", pady=(0, 10))

        self.confirm_f = LabeledEntry(card, "Confirm Password", show="•", bg=COLORS["bg_card"])
        self.confirm_f.pack(fill="x", pady=(0, 14))

        # Status
        self.status = StatusLabel(card, bg=COLORS["bg_card"])
        self.status.pack(fill="x", pady=(0, 8))

        # Buttons
        PrimaryButton(
            card,
            "Create Account",
            command=self.register_user
        ).pack(fill="x", pady=(0, 8))

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=8)

        SecondaryButton(
            card,
            "Already have an account? Sign In",
            command=self.destroy
        ).pack(fill="x")

        # Enter key support
        self.bind("<Return>", lambda e: self.register_user())

        self.username_f.focus()

    def register_user(self):
        username = self.username_f.get().strip()
        email = self.email_f.get().strip()
        password = self.password_f.get()
        confirm = self.confirm_f.get()

        # Validation
        ok, msg = validate_signup(username, email, password, confirm)
        if not ok:
            self.status.show_error(msg)
            return

        conn = get_db()
        if not conn:
            self.status.show_error("Database connection failed.")
            return

        try:
            # ✅ ensure connection alive
            if not conn.is_connected():
                self.status.show_error("Database disconnected.")
                return

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hash_password(password)),
            )

            conn.commit()

            cursor.close()
            conn.close()   # ✅ ADDED (important fix)

        except Exception as e:
            err = str(e)

            if "Duplicate entry" in err:
                if "username" in err:
                    self.status.show_error("Username already taken.")
                elif "email" in err:
                    self.status.show_error("Email already registered.")
                else:
                    self.status.show_error("Duplicate data error.")
            else:
                self.status.show_error(f"Registration error: {e}")
            return

        # Success
        messagebox.showinfo(
            "Account Created",
            f"Welcome to Swastha, {username}!\nYou can now sign in.",
            parent=self,
        )

        self.destroy()