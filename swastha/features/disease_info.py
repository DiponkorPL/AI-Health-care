# features/disease_info.py
# Searchable static disease information database

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import SectionHeader, OutputBox


# ── Disease database ──────────────────────────────────────────────────────────
# Each entry is a dict with consistent keys for clean display.
DISEASE_DB = [
    {
        "name": "Diabetes Mellitus (Type 2)",
        "category": "Metabolic",
        "icd": "E11",
        "overview": (
            "A chronic condition in which the body does not use insulin properly, "
            "leading to elevated blood glucose levels. Type 2 accounts for ~90% of all diabetes cases."
        ),
        "symptoms": [
            "Excessive thirst (polydipsia)",
            "Frequent urination (polyuria)",
            "Unexplained weight loss",
            "Blurred vision",
            "Slow-healing sores",
            "Frequent infections",
            "Fatigue and weakness",
        ],
        "causes": [
            "Insulin resistance in muscles and liver",
            "Genetic predisposition",
            "Obesity and sedentary lifestyle",
            "Unhealthy diet (high sugar/refined carbs)",
            "Age (risk increases after 45)",
        ],
        "diagnosis": [
            "Fasting blood glucose ≥ 126 mg/dL",
            "HbA1c ≥ 6.5%",
            "Oral Glucose Tolerance Test (OGTT)",
            "Random blood glucose ≥ 200 mg/dL with symptoms",
        ],
        "treatment": [
            "Lifestyle: healthy diet, weight loss, 150 min/week exercise",
            "Medications: Metformin (first-line), SGLT2 inhibitors, GLP-1 agonists",
            "Blood sugar monitoring",
            "Regular HbA1c checks (every 3–6 months)",
            "Management of related conditions (BP, cholesterol)",
        ],
        "prevention": [
            "Maintain healthy weight (BMI < 25)",
            "Regular physical activity",
            "Balanced low-GI diet",
            "Avoid smoking and excessive alcohol",
            "Regular health screenings",
        ],
        "prognosis": "Manageable with lifestyle changes and medication. Long-term complications include cardiovascular disease, neuropathy, nephropathy, and retinopathy if poorly controlled.",
    },
    {
        "name": "Hypertension (High Blood Pressure)",
        "category": "Cardiovascular",
        "icd": "I10",
        "overview": (
            "A common condition where the force of blood against artery walls is consistently too high "
            "(≥130/80 mmHg). Often called the 'silent killer' due to lack of obvious symptoms."
        ),
        "symptoms": [
            "Often asymptomatic (no symptoms)",
            "Headaches (severe cases)",
            "Shortness of breath",
            "Nosebleeds (uncommon)",
            "Chest pain (severe hypertension)",
            "Visual disturbances",
        ],
        "causes": [
            "Primary (essential) — no identifiable cause (~90% of cases)",
            "Secondary — kidney disease, hormonal disorders, sleep apnoea",
            "Risk factors: obesity, smoking, high salt diet, stress, family history",
        ],
        "diagnosis": [
            "Blood pressure readings on multiple occasions",
            "Stage 1: 130–139 / 80–89 mmHg",
            "Stage 2: ≥140 / ≥90 mmHg",
            "Ambulatory blood pressure monitoring (24-hour)",
        ],
        "treatment": [
            "Lifestyle: DASH diet, reduce sodium (<2g/day), exercise, weight loss",
            "Medications: ACE inhibitors, ARBs, calcium channel blockers, diuretics",
            "Limit alcohol; quit smoking",
            "Manage stress (meditation, yoga)",
        ],
        "prevention": [
            "Reduce dietary salt",
            "Maintain healthy weight",
            "Regular physical activity",
            "Limit alcohol",
            "No smoking",
            "Manage stress",
        ],
        "prognosis": "Well controlled with medication and lifestyle. Uncontrolled hypertension significantly raises risk of stroke, heart attack, heart failure, and kidney disease.",
    },
    {
        "name": "Asthma",
        "category": "Respiratory",
        "icd": "J45",
        "overview": (
            "A chronic inflammatory disease of the airways causing recurrent episodes of "
            "wheezing, breathlessness, chest tightness, and coughing, particularly at night or early morning."
        ),
        "symptoms": [
            "Wheezing (whistling sound when breathing)",
            "Shortness of breath",
            "Chest tightness",
            "Coughing (worse at night or exercise)",
            "Rapid breathing",
        ],
        "causes": [
            "Allergens (pollen, dust mites, pet dander, mould)",
            "Air pollution and smoke",
            "Exercise (exercise-induced bronchoconstriction)",
            "Respiratory infections",
            "Cold air, stress",
            "Genetic predisposition",
        ],
        "diagnosis": [
            "Spirometry — measures lung function (FEV1/FVC ratio)",
            "Peak flow monitoring",
            "Bronchoprovocation test",
            "Allergy testing",
            "Chest X-ray (to rule out other conditions)",
        ],
        "treatment": [
            "Quick-relief: Short-acting beta-agonists (salbutamol/albuterol inhaler)",
            "Long-term: Inhaled corticosteroids (ICS) — beclometasone",
            "Combination inhalers (ICS + LABA) for moderate-severe cases",
            "Avoid known triggers",
            "Allergy immunotherapy",
        ],
        "prevention": [
            "Identify and avoid personal triggers",
            "Use air purifiers at home",
            "Maintain clean, dust-free environment",
            "Get annual flu vaccine",
            "Follow asthma action plan",
        ],
        "prognosis": "Asthma cannot be cured but can be effectively managed. Most people lead normal, active lives with proper treatment.",
    },
    {
        "name": "Dengue Fever",
        "category": "Infectious Disease",
        "icd": "A90",
        "overview": (
            "A mosquito-borne viral disease caused by the dengue virus (DENV), "
            "transmitted by Aedes aegypti mosquitoes. Endemic in tropical and sub-tropical regions."
        ),
        "symptoms": [
            "Sudden high fever (40°C / 104°F)",
            "Severe headache",
            "Pain behind the eyes",
            "Muscle and joint pain ('breakbone fever')",
            "Nausea and vomiting",
            "Swollen glands",
            "Skin rash (appears 2–5 days after fever)",
            "Bleeding gums/nose (severe dengue)",
        ],
        "causes": [
            "4 dengue virus serotypes (DENV-1 to DENV-4)",
            "Transmitted by female Aedes aegypti mosquito bites",
            "Peak risk: rainy season / standing water near homes",
        ],
        "diagnosis": [
            "NS1 antigen test (early infection — days 1–5)",
            "Dengue IgM/IgG antibody test",
            "Complete Blood Count (CBC) — platelet count",
            "PCR test for virus detection",
        ],
        "treatment": [
            "No specific antiviral treatment exists",
            "Supportive: rest, fluids, paracetamol for fever/pain",
            "AVOID aspirin and ibuprofen (increase bleeding risk)",
            "Hospitalisation for severe dengue (platelet < 100,000)",
            "IV fluid therapy if required",
            "Monitor platelet counts daily during fever",
        ],
        "prevention": [
            "Eliminate standing water (breeding sites)",
            "Use mosquito repellent (DEET-based)",
            "Wear long-sleeved clothing",
            "Use bed nets",
            "Dengvaxia vaccine (for previously infected individuals in endemic areas)",
        ],
        "prognosis": "Most cases resolve in 1–2 weeks. Severe dengue (~5% of cases) can be life-threatening without proper medical care.",
    },
    {
        "name": "Tuberculosis (TB)",
        "category": "Infectious Disease",
        "icd": "A15",
        "overview": (
            "A serious bacterial infection caused by Mycobacterium tuberculosis, "
            "primarily affecting the lungs (pulmonary TB). One of the leading infectious disease killers worldwide."
        ),
        "symptoms": [
            "Persistent cough (3+ weeks), may produce blood",
            "Chest pain",
            "Unintentional weight loss",
            "Fatigue and weakness",
            "Fever and night sweats",
            "Loss of appetite",
        ],
        "causes": [
            "Mycobacterium tuberculosis bacterium",
            "Spread through airborne droplets (coughing, sneezing)",
            "Risk factors: HIV, malnutrition, diabetes, close contact with TB patient",
            "Living in overcrowded conditions",
        ],
        "diagnosis": [
            "Tuberculin skin test (Mantoux test)",
            "Interferon-gamma release assays (IGRAs) — blood test",
            "Chest X-ray",
            "Sputum smear microscopy and culture",
            "GeneXpert MTB/RIF (rapid molecular test)",
        ],
        "treatment": [
            "Standard 6-month regimen: Isoniazid + Rifampicin + Pyrazinamide + Ethambutol",
            "First 2 months: 4 drugs; Last 4 months: 2 drugs (INH + RIF)",
            "MUST complete full course — stopping early causes drug resistance",
            "Directly Observed Therapy (DOT) recommended",
            "Drug-resistant TB (MDR-TB) requires longer treatment (18–24 months)",
        ],
        "prevention": [
            "BCG vaccine (given to infants in high-burden countries)",
            "Treat latent TB infection",
            "Good ventilation in living spaces",
            "Isolate active TB patients during infectious period",
            "Healthcare worker PPE",
        ],
        "prognosis": "Curable with proper antibiotic course. Drug-resistant TB is harder to treat and carries higher mortality.",
    },
    {
        "name": "Major Depressive Disorder",
        "category": "Mental Health",
        "icd": "F32",
        "overview": (
            "A common and serious mental health condition characterised by persistent low mood, "
            "loss of interest, and a range of emotional, cognitive, and physical symptoms that "
            "significantly impair daily functioning."
        ),
        "symptoms": [
            "Persistent sadness or empty feeling",
            "Loss of interest in previously enjoyed activities",
            "Changes in appetite (weight loss or gain)",
            "Sleep disturbances (insomnia or hypersomnia)",
            "Fatigue and loss of energy",
            "Difficulty concentrating or making decisions",
            "Feelings of worthlessness or excessive guilt",
            "Thoughts of death or suicide",
        ],
        "causes": [
            "Biological: neurotransmitter imbalance (serotonin, dopamine)",
            "Genetic predisposition",
            "Traumatic life events or chronic stress",
            "Medical conditions (thyroid disorders, chronic pain)",
            "Certain medications",
            "Substance abuse",
        ],
        "diagnosis": [
            "Clinical interview using DSM-5 criteria",
            "PHQ-9 depression screening questionnaire",
            "Rule out medical causes: thyroid function tests, blood tests",
            "Assessment of suicide risk",
        ],
        "treatment": [
            "Psychotherapy: Cognitive Behavioural Therapy (CBT) — first-line",
            "Medications: SSRIs (fluoxetine, sertraline), SNRIs, tricyclics",
            "Combination of therapy + medication most effective",
            "Lifestyle: exercise, sleep hygiene, social support",
            "ECT (electroconvulsive therapy) for severe/treatment-resistant cases",
        ],
        "prevention": [
            "Build strong social connections",
            "Regular physical exercise",
            "Stress management techniques",
            "Seek help early at first signs",
            "Limit alcohol and substance use",
        ],
        "prognosis": "Highly treatable — 80–90% of people respond to treatment. Without treatment, episodes may become more frequent and severe.",
    },
    {
        "name": "Chronic Kidney Disease (CKD)",
        "category": "Renal",
        "icd": "N18",
        "overview": (
            "A long-term condition where the kidneys don't work as well as they should, "
            "gradually losing their ability to filter waste and excess fluids from blood. "
            "Often progresses silently over years."
        ),
        "symptoms": [
            "Fatigue and weakness",
            "Swelling in ankles/feet (oedema)",
            "Shortness of breath",
            "Nausea and vomiting",
            "Decreased urine output",
            "Foamy/bloody urine",
            "Persistent itching",
            "High blood pressure",
        ],
        "causes": [
            "Diabetes mellitus (leading cause)",
            "Hypertension (second leading cause)",
            "Glomerulonephritis",
            "Polycystic kidney disease (genetic)",
            "Repeated kidney infections",
            "Long-term NSAID use",
        ],
        "diagnosis": [
            "Serum creatinine and estimated GFR (eGFR)",
            "Urine albumin-to-creatinine ratio (ACR)",
            "Kidney ultrasound",
            "Kidney biopsy (in certain cases)",
            "Blood tests: BUN, electrolytes",
        ],
        "treatment": [
            "Control underlying causes (diabetes, hypertension)",
            "Low-protein, low-salt, low-potassium diet",
            "ACE inhibitors / ARBs to protect kidneys",
            "Avoid nephrotoxic drugs (NSAIDs, contrast dye)",
            "Dialysis (haemodialysis or peritoneal) for advanced CKD",
            "Kidney transplant for end-stage renal disease",
        ],
        "prevention": [
            "Control blood sugar and blood pressure",
            "Stay well hydrated",
            "Maintain healthy weight",
            "Avoid excessive painkiller use",
            "Regular kidney function checks if at risk",
        ],
        "prognosis": "Progression can be slowed with early detection and management. End-stage kidney disease requires dialysis or transplant.",
    },
    {
        "name": "Malaria",
        "category": "Infectious Disease",
        "icd": "B50",
        "overview": (
            "A life-threatening parasitic disease caused by Plasmodium parasites, "
            "transmitted to humans through bites of infected female Anopheles mosquitoes. "
            "Preventable and curable."
        ),
        "symptoms": [
            "Cyclical fever and chills",
            "Profuse sweating",
            "Headache",
            "Nausea and vomiting",
            "Muscle aches",
            "Fatigue",
            "Jaundice (in severe malaria)",
            "Impaired consciousness (severe — cerebral malaria)",
        ],
        "causes": [
            "Plasmodium falciparum (most deadly)",
            "Plasmodium vivax (most common worldwide)",
            "P. malariae, P. ovale, P. knowlesi",
            "Transmitted by female Anopheles mosquito",
        ],
        "diagnosis": [
            "Rapid Diagnostic Test (RDT) — detects malaria antigens",
            "Blood smear microscopy (gold standard)",
            "PCR for species confirmation",
            "Complete blood count (haemolytic anaemia)",
        ],
        "treatment": [
            "Artemisinin-based combination therapy (ACT) — first-line",
            "Chloroquine for P. vivax (where sensitive)",
            "Primaquine for P. vivax/P. ovale radical cure (check G6PD first)",
            "IV Artesunate for severe malaria — hospital admission",
            "Supportive: antipyretics, IV fluids",
        ],
        "prevention": [
            "Insecticide-treated bed nets (ITNs)",
            "Indoor residual spraying (IRS)",
            "Mosquito repellent and protective clothing",
            "Chemoprophylaxis for travellers to endemic areas",
            "RTS,S/AS01 (Mosquirix) vaccine for children in high-risk areas",
        ],
        "prognosis": "Uncomplicated malaria: full recovery with prompt treatment. Severe malaria: 15–20% mortality even with treatment.",
    },
]


class DiseaseInfo(tk.Frame):
    """Comprehensive searchable disease information database."""

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._all_data = DISEASE_DB
        self._build_ui()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg_dark"], pady=PADDING_MD, padx=PADDING_LG)
        hdr.pack(fill="x")
        SectionHeader(hdr, "📋  Disease Information",
                      f"{len(DISEASE_DB)} conditions in database",
                      bg=COLORS["bg_dark"]).pack(side="left")

        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill="both", expand=True, padx=PADDING_LG, pady=(0, PADDING_LG))

        # ── Left: search + list ────────────────────────────────────────────
        left = tk.Frame(body, bg=COLORS["bg_medium"], width=260)
        left.pack(side="left", fill="y", padx=(0, PADDING_MD))
        left.pack_propagate(False)

        # Search
        search_frame = tk.Frame(left, bg=COLORS["bg_medium"], pady=8, padx=8)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="🔍  Search", font=FONTS["heading_sm"],
                 bg=COLORS["bg_medium"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 4))

        border = tk.Frame(search_frame, bg=COLORS["border_light"], padx=1, pady=1)
        border.pack(fill="x")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._filter)
        tk.Entry(border, textvariable=self._search_var,
                 bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["primary"], relief="flat", font=FONTS["body"]
                 ).pack(fill="x", ipady=7, ipadx=8)

        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x")

        # Category filter
        self._cat_var = tk.StringVar(value="All Categories")
        cats = ["All Categories"] + sorted({d["category"] for d in DISEASE_DB})
        cat_menu = tk.OptionMenu(left, self._cat_var, *cats, command=lambda _: self._filter())
        cat_menu.configure(bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                           relief="flat", font=FONTS["body_sm"], highlightthickness=0,
                           activebackground=COLORS["bg_hover"], activeforeground=COLORS["text_primary"])
        cat_menu["menu"].configure(bg=COLORS["bg_input"], fg=COLORS["text_primary"])
        cat_menu.pack(fill="x", padx=8, pady=6)

        # Disease list
        list_canvas = tk.Canvas(left, bg=COLORS["bg_medium"], highlightthickness=0)
        list_sb = tk.Scrollbar(left, orient="vertical", command=list_canvas.yview)
        list_canvas.configure(yscrollcommand=list_sb.set)
        list_sb.pack(side="right", fill="y")
        list_canvas.pack(fill="both", expand=True)

        self._list_frame = tk.Frame(list_canvas, bg=COLORS["bg_medium"])
        list_canvas.create_window((0, 0), window=self._list_frame, anchor="nw")
        self._list_frame.bind("<Configure>",
                              lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        self._render_list(DISEASE_DB)

        # ── Right: detail view ─────────────────────────────────────────────
        right = tk.Frame(body, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        self._out = OutputBox(right, height=32)
        self._out.pack(fill="both", expand=True)
        self._out.write("Select a disease from the list on the left to view details.")

    def _render_list(self, items):
        for w in self._list_frame.winfo_children():
            w.destroy()

        cat_colors = {
            "Cardiovascular": "#EF5350",
            "Metabolic":       "#FFB300",
            "Respiratory":     "#29B6F6",
            "Infectious Disease": "#66BB6A",
            "Mental Health":   "#AB47BC",
            "Renal":           "#FF7043",
        }

        for disease in items:
            color = cat_colors.get(disease["category"], COLORS["secondary"])

            row = tk.Frame(self._list_frame, bg=COLORS["bg_medium"], cursor="hand2")
            row.pack(fill="x")

            accent = tk.Frame(row, bg=color, width=4)
            accent.pack(side="left", fill="y")

            content = tk.Frame(row, bg=COLORS["bg_medium"], padx=10, pady=8)
            content.pack(side="left", fill="x", expand=True)

            name_lbl = tk.Label(content, text=disease["name"], font=FONTS["body"],
                                bg=COLORS["bg_medium"], fg=COLORS["text_primary"], anchor="w",
                                wraplength=200, justify="left")
            name_lbl.pack(fill="x")

            cat_lbl = tk.Label(content, text=disease["category"], font=FONTS["body_sm"],
                               bg=COLORS["bg_medium"], fg=color, anchor="w")
            cat_lbl.pack(fill="x")

            all_w = [row, content, name_lbl, cat_lbl]

            def on_enter(e, aw=all_w, a=accent):
                for w in aw:
                    w.configure(bg=COLORS["bg_hover"])

            def on_leave(e, aw=all_w):
                for w in aw:
                    w.configure(bg=COLORS["bg_medium"])

            def on_click(e, d=disease):
                self._show_disease(d)

            for w in all_w + [accent]:
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)

            tk.Frame(self._list_frame, bg=COLORS["border"], height=1).pack(fill="x")

    def _filter(self, *_):
        term = self._search_var.get().lower()
        cat  = self._cat_var.get()

        results = [
            d for d in DISEASE_DB
            if (term in d["name"].lower() or term in d["category"].lower())
            and (cat == "All Categories" or d["category"] == cat)
        ]
        self._render_list(results)

    def _show_disease(self, d: dict):
        """Render full disease detail in the output box."""
        self._out.clear()

        self._out.write("=" * 60)
        self._out.write(f"  {d['name']}")
        self._out.write(f"  Category: {d['category']}   |   ICD-10: {d['icd']}")
        self._out.write("=" * 60)

        self._out.write(f"\n  OVERVIEW\n  {d['overview']}\n")

        sections = [
            ("SYMPTOMS",     d["symptoms"]),
            ("CAUSES / RISK FACTORS", d["causes"]),
            ("DIAGNOSIS",    d["diagnosis"]),
            ("TREATMENT",    d["treatment"]),
            ("PREVENTION",   d["prevention"]),
        ]

        for heading, items in sections:
            self._out.write(f"{'─'*60}")
            self._out.write(f"  {heading}")
            for item in items:
                if item:
                    self._out.write(f"    • {item}")
            self._out.write("")

        self._out.write("─" * 60)
        self._out.write(f"  PROGNOSIS\n  {d['prognosis']}")
        self._out.write("─" * 60)
        self._out.write("\n  ⚕  Always consult a licensed physician for diagnosis and treatment.")