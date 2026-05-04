# auth/reset_password.py
# Password reset flow — looks up user by email, updates password

import tkinter as tk
from tkinter import messagebox
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.theme import COLORS, FONTS
from ui.component import LabeledEntry, PrimaryButton, SecondaryButton, StatusLabel
from utils.helpers import hash_password, center_window
from utils.validation import validate_password_reset
from db.db_connection import get_db


class ResetPasswordWindow(tk.Toplevel):
    """Password reset dialog — email-based lookup then set new password."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Swastha — Reset Password")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_dark"])
        center_window(self, 1000, 780)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self, bg=COLORS["bg_dark"])
        outer.pack(fill="both", expand=True, padx=36, pady=24)

        tk.Label(
            outer,
            text="🔑  Reset Password",
            font=FONTS["heading_xl"],
            bg=COLORS["bg_dark"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 4))

        tk.Label(
            outer,
            text="Enter your registered email and choose a new password",
            font=FONTS["body"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"],
            wraplength=380,
            justify="center",
        ).pack(pady=(0, 18))

        card = tk.Frame(outer, bg=COLORS["bg_card"], padx=26, pady=22)
        card.pack(fill="x")
        tk.Frame(card, bg=COLORS["warning"], height=3).pack(fill="x", pady=(0, 16))

        self.email_f    = LabeledEntry(card, "Registered Email", bg=COLORS["bg_card"])
        self.email_f.pack(fill="x", pady=(0, 10))

        self.new_pass_f = LabeledEntry(card, "New Password", show="•", bg=COLORS["bg_card"])
        self.new_pass_f.pack(fill="x", pady=(0, 10))

        self.confirm_f  = LabeledEntry(card, "Confirm New Password", show="•", bg=COLORS["bg_card"])
        self.confirm_f.pack(fill="x", pady=(0, 14))

        self.status = StatusLabel(card, bg=COLORS["bg_card"])
        self.status.pack(fill="x", pady=(0, 8))

        PrimaryButton(card, "Reset Password", command=self._reset).pack(fill="x", pady=(0, 8))
        SecondaryButton(card, "Cancel", command=self.destroy).pack(fill="x")

        self.bind("<Return>", lambda e: self._reset())
        self.email_f.focus()

    def _reset(self):
        """Find user by email and update their password."""
        email    = self.email_f.get().strip()
        new_pass = self.new_pass_f.get()
        confirm  = self.confirm_f.get()

        ok, msg = validate_password_reset(email, new_pass, confirm)
        if not ok:
            self.status.show_error(msg)
            return

        conn = get_db()
        if not conn:
            self.status.show_error("Database connection failed.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                self.status.show_error("No account found with that email address.")
                cursor.close()
                return

            cursor.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (hash_password(new_pass), email),
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            self.status.show_error(f"Database error: {e}")
            return

        messagebox.showinfo(
            "Password Reset",
            "Your password has been updated successfully.\nYou can now sign in with your new password.",
            parent=self,
        )
        self.destroy()