# features/medicine_reminder.py
# Add, view, and delete medicine reminders stored in MySQL

import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import (Card, LabeledEntry, PrimaryButton,
                            SecondaryButton, SectionHeader, StatusLabel)
from db.db_connection import get_db

FREQUENCY_OPTIONS = ["Daily", "Twice a day", "Three times a day", "Weekly", "As needed"]


class MedicineReminder(tk.Frame):
    """
    Medicine reminder panel.
    - Add a reminder with name, time, frequency, and notes.
    - Displays all reminders for the logged-in user.
    - Delete individual reminders.
    """

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._build_ui()
        self._load_reminders()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg_dark"], pady=PADDING_MD, padx=PADDING_LG)
        hdr.pack(fill="x")
        SectionHeader(hdr, "💊  Medicine Reminder",
                      "Manage your daily medications", bg=COLORS["bg_dark"]).pack(side="left")

        # Two-column layout: form | list
        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill="both", expand=True, padx=PADDING_LG, pady=(0, PADDING_LG))

        # ── Left: Add Reminder Form ────────────────────────────────────────
        left = Card(body, title="Add New Reminder", accent=COLORS["primary"])
        left.pack(side="left", fill="y", padx=(0, PADDING_MD), ipadx=4)

        form = tk.Frame(left, bg=COLORS["bg_card"], padx=PADDING_MD, pady=PADDING_MD)
        form.pack(fill="both", expand=True)

        self.med_name = LabeledEntry(form, "Medicine Name", bg=COLORS["bg_card"])
        self.med_name.pack(fill="x", pady=(0, 10))

        self.med_time = LabeledEntry(form, "Reminder Time  (e.g. 08:00 AM)", bg=COLORS["bg_card"])
        self.med_time.pack(fill="x", pady=(0, 10))

        # Frequency dropdown
        tk.Label(form, text="Frequency", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x", pady=(0, 3))

        self._freq_var = tk.StringVar(value=FREQUENCY_OPTIONS[0])
        freq_menu = tk.OptionMenu(form, self._freq_var, *FREQUENCY_OPTIONS)
        freq_menu.configure(
            bg=COLORS["bg_input"], fg=COLORS["text_primary"],
            activebackground=COLORS["bg_hover"], activeforeground=COLORS["text_primary"],
            relief="flat", font=FONTS["body"], highlightthickness=0,
        )
        freq_menu["menu"].configure(bg=COLORS["bg_input"], fg=COLORS["text_primary"])
        freq_menu.pack(fill="x", pady=(0, 10))

        # Notes
        tk.Label(form, text="Notes (optional)", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x", pady=(0, 3))
        notes_border = tk.Frame(form, bg=COLORS["border_light"], padx=1, pady=1)
        notes_border.pack(fill="x")
        self.notes_text = tk.Text(
            notes_border, height=4,
            bg=COLORS["bg_input"], fg=COLORS["text_primary"],
            insertbackground=COLORS["primary"], relief="flat", font=FONTS["body"],
            padx=8, pady=6, wrap="word",
        )
        self.notes_text.pack(fill="x")

        self._form_status = StatusLabel(form, bg=COLORS["bg_card"])
        self._form_status.pack(fill="x", pady=(8, 4))

        PrimaryButton(form, "  Add Reminder  ", command=self._add_reminder).pack(fill="x", pady=(0, 4))
        SecondaryButton(form, "  Clear Form  ", command=self._clear_form).pack(fill="x")

        # ── Right: Reminder List ───────────────────────────────────────────
        right = tk.Frame(body, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        list_card = Card(right, title="Your Reminders", accent=COLORS["secondary"])
        list_card.pack(fill="both", expand=True)

        # Treeview table
        cols = ("Medicine", "Time", "Frequency", "Notes")
        tree_frame = tk.Frame(list_card, bg=COLORS["bg_card"])
        tree_frame.pack(fill="both", expand=True, padx=PADDING_MD, pady=PADDING_MD)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Rem.Treeview",
                        background=COLORS["bg_input"],
                        foreground=COLORS["text_primary"],
                        fieldbackground=COLORS["bg_input"],
                        rowheight=32,
                        font=FONTS["body"])
        style.configure("Rem.Treeview.Heading",
                        background=COLORS["bg_medium"],
                        foreground=COLORS["primary"],
                        font=FONTS["heading_sm"])
        style.map("Rem.Treeview", background=[("selected", COLORS["primary"])],
                  foreground=[("selected", COLORS["bg_dark"])])

        self._tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                   style="Rem.Treeview", selectmode="browse")
        col_widths = {"Medicine": 160, "Time": 100, "Frequency": 130, "Notes": 220}
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=col_widths[col], anchor="w")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)

        # Buttons under table
        btn_row = tk.Frame(list_card, bg=COLORS["bg_card"], padx=PADDING_MD, pady=8)
        btn_row.pack(fill="x")
        SecondaryButton(btn_row, "🔄  Refresh", command=self._load_reminders).pack(side="left")
        tk.Button(
            btn_row, text="🗑  Delete Selected",
            font=FONTS["button"], bg=COLORS["error"], fg="white",
            activebackground="#C62828", activeforeground="white",
            relief="flat", cursor="hand2", bd=0, padx=12, pady=7,
            command=self._delete_reminder,
        ).pack(side="right")

        # Row ID mapping: tree item → DB id
        self._id_map: dict[str, int] = {}

    # ── Data Operations ────────────────────────────────────────────────────────
    def _load_reminders(self):
        """Fetch all reminders for the current user and populate the table."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._id_map.clear()

        conn = get_db()
        if not conn:
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM medicine_reminders WHERE user_id = %s ORDER BY reminder_time",
                (self.user["id"],),
            )
            rows = cursor.fetchall()
            cursor.close()
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=self)
            return

        for row in rows:
            item_id = self._tree.insert(
                "", "end",
                values=(row["medicine_name"], row["reminder_time"],
                        row["frequency"], row["notes"] or ""),
            )
            self._id_map[item_id] = row["id"]

        if not rows:
            self._tree.insert("", "end", values=("No reminders yet", "", "", ""))

    def _add_reminder(self):
        """Insert a new reminder into the database."""
        name  = self.med_name.get().strip()
        time  = self.med_time.get().strip()
        freq  = self._freq_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not name:
            self._form_status.show_error("Medicine name is required.")
            return
        if not time:
            self._form_status.show_error("Reminder time is required.")
            return

        conn = get_db()
        if not conn:
            self._form_status.show_error("Database connection failed.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO medicine_reminders (user_id, medicine_name, reminder_time, frequency, notes) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.user["id"], name, time, freq, notes or None),
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            self._form_status.show_error(f"Error: {e}")
            return

        self._form_status.show_success(f"✔  '{name}' reminder added successfully.")
        self._clear_form()
        self._load_reminders()

    def _delete_reminder(self):
        """Delete the selected reminder from the database."""
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reminder to delete.", parent=self)
            return

        item_id = selected[0]
        db_id   = self._id_map.get(item_id)
        if db_id is None:
            return   # Placeholder row

        name = self._tree.item(item_id, "values")[0]
        if not messagebox.askyesno("Confirm Delete", f"Delete reminder for '{name}'?", parent=self):
            return

        conn = get_db()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicine_reminders WHERE id = %s AND user_id = %s",
                           (db_id, self.user["id"]))
            conn.commit()
            cursor.close()
        except Exception as e:
            messagebox.showerror("DB Error", str(e), parent=self)
            return

        self._load_reminders()

    def _clear_form(self):
        """Reset all form fields."""
        self.med_name.clear()
        self.med_time.clear()
        self._freq_var.set(FREQUENCY_OPTIONS[0])
        self.notes_text.delete("1.0", tk.END)
        self._form_status.clear()