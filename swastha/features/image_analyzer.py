# image_analyzer.py
# Swastha - AI Smart Healthcare System
# Feature: Medical Image Analyzer — AI analysis of skin, wound, eye, rash & body images

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import base64
import json
import urllib.request
from datetime import datetime

try:
    from PIL import Image, ImageTk, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────
API_KEY      = ""
API_URL      = "https://api.anthropic.com/v1/messages"
MODEL        = "claude-opus-4-5"
MAX_TOKENS   = 2048

DARK_BG      = "#0d1117"
CARD_BG      = "#161b22"
BORDER       = "#30363d"
ACCENT       = "#f59e0b"          # amber — medical/clinical feel
ACCENT2      = "#10b981"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED   = "#8b949e"
TEXT_DANGER  = "#f85149"
TEXT_OK      = "#3fb950"
TEXT_WARN    = "#f0883e"

FONT_TITLE   = ("Segoe UI Semibold", 16)
FONT_BODY    = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 9)

ANALYSIS_TYPES = {
    "General Medical": {
        "icon": "🏥",
        "prompt": (
            "You are a medical image analysis assistant. Analyze this medical image thoroughly. "
            "Describe what you observe, any visible symptoms or abnormalities, potential conditions "
            "to consider, and recommended next steps. Structure your response with:\n"
            "## OBSERVATIONS\n## POSSIBLE CONDITIONS\n## SEVERITY ASSESSMENT\n## RECOMMENDED ACTION\n"
            "Always advise consulting a licensed physician for diagnosis."
        ),
    },
    "Skin & Dermatology": {
        "icon": "🔍",
        "prompt": (
            "You are a dermatology image analysis assistant. Analyze this skin image. "
            "Describe: lesion characteristics (size, color, border, texture), distribution pattern, "
            "possible dermatological conditions (common to rare), differential diagnoses, and urgency. "
            "Use dermatological terminology. Structure:\n"
            "## LESION CHARACTERISTICS\n## DIFFERENTIAL DIAGNOSIS\n## URGENCY LEVEL\n## NEXT STEPS\n"
            "Note: This is not a medical diagnosis. Always recommend a dermatologist."
        ),
    },
    "Wound Assessment": {
        "icon": "🩹",
        "prompt": (
            "You are a wound care assessment assistant. Analyze this wound image. "
            "Assess: wound type, size estimation, depth appearance, wound bed characteristics, "
            "signs of infection (redness, swelling, discharge, odor description if visible), "
            "healing stage, and care recommendations. Structure:\n"
            "## WOUND TYPE & CHARACTERISTICS\n## INFECTION INDICATORS\n## HEALING STAGE\n## CARE RECOMMENDATIONS\n"
            "For serious wounds, always recommend immediate medical attention."
        ),
    },
    "Eye Examination": {
        "icon": "👁️",
        "prompt": (
            "You are an ophthalmology image analysis assistant. Analyze this eye image. "
            "Examine: conjunctiva appearance, pupil characteristics, iris details, visible vessels, "
            "any redness/discharge/abnormalities, potential conditions (conjunctivitis, stye, etc.). "
            "Structure:\n"
            "## EYE APPEARANCE\n## ABNORMALITIES NOTED\n## POSSIBLE CONDITIONS\n## RECOMMENDED ACTION\n"
            "Always recommend an ophthalmologist for proper examination."
        ),
    },
    "Rash Analysis": {
        "icon": "🌡️",
        "prompt": (
            "You are a medical rash analysis assistant. Analyze this rash image. "
            "Describe: morphology (macule/papule/vesicle/pustule/plaque), distribution, color, "
            "borders, associated symptoms visible, pattern (systemic vs contact vs infectious), "
            "differential diagnoses ordered by likelihood. Structure:\n"
            "## RASH MORPHOLOGY\n## DISTRIBUTION PATTERN\n## DIFFERENTIAL DIAGNOSIS\n## URGENCY & NEXT STEPS\n"
            "Recommend allergy/dermatology consultation."
        ),
    },
    "X-Ray / Scan": {
        "icon": "🫁",
        "prompt": (
            "You are a radiological image description assistant. Analyze this medical imaging. "
            "Describe visible anatomical structures, any densities or opacities, apparent "
            "abnormalities, symmetry, and observations. Note: AI cannot replace radiologist reading. "
            "Structure:\n"
            "## IMAGE QUALITY & TYPE\n## ANATOMICAL OBSERVATIONS\n## NOTABLE FINDINGS\n## LIMITATIONS & RECOMMENDATION\n"
            "Always recommend a qualified radiologist for official interpretation."
        ),
    },
}

