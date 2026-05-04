# features/diet_guide.py
# Age + weight + goal based personalised diet guide

import tkinter as tk
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.theme import COLORS, FONTS, PADDING_MD, PADDING_LG
from ui.component import (
    Card,
    PrimaryButton,
    SecondaryButton,
    OutputBox,
    SectionHeader,
    StatusLabel
)


# ─────────────────────────────────────────────────────────────
# CALCULATION HELPERS
# ─────────────────────────────────────────────────────────────
def _calculate_bmi(weight_kg: float, height_cm: float):
    h_m = height_cm / 100
    bmi = weight_kg / (h_m * h_m)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 1), category


def _calculate_tdee(age, weight, height, gender, activity):
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Lightly active (1–3 days/week)": 1.375,
        "Moderately active (3–5 days/week)": 1.55,
        "Very active (6–7 days/week)": 1.725,
        "Extra active (physical job)": 1.9,
    }

    return int(bmr * multipliers.get(activity, 1.2))


def _get_macros(tdee, goal):
    adjustments = {
        "Lose Weight": -500,
        "Maintain Weight": 0,
        "Gain Muscle": 300,
    }

    calories = tdee + adjustments.get(goal, 0)

    protein = int((calories * 0.25) / 4)
    carbs = int((calories * 0.45) / 4)
    fat = int((calories * 0.30) / 9)

    return calories, protein, carbs, fat


# ─────────────────────────────────────────────────────────────
# FOOD DATABASE
# ─────────────────────────────────────────────────────────────
FOOD_GROUPS = {
    "Lose Weight": {
        "Proteins": ["Chicken breast", "Turkey", "Egg whites", "Greek yogurt", "Lentils", "Tofu"],
        "Vegetables": ["Broccoli", "Spinach", "Kale", "Cucumber", "Bell peppers"],
        "Fruits": ["Berries", "Apple", "Grapefruit", "Watermelon"],
        "Carbs": ["Oats", "Brown rice", "Quinoa", "Sweet potato"],
        "Fats": ["Avocado", "Olive oil", "Walnuts"],
        "Avoid": ["Sugar drinks", "Fried foods", "White bread"],
    },
    "Maintain Weight": {
        "Proteins": ["Chicken", "Eggs", "Fish", "Dairy", "Nuts"],
        "Vegetables": ["All vegetables"],
        "Fruits": ["Seasonal fruits"],
        "Carbs": ["Whole grains", "Rice", "Oats"],
        "Fats": ["Olive oil", "Nuts", "Avocado"],
        "Limit": ["Sugar", "Processed food"],
    },
    "Gain Muscle": {
        "Proteins": ["Chicken", "Eggs", "Beef", "Fish", "Whey protein"],
        "Carbs": ["Rice", "Pasta", "Oats", "Potato", "Banana"],
        "Vegetables": ["Spinach", "Broccoli"],
        "Fats": ["Peanut butter", "Olive oil"],
        "Workout": ["Protein shake", "Eggs + rice"],
    },
}

ACTIVITY_LEVELS = [
    "Sedentary (little/no exercise)",
    "Lightly active (1–3 days/week)",
    "Moderately active (3–5 days/week)",
    "Very active (6–7 days/week)",
    "Extra active (physical job)",
]

GOALS = ["Lose Weight", "Maintain Weight", "Gain Muscle"]
GENDERS = ["Male", "Female"]


# ─────────────────────────────────────────────────────────────
# MAIN CLASS
# ─────────────────────────────────────────────────────────────
class DietGuide(tk.Frame):

    def __init__(self, parent, user: dict, **kwargs):
        super().__init__(parent, bg=COLORS["bg_dark"], **kwargs)
        self.user = user
        self._build_ui()

    def _build_ui(self):
        canvas = tk.Canvas(self, bg=COLORS["bg_dark"], highlightthickness=0)
        scroll = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLORS["bg_dark"])
        window = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._build_content(inner)

    def _build_content(self, parent):
        pad = PADDING_LG

        header = tk.Frame(parent, bg=COLORS["bg_dark"], padx=pad, pady=PADDING_MD)
        header.pack(fill="x")

        SectionHeader(
            header,
            "🥗 Diet & Nutrition Guide",
            "Personalised meal plan based on your profile",
            bg=COLORS["bg_dark"]
        ).pack(side="left")

        main = tk.Frame(parent, bg=COLORS["bg_dark"])
        main.pack(fill="both", expand=True, padx=pad, pady=pad)

        # LEFT
        left = Card(main, title="Your Profile", accent=COLORS["primary"])
        left.pack(side="left", fill="y", padx=(0, PADDING_MD))

        form = tk.Frame(left, bg=COLORS["bg_card"], padx=PADDING_MD, pady=PADDING_MD)
        form.pack(fill="both")

        def entry():
            e = tk.Entry(
                form,
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                insertbackground=COLORS["primary"],
                relief="flat"
            )
            e.pack(fill="x", pady=5, ipady=6)
            return e

        def label(text):
            tk.Label(
                form,
                text=text,
                bg=COLORS["bg_card"],
                fg=COLORS["text_secondary"]
            ).pack(anchor="w")

        label("Age")
        self.age = entry()

        label("Weight")
        self.weight = entry()

        label("Height")
        self.height = entry()

        self.gender = tk.StringVar(value=GENDERS[0])
        tk.OptionMenu(form, self.gender, *GENDERS).pack(fill="x")

        self.activity = tk.StringVar(value=ACTIVITY_LEVELS[0])
        tk.OptionMenu(form, self.activity, *ACTIVITY_LEVELS).pack(fill="x")

        self.goal = tk.StringVar(value=GOALS[0])
        tk.OptionMenu(form, self.goal, *GOALS).pack(fill="x")

        self.status = StatusLabel(form, bg=COLORS["bg_card"])
        self.status.pack(fill="x")

        PrimaryButton(form, "Generate", command=self._generate).pack(fill="x")
        SecondaryButton(form, "Clear", command=self._clear).pack(fill="x")

        # RIGHT
        right = tk.Frame(main, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        card = Card(right, title="Diet Plan", accent="#66BB6A")
        card.pack(fill="both", expand=True)

        self.output = OutputBox(card)
        self.output.pack(fill="both", expand=True)

        self.output.write("Fill form and generate plan.")

    def _generate(self):
        try:
            age = int(self.age.get())
            weight = float(self.weight.get())
            height = float(self.height.get())
        except:
            self.status.show_error("Invalid input")
            return

        bmi, cat = _calculate_bmi(weight, height)
        tdee = _calculate_tdee(age, weight, height, self.gender.get(), self.activity.get())
        cal, p, c, f = _get_macros(tdee, self.goal.get())

        self.output.clear()
        self.output.write(f"BMI: {bmi} ({cat})")
        self.output.write(f"Calories: {cal}")
        self.output.write(f"P: {p}g C: {c}g F: {f}g")

        foods = FOOD_GROUPS[self.goal.get()]
        for k, v in foods.items():
            self.output.write(f"\n{k}:")
            for item in v:
                self.output.write(f" - {item}")

    def _clear(self):
        self.age.delete(0, tk.END)
        self.weight.delete(0, tk.END)
        self.height.delete(0, tk.END)
        self.status.clear()
        self.output.clear()