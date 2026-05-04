# features/first_aid.py
# Static emergency first aid instruction guide

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import SectionHeader, OutputBox


# ── First Aid knowledge base ──────────────────────────────────────────────────
# Each entry: (emoji, category, title, severity_color, steps_list)
FIRST_AID_DATA = [
    (
        "🚨", "Emergency", "Heart Attack",
        "#EF5350",
        [
            "CALL EMERGENCY SERVICES (911 / 999 / 112) IMMEDIATELY.",
            "Have the person sit or lie down in a comfortable position.",
            "Loosen tight clothing around the neck and chest.",
            "If prescribed, help them take their nitroglycerine.",
            "If they become unconscious and stop breathing, begin CPR.",
            "Give one aspirin (325mg) to chew — if not allergic and conscious.",
            "Stay calm and reassure the person until help arrives.",
            "Do NOT leave them alone.",
        ],
    ),
    (
        "🚨", "Emergency", "Stroke (FAST Protocol)",
        "#EF5350",
        [
            "Use FAST: Face drooping | Arm weakness | Speech difficulty | Time to call 911.",
            "CALL EMERGENCY SERVICES IMMEDIATELY — every minute matters.",
            "Note the exact time symptoms began — tell paramedics.",
            "Keep the person calm and still; lay them on their side if unconscious.",
            "Do NOT give food, water, or medication.",
            "Do NOT leave them alone.",
        ],
    ),
    (
        "🔥", "Burns", "Burns — Minor to Severe",
        "#FF7043",
        [
            "MINOR BURNS (redness, no blisters):",
            "  • Cool the burn with cool (not ice cold) running water for 10–20 minutes.",
            "  • Do NOT use ice, butter, or toothpaste.",
            "  • Cover with a clean, non-fluffy dressing.",
            "  • Take paracetamol for pain relief.",
            "",
            "SEVERE BURNS (large area, deep, or on face/hands/genitals):",
            "  • Call emergency services.",
            "  • Cool the burn while waiting for help.",
            "  • Do NOT remove clothing stuck to the burn.",
            "  • Do NOT burst blisters.",
            "  • Cover loosely with cling film or a clean plastic bag.",
        ],
    ),
    (
        "🩸", "Bleeding", "Severe Bleeding / Cuts",
        "#FF7043",
        [
            "Apply firm, direct pressure with a clean cloth or bandage.",
            "Maintain pressure for at least 10 minutes — do NOT peek.",
            "If the wound is on a limb, raise it above heart level.",
            "If bleeding soaks through, add more cloth on top; do NOT remove the first layer.",
            "For deep wounds or arterial bleeding (bright red, spurting) — call 911.",
            "Once bleeding slows, secure the dressing firmly.",
            "Watch for signs of shock: pale, cold, clammy skin; rapid pulse; confusion.",
        ],
    ),
    (
        "⚡", "Shock", "Anaphylaxis (Severe Allergy)",
        "#EF5350",
        [
            "CALL EMERGENCY SERVICES IMMEDIATELY.",
            "Use epinephrine auto-injector (EpiPen) if available — outer thigh.",
            "Lay the person flat with legs raised (unless breathing is difficult — then sit up).",
            "Give a second EpiPen dose after 5–15 minutes if no improvement.",
            "Even if symptoms improve, the person MUST go to hospital.",
            "Do NOT give antihistamines as a substitute for epinephrine.",
        ],
    ),
    (
        "🧊", "Injuries", "Sprains & Fractures — RICE",
        "#FFB300",
        [
            "RICE Method:",
            "  R — Rest:    Stop activity; do not put weight on the injury.",
            "  I — Ice:     Apply ice pack wrapped in cloth for 20 min every 2 hours.",
            "  C — Compress: Use an elastic bandage — snug but not tight.",
            "  E — Elevate: Keep the injured limb raised above heart level.",
            "",
            "Seek medical attention if:",
            "  • Severe pain or deformity (likely fracture).",
            "  • Numbness, tingling, or the skin is broken.",
            "  • Cannot bear weight at all.",
        ],
    ),
    (
        "🌡️", "Illness", "High Fever",
        "#FFB300",
        [
            "Keep the person cool — remove excess clothing.",
            "Give paracetamol (acetaminophen) or ibuprofen per dosage instructions.",
            "Encourage plenty of fluids (water, diluted juice, electrolyte drinks).",
            "Use lukewarm (not cold) sponging if the fever is very high.",
            "Monitor temperature every 30 minutes.",
            "Seek medical care if fever is above 39.5°C (103°F).",
            "Seek EMERGENCY care if the person has seizures, stiff neck, rash, or confusion.",
            "For children under 3 months — any fever requires immediate medical attention.",
        ],
    ),
    (
        "😮", "Breathing", "Choking — Heimlich Manoeuvre",
        "#EF5350",
        [
            "FOR ADULTS/CHILDREN (over 1 year):",
            "  1. Encourage them to cough forcefully if they can.",
            "  2. Give up to 5 firm back blows between the shoulder blades.",
            "  3. Give up to 5 abdominal thrusts (Heimlich): stand behind, arms around waist,",
            "     fist above navel, pull sharply inward and upward.",
            "  4. Alternate 5 back blows and 5 abdominal thrusts.",
            "  5. Call 911 if the object is not dislodged.",
            "",
            "FOR INFANTS (under 1 year):",
            "  • Use 5 back blows + 5 chest thrusts — NEVER abdominal thrusts.",
        ],
    ),
    (
        "💧", "Illness", "Dehydration",
        "#4CAF50",
        [
            "Mild dehydration:",
            "  • Drink water or oral rehydration solution (ORS) slowly.",
            "  • Avoid alcohol, caffeine, and sugary drinks.",
            "  • Rest and stay in a cool environment.",
            "",
            "Signs of severe dehydration (seek emergency care):",
            "  • No urination for 8+ hours.",
            "  • Sunken eyes, very dry mouth, rapid heart rate.",
            "  • Dizziness preventing standing; confusion.",
            "",
            "Prevention: drink 8–10 glasses of water daily; more during exercise or heat.",
        ],
    ),
    (
        "⚠️", "Poisoning", "Poisoning / Overdose",
        "#EF5350",
        [
            "CALL POISON CONTROL CENTER or EMERGENCY SERVICES immediately.",
            "Do NOT induce vomiting unless specifically instructed by medical professionals.",
            "Try to identify what was ingested — label, quantity, time.",
            "If the person is unconscious but breathing — place in recovery position.",
            "If not breathing — begin CPR.",
            "Do NOT give anything to eat or drink unless instructed.",
            "Keep packaging / substance for medical team to identify.",
        ],
    ),
    (
        "🌊", "Drowning", "Drowning",
        "#EF5350",
        [
            "Ensure your OWN safety before entering water.",
            "Call emergency services (911) immediately.",
            "Reach out with a rope, pole, or throw a flotation device.",
            "Once out of water: lay the person flat.",
            "If unconscious and not breathing — start CPR immediately.",
            "  • 30 chest compressions : 2 rescue breaths.",
            "Continue CPR until help arrives or the person regains consciousness.",
            "Even if the person seems fine — take them to hospital. Secondary drowning is a risk.",
        ],
    ),
    (
        "🐍", "Bites", "Animal Bites & Stings",
        "#FFB300",
        [
            "DOG / ANIMAL BITES:",
            "  • Wash with soap and water for 10 minutes.",
            "  • Apply antiseptic; cover with clean bandage.",
            "  • Seek medical care — rabies prophylaxis may be needed.",
            "",
            "SNAKE BITES:",
            "  • Keep the person calm and still; immobilise bitten limb at heart level.",
            "  • Remove watches, rings near bite area (swelling).",
            "  • Go to hospital IMMEDIATELY — do NOT suck venom or apply tourniquet.",
            "",
            "BEE / WASP STINGS:",
            "  • Remove stinger by scraping (not squeezing).",
            "  • Apply ice pack. Take antihistamine for localised swelling.",
            "  • Watch for anaphylaxis signs — use EpiPen if available.",
        ],
    ),
]