DISCLAIMER = (
    "⚠️  MEDICAL DISCLAIMER: This AI analysis is for informational purposes only. "
    "It does NOT constitute medical advice, diagnosis, or treatment. "
    "Always consult a licensed healthcare professional for medical concerns."
)


def _get_api_key() -> str:
    return API_KEY or os.environ.get("ANTHROPIC_API_KEY", "")


def _image_to_base64(path: str) -> tuple[str, str]:
    ext = os.path.splitext(path)[1].lower()
    mime = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
        ".gif":  "image/gif",
    }.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8"), mime


def _call_claude_vision(image_path: str, analysis_type: str) -> str:
    key = _get_api_key()
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set.")

    b64, mime    = _image_to_base64(image_path)
    system_prompt = ANALYSIS_TYPES[analysis_type]["prompt"]

    payload = {
        "model":      MODEL,
        "max_tokens": MAX_TOKENS,
        "system":     system_prompt,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64", "media_type": mime, "data": b64}},
                {"type": "text",
                 "text": "Please analyze this medical image as described in your instructions."},
            ],
        }],
    }
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        API_URL, data=data,
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["content"][0]["text"]


# ── Main Widget ───────────────────────────────────────────────────────────────

class ImageAnalyzer(tk.Frame):
    """Medical Image Analyzer with AI-powered visual diagnosis support."""

    SUPPORTED_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff")

    def __init__(self, parent, user_data: dict | None = None, **kwargs):
        super().__init__(parent, bg=DARK_BG, **kwargs)
        self.user_data     = user_data or {}
        self.image_path    = None
        self.is_analyzing  = False
        self.analysis_hist = []
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._build_header()
        self._build_body()

    def _build_header(self):
        hdr = tk.Frame(self, bg=CARD_BG, padx=24, pady=16)
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        hdr.columnconfigure(1, weight=1)

        tk.Label(hdr, text="🔬", font=("Segoe UI Emoji", 24),
                 bg=CARD_BG).grid(row=0, column=0, rowspan=2, padx=(0, 14))
        tk.Label(hdr, text="Medical Image Analyzer",
                 font=FONT_TITLE, bg=CARD_BG, fg=TEXT_PRIMARY).grid(
            row=0, column=1, sticky="w")
        tk.Label(hdr, text="AI-powered visual analysis for skin, wounds, eyes, rashes & more",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED).grid(
            row=1, column=1, sticky="w")

        # Disclaimer banner
        disclaimer = tk.Label(hdr, text=DISCLAIMER,
                              font=FONT_SMALL, bg="#2d1b00", fg=TEXT_WARN,
                              wraplength=700, justify="left", padx=10, pady=6)
        disclaimer.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))

    def _build_body(self):
        body = tk.Frame(self, bg=DARK_BG)
        body.grid(row=1, column=0, sticky="nsew", padx=20, pady=16)
        body.columnconfigure(0, weight=1, minsize=300)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

    # ── Left Panel ────────────────────────────────────────────────────────────

    def _build_left(self, parent):
        left = tk.Frame(parent, bg=CARD_BG, padx=16, pady=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)

        # Analysis type selector
        tk.Label(left, text="ANALYSIS TYPE",
                 font=("Segoe UI Semibold", 9), bg=CARD_BG, fg=ACCENT).grid(
            row=0, column=0, sticky="w", pady=(0, 8))

        self.analysis_var = tk.StringVar(value="General Medical")
        for name, meta in ANALYSIS_TYPES.items():
            rb = tk.Radiobutton(
                left, text=f"{meta['icon']}  {name}",
                variable=self.analysis_var, value=name,
                bg=CARD_BG, fg=TEXT_MUTED,
                selectcolor=DARK_BG, activebackground=CARD_BG,
                font=FONT_BODY, cursor="hand2",
            )
            rb.grid(sticky="w")

        # Upload zone
        tk.Label(left, text="IMAGE", font=("Segoe UI Semibold", 9),
                 bg=CARD_BG, fg=ACCENT).grid(
            row=0, column=1, sticky="nw", pady=(0, 8), padx=(20, 0))

        upload_col = tk.Frame(left, bg=CARD_BG)
        upload_col.grid(row=0, column=1, rowspan=8, sticky="nsew", padx=(20, 0))
        upload_col.columnconfigure(0, weight=1)
        upload_col.rowconfigure(1, weight=1)

        # Drop zone
        drop = tk.Frame(upload_col, bg=DARK_BG, relief="flat",
                        highlightthickness=1, highlightbackground=BORDER,
                        cursor="hand2")
        drop.grid(row=0, column=0, sticky="ew", pady=(20, 8))
        drop.columnconfigure(0, weight=1)

        tk.Label(drop, text="📸", font=("Segoe UI Emoji", 28), bg=DARK_BG).grid(
            row=0, column=0, pady=(14, 4))
        tk.Label(drop, text="Click to upload image",
                 font=FONT_BODY, bg=DARK_BG, fg=TEXT_PRIMARY).grid(row=1, column=0)
        tk.Label(drop, text="PNG · JPG · WEBP · BMP",
                 font=FONT_SMALL, bg=DARK_BG, fg=TEXT_MUTED).grid(
            row=2, column=0, pady=(2, 14))

        for w in [drop] + drop.winfo_children():
            w.bind("<Button-1>", lambda e: self._browse_image())
            w.bind("<Enter>",    lambda e: drop.config(highlightbackground=ACCENT))
            w.bind("<Leave>",    lambda e: drop.config(highlightbackground=BORDER))

        # Image preview
        self.img_preview = tk.Label(upload_col, bg=DARK_BG, text="",
                                    relief="flat", highlightthickness=1,
                                    highlightbackground=BORDER)
        self.img_preview.grid(row=1, column=0, sticky="nsew", pady=(0, 8))

        self.file_info = tk.Label(upload_col, text="No image selected",
                                  font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED)
        self.file_info.grid(row=2, column=0, sticky="w")

        # Image tools (only if PIL available)
        if PIL_AVAILABLE:
            tools_frame = tk.Frame(upload_col, bg=CARD_BG)
            tools_frame.grid(row=3, column=0, sticky="ew", pady=(4, 0))

            tk.Label(tools_frame, text="Enhance:",
                     font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED).pack(side="left")
            for lbl, cmd in [("Contrast", self._enhance_contrast),
                             ("Sharpen",  self._enhance_sharpen),
                             ("Reset",    self._reset_image)]:
                tk.Button(
                    tools_frame, text=lbl, font=FONT_SMALL,
                    bg=BORDER, fg=TEXT_PRIMARY, relief="flat",
                    cursor="hand2", padx=6, pady=3,
                    command=cmd,
                ).pack(side="left", padx=(4, 0))

        # Analyze button
        self.analyze_btn = tk.Button(
            upload_col, text="🔬  Analyze Image",
            font=("Segoe UI Semibold", 10),
            bg=ACCENT, fg="#000000", activebackground="#d97706",
            relief="flat", cursor="hand2", pady=10,
            command=self._start_analysis,
        )
        self.analyze_btn.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        tk.Button(
            upload_col, text="🗑  Clear",
            font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED,
            activebackground=BORDER, relief="flat", cursor="hand2",
            command=self._clear,
        ).grid(row=5, column=0, sticky="ew", pady=(4, 0))

    # ── Right Panel ───────────────────────────────────────────────────────────

    def _build_right(self, parent):
        right = tk.Frame(parent, bg=CARD_BG, padx=16, pady=16)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        top = tk.Frame(right, bg=CARD_BG)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top.columnconfigure(0, weight=1)

        tk.Label(top, text="ANALYSIS RESULTS",
                 font=("Segoe UI Semibold", 9), bg=CARD_BG, fg=ACCENT).grid(
            row=0, column=0, sticky="w")
        self.status_lbl = tk.Label(top, text="● Ready",
                                   font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED)
        self.status_lbl.grid(row=0, column=1, sticky="e")

        # Tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("IA.TNotebook",      background=CARD_BG, borderwidth=0)
        style.configure("IA.TNotebook.Tab",
                        background=DARK_BG, foreground=TEXT_MUTED,
                        padding=[12, 6], borderwidth=0)
        style.map("IA.TNotebook.Tab",
                  background=[("selected", CARD_BG)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(right, style="IA.TNotebook")
        nb.grid(row=1, column=0, sticky="nsew")

        self.result_text  = self._make_tab(nb, "📋 Analysis")
        self.summary_text = self._make_tab(nb, "🩺 Summary")
        self.history_text = self._make_tab(nb, "📂 History")

        self._show_welcome()

    def _make_tab(self, nb, label: str) -> tk.Text:
        frame = tk.Frame(nb, bg=DARK_BG)
        nb.add(frame, text=label)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        text = tk.Text(
            frame, bg=DARK_BG, fg=TEXT_PRIMARY,
            font=FONT_BODY, relief="flat", wrap="word",
            padx=14, pady=14, state="disabled",
            selectbackground=BORDER,
            insertbackground=TEXT_PRIMARY,
        )
        text.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        text.configure(yscrollcommand=sb.set)

        text.tag_configure("heading",   font=("Segoe UI Semibold", 11), foreground=ACCENT)
        text.tag_configure("subhead",   font=("Segoe UI Semibold", 10), foreground=ACCENT2)
        text.tag_configure("warn",      foreground=TEXT_WARN)
        text.tag_configure("danger",    foreground=TEXT_DANGER)
        text.tag_configure("ok",        foreground=TEXT_OK)
        text.tag_configure("muted",     foreground=TEXT_MUTED)
        text.tag_configure("bold",      font=("Segoe UI Semibold", 10))
        text.tag_configure("separator", foreground=BORDER)
        return text

    def _show_welcome(self):
        msg = (
            "Welcome to the Medical Image Analyzer\n\n"
            "How to use:\n"
            "  1. Select an analysis type from the left panel\n"
            "  2. Upload your medical image (skin, wound, eye, rash, X-ray, etc.)\n"
            "  3. Click 'Analyze Image' for AI-powered insights\n\n"
            "Supported image types:\n"
            "  PNG · JPG · JPEG · WEBP · BMP · GIF\n\n"
            "Remember: This tool provides informational analysis only.\n"
            "Always consult a licensed physician for medical decisions."
        )
        for w in (self.result_text, self.summary_text):
            self._write(w, msg, "muted")
        self._write(self.history_text, "No analyses yet.\n\nCompleted analyses will appear here.", "muted")

    # ── Image Handling ────────────────────────────────────────────────────────

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Select Medical Image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp *.gif *.bmp *.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        self.image_path = path
        self._original_path = path
        fname = os.path.basename(path)
        size  = os.path.getsize(path)
        self.file_info.config(
            text=f"📎 {fname}  ·  {size/1024:.1f} KB",
            fg=TEXT_PRIMARY,
        )
        self._show_preview(path)

    def _show_preview(self, path: str):
        if not PIL_AVAILABLE:
            self.img_preview.config(text=f"📷\n{os.path.basename(path)}",
                                    font=FONT_BODY, fg=TEXT_MUTED)
            return
        try:
            img   = Image.open(path)
            img.thumbnail((260, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.img_preview.config(image=photo, text="")
            self.img_preview.image = photo
            self._current_pil_image = Image.open(path)
        except Exception as e:
            self.img_preview.config(text=f"Preview error:\n{e}",
                                    font=FONT_SMALL, fg=TEXT_DANGER)

    def _enhance_contrast(self):
        if not (PIL_AVAILABLE and hasattr(self, "_current_pil_image")):
            return
        enhanced = ImageEnhance.Contrast(self._current_pil_image).enhance(1.5)
        tmp_path  = os.path.join(os.path.dirname(self.image_path), "_enhanced_tmp.png")
        enhanced.save(tmp_path)
        self.image_path = tmp_path
        self._show_preview_pil(enhanced)

    def _enhance_sharpen(self):
        if not (PIL_AVAILABLE and hasattr(self, "_current_pil_image")):
            return
        sharpened = self._current_pil_image.filter(ImageFilter.SHARPEN)
        tmp_path   = os.path.join(os.path.dirname(self.image_path), "_sharpened_tmp.png")
        sharpened.save(tmp_path)
        self.image_path = tmp_path
        self._show_preview_pil(sharpened)

    def _reset_image(self):
        if hasattr(self, "_original_path"):
            self.image_path = self._original_path
            self._show_preview(self._original_path)

    def _show_preview_pil(self, img: "Image.Image"):
        preview = img.copy()
        preview.thumbnail((260, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(preview)
        self.img_preview.config(image=photo, text="")
        self.img_preview.image = photo

    # ── Analysis ──────────────────────────────────────────────────────────────

    def _start_analysis(self):
        if self.is_analyzing:
            return
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        if not _get_api_key():
            messagebox.showerror("API Key Missing",
                                 "Set ANTHROPIC_API_KEY in config.py or environment variables.")
            return

        self.is_analyzing = True
        atype = self.analysis_var.get()
        self.analyze_btn.config(state="disabled", text="⏳  Analyzing…")
        self.status_lbl.config(text="● Analyzing…", fg=TEXT_WARN)

        for w in (self.result_text, self.summary_text):
            self._write(w, f"Performing {atype} analysis…\nThis may take 15-30 seconds.", "muted")

        threading.Thread(
            target=self._run_analysis,
            args=(atype,),
            daemon=True,
        ).start()

    def _run_analysis(self, atype: str):
        try:
            raw = _call_claude_vision(self.image_path, atype)
            self.after(0, self._display_result, atype, raw)
        except Exception as exc:
            self.after(0, self._display_error, str(exc))

    def _display_result(self, atype: str, raw: str):
        self.is_analyzing = False
        self.analyze_btn.config(state="normal", text="🔬  Analyze Image")
        self.status_lbl.config(text="● Complete", fg=TEXT_OK)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        fname = os.path.basename(self.image_path) if self.image_path else "unknown"

        # Full analysis tab
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        icon = ANALYSIS_TYPES[atype]["icon"]
        self.result_text.insert("end", f"{icon}  {atype}  ·  {ts}\n", "heading")
        self.result_text.insert("end", f"File: {fname}\n", "muted")
        self.result_text.insert("end", "─" * 50 + "\n\n", "separator")
        self._render_sections(self.result_text, raw)
        self.result_text.config(state="disabled")

        # Summary tab — just first section
        sections = self._parse_sections(raw)
        summary_key = next(iter(sections), None)
        summary_txt = sections.get(summary_key, raw[:400]) if summary_key else raw[:400]

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("end", "KEY FINDINGS\n", "heading")
        self.summary_text.insert("end", "─" * 30 + "\n", "separator")
        self.summary_text.insert("end", summary_txt + "\n\n", "")
        self.summary_text.insert("end", DISCLAIMER + "\n", "warn")
        self.summary_text.config(state="disabled")

        # History tab
        self.analysis_hist.append({
            "time": ts, "type": atype, "file": fname, "result": raw[:200] + "…"
        })
        self._refresh_history()

    def _render_sections(self, widget: tk.Text, text: str):
        import re
        sections = re.split(r"(##\s+[^\n]+)", text)
        for chunk in sections:
            if chunk.startswith("##"):
                heading = chunk.lstrip("# ").strip()
                widget.insert("end", f"\n{heading}\n", "subhead")
                widget.insert("end", "─" * 35 + "\n", "separator")
            else:
                for line in chunk.split("\n"):
                    upper = line.upper()
                    if any(kw in upper for kw in ("URGENT", "EMERGENCY", "CRITICAL", "IMMEDIATE")):
                        tag = "danger"
                    elif any(kw in upper for kw in ("CONCERN", "ABNORMAL", "IRREGULAR", "MONITOR")):
                        tag = "warn"
                    elif any(kw in upper for kw in ("NORMAL", "HEALTHY", "BENIGN", "WITHIN")):
                        tag = "ok"
                    else:
                        tag = ""
                    widget.insert("end", line + "\n", tag)

    def _parse_sections(self, text: str) -> dict:
        import re
        sections = {}
        pattern  = re.compile(r"##\s+([^\n]+)\n(.*?)(?=##\s+|\Z)", re.DOTALL)
        for m in pattern.finditer(text):
            sections[m.group(1).strip()] = m.group(2).strip()
        return sections

    def _refresh_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        if not self.analysis_hist:
            self.history_text.insert("end", "No analyses yet.\n", "muted")
        else:
            for entry in reversed(self.analysis_hist):
                icon = ANALYSIS_TYPES.get(entry["type"], {}).get("icon", "🔬")
                self.history_text.insert(
                    "end",
                    f"{icon}  {entry['type']}\n", "subhead")
                self.history_text.insert(
                    "end",
                    f"  {entry['time']}  ·  {entry['file']}\n", "muted")
                self.history_text.insert(
                    "end",
                    f"  {entry['result']}\n\n", "")
        self.history_text.config(state="disabled")

    def _display_error(self, msg: str):
        self.is_analyzing = False
        self.analyze_btn.config(state="normal", text="🔬  Analyze Image")
        self.status_lbl.config(text="● Error", fg=TEXT_DANGER)
        err = f"Analysis failed:\n\n{msg}\n\nPlease check:\n• API key is set\n• Image file is valid\n• Internet connection"
        for w in (self.result_text, self.summary_text):
            self._write(w, err, "danger")

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _write(self, widget: tk.Text, text: str, tag: str = ""):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text, tag)
        widget.config(state="disabled")

    def _clear(self):
        self.image_path   = None
        self.is_analyzing = False
        if hasattr(self, "_current_pil_image"):
            del self._current_pil_image
        self.img_preview.config(image="", text="")
        self.file_info.config(text="No image selected", fg=TEXT_MUTED)
        self.analyze_btn.config(state="normal", text="🔬  Analyze Image")
        self.status_lbl.config(text="● Ready", fg=TEXT_MUTED)
        self._show_welcome()
