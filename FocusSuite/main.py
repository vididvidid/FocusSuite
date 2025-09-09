
import ctypes
import tkinter as tk
from dotenv import load_dotenv

from app import OptimizedProductivitySuite
from utils.logger import setup_logging

def main():
    load_dotenv()

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    root = tk.Tk()
    root.geometry("800x600")

    app =  OptimizedProductivitySuite(root)

    setup_logging(console_widget=app.ui.distraction_tab.console_text)

    root.mainloop()

if __name__ == "__main__":
    main()
