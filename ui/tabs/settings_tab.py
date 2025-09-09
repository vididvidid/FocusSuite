import tkinter as tk
from tkinter import ttk

class SettingsTab(ttk.Frame):
    def __init__(self, parent, callbacks, theme_var, theme_applier):
        super().__init__(parent, padding=10)
        self.callbacks = callbacks
        self.theme_var = theme_var
        self.theme_applier = theme_applier

        self.api_key_entry = None
        self.worker_url_entry = None
        self.whitelist_text = None

        self._setup_widgets()

    def _setup_widgets(self):
        
        self._create_openai_frame()
        self._create_worker_frame()
        self._create_whitelist_frame()
        self._create_appearance_frame()

        
        save_button = ttk.Button(self, text="Save Whitelist & Appearance",
                                 command=self.callbacks['save_settings'])
        save_button.pack(pady=20)

    def _create_openai_frame(self):
        """Creates the dedicated frame for OpenAI API configuration."""
        frame = ttk.LabelFrame(self, text="OpenAI Configuration", padding=10)
        frame.pack(fill='x', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="OpenAI API Key:").grid(row=0, column=0, sticky='w')
        self.api_key_entry = ttk.Entry(frame, width=50, show='*')
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        
        test_button = ttk.Button(frame, text="Save & Test", command=self.callbacks['test_openai'])
        test_button.grid(row=0, column=2, padx=5)

    def _create_worker_frame(self):
        """Creates the dedicated frame for the Worker endpoint configuration."""
        frame = ttk.LabelFrame(self, text="Local LLM / Worker Configuration", padding=10)
        frame.pack(fill='x', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Worker Endpoint URL:").grid(row=0, column=0, sticky='w', pady=2)
        self.worker_url_entry = ttk.Entry(frame, width=50)
        self.worker_url_entry.grid(row=0, column=1, padx=5, pady=2, sticky='ew')

        
        test_button = ttk.Button(frame, text="Save & Test", command=self.callbacks['test_worker'])
        test_button.grid(row=0, column=2, padx=5)

    def _create_whitelist_frame(self):
        whitelist_frame = ttk.LabelFrame(self, text="Whitelist (one window title per line)", padding=10)
        whitelist_frame.pack(fill='both', padx=5, pady=5, expand=True)
        self.whitelist_text = tk.Text(whitelist_frame, height=5, font=('Consolas', 9), wrap='word')
        self.whitelist_text.pack(fill='both', expand=True)

    def _create_appearance_frame(self):
        theme_frame = ttk.LabelFrame(self, text="Appearance", padding=10)
        theme_frame.pack(fill='x', padx=5, pady=5)
        light_rb = ttk.Radiobutton(theme_frame, text="Light Mode", variable=self.theme_var, value="light", command=lambda: self.theme_applier("light"))
        light_rb.pack(side='left', padx=10)
        dark_rb = ttk.Radiobutton(theme_frame, text="Dark Mode", variable=self.theme_var, value="dark", command=lambda: self.theme_applier("dark"))
        dark_rb.pack(side='left', padx=10)

    def get_settings_data(self) -> dict:
        return {
            'api_key': self.api_key_entry.get(),
            'worker_url': self.worker_url_entry.get(),
            'whitelist': self.whitelist_text.get('1.0', 'end-1c').splitlines()
        }

    def load_settings_data(self, settings: dict):
        self.api_key_entry.delete(0, 'end')
        self.api_key_entry.insert(0, settings.get('api_key', ''))
        self.worker_url_entry.delete(0, 'end')
        self.worker_url_entry.insert(0, settings.get('worker_url', ''))
        self.whitelist_text.delete('1.0', 'end')
        self.whitelist_text.insert('1.0', "\n".join(settings.get('whitelist', [])))

    def apply_theme(self, colors: dict):
        if self.whitelist_text:
            self.whitelist_text.configure(bg=colors["console_bg"], fg=colors["fg"])