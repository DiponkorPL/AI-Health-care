# ui/components.py
# Reusable UI building blocks used across the application

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_SM, PADDING_LG


# ─── Card Frame ───────────────────────────────────────────────────────────────
class Card(tk.Frame):
    """A styled container that looks like a card with a colored top border."""

    def __init__(self, parent, title="", accent=None, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["bg_card"],
            bd=0,
            relief="flat",
            **kwargs,
        )

        if accent is None:
            accent = COLORS["primary"]

        tk.Frame(self, bg=accent, height=3).pack(fill="x")

        if title:
            tk.Label(
                self,
                text=title,
                font=FONTS["heading_sm"],
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
                anchor="w",
                pady=6,
                padx=PADDING_MD,
            ).pack(fill="x")


# ─── Labeled Entry ───────────────────────────────────────────────────────────
class LabeledEntry(tk.Frame):
    """Label + Entry with optional show/hide password button"""

    def __init__(self, parent, label_text, **kwargs):
        bg = kwargs.pop("bg", COLORS["bg_dark"])
        show_char = kwargs.pop("show", None)

        super().__init__(parent, bg=bg)

        self.is_password = show_char is not None
        self.hidden = True

        # Label
        tk.Label(
            self,
            text=label_text,
            font=FONTS["label"],
            bg=bg,
            fg=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(0, 3))

        # Entry container
        box = tk.Frame(self, bg=COLORS["border_light"], padx=1, pady=1)
        box.pack(fill="x")

        # Entry
        self.entry = tk.Entry(
            box,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["primary"],
            relief="flat",
            font=FONTS["body"],
            show=show_char
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=10)

        # 👁️ Toggle button (only for password fields)
        if self.is_password:
            self.toggle_btn = tk.Button(
                box,
                text="👁️",
                width=3,
                bd=0,
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                cursor="hand2",
                command=self.toggle_password
            )
            self.toggle_btn.pack(side="right")

    # ─── Toggle Function ───
    def toggle_password(self):
        if self.hidden:
            self.entry.config(show="")   # show password
            self.toggle_btn.config(text="🙈")
        else:
            self.entry.config(show="•")  # hide password
            self.toggle_btn.config(text="👁️")

        self.hidden = not self.hidden

    # utilities
    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def clear(self):
        self.entry.delete(0, tk.END)

    def focus(self):
        self.entry.focus()

    def bind(self, event, callback):
        self.entry.bind(event, callback)

# ─── Status Label ────────────────────────────────────────────────────────────
class StatusLabel(tk.Label):
    """Label for showing success / error messages inline."""

    def __init__(self, parent, **kwargs):
        base_kwargs = dict(
            text="",
            font=FONTS["body_sm"],
            bg=COLORS["bg_dark"],
            fg=COLORS["error"],
            wraplength=380,
            justify="center",
        )

        base_kwargs.update(kwargs)
        super().__init__(parent, **base_kwargs)

    def show_error(self, msg):
        self.configure(text=msg, fg=COLORS["error"])

    def show_success(self, msg):
        self.configure(text=msg, fg=COLORS["success"])

    def clear(self):
        self.configure(text="")


# ─── Styled Button ───────────────────────────────────────────────────────────
class PrimaryButton(tk.Button):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=COLORS["primary"],
            fg=COLORS["bg_dark"],
            activebackground=COLORS["primary_dark"],
            activeforeground=COLORS["bg_dark"],
            relief="flat",
            font=FONTS["button"],
            cursor="hand2",
            bd=0,
            padx=18,
            pady=9,
            **kwargs,
        )


class SecondaryButton(tk.Button):

    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            font=FONTS["button"],
            cursor="hand2",
            bd=0,
            padx=14,
            pady=7,
            **kwargs,
        )


# ─── Section Header ──────────────────────────────────────────────────────────
class SectionHeader(tk.Frame):

    def __init__(self, parent, title, subtitle="", bg=None, **kwargs):
        bg = bg or COLORS["bg_dark"]

        super().__init__(parent, bg=bg, **kwargs)

        tk.Label(
            self,
            text=title,
            font=FONTS["heading_lg"],
            bg=bg,
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(side="left")

        if subtitle:
            tk.Label(
                self,
                text=f"  —  {subtitle}",
                font=FONTS["body"],
                bg=bg,
                fg=COLORS["text_secondary"],
                anchor="w",
            ).pack(side="left", pady=(4, 0))


# ─── Output Box ──────────────────────────────────────────────────────────────
class OutputBox(tk.Frame):

    def __init__(self, parent, height=10, **kwargs):
        bg = kwargs.pop("bg", COLORS["bg_card"])

        super().__init__(parent, bg=bg, **kwargs)

        self.text = tk.Text(
            self,
            height=height,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["primary"],
            relief="flat",
            font=FONTS["mono"],
            state="disabled",
            wrap="word",
            padx=10,
            pady=8,
        )

        scrollbar = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def write(self, text, clear_first=False, tag=None):
        self.text.configure(state="normal")

        if clear_first:
            self.text.delete("1.0", tk.END)

        self.text.insert(tk.END, text + "\n")
        self.text.configure(state="disabled")
        self.text.see(tk.END)

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")


# ─── Divider ────────────────────────────────────────────────────────────────
class Divider(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["border"], height=1, **kwargs)


# ─── Info Row ────────────────────────────────────────────────────────────────
class InfoRow(tk.Frame):

    def __init__(self, parent, label, value, bg=None, **kwargs):
        bg = bg or COLORS["bg_card"]

        super().__init__(parent, bg=bg, **kwargs)

        tk.Label(
            self,
            text=f"{label}:",
            font=FONTS["label"],
            bg=bg,
            fg=COLORS["text_secondary"],
            width=18,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            self,
            text=value,
            font=FONTS["body"],
            bg=bg,
            fg=COLORS["text_primary"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)