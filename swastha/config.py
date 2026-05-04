# config.py
# Central configuration for Swastha Healthcare System

# ─────────────────────────────────────────────────────────
# 🗄️ Database Configuration
# ─────────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "605855",
    "database": "swastha",
    "port": 3306,
    "autocommit": True
}


# ─────────────────────────────────────────────────────────
# 📱 App Configuration
# ─────────────────────────────────────────────────────────
APP_CONFIG = {
    "name": "Swastha - AI Smart Healthcare System",
    "version": "1.0.0",
    "author": "Swastha Team"
}

# 👉 dashboard.py compatibility
APP_NAME = APP_CONFIG["name"]


# ─────────────────────────────────────────────────────────
# 🖥️ Window Configuration
# ─────────────────────────────────────────────────────────
WINDOW_CONFIG = {
    "login": {
        "width": 1000,
        "height": 780
    },
    "signup": {
        "width": 1000,
        "height": 780
    },
    "dashboard": {
        "width": 1280,
        "height": 760,
        "min_width": 800,
        "min_height": 500
    }
}

# 👉 dashboard.py compatibility (important 🔥)
DASHBOARD_WIDTH  = WINDOW_CONFIG["dashboard"]["width"]
DASHBOARD_HEIGHT = WINDOW_CONFIG["dashboard"]["height"]

LOGIN_WIDTH  = WINDOW_CONFIG["login"]["width"]
LOGIN_HEIGHT = WINDOW_CONFIG["login"]["height"]

# ─────────────────────────────────────────────────────────
# 🎨 Theme Configuration (Global UI System)
# ─────────────────────────────────────────────────────────
COLORS = {
    "bg_dark": "#0A0F1E",
    "bg_medium": "#0F172A",   # 👉 header bg (dashboard use করছে)
    "bg_card": "#111827",
    "bg_sidebar": "#0D1424",

    "primary": "#00D4AA",     # 👉 dashboard uses this
    "accent": "#00D4AA",
    "accent2": "#3B82F6",
    "accent3": "#F59E0B",

    "danger": "#EF4444",
    "success": "#10B981",

    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#4B5563",

    "border": "#1E293B",
    "hover": "#1A2540",
}


FONTS = {
    "title": ("Georgia", 22, "bold"),
    "heading": ("Georgia", 15, "bold"),

    # 👉 dashboard uses these
    "heading_lg": ("Georgia", 16, "bold"),
    "heading_sm": ("Helvetica", 12, "bold"),
    "body_sm": ("Helvetica", 10),

    "subhead": ("Helvetica", 12, "bold"),
    "body": ("Helvetica", 11),
    "small": ("Helvetica", 9),
    "mono": ("Courier", 10),
    "nav": ("Helvetica", 10, "bold"),
}


# ─────────────────────────────────────────────────────────
# ⚙️ Feature Flags (Future Control)
# ─────────────────────────────────────────────────────────
FEATURE_FLAGS = {
    "lab_analyzer": False,
    "mental_health": False,
    "image_analyzer": False
}