class FirstAid(tk.Frame):
    """First Aid guide — searchable emergency instruction reference."""

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._selected_key = None
        self._build_ui()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg_dark"], pady=PADDING_MD, padx=PADDING_LG)
        hdr.pack(fill="x")
        SectionHeader(hdr, "🚑  First Aid Guide",
                      "Emergency instructions for common situations",
                      bg=COLORS["bg_dark"]).pack(side="left")

        emer_lbl = tk.Label(hdr, text="Emergency? Call 911 / 999 / 112",
                            font=FONTS["heading_sm"], bg=COLORS["bg_dark"],
                            fg=COLORS["error"])
        emer_lbl.pack(side="right")

        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")

        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill="both", expand=True, padx=PADDING_LG, pady=PADDING_LG)

        # ── Left: category list ────────────────────────────────────────────
        left = tk.Frame(body, bg=COLORS["bg_medium"], width=240)
        left.pack(side="left", fill="y", padx=(0, PADDING_MD))
        left.pack_propagate(False)

        tk.Label(left, text="Topics", font=FONTS["heading_sm"],
                 bg=COLORS["bg_medium"], fg=COLORS["primary"],
                 padx=12, pady=10, anchor="w").pack(fill="x")
        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x")

        # Search bar
        search_f = tk.Frame(left, bg=COLORS["bg_medium"], padx=8, pady=6)
        search_f.pack(fill="x")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._filter_list)
        tk.Entry(search_f, textvariable=self._search_var,
                 bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["primary"], relief="flat", font=FONTS["body"]
                 ).pack(fill="x", ipady=6, ipadx=6)

        # Scrollable list
        list_canvas = tk.Canvas(left, bg=COLORS["bg_medium"], highlightthickness=0)
        list_sb = tk.Scrollbar(left, orient="vertical", command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=list_sb.set)
        list_sb.pack(side="right", fill="y")
        list_canvas.pack(fill="both", expand=True)

        self._list_frame = tk.Frame(list_canvas, bg=COLORS["bg_medium"])
        list_canvas.create_window((0, 0), window=self._list_frame, anchor="nw")
        self._list_frame.bind("<Configure>",
                              lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))

        self._list_canvas = list_canvas
        self._render_list(FIRST_AID_DATA)

        # ── Right: instruction display ─────────────────────────────────────
        right = tk.Frame(body, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        self._out = OutputBox(right, height=30)
        self._out.pack(fill="both", expand=True)
        self._out.write("Select an emergency topic from the list on the left.")

    def _render_list(self, items):
        """Populate the topic list."""
        for w in self._list_frame.winfo_children():
            w.destroy()

        for idx, (emoji, category, title, color, _) in enumerate(items):
            row = tk.Frame(self._list_frame, bg=COLORS["bg_medium"], cursor="hand2", pady=2)
            row.pack(fill="x")

            accent = tk.Frame(row, bg=COLORS["bg_medium"], width=4)
            accent.pack(side="left", fill="y")

            content = tk.Frame(row, bg=COLORS["bg_medium"], padx=8)
            content.pack(side="left", fill="x", expand=True)

            cat_lbl = tk.Label(content, text=category, font=FONTS["body_sm"],
                               bg=COLORS["bg_medium"], fg=COLORS["text_muted"], anchor="w")
            cat_lbl.pack(fill="x")

            title_lbl = tk.Label(content, text=f"{emoji}  {title}", font=FONTS["body"],
                                 bg=COLORS["bg_medium"], fg=COLORS["text_primary"], anchor="w")
            title_lbl.pack(fill="x")

            all_w = [row, accent, content, cat_lbl, title_lbl]

            def on_enter(e, aw=all_w, c=color, a=accent):
                for w in aw:
                    if w is not a:
                        w.configure(bg=COLORS["bg_hover"])
                a.configure(bg=c)

            def on_leave(e, aw=all_w, a=accent):
                for w in aw:
                    w.configure(bg=COLORS["bg_medium"])

            def on_click(e, i=idx, data=items):
                self._show_topic(data[i])

            for w in all_w:
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)

            # Divider
            tk.Frame(self._list_frame, bg=COLORS["border"], height=1).pack(fill="x")

    def _filter_list(self, *_):
        term = self._search_var.get().lower()
        filtered = [item for item in FIRST_AID_DATA
                    if term in item[2].lower() or term in item[1].lower()]
        self._render_list(filtered)

    def _show_topic(self, item):
        """Display the selected topic's instructions in the output box."""
        emoji, category, title, color, steps = item

        self._out.clear()
        self._out.write(f"{'='*58}")
        self._out.write(f"  {emoji}  {title.upper()}")
        self._out.write(f"  Category: {category}")
        self._out.write(f"{'='*58}\n")

        for i, step in enumerate(steps, 1):
            if step == "":
                self._out.write("")
            elif step.startswith("  "):
                self._out.write(step)
            else:
                self._out.write(f"  {i}.  {step}")

        self._out.write(f"\n{'─'*58}")
        self._out.write("  ⚕  Always seek professional medical care after first aid.")
        self._out.write("  📞  Emergency: 911 (US) | 999 (UK) | 112 (EU/Global)")