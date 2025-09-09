import tkinter as tk
from tkinter import ttk
from ui.widgets.custom_widgets import Console

class DistractionBlockerTab(ttk.Frame):
    """
    A ttk.Frame that contains all widgets for the distraction 
    blocker feature.
    """

    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callbacks = callback

        # Widget variables
        self.provider_var = tk.StringVar()
        self.focus_entry = None
        self.start_button = None
        self.stop_button = None
        self.console_text = None

        self._setup_widgets()

    def _setup_widgets(self):
        self._create_control_frame()
        self._create_console_frame()

    def _create_control_frame(self):
        control_frame = ttk.LabelFrame(self, text="Focus Control", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        control_frame.grid_columnconfigure(1,weight=1)

        ttk.Label(control_frame, text="AI Provider:").grid(row=0, column=0, sticky='w', pady=2)
        provider_menu = ttk.Combobox(
            control_frame,
            textvariable=self.provider_var,
            values=["OpenAI", "Worker Endpoint"],
            state = "readonly"
        )
        provider_menu.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        provider_menu.set("OpenAI")


        ttk.Label(control_frame, text="Focus Topic:").grid(row=1,column=0, sticky='w', pady=5)
        self.focus_entry = ttk.Entry(control_frame, width=40)
        self.focus_entry.grid(row=1, column=1, padx=5, pady=5,sticky='ew')

        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.callbacks['start'])
        self.start_button.pack(side='left', padx=5)
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.callbacks['stop'], state='disabled')
        self.stop_button.pack(side='left', padx=5)


    def _create_console_frame(self):
        console_frame = ttk.LabelFrame(self, text="Log", padding=5)
        console_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.console_text = Console(console_frame, height=10, font=('Consolas', 9), wrap='word')
        self.console_text.pack(side='left', fill='both', expand=True)

        console_scroll = ttk.Scrollbar(console_frame, command=self.console_text.yview)
        console_scroll.pack(side='right', fill='y')
        self.console_text.configure(yscrollcommand=console_scroll.set)

    def apply_theme(self, colors:dict):
        if self.console_text:
            self.console_text.configure(bg=colors["console_bg"],
                                        fg=colors["console_fg"])


