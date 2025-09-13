# themed_style.py

from tkinter import ttk

class ThemedStyle(ttk.Style):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_use('clam')

        # Define font families with fallbacks
        self.display_font = ('Crimson Text', 12, 'bold')
        self.body_font = ('Source Serif Pro', 10)
        self.mono_font = ('IBM Plex Mono', 9) # This will be used in other files

        self.themes = {
            "scholarly_light": {
                "bg": "#faf9f7",           # Warm paper white
                "fg": "#2d2d2d",           # Deep charcoal text
                "bg_accent": "#f0ede8",    # Soft cream
                "select_bg": "#E0DACE",    # A slightly darker cream for selection
                "console_bg": "#f0ede8",   # Soft cream for console background
                "console_fg": "#2d2d2d",   # Deep charcoal for console text
                "success": "#28a745",      # A modern, gentle green
                "error": "#dc3545",        # A modern, clear red
            },
            "scholarly_dark": {
                "bg": "#2d2d2d",           # Inverted: Deep charcoal background
                "fg": "#faf9f7",           # Inverted: Warm paper white text
                "bg_accent": "#4a4a4a",    # Sophisticated gray from docs
                "select_bg": "#6b6b6b",    # Muted gray from docs for selection
                "console_bg": "#1E1E1E",   # High-contrast console background
                "console_fg": "#00FF00",   # High-contrast console text
                "success": "#28a745",
                "error": "#FF4C4C",        # A brighter red for dark mode visibility
            }
        }

    def apply_theme(self, theme_name: str) -> dict:
        """Applies a color theme and fonts to all relevant ttk widgets."""
        colors = self.themes.get(theme_name, self.themes["scholarly_light"])
        
        # Apply fonts
        self.configure('.', font=self.body_font)
        self.configure('TLabelframe.Label', font=self.display_font)
        self.configure('TNotebook.Tab', font=self.body_font)

        # Apply colors
        self.configure('.', background=colors["bg"], foreground=colors["fg"], fieldbackground=colors["bg_accent"])
        self.configure('TFrame', background=colors["bg"])
        self.configure('TLabel', background=colors["bg"], foreground=colors["fg"])
        self.configure('TButton', background=colors["bg_accent"], foreground=colors["fg"])
        self.map('TButton', background=[('active', colors["select_bg"])])
        self.configure('TNotebook', background=colors["bg"])
        self.configure('TNotebook.Tab', background=colors["bg_accent"], foreground=colors["fg"])
        self.map('TNotebook.Tab', background=[('selected', colors["select_bg"])])
        self.configure('TLabelframe', background=colors["bg"], foreground=colors["fg"])
        self.configure('TEntry', fieldbackground=colors["bg_accent"], foreground=colors["fg"])
        self.configure('TCombobox', fieldbackground=colors["bg_accent"], foreground=colors["fg"])

        # Special styles
        self.configure('Success.TLabel', foreground=colors["success"], background=colors["bg"])
        self.configure('Error.TLabel', foreground=colors["error"], background=colors["bg"])
        
        return colors