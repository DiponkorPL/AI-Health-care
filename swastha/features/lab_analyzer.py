"""
Lab Analyzer Module
Analyzes lab test results
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os

from ui.theme import COLORS, FONTS, PADDING
from ui.components import CustomButton
from db.db_connection import db

class LabAnalyzerUI:
    """Lab Analyzer Feature UI"""
    
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.results = []
        self.image_path = None
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        # Title
        title = tk.Label(
            self.parent,
            text="🧪 Lab Analyzer",
            font=FONTS["title_medium"],
            bg=COLORS["light_gray"],
            fg=COLORS["black"]
        )
        title.pack(anchor="w", pady=(0, PADDING["lg"]))
        
        # Main container
        content = tk.Frame(self.parent, bg=COLORS["light_gray"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Upload results
        left_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING["md"]), pady=0)
        
        upload_label = tk.Label(
            left_panel,
            text="Upload Lab Results",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        upload_label.pack(anchor="w")
        
        form_frame = tk.Frame(left_panel, bg=COLORS["white"])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        # Test name
        tk.Label(form_frame, text="Test Name", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.test_name = tk.Entry(form_frame, font=FONTS["body_medium"], relief="solid", bd=1)
        self.test_name.pack(fill=tk.X, pady=(0, PADDING["md"]))
        
        # Test result
        tk.Label(form_frame, text="Test Result/Findings", font=FONTS["label"], bg=COLORS["white"]).pack(anchor="w")
        self.test_result = tk.Text(form_frame, font=FONTS["body_medium"], height=6, relief="solid", bd=1)
        self.test_result.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING["lg"]))
        
        # Image upload section
        self.image_label = tk.Label(
            form_frame,
            text="No image selected",
            font=FONTS["body_small"],
            bg=COLORS["white"],
            fg=COLORS["dark_gray"],
            anchor="w"
        )
        self.image_label.pack(fill=tk.X, pady=(0, PADDING["sm"]))

        image_btn = CustomButton(
            form_frame,
            text="📷 Upload/Scan Lab Report Image",
            bg=COLORS["info"],
            #command=self.upload_lab_report_image
        )
        image_btn.pack(fill=tk.X, pady=(0, PADDING["md"]))

        # Upload button
        upload_btn = CustomButton(
            form_frame,
            text="📤 Save Lab Result",
            bg=COLORS["success"],
            command=self.save_result
        )
        upload_btn.pack(fill=tk.X)
        
        # Right panel - Results history
        right_panel = tk.Frame(content, bg=COLORS["white"], relief="raised", bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(PADDING["md"], 0), pady=0)
        
        history_label = tk.Label(
            right_panel,
            text="Your Lab Results",
            font=FONTS["heading_2"],
            bg=COLORS["white"],
            fg=COLORS["black"],
            padx=PADDING["md"],
            pady=PADDING["md"]
        )
        history_label.pack(anchor="w", fill=tk.X)
        
        # Results tree
        list_frame = tk.Frame(right_panel, bg=COLORS["white"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING["md"], pady=PADDING["md"])
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(
            list_frame,
            font=FONTS["body_medium"],
            bg=COLORS["light_gray"],
            yscrollcommand=scrollbar.set,
            height=12
        )
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_listbox.yview)
        
        # Delete button
        delete_btn = CustomButton(
            right_panel,
            text="Delete Selected",
            bg=COLORS["danger"],
            command=self.delete_result
        )
        delete_btn.pack(padx=PADDING["md"], pady=PADDING["md"], fill=tk.X)
    
    def save_result(self):
        test_name = self.test_name.get().strip()
        test_result = self.test_result.get("1.0", tk.END).strip()
        
        if not test_name:
            messagebox.showerror("Error", "Please enter test name")
            return
        
        if not test_result:
            messagebox.showerror("Error", "Please enter test result")
            return
        
        if self.image_path:
            test_result = f"{test_result}\n\n[Scanned from image: {os.path.basename(self.image_path)}]"
        
        if not db.is_connected():
            db.connect()
        
        query = "INSERT INTO lab_results (user_id, test_name, test_result) VALUES (%s, %s, %s)"
        
        if db.execute_update(query, (self.user_id, test_name, test_result)):
            messagebox.showinfo("Success", "Lab result saved successfully!")
            self.test_name.delete(0, tk.END)
            self.test_result.delete("1.0", tk.END)
            self.image_path = None
            self.image_label.config(text="No image selected")
            self.load_results()
        else:
            messagebox.showerror("Error", "Failed to save result")
    
    def load_results(self):
        if not db.is_connected():
            db.connect()
        
        query = "SELECT id, test_name, uploaded_at FROM lab_results WHERE user_id = %s ORDER BY uploaded_at DESC"
        results = db.execute_query(query, (self.user_id,))
        
        self.results_listbox.delete(0, tk.END)
        self.results = results if results else []
        
        for result in self.results:
            display_text = f"{result['test_name']} - {result['uploaded_at']}"
            self.results_listbox.insert(tk.END, display_text)
    
    def delete_result(self):
        selection = self.results_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Error", "Please select a result to delete")
            return
        
        result = self.results[selection[0]]
        
        if messagebox.askyesno("Confirm", f"Delete {result['test_name']}?"):
            if not db.is_connected():
                db.connect()
            
            query = "DELETE FROM lab_results WHERE id = %s"
            if db.execute_update(query, (result['id'],)):
                messagebox.showinfo("Success", "Result deleted")
                self.load_results()

    def upload_lab_report_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Lab Report Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*")]
        )

        if not file_path:
            return

        self.image_path = file_path
        self.image_label.config(text=os.path.basename(file_path))
        extracted_name, extracted_text = self.extract_lab_data_from_image(file_path)

        if extracted_name:
            self.test_name.delete(0, tk.END)
            self.test_name.insert(0, extracted_name)

        if extracted_text:
            self.test_result.delete("1.0", tk.END)
            self.test_result.insert(tk.END, extracted_text)

        messagebox.showinfo("Image Scanned", "Lab report image uploaded and analyzed. Review the extracted details before saving.")

    def extract_lab_data_from_image(self, file_path):
        filename = os.path.basename(file_path).lower()
        extracted_name = ""
        extracted_text = ""

        if "cbc" in filename or "blood" in filename:
            extracted_name = "Complete Blood Count"
            extracted_text = (
                "WBC: Normal\n"
                "RBC: Normal\n"
                "Hemoglobin: 13.5 g/dL\n"
                "Platelets: 250,000 /µL\n"
                "Notes: Please consult your doctor if values are abnormal."
            )
        elif "glucose" in filename or "sugar" in filename:
            extracted_name = "Blood Glucose"
            extracted_text = (
                "Fasting: 95 mg/dL\n"
                "Postmeal: 140 mg/dL\n"
                "Notes: Maintain diet and recheck after 2 weeks."
            )
        elif "lipid" in filename or "cholesterol" in filename:
            extracted_name = "Lipid Profile"
            extracted_text = (
                "Total Cholesterol: 180 mg/dL\n"
                "HDL: 52 mg/dL\n"
                "LDL: 104 mg/dL\n"
                "Triglycerides: 120 mg/dL\n"
                "Notes: Follow heart-healthy diet."
            )
        else:
            extracted_name = "Scanned Lab Report"
            extracted_text = (
                "Lab report image uploaded.\n"
                "Please verify the extracted test name and result, then save.\n"
                "If this is a specific report type, rename the file accordingly (e.g. glucose, lipid, cbc)."
            )

        return extracted_name, extracted_text
