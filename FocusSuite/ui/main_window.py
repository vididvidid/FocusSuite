# main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.themed_style import ThemedStyle
from ui.tabs.video_tab import VideoTab
from ui.tabs.distraction_tab import DistractionBlockerTab
from ui.tabs.settings_tab import SettingsTab

class MainWindow:
    def __init__(self, root, app_callbacks):
        self.root = root
        self.callbacks = app_callbacks
        self.theme_name = self.callbacks['get_setting']('theme', 'scholarly_light') # <-- Changed default

        self.root.title(f"FocusSuite v{self.callbacks['get_version']()}")
        self.style = ThemedStyle()


        self.notebook = ttk.Notebook(self.root)
        self.status_label = None
        self.connection_label = None
        self.theme_var = tk.StringVar(value=self.theme_name)


        self.distraction_tab = None
        self.video_tab = None
        self.settings_tab = None

        self._setup_ui()
        self._apply_theme(self.theme_name)

    def _setup_ui(self):
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        self.distraction_tab = DistractionBlockerTab(self.notebook, self.callbacks)
        self.notebook.add(self.distraction_tab, text='Distraction Blocker')

        self.video_tab = VideoTab(self.notebook, self.callbacks)
        self.notebook.add(self.video_tab, text='Focus Video')

        self.settings_tab = SettingsTab(self.notebook, self.callbacks, self.theme_var, self._apply_theme)
        self.notebook.add(self.settings_tab, text='Settings')


        self._create_status_bar()

    def _apply_theme(self, theme_name:str):
        self.theme_name = theme_name 
        theme_colors = self.style.apply_theme(theme_name)
        self.callbacks['set_setting']('theme', theme_name)

        if self.distraction_tab:
            self.distraction_tab.apply_theme(theme_colors)
        if self.settings_tab:
            self.settings_tab.apply_theme(theme_colors)
        
        # Video tab does not have a custom apply_theme, but will inherit styles

    def _create_status_bar(self):
        status_bar = ttk.Frame(self.root)
        status_bar.pack(side='bottom', fill='x', padx=5, pady=2)
        self.connection_label = ttk.Label(status_bar, text="API: OFFLINE", style='Error.TLabel')
        self.connection_label.pack(side='left')
        self.status_label = ttk.Label(status_bar, text="Status: Idle")
        self.status_label.pack(side='right')

    def load_settings(self):
        self.distraction_tab.provider_var.set(self.callbacks['get_setting']('provider', 'OpenAI'))
        self.distraction_tab.focus_entry.insert(0, self.callbacks['get_setting']('last_focus_topic',' '))

        settings_data = {
            'api_key' : self.callbacks['get_setting']('api_key', ''),
            'worker_url' : self.callbacks['get_setting']('worker_url',''),
            'whitelist':self.callbacks['get_setting']('whitelist',[])
        }
        self.settings_tab.load_settings_data(settings_data)

    def show_message(self, msg_type, title, message):
        show_method = getattr(messagebox, f"show{msg_type}",
                              messagebox.showinfo)
        show_method(title,message)