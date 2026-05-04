# features/disease_prediction.py
# Rule-based disease prediction from selected symptoms

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import Card, PrimaryButton, SecondaryButton, OutputBox, SectionHeader


# ── Rule database: symptom-sets → disease ────────────────────────────────────
# Each entry: (frozenset_of_key_symptoms, disease_name, description, severity)
DISEASE_RULES = [
    (
        {"fever", "cough", "sore throat", "runny nose"},
        "Common Cold",
        "A viral infection of the upper respiratory tract. Usually resolves in 7–10 days with rest and fluids.",
        "Mild",
    ),
    (
        {"fever", "cough", "body ache", "fatigue", "headache", "chills"},
        "Influenza (Flu)",
        "A contagious respiratory illness caused by influenza viruses. Rest, fluids, and antivirals may help.",
        "Moderate",
    ),
    (
        {"fever", "cough", "shortness of breath", "chest pain", "fatigue"},
        "COVID-19 / Pneumonia",
        "Respiratory infection possibly involving the lungs. Seek immediate medical evaluation.",
        "High",
    ),
    (
        {"headache", "fever", "stiff neck", "sensitivity to light", "nausea"},
        "Meningitis",
        "Inflammation of the membranes surrounding the brain and spinal cord. SEEK EMERGENCY CARE.",
        "Critical",
    ),
    (
        {"chest pain", "shortness of breath", "sweating", "nausea", "arm pain"},
        "Heart Attack (Suspected)",
        "Classic symptoms of a myocardial infarction. CALL EMERGENCY SERVICES IMMEDIATELY.",
        "Critical",
    ),
    (
        {"abdominal pain", "nausea", "vomiting", "diarrhea", "fever"},
        "Gastroenteritis",
        "Stomach flu — usually caused by a virus or contaminated food. Stay hydrated.",
        "Mild",
    ),
    (
        {"frequent urination", "burning urination", "lower back pain", "fever"},
        "Urinary Tract Infection (UTI)",
        "Bacterial infection of the urinary system. Antibiotics prescribed by a doctor are required.",
        "Moderate",
    ),
    (
        {"joint pain", "swelling", "stiffness", "fatigue"},
        "Arthritis",
        "Inflammation of joints. Consult a rheumatologist for a proper diagnosis and treatment plan.",
        "Moderate",
    ),
    (
        {"skin rash", "itching", "redness", "swelling"},
        "Allergic Reaction / Dermatitis",
        "May be contact allergy, eczema, or urticaria. Avoid known triggers and consult a dermatologist.",
        "Mild",
    ),
    (
        {"excessive thirst", "frequent urination", "fatigue", "blurred vision", "weight loss"},
        "Diabetes (Suspected)",
        "Symptoms suggest elevated blood sugar. Consult a physician for blood glucose testing.",
        "Moderate",
    ),
    (
        {"severe headache", "dizziness", "vision problems", "nausea"},
        "Migraine",
        "Intense recurring headaches often with aura. Rest in a dark room; consult a neurologist.",
        "Moderate",
    ),
    (
        {"wheezing", "shortness of breath", "chest tightness", "cough"},
        "Asthma",
        "A chronic respiratory condition causing airway inflammation. Use prescribed inhalers.",
        "Moderate",
    ),
    (
        {"yellowing skin", "dark urine", "abdominal pain", "fatigue", "nausea"},
        "Jaundice / Hepatitis",
        "Liver involvement indicated. Seek prompt medical attention for liver function tests.",
        "High",
    ),
    (
        {"cold hands", "fatigue", "pale skin", "dizziness", "shortness of breath"},
        "Anemia",
        "Low red blood cell count. Dietary changes or supplements — consult a physician.",
        "Mild",
    ),
    (
        {"high fever", "rash", "muscle pain", "behind-eye pain"},
        "Dengue Fever",
        "Mosquito-borne viral disease. Hospitalisation may be required. Avoid aspirin.",
        "High",
    ),
]

ALL_SYMPTOMS = sorted({s for rule in DISEASE_RULES for s in rule[0]})

SEVERITY_COLORS = {
    "Mild":     "#4CAF50",
    "Moderate": "#FFB300",
    "High":     "#FF7043",
    "Critical": "#EF5350",
}


