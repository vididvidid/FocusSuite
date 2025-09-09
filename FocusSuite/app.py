import os
import logging
import threading
import requests
from tkinter import messagebox

# Third-party
import keyboard
import pytesseract
from PIL import Image
from pystray import Icon as pystray_Icon, Menu as pystray_Menu, MenuItem as pystray_MenuItem

# local imports
from config import ConfigManager
from api.openai_manager import OpenAIAPIManager
from api.worker_api import WorkerTextAPIManager
from api.vision_api_manager import VisionAPIManager
from core.video_feature_manager import VideoFeatureManager
from core.focus_monitor_manager import FocusMonitorManager 
from ui.main_window import MainWindow
from ui.overlay import SmartOverlayManager
from utils import windows_utils
from utils.constants import APP_VERSION, UPDATE_CHECK_URL, TESSERACT_CMD_PATH

# configure Tesseract
try:
    pytesseract.pytesseract.tesseract_command = TESSERACT_CMD_PATH
except Exception:
    pass


class OptimizedProductivitySuite:
    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(__name__)
        self.config = ConfigManager()

        self.api_manager = OpenAIAPIManager(self.logger)
        self.worker_api_manager = WorkerTextAPIManager(self.logger)
        self.vision_api_manager = VisionAPIManager(self.logger)
        self.video_manager = VideoFeatureManager(self.logger, self.root, self.vision_api_manager)
        self.overlay_manager = SmartOverlayManager(self.root)

        monitor_ui_callbacks = {
            'on_start': self._on_monitoring_started,
            'on_stop': self._on_monitoring_stopped,
            'show_message': self.show_ui_message,
        }
        self.monitor_manager = FocusMonitorManager(
            self.root, self.config, self.api_manager, 
            self.overlay_manager, monitor_ui_callbacks, self.logger
        )

        self.tray_icon = None

        app_callbacks = {
            'start': lambda: self.monitor_manager.start_monitoring(self.ui.distraction_tab.focus_entry.get().strip()),
            'stop': self.monitor_manager.stop_monitoring,
            'save_settings': self._save_settings_from_ui,
            'test_openai': self.test_openai_api,
            'test_worker': self.test_worker_api,
            'get_setting': self.config.get,
            'set_setting': self.config.set,
            'get_version': lambda: APP_VERSION,
            'select_video': self.video_manager.select_video,
            'start_video_processing': self.video_manager.start_video_processing,
        }
        self.ui = MainWindow(root, app_callbacks)
        self.video_manager.register_ui_tabs(self.ui.video_tab)

        self._initialize()

    def _initialize(self):
        """Final setup steps after the UI is created."""
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        app_title = f"FocusSuite v{APP_VERSION}"
        current_whitelist = self.config.get('whitelist', [])
        if app_title not in current_whitelist:
            current_whitelist.append(app_title)
            self.config.set('whitelist', current_whitelist)
            self.config.save()
            self.logger.info(f"Application window '{app_title}' auto-whitelisted.")

        self.ui.load_settings()

        if hasattr(self.ui.settings_tab, 'worker_url_entry') and self.ui.settings_tab.worker_url_entry:
            if not self.ui.settings_tab.worker_url_entry.get():
                worker_url_from_env = os.getenv("WORKER_API_URL")
                if worker_url_from_env:
                    self.ui.settings_tab.worker_url_entry.insert(0, worker_url_from_env)
                    self.logger.info("Loaded Worker Endpoint URL from .env file.")
        else:
            self.logger.warning("'worker_url_entry' UI element not found on settings tab.")

        self.configure_api_from_settings()
        self._setup_keyboard_shortcuts()
        self._setup_tray_icon()
        self.check_for_updates()
        self._verify_tesseract()

    def _verify_tesseract(self):
        """Checks for Tesseract installation and logs/shows an error if not found."""
        try:
            pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract version {pytesseract.get_tesseract_version()} found.")
        except pytesseract.TesseractNotFoundError:
            msg = 'Tesseract OCR is not found. Please install it and ensure the path in utils/constants.py is correct.'
            self.logger.error(msg)
            self.ui.show_message('error', 'Tesseract Not Found', msg)

    def _on_monitoring_started(self):
        """Callback function to update UI when monitoring starts."""
        self.ui.distraction_tab.start_button.config(state='disabled')
        self.ui.distraction_tab.stop_button.config(state='normal')
        self.ui.status_label.config(text="Status: Running")
        self.hide_to_tray()

    def _on_monitoring_stopped(self):
        """Callback function to update UI when monitoring stops."""
        self.ui.distraction_tab.start_button.config(state='normal')
        self.ui.distraction_tab.stop_button.config(state='disabled')
        self.ui.status_label.config(text="Status: Idle")
        
    def show_ui_message(self, *args):
        """Helper to allow managers to show messages in the UI."""
        self.ui.show_message(*args)
        

    def configure_api_from_settings(self):
        """Configures the OpenAI API manager from settings or .env file."""
        api_key = self.ui.settings_tab.api_key_entry.get()
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.ui.settings_tab.api_key_entry.delete(0, 'end')
                self.ui.settings_tab.api_key_entry.insert(0, api_key)
                self.logger.info("Loaded OpenAI API key from .env file.")

        if self.api_manager.configure(api_key):
            self.ui.connection_label.config(text="API: Online", style="Success.TLabel")
        else:
            self.ui.connection_label.config(text="API: Offline", style="Error.TLabel")
    
    def test_openai_api(self):
        """Tests the OpenAI API connection using the key from the UI."""
        api_key = self.ui.settings_tab.api_key_entry.get()
        self.config.set('api_key', api_key)
        self.config.save()
        self.logger.info("Saved OpenAI API key, now testing.")
        
        self.configure_api_from_settings()
        
        if self.api_manager.test_connection():
            self.ui.show_message("info", "Success", "OpenAI API connection successful!")
        else:
            self.ui.show_message("error", "Failed", "Could not connect to OpenAI API. Check your key and network.")

    def test_worker_api(self):
        """Tests the local worker API connection using the URL from the UI."""
        worker_url = self.ui.settings_tab.worker_url_entry.get()
        self.config.set('worker_url', worker_url)
        self.config.save()
        self.logger.info("Saved Worker URL, now testing.")

        if self.worker_api_manager.test_connection(worker_url):
            self.ui.show_message("info", "Success", "Worker endpoint connection successful!")
        else:
            self.ui.show_message("error", "Failed", "Could not connect to the Worker endpoint. Check the URL and ensure the worker is running.")

    def _save_settings_from_ui(self, show_success_popup=True):
        """Gathers settings from all UI tabs and saves them to the config file."""
        try:
            settings_data = self.ui.settings_tab.get_settings_data()
            for key, value in settings_data.items():
                self.config.set(key, value)

            self.config.set('provider', self.ui.distraction_tab.provider_var.get())
            self.config.set('last_focus_topic', self.ui.distraction_tab.focus_entry.get())
            
            self.config.save()
            
            if show_success_popup:
                self.ui.show_message("info", "Success", "Settings have been saved.")
            self.logger.info("Settings saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
            self.ui.show_message('error', 'Error', f'Could not save settings: {e}')

    def _setup_keyboard_shortcuts(self):
        """Registers global hotkeys."""
        try:
            toggle_func = lambda: self.monitor_manager.toggle_monitoring(
                get_focus_topic_func=lambda: self.ui.distraction_tab.focus_entry.get().strip()
            )
            keyboard.add_hotkey('ctrl+shift+s', toggle_func)
            self.logger.info("Global keyboard shortcut 'Ctrl+Shift+S' registered.")
        except Exception as e:
            self.logger.warning(f"Failed to register global hotkey: {e}. Try running as administrator.")

    def _setup_tray_icon(self):
        """Initializes and runs the system tray icon."""
        image = Image.new('RGB', (64, 64), 'black')
        toggle_func = lambda: self.monitor_manager.toggle_monitoring(
                get_focus_topic_func=lambda: self.ui.distraction_tab.focus_entry.get().strip()
            )
        menu = pystray_Menu(
            pystray_MenuItem('Show', self.show_from_tray, default=True),
            pystray_MenuItem('Toggle Monitoring', toggle_func),
            pystray_Menu.SEPARATOR,
            pystray_MenuItem('Quit', self.quit_app)
        )
        self.tray_icon = pystray_Icon("FocusSuite", image, "FocusSuite", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self):
        """Hides the main window."""
        self.root.withdraw()
        self.logger.info("Application hidden to system tray.")

    def show_from_tray(self):
        """Shows the main window from the system tray."""
        self.root.deiconify()

    def quit_app(self):
        """Shuts down the application cleanly."""
        self.logger.info("Quit command received. Shutting down.")
        self.monitor_manager.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        self.root.quit()

    def check_for_updates(self):
        """Checks for new application versions in a background thread."""
        def run_check():
            try:
                response = requests.get(UPDATE_CHECK_URL, timeout=5)
                response.raise_for_status()
                latest_version = response.text.strip()
                if latest_version > APP_VERSION:
                    self.logger.info(f"New version available: {latest_version}")
                    self.root.after(0, self.ui.show_message, "info", "Update Available", f"A new version ({latest_version}) is available!")
                else:
                    self.logger.info("Application is up to date.")
            except requests.RequestException as e:
                self.logger.warning(f"Could not check for updates: {e}")
        
        threading.Thread(target=run_check, daemon=True).start()