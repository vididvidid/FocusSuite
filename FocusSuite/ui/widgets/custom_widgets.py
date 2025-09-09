import tkinter as tk

class Console(tk.Text):
    """
    A Custom Text Widget for logging, with support for color-coded 
    log levels.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_configure("info",foreground="#00BFFF")
        self.tag_configure("debug", foreground="#A9A9A9")
        self.tag_configure("warning", foreground="#FFA500")
        self.tag_configure("error", foreground="#FF4C4C")
        self.tag_configure("critical", foreground="#FF0000",font=('Consolas',9,'bold'))

    def log(self, message, level='info'):
        """
        Inserts a new message into the console with the 
        appropriate tag.
        """
        self.insert('end',f"{message}\n", level)
        self.see('end')

