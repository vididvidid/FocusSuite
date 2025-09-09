import logging
import logging.handlers
from tkinter import Text
from utils.constants import LOG_FILE

class TkinterTextHandler(logging.Handler):
    # a logging handler that directs records to a tkinter text widget.
    def __init__(self, text_widget: Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self.text_widget.log, msg, record.levelname.lower())

def setup_logging(console_widget=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5*1024*1024, backupCount=2
    )
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if console_widget:
        console_handler = TkinterTextHandler(console_widget)
        console_formatter = logging.Formatter('%(asctime)s - %(message)s', '%H:%M:%S')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    logging.info("Logging configured.")
