# ui/theme.py
# Central design tokens — colors, fonts, spacing for Swastha

# ─────────────────────────────────────────────────────────────
# COLOR PALETTE
# ─────────────────────────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_dark": "#0D1B2A",
    "bg_medium": "#1B2A3B",
    "bg_card": "#1E3448",
    "bg_input": "#162232",
    "bg_hover": "#243B52",

    # Brand
    "primary": "#00C9A7",
    "primary_dark": "#00A88A",
    "secondary": "#4FC3F7",

    # Status
    "success": "#4CAF50",
    "warning": "#FFB300",
    "error": "#EF5350",
    "info": "#29B6F6",

    # Text
    "text_primary": "#E8F4FD",
    "text_secondary": "#8AAFC7",
    "text_muted": "#4A6278",

    # Borders
    "border": "#243B52",
    "border_light": "#2E4D6B",

    # Sidebar
    "sidebar_active": "#00C9A7",
    "sidebar_text": "#8AAFC7",
    "sidebar_active_text": "#0D1B2A",
}

# ─────────────────────────────────────────────────────────────
# TYPOGRAPHY
# ─────────────────────────────────────────────────────────────
FONTS = {
    "heading_xl": ("Segoe UI", 22, "bold"),
    "heading_lg": ("Segoe UI", 16, "bold"),
    "heading_md": ("Segoe UI", 13, "bold"),
    "heading_sm": ("Segoe UI", 11, "bold"),

    "body": ("Segoe UI", 10),
    "body_sm": ("Segoe UI", 9),

    "mono": ("Consolas", 10),
    "label": ("Segoe UI", 10, "bold"),
    "button": ("Segoe UI", 10, "bold"),

    "sidebar": ("Segoe UI", 11),
    "sidebar_hd": ("Segoe UI", 13, "bold"),

    "logo": ("Segoe UI", 18, "bold"),
    "tagline": ("Segoe UI", 9),
}

# ─────────────────────────────────────────────────────────────
# DIMENSIONS
# ─────────────────────────────────────────────────────────────
SIDEBAR_WIDTH = 220
HEADER_HEIGHT = 60

PADDING_SM = 8
PADDING_MD = 16
PADDING_LG = 24

CARD_RADIUS = 8


# ─────────────────────────────────────────────────────────────
# WIDGET STYLE HELPERS
# ─────────────────────────────────────────────────────────────
def apply_entry_style(entry_widget):
    """Apply consistent styling to Entry widgets."""

    entry_widget.configure(
        bg=COLORS["bg_input"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["primary"],
        relief="flat",
        font=FONTS["body"],
        bd=0,
    )


def apply_button_style(btn, style="primary"):
    """Apply button styling (primary / secondary / danger)."""

    styles = {
        "primary": {
            "bg": COLORS["primary"],
            "fg": COLORS["bg_dark"],
            "activebackground": COLORS["primary_dark"],
            "activeforeground": COLORS["bg_dark"],
        },
        "secondary": {
            "bg": COLORS["bg_card"],
            "fg": COLORS["text_primary"],
            "activebackground": COLORS["bg_hover"],
            "activeforeground": COLORS["text_primary"],
        },
        "danger": {
            "bg": COLORS["error"],
            "fg": "#FFFFFF",
            "activebackground": "#C62828",
            "activeforeground": "#FFFFFF",
        },
    }

    s = styles.get(style, styles["primary"])

    btn.configure(
        bg=s["bg"],
        fg=s["fg"],
        activebackground=s["activebackground"],
        activeforeground=s["activeforeground"],
        relief="flat",
        font=FONTS["button"],
        cursor="hand2",
        bd=0,
        padx=14,
        pady=8,
    )