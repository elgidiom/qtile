THEMES = {
    # Minimal, basada en el tema rofi actual (predeterminado)
    "ocean": {
        "fg": "#F6F1EB",
        "fg_muted": "#F6F1EBA6",
        "bg": "#242424E6",
        "bg_alt": "#393E41",
        "accent": "#3F88C5",
        "bar_bg": "#242424E6",
        "bar_fg": "#F6F1EB",
    },
    # Fríos tipo Nord
    "nord": {
        "fg": "#ECEFF4",
        "fg_muted": "#D8DEE9A6",
        "bg": "#2E3440E6",
        "bg_alt": "#3B4252",
        "accent": "#88C0D0",
        "bar_bg": "#2E3440E6",
        "bar_fg": "#ECEFF4",
    },
    # Cálidos tipo Gruvbox (dark)
    "gruvbox": {
        "fg": "#EBDBB2",
        "fg_muted": "#EBDBB2A6",
        "bg": "#282828E6",
        "bg_alt": "#3C3836",
        "accent": "#83A598",
        "bar_bg": "#282828E6",
        "bar_fg": "#EBDBB2",
    },
    # Verdes suaves tipo Everforest
    "everforest": {
        "fg": "#D3C6AA",
        "fg_muted": "#D3C6AAA6",
        "bg": "#2B3339E6",
        "bg_alt": "#323C41",
        "accent": "#A7C080",
        "bar_bg": "#2B3339E6",
        "bar_fg": "#D3C6AA",
    },
    # Catppuccin Mocha-like
    "catppuccin-mocha": {
        "fg": "#CDD6F4",
        "fg_muted": "#BAC2DE99",
        "bg": "#1E1E2EE6",
        "bg_alt": "#313244",
        "accent": "#89B4FA",
        "bar_bg": "#1E1E2EE6",
        "bar_fg": "#CDD6F4",
    },
}

def get_theme(name: str):
    return THEMES.get(name, THEMES["ocean"]).copy()

