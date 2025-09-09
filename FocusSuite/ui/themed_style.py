# a custom ttk.style class for easy theme switching

from tkinter import ttk

class ThemedStyle(ttk.Style):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_use('clam')
        self.themes = {
            "light":{
                "bg": "#F0F0F0", "fg":"#000000","bg_accent":"#FFFFFF","select_bg":"#DDDDDD","console_bg":"#FFFFFF","console_fg":"#000000","success":"green","error":"red",
            },
            "dark":{
                "bg":"#2E2E2E","fg":"#FFFFFF","bg_accent":"#3C3C3C","select_bg":"#555555","console_bg":"#1E1E1E","console_fg":"#00FF00","success":"#00FF00","error":"#FF4C4C",
            }
        }

    def apply_theme(self, theme_name: str) -> dict:
        #Applies a color theme to all relevant ttk widgets..
        colors = self.themes.get(theme_name, self.themes["light"])
        self.configure('.',background=colors["bg"],foreground=colors["fg"],fieldbackground=colors["bg_accent"])
        self.configure('TFrame', background=colors["bg"])
        self.configure('TLabel',background=colors["bg"],foreground=colors["fg"])
        self.configure('TButton',background=colors["bg_accent"],foreground=colors["fg"])
        self.map('TButton',background=[('active',colors["select_bg"])])
        self.configure('TNotebook', background=colors["bg"])
        self.configure('TNotebook.Tab',background=colors["bg_accent"],foreground=colors["fg"])
        self.map('TNotebook.Tab', background=[('selected',colors["select_bg"])])
        self.configure('TLabelframe',background=colors["bg"],foreground=colors["fg"])
        self.configure('Success.TLabel', foreground=colors["success"],background=colors["bg"])
        self.configure('Error.TLabel', foreground=colors["error"], background=colors["bg"])
        return colors
