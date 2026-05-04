# features/chatbot.py
# Keyword-based AI health chatbot with a chat-bubble UI

import tkinter as tk
from tkinter import ttk
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import SectionHeader, PrimaryButton


# ── Knowledge base: keyword lists → response ──────────────────────────────────
KB = [
    # (keywords_that_must_match_any, response)
    (["hello", "hi", "hey", "greet"],
     "Hello! 👋 I'm your Swastha health assistant. How can I help you today?"),

    (["headache", "head pain", "migraine"],
     "Headaches can be caused by dehydration, stress, eye strain, or tension. "
     "Drink water, rest in a quiet dark room, and consider a mild painkiller. "
     "If headaches are severe, frequent, or come with vomiting/vision changes, see a doctor."),

    (["fever", "temperature", "hot"],
     "For fever, drink plenty of fluids, rest, and you can take paracetamol (acetaminophen) "
     "to reduce temperature. See a doctor if fever exceeds 39°C (102°F), lasts more than 3 days, "
     "or is accompanied by a rash or difficulty breathing."),

    (["cough", "cold", "runny nose", "sneezing"],
     "For a common cold: rest, stay hydrated, use saline nasal spray, and try honey & ginger tea. "
     "Symptoms usually resolve in 7–10 days. If cough persists beyond 2 weeks or you have breathing "
     "difficulty, consult a physician."),

    (["stomach", "abdominal", "belly", "digestion", "nausea"],
     "Stomach discomfort can be caused by indigestion, gastritis, or food intolerance. "
     "Try the BRAT diet (bananas, rice, applesauce, toast). Avoid spicy or fatty foods. "
     "Seek care if you experience severe pain, blood in stool, or persistent vomiting."),

    (["diabetes", "blood sugar", "glucose"],
     "Diabetes management includes monitoring blood sugar, a balanced low-GI diet, "
     "regular exercise (30 min/day), and prescribed medication. "
     "Common symptoms: excessive thirst, frequent urination, fatigue, and blurred vision."),

    (["blood pressure", "hypertension", "bp"],
     "To manage blood pressure: reduce salt intake, exercise regularly, "
     "limit alcohol, quit smoking, and manage stress. "
     "Normal BP is around 120/80 mmHg. Above 130/80 is considered high — consult your doctor."),

    (["sleep", "insomnia", "tired"],
     "For better sleep: maintain a consistent schedule, avoid screens 1 hour before bed, "
     "limit caffeine after noon, and keep your room cool and dark. "
     "Adults need 7–9 hours per night for optimal health."),

    (["stress", "anxiety", "anxious", "panic"],
     "Managing anxiety: practice deep breathing (4-7-8 technique), mindfulness meditation, "
     "regular exercise, and limit caffeine. Talk to a trusted person. "
     "If anxiety is affecting daily life, consider speaking with a mental health professional."),

    (["depression", "sad", "hopeless", "unhappy"],
     "Feeling persistently low is important to address. Speak with a trusted friend, family member, "
     "or mental health professional. Regular exercise, sunlight, and social connection can help. "
     "If you're in crisis, please contact a helpline immediately. You are not alone. 💙"),

    (["diet", "nutrition", "food", "eat", "weight"],
     "A healthy diet includes: plenty of vegetables, fruits, whole grains, lean proteins, and healthy fats. "
     "Limit processed foods, sugar, and excess salt. "
     "Stay hydrated — aim for 8 glasses of water daily."),

    (["exercise", "workout", "fitness"],
     "The WHO recommends at least 150 minutes of moderate aerobic activity per week, "
     "plus muscle-strengthening activities twice a week. "
     "Even a 30-minute daily walk significantly improves cardiovascular health."),

    (["vitamin", "supplement", "deficiency"],
     "Common deficiencies include Vitamin D (fatigue, bone pain), Iron (anaemia), "
     "B12 (nerve issues), and Calcium (weak bones). "
     "Get blood tests done before starting supplements — excess can also be harmful."),

    (["skin", "rash", "acne", "eczema", "allergy"],
     "Skin issues: keep skin clean and moisturised, avoid known triggers, and use sunscreen daily. "
     "For rashes, avoid scratching. If a rash spreads rapidly, is painful, or comes with fever, "
     "see a dermatologist promptly."),

    (["back pain", "spine", "posture"],
     "For back pain: maintain good posture, strengthen core muscles, use an ergonomic chair, "
     "and avoid lifting heavy objects with your back. "
     "Physiotherapy is highly effective. Seek care for numbness or radiating leg pain."),

    (["heart", "chest", "cardiac"],
     "Chest pain should always be taken seriously. "
     "If you experience sudden chest pain, pressure, or pain radiating to your arm or jaw, "
     "call emergency services immediately. For heart health: eat well, exercise, quit smoking, "
     "and control blood pressure."),

    (["medicine", "medication", "drug", "dose"],
     "Never self-prescribe or adjust medication without consulting your doctor. "
     "Always complete the full course of antibiotics. Store medicines as directed on the label. "
     "Check for drug interactions if taking multiple medications."),

    (["pregnant", "pregnancy"],
     "During pregnancy: take prenatal vitamins (especially folic acid), "
     "attend regular antenatal check-ups, avoid alcohol and smoking, "
     "and eat a balanced nutritious diet. Consult your OB/GYN for personalised guidance."),

    (["child", "baby", "infant", "kid"],
     "Children's health: ensure vaccinations are up to date, promote regular physical activity, "
     "limit screen time, serve balanced meals, and ensure adequate sleep. "
     "For illness symptoms in infants, always consult a paediatrician."),

    (["covid", "coronavirus", "pandemic"],
     "COVID-19 symptoms: fever, cough, fatigue, loss of taste/smell, shortness of breath. "
     "Isolate if symptomatic, get tested, and follow local health guidelines. "
     "Vaccination significantly reduces severe illness risk."),

    (["thank", "thanks", "great", "helpful"],
     "You're welcome! 😊 Stay healthy and don't hesitate to ask if you need anything else. "
     "Remember — regular check-ups are the best prevention!"),

    (["bye", "goodbye", "exit"],
     "Take care! 👋 Remember: your health is your greatest asset. "
     "Come back anytime you need health guidance. Stay well! 🌿"),
]

