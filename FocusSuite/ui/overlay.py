# manages the transparent, click through overlay window that displays distraction boxes.

import tkinter as tk
from typing import List
from core.models import DistractionArea

class SmartOverlayManager:
    #Manages a single, dynamically updatable overlay window.
    def __init__(self, root: tk.Tk):
        self.root = root
        self.overlay_window = None
        self.canvas = None
        self.drawn_rects = []

    def _create_window(self):
        #Creates the full-screen, transparent toplevel window.
        self.overlay_window = tk.Toplevel(self.root)
        self.overlay_window.overrideredirect(True)
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.attributes("-alpha",0.7)
        self.overlay_window.attributes("-transparentcolor","white")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self.overlay_window, bg="white", highlightthickness=0)
        self.canvas.pack(fill='both', expan=True)

    def update_or_create_overlay(self, areas: List[DistractionArea]):
        # clears old distraction boxes and draws new ones.
        if not self.overlay_window or not self.overlay_window.winfo_exists():
            self._create_window()

        for rect in self.drawn_rects:
            self.canvas.delete(rect)
        self.drawn_rects.clear()

        for area in areas:
            rect_id = self.canvas.create_rectangle(
                area.x, area.y, area.x + area.width, area.y + area.height,
                fill='black', outline='red', width=1
            )
            self.drawn_rects.append(rect_id)

        if areas:
            self.show()
        else:
            self.hide()

    def show(self):
        if self.overlay_window and self.overlay_window.winfo_exists():
            self.overlay_window.deiconify()

    def hide(self):
        if self.overlay_window and self.overlay_window.winfo_exists():
            self.overlay_window.withdraw()

    def destroy(self):
        if self.overlay_window and self.overlay_window.winfo_exists():
            self.overlay_window.destroy()
        self.overlay_window = None
