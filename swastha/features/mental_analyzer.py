"""
Mental Health Module
Tracks mood and provides mental wellness support
"""

import tkinter as tk
from tkinter import messagebox

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton
from db.db_connection import db

class MentalHealthUI:
    """Mental Health Feature UI"""
    
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.moods = []
        self.create_ui()
        self.load_moods()
    
    def create_ui(self):
        # Title
        title = tk.Label(
            self.parent,
            text="🧠 Mental Health & Wellness",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Mood tracking
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        mood_label = tk.Label(
            left_panel,
            text="How are you feeling?",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        mood_label.pack(anchor="w", fill=tk.X)
        
        form_frame = tk.Frame(left_panel, bg=COLORS["white"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Mood selection
        tk.Label(form_frame, text="Select Your Mood", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w", pady=(0, PADDING["md"]))
        
        moods_buttons_frame = tk.Frame(form_frame, bg=COLORS["white"])
        moods_buttons_frame.pack(fill=tk.X, pady=(0, PADDING["lg"]))
        
        self.selected_mood = tk.StringVar()
        
        moods = [
            ("😄 Great", "great"),
            ("😊 Good", "good"),
            ("😐 Neutral", "neutral"),
            ("😞 Sad", "sad"),
            ("😤 Stressed", "stressed"),
        ]
        
        for mood_text, mood_value in moods:
            rb = tk.Radiobutton(
                moods_buttons_frame,
                text=mood_text,
                variable=self.selected_mood,
                value=mood_value,
                font=FONTS["body_medium"],
                bg=COLORS["white"],
                fg=COLORS["black"],
                selectcolor=COLORS["primary"]
            )
            rb.pack(anchor="w", pady=PADDING["sm"])
        
        self.selected_mood.set("neutral")
        
        # Notes
        tk.Label(form_frame, text="Notes", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w", pady=(PADDING["lg"], 0))
        self.notes_text = tk.Text(form_frame, font=FONTS["body_medium"], height=4, relief="solid", bd=1)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING["lg"]))
        
        # Submit button
        submit_btn = CustomButton(
            form_frame,
            text="Log Mood",
            bg=COLORS["success"],
            command=self.log_mood
        )
        submit_btn.pack(fill=tk.X)
        
        # Right panel - History and resources
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        # Tabs
        tab_frame = tk.Frame(right_panel, bg=COLORS["white"])
        tab_frame.pack(fill=tk.X, padx=PADDING["md"], pady=PADDING["md"])
        
        history_btn = tk.Button(
            tab_frame,
            text="Mood History",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
            relief="flat",
            command=self.show_history
        )
        history_btn.pack(side=tk.LEFT, padx=(0, PADDING["sm"]))
        
        resources_btn = tk.Button(
            tab_frame,
            text="Resources",
            font=FONTS["button"],
            bg=COLORS["gray"],
            fg=COLORS["white"],
            relief="flat",
            command=self.show_resources
        )
        resources_btn.pack(side=tk.LEFT)
        
        # Display area
        self.display_frame = tk.Frame(right_panel, bg=COLORS["white"])
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        self.show_history()
    
    def log_mood(self):
        mood = self.selected_mood.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Convert mood to level
        mood_levels = {
            "great": 5,
            "good": 4,
            "neutral": 3,
            "sad": 2,
            "stressed": 1,
        }
        
        if not db.is_connected():
            db.connect()
        
        query = "INSERT INTO mood_records (user_id, mood, mood_level, notes) VALUES (%s, %s, %s, %s)"
        
        if db.execute_update(query, (self.user_id, mood, mood_levels[mood], notes)):
            messagebox.showinfo("Success", "Mood logged successfully!")
            self.notes_text.delete("1.0", tk.END)
            self.load_moods()
            self.show_history()
        else:
            messagebox.showerror("Error", "Failed to log mood")
    
    def load_moods(self):
        if not db.is_connected():
            db.connect()
        
        query = "SELECT mood, mood_level, notes, recorded_at FROM mood_records WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 10"
        results = db.execute_query(query, (self.user_id,))
        
        self.moods = results if results else []
    
    def show_history(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.moods:
            no_data = tk.Label(
                self.display_frame,
                text="No mood records yet. Start tracking!",
                font=FONTS["body_medium"],
                bg=COLORS["white"],
                fg=COLORS["gray"]
            )
            no_data.pack(expand=True)
            return
        
        scrollbar = tk.Scrollbar(self.display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_listbox = tk.Listbox(
            self.display_frame,
            font=FONTS["body_small"],
            bg=COLORS["light_gray"],
            yscrollcommand=scrollbar.set
        )
        history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_listbox.yview)
        
        for mood in self.moods:
            display_text = f"{mood['recorded_at']} - {mood['mood'].upper()}"
            history_listbox.insert(tk.END, display_text)
    
    def show_resources(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        resources = tk.Text(
            self.display_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            relief="solid",
            bd=1,
            state="disabled"
        )
        resources.pack(fill=tk.BOTH, expand=True)
        
        content = """MENTAL WELLNESS TIPS

🧘 Meditation & Mindfulness
• Practice daily meditation (10-20 mins)
• Focus on breathing exercises
• Use mindfulness apps for guidance

💪 Physical Activity
• Exercise 30 mins daily
• Yoga for stress relief
• Walk in nature regularly

😴 Sleep Hygiene
• Maintain consistent sleep schedule
• Avoid screens 1 hour before bed
• Create a comfortable sleep environment

🤝 Social Connection
• Maintain relationships with loved ones
• Join support groups
• Talk to friends and family

🎨 Creative Activities
• Pursue hobbies and interests
• Art, music, or writing
• Engage in enjoyable activities

📚 Learning
• Read motivational books
• Take courses on wellness
• Learn new skills

⚠️ If struggling with mental health:
• Contact a mental health professional
• Call mental health helplines
• Seek professional counseling"""
        
        resources.config(state="normal")
        resources.insert("1.0", content)
        resources.config(state="disabled")