class DiseasePrediction(tk.Frame):
    """
    Rule-based disease prediction panel.
    User selects symptoms via checkboxes → app scores rules → shows best matches.
    """

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._sym_vars: dict[str, tk.BooleanVar] = {}
        self._build_ui()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Main scrollable layout
        canvas = tk.Canvas(self, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLORS["bg_dark"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._fill(inner)

    def _fill(self, parent):
        p = PADDING_LG

        # ── Header ─────────────────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", padx=p, pady=(p, PADDING_MD))
        SectionHeader(hdr, "🩺  Disease Prediction",
                      "Select your symptoms below", bg=COLORS["bg_dark"]).pack(side="left")

        # ── Disclaimer ─────────────────────────────────────────────────────
        disc = tk.Frame(parent, bg="#1A2A1A", pady=8, padx=14)
        disc.pack(fill="x", padx=p, pady=(0, PADDING_MD))
        tk.Label(
            disc,
            text="⚠️  This tool provides general guidance only. "
                 "Always consult a qualified medical professional for diagnosis.",
            font=FONTS["body_sm"],
            bg="#1A2A1A",
            fg="#88CC88",
            wraplength=800,
            justify="left",
        ).pack(anchor="w")

        # ── Symptom selector + results (side by side) ──────────────────────
        columns = tk.Frame(parent, bg=COLORS["bg_dark"])
        columns.pack(fill="both", expand=True, padx=p, pady=(0, p))

        # Left: symptom checkboxes
        left = Card(columns, title="Select Symptoms", accent=COLORS["primary"])
        left.pack(side="left", fill="both", expand=True, padx=(0, PADDING_MD))

        search_frame = tk.Frame(left, bg=COLORS["bg_card"], padx=PADDING_MD, pady=8)
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="Filter:", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._filter_symptoms)
        tk.Entry(search_frame, textvariable=self._search_var,
                 bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["primary"], relief="flat",
                 font=FONTS["body"]).pack(side="left", fill="x", expand=True,
                                          padx=(8, 0), ipady=5, ipadx=6)

        # Scrollable checkbox area
        cb_canvas = tk.Canvas(left, bg=COLORS["bg_card"], highlightthickness=0, height=320)
        cb_scroll = tk.Scrollbar(left, orient="vertical", command=cb_canvas.yview)
        cb_canvas.configure(yscrollcommand=cb_scroll.set)
        cb_scroll.pack(side="right", fill="y")
        cb_canvas.pack(fill="both", expand=True, padx=PADDING_MD)

        self._cb_frame = tk.Frame(cb_canvas, bg=COLORS["bg_card"])
        cb_canvas.create_window((0, 0), window=self._cb_frame, anchor="nw")
        self._cb_frame.bind("<Configure>",
                            lambda e: cb_canvas.configure(scrollregion=cb_canvas.bbox("all")))

        self._cb_canvas = cb_canvas
        self._render_checkboxes(ALL_SYMPTOMS)

        # Buttons under checkboxes
        btn_row = tk.Frame(left, bg=COLORS["bg_card"], pady=10, padx=PADDING_MD)
        btn_row.pack(fill="x")
        PrimaryButton(btn_row, "  Predict Disease  ", command=self._predict).pack(side="left")
        SecondaryButton(btn_row, "  Clear All  ", command=self._clear_all).pack(side="left", padx=(8, 0))

        # Right: results
        right = tk.Frame(columns, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        result_card = Card(right, title="Prediction Results", accent=COLORS["secondary"])
        result_card.pack(fill="both", expand=True)

        self._result_box = OutputBox(result_card, height=22)
        self._result_box.pack(fill="both", expand=True, padx=PADDING_MD, pady=PADDING_MD)
        self._result_box.write("Select symptoms on the left, then click 'Predict Disease'.")

    def _render_checkboxes(self, symptoms):
        """(Re-)populate the checkbox grid with given symptom list."""
        for w in self._cb_frame.winfo_children():
            w.destroy()

        for sym in symptoms:
            if sym not in self._sym_vars:
                self._sym_vars[sym] = tk.BooleanVar()
            var = self._sym_vars[sym]

            cb = tk.Checkbutton(
                self._cb_frame,
                text=sym.capitalize(),
                variable=var,
                bg=COLORS["bg_card"],
                fg=COLORS["text_primary"],
                selectcolor=COLORS["bg_input"],
                activebackground=COLORS["bg_card"],
                activeforeground=COLORS["primary"],
                font=FONTS["body"],
                anchor="w",
                relief="flat",
                cursor="hand2",
            )
            cb.pack(fill="x", padx=6, pady=2)

    def _filter_symptoms(self, *_):
        """Filter visible checkboxes by search term."""
        term = self._search_var.get().lower()
        filtered = [s for s in ALL_SYMPTOMS if term in s.lower()]
        self._render_checkboxes(filtered)

    def _clear_all(self):
        """Uncheck all symptoms."""
        for var in self._sym_vars.values():
            var.set(False)
        self._result_box.clear()
        self._result_box.write("Symptoms cleared. Select new symptoms and click 'Predict Disease'.")

    # ── Prediction Logic ───────────────────────────────────────────────────────
    def _predict(self):
        """Score rules against selected symptoms and display top matches."""
        selected = {sym for sym, var in self._sym_vars.items() if var.get()}

        if not selected:
            self._result_box.clear()
            self._result_box.write("⚠  Please select at least one symptom.")
            return

        # Score each rule by how many of its key symptoms are present
        scores = []
        for rule_symptoms, disease, description, severity in DISEASE_RULES:
            matched = selected & rule_symptoms
            if matched:
                score = len(matched) / len(rule_symptoms)   # coverage ratio
                scores.append((score, len(matched), disease, description, severity, rule_symptoms))

        scores.sort(key=lambda x: (x[0], x[1]), reverse=True)

        self._result_box.clear()
        self._result_box.write(f"Symptoms entered: {', '.join(sorted(selected))}\n")
        self._result_box.write("=" * 55)

        if not scores:
            self._result_box.write(
                "\n⚠  No matching conditions found.\n"
                "   Please consult a healthcare professional."
            )
            return

        self._result_box.write(f"\n  Top {min(3, len(scores))} possible condition(s):\n")

        for rank, (score, matched_count, disease, desc, severity, rule_syms) in enumerate(scores[:3], 1):
            pct = int(score * 100)
            sev_label = f"[{severity}]"
            matched_syms = sorted(selected & rule_syms)

            self._result_box.write(f"\n{'─'*50}")
            self._result_box.write(f"  #{rank}  {disease}  {sev_label}")
            self._result_box.write(f"  Match: {pct}%  ({matched_count} of {len(rule_syms)} key symptoms)")
            self._result_box.write(f"  Matched: {', '.join(matched_syms)}")
            self._result_box.write(f"\n  {desc}")

        self._result_box.write(f"\n{'='*55}")
        self._result_box.write(
            "\n⚕  IMPORTANT: This is not a medical diagnosis.\n"
            "   Please consult a licensed physician for proper evaluation."
        )