QUICK_SUGGESTIONS = [
    "What helps with a headache?",
    "How to manage diabetes?",
    "Tips for better sleep",
    "How to lower blood pressure?",
    "What is a healthy diet?",
    "How to reduce stress?",
]


def _get_response(user_input: str) -> str:
    """Match user input to knowledge base using keyword search."""
    text = user_input.lower()

    for keywords, response in KB:
        if any(kw in text for kw in keywords):
            return response

    return (
        "I'm not sure about that specific topic. 🤔\n"
        "For accurate medical advice, please consult a licensed healthcare professional.\n"
        "You can also try asking about: fever, headache, diabetes, diet, sleep, "
        "stress, heart health, or exercise."
    )


class Chatbot(tk.Frame):
    """AI Health Chatbot with a chat-bubble style interface."""

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._build_ui()
        # Show welcome message
        self._add_bubble(
            "assistant",
            f"Hello {user['username']}! 👋 I'm your AI health assistant.\n"
            "Ask me anything about symptoms, diet, medications, or general wellness.\n"
            "Remember: I'm an AI — always consult a doctor for medical decisions.",
        )

    def _build_ui(self):
        # ── Header strip ───────────────────────────────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_medium"], pady=10, padx=PADDING_LG)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🤖  AI Health Chatbot",
            font=FONTS["heading_lg"],
            bg=COLORS["bg_medium"],
            fg=COLORS["text_primary"],
        ).pack(side="left")

        tk.Label(
            header,
            text="● Online",
            font=FONTS["body_sm"],
            bg=COLORS["bg_medium"],
            fg=COLORS["success"],
        ).pack(side="right")

        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")

        # ── Quick suggestion chips ─────────────────────────────────────────
        chip_bar = tk.Frame(self, bg=COLORS["bg_dark"], pady=8, padx=PADDING_LG)
        chip_bar.pack(fill="x")

        tk.Label(chip_bar, text="Quick topics:",
                 font=FONTS["body_sm"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"]).pack(side="left", padx=(0, 8))

        for suggestion in QUICK_SUGGESTIONS:
            chip = tk.Button(
                chip_bar,
                text=suggestion,
                font=FONTS["body_sm"],
                bg=COLORS["bg_card"],
                fg=COLORS["secondary"],
                activebackground=COLORS["bg_hover"],
                activeforeground=COLORS["secondary"],
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=4,
                bd=0,
                command=lambda s=suggestion: self._send_message(s),
            )
            chip.pack(side="left", padx=3)

        # ── Chat display area ──────────────────────────────────────────────
        chat_outer = tk.Frame(self, bg=COLORS["bg_dark"])
        chat_outer.pack(fill="both", expand=True, padx=PADDING_LG, pady=(0, PADDING_MD))

        self._chat_canvas = tk.Canvas(
            chat_outer, bg=COLORS["bg_dark"], highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            chat_outer, orient="vertical", command=self._chat_canvas.yview
        )
        self._chat_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._chat_canvas.pack(side="left", fill="both", expand=True)

        self._chat_frame = tk.Frame(self._chat_canvas, bg=COLORS["bg_dark"])
        self._canvas_window = self._chat_canvas.create_window(
            (0, 0), window=self._chat_frame, anchor="nw"
        )

        self._chat_canvas.bind(
            "<Configure>",
            lambda e: self._chat_canvas.itemconfig(self._canvas_window, width=e.width),
        )
        self._chat_frame.bind(
            "<Configure>",
            lambda e: self._chat_canvas.configure(scrollregion=self._chat_canvas.bbox("all")),
        )
        self._chat_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self._chat_canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )

        # ── Input bar ──────────────────────────────────────────────────────
        input_bar = tk.Frame(self, bg=COLORS["bg_medium"], pady=10, padx=PADDING_LG)
        input_bar.pack(fill="x", side="bottom")

        border = tk.Frame(input_bar, bg=COLORS["border_light"], padx=1, pady=1)
        border.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self._input_var = tk.StringVar()
        self._entry = tk.Entry(
            border,
            textvariable=self._input_var,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["primary"],
            relief="flat",
            font=FONTS["body"],
        )
        self._entry.pack(fill="x", ipady=10, ipadx=12)
        self._entry.bind("<Return>", lambda e: self._send_message())

        self._entry.insert(0, "Ask a health question…")
        self._entry.configure(fg=COLORS["text_muted"])

        def _on_focus_in(e):
            if self._entry.get() == "Ask a health question…":
                self._entry.delete(0, tk.END)
                self._entry.configure(fg=COLORS["text_primary"])

        def _on_focus_out(e):
            if not self._entry.get():
                self._entry.insert(0, "Ask a health question…")
                self._entry.configure(fg=COLORS["text_muted"])

        self._entry.bind("<FocusIn>", _on_focus_in)
        self._entry.bind("<FocusOut>", _on_focus_out)

        PrimaryButton(input_bar, "Send ➤", command=self._send_message).pack(side="right")

    # ── Chat logic ─────────────────────────────────────────────────────────────
    def _send_message(self, text: str = None):
        """Read user input, add bubble, generate and show response."""
        msg = text or self._input_var.get().strip()
        if not msg or msg == "Ask a health question…":
            return

        self._input_var.set("")
        self._add_bubble("user", msg)

        response = _get_response(msg)
        # Slight delay so it feels more like a real chat
        self.after(400, lambda: self._add_bubble("assistant", response))

    def _add_bubble(self, sender: str, text: str):
        """Render one chat message bubble."""
        is_user = sender == "user"
        bubble_bg = COLORS["primary"] if is_user else COLORS["bg_card"]
        text_fg   = COLORS["bg_dark"] if is_user else COLORS["text_primary"]
        side      = "right" if is_user else "left"

        row = tk.Frame(self._chat_frame, bg=COLORS["bg_dark"], pady=4)
        row.pack(fill="x", padx=PADDING_LG)

        # Timestamp
        ts = datetime.now().strftime("%H:%M")

        if is_user:
            tk.Label(row, text=ts, font=FONTS["body_sm"],
                     bg=COLORS["bg_dark"], fg=COLORS["text_muted"]).pack(side="right", anchor="e", padx=(0, 4))

        bubble_outer = tk.Frame(row, bg=COLORS["bg_dark"])
        bubble_outer.pack(side=side)

        if not is_user:
            tk.Label(bubble_outer, text="🤖", font=("Segoe UI Emoji", 14),
                     bg=COLORS["bg_dark"]).pack(side="left", anchor="n", padx=(0, 6))

        bubble = tk.Frame(bubble_outer, bg=bubble_bg, padx=14, pady=10)
        bubble.pack(side=side)

        tk.Label(
            bubble,
            text=text,
            font=FONTS["body"],
            bg=bubble_bg,
            fg=text_fg,
            wraplength=480,
            justify="left",
            anchor="w",
        ).pack()

        if not is_user:
            tk.Label(row, text=ts, font=FONTS["body_sm"],
                     bg=COLORS["bg_dark"], fg=COLORS["text_muted"]).pack(side="left", anchor="w", padx=(6, 0))

        # Auto-scroll to bottom
        self._chat_canvas.update_idletasks()
        self._chat_canvas.yview_moveto(1.0)