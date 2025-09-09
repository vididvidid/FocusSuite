import tkinter as tk
from tkinter import ttk, scrolledtext

class VideoTab(ttk.Frame):
    def __init__(self,parent,callbacks):
        super().__init__(parent,padding=10)
        self.callbacks = callbacks
        self.columnconfigure(0,weight=1)

        self._create_widgets()

    def _create_widgets(self):
        video_select_frame = ttk.LabelFrame(self,text="1.Select Video",padding=10)
        video_select_frame.grid(row=0,column=0,padx=(0,10),pady=(0,10),sticky="ew")
        video_select_frame.columnconfigure(1,weight=1)

        self.select_video_button = ttk.Button(video_select_frame, text="Browse...",command=self.callbacks['select_video'])
        self.select_video_button.grid(row=0,column=0, padx=(0,5))

        self.video_path_label = ttk.Label(video_select_frame, text="No video selected.", wraplength=450)
        self.video_path_label.grid(row=0, column=1, stick="w")

        # prompt
        prompt_frame = ttk.LabelFrame(self, text="2. Describe what to Blur", padding=10)
        prompt_frame.grid(row=1, column=0, padx=(0,10), pady=10, stick="ew")
        prompt_frame.columnconfigure(0,weight=1)


        self.video_prompt_entry = ttk.Entry(prompt_frame)
        self.video_prompt_entry.grid(row=0, column=0, sticky="ew")
        self.video_prompt_entry.insert(0, "e.g., a person walking")

        # action and progress
        action_frame = ttk.Frame(self)
        action_frame.grid(row=2, column=0, padx=(0,10), pady=10, stick="ew")
        action_frame.columnconfigure(0,weight=1)

        self.start_video_button = ttk.Button(action_frame, text="Start Processing", command=self.callbacks['start_video_processing'])
        self.start_video_button.grid(row=0,column=0, sticky="ew")

        progress_frame = ttk.LabelFrame(self, text="Progress", padding=10)
        progress_frame.grid(row=3, column=0,padx=(0,10), pady=10, sticky="nsew")
        self.rowconfigure(3,weight=1)
        progress_frame.columnconfigure(0,weight = 1)
        progress_frame.rowconfigure(0,weight=1)

        self.video_log_text = scrolledtext.ScrolledText(progress_frame, height=8, state='disabled', wrap=tk.WORD)

        self.video_log_text.grid(row=0, column=0, sticky="nsew")

    def append_video_log(self,message: str):
        self.video_log_text.config(state='normal')
        self.video_log_text.insert(tk.END,message + '\n')
        self.video_log_text.see(tk.END)
        self.video_log_text.config(state='disabled')
        self.master.update_idletasks()
