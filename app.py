import os
import time
import json
import logging
import threading
import requests
from tkinter import messagebox

# Third-party
import keyboard
import pytesseract
from PIL import Image, ImageGrab
import numpy as np
from pystray import Icon as pystray_Icon, Menu as pystray_Menu, MenuItem as pystray_MenuItem
from skimage.metrics import structural_similarity as ssim

# local imports
from config import ConfigManager
from api.openai_manager import OpenAIAPIManager
# api.worker_api is not in the provided context, assuming it exists
# from api.worker_api import WorkerTextAPIManager
from api.vision_api_manager import VisionAPIManager
from core.video_feature_manager import VideoFeatureManager
from core.models import DistractionArea
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

        self.vision_api_manager = VisionAPIManager(self.logger)
        self.video_manager = VideoFeatureManager(self.logger, self.root, self.vision_api_manager)

        self.monitoring = False
        self.monitor_thread = None
        self.tray_icon = None
        self.focus_topic = ""

        app_callbacks = {
            'start': self.start_monitoring,
            'stop': self.stop_monitoring,
            'save_settings': self._save_settings_from_ui,
            'test_api': self.test_api,
            'get_setting': self.config.get,
            'set_setting': self.config.set,
            'get_version': lambda: APP_VERSION,
            'select_video': self.video_manager.select_video,
            'start_video_processing': self.video_manager.start_video_processing,
        }
        self.ui = MainWindow(root, app_callbacks)
        self.overlay_manager = SmartOverlayManager(self.root)

        self.video_manager.register_ui_tabs(self.ui.video_tab)

        self._initialize()

    def _initialize(self):
        # final setup steps after ui is created
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
        # verify tesseract installation
        try:
            pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract version {pytesseract.get_tesseract_version()} found.")
        except pytesseract.TesseractNotFoundError:
            msg = 'Tesseract OCR is not found. Please install it and ensure the path in utils/constants.py is correct.'
            self.logger.error(msg)
            self.ui.show_message('error', 'Tesseract Not Found', msg)

    def start_monitoring(self):
        focus_topic = self.ui.distraction_tab.focus_entry.get().strip()
        if not focus_topic:
            self.ui.show_message('warning', "Input Required", "Please enter a focus topic.")
            return
        if not self.api_manager.is_available():
            self.ui.show_message('error', "API Error", "API is not configured or offline. Cannot start.")
            return

        self.focus_topic = focus_topic
        self.config.set('last_focus_topic', self.focus_topic)
        self.config.save()
        self.monitoring = True

        self.ui.distraction_tab.start_button.config(state='disabled')
        self.ui.distraction_tab.stop_button.config(state='normal')
        self.ui.status_label.config(text="Status: Running")
        self.logger.info(f"Monitoring started for topic: '{self.focus_topic}'")
        self.hide_to_tray()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        self.overlay_manager.hide()
        self.ui.distraction_tab.start_button.config(state='normal')
        self.ui.distraction_tab.stop_button.config(state='disabled')
        self.ui.status_label.config(text="Status: Idle")
        self.logger.info("Monitoring stopped.")

    def toggle_monitoring(self):
        if self.monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()

    def _monitor_loop(self):
        last_screenshot_gray = None
        self.logger.info("Monitor loop started.")
        while self.monitoring:
            time.sleep(2)

            if windows_utils.is_whitelisted(self.config.get('whitelist', [])):
                self.overlay_manager.hide()
                continue

            try:
                bbox = windows_utils.get_active_window_bbox()
                if not bbox:
                    continue
                screenshot = ImageGrab.grab(bbox=bbox)
            except Exception as e:
                self.logger.error(f"Failed to grab screenshot: {e}")
                continue

            current_screenshot_small = screenshot.resize((256, 144))
            current_screenshot_gray = np.array(current_screenshot_small.convert('L'))

            if last_screenshot_gray is not None:
                score, _ = ssim(last_screenshot_gray, current_screenshot_gray, full=True)
                if score > 0.98:
                    continue
                self.logger.info(f"Significant screen change detected (SSIM Score: {score:.4f}).")

            last_screenshot_gray = current_screenshot_gray
            distractions = self._process_screenshot(screenshot)
            
            if not self.monitoring:
                break

            adjusted_distractions = []
            for d in distractions:
                d.x += bbox[0]
                d.y += bbox[1]
                adjusted_distractions.append(d)

            self.root.after(0, self.overlay_manager.update_or_create_overlay, adjusted_distractions)
            
            
    def _process_screenshot(self, screenshot: Image.Image) -> list[DistractionArea]:
        try:
            ocr_data = pytesseract.image_to_data(
                screenshot, output_type=pytesseract.Output.DICT, config='--psm 6'
            )
            full_text = " ".join([word for i, word in enumerate(ocr_data['text']) if word.strip() and int(ocr_data['conf'][i]) > 40])
            if not full_text:
                return []

            prompt = f"Review the text from a screen. The user's goal is '{self.focus_topic}'. Identify unrelated text. Text: \"{full_text[:3000]}\""
            response_text = self.api_manager.generate_with_retry(prompt)
            if not response_text:
                return []

            data = json.loads(response_text)
            distracting_phrases = data.get("distractions", [])
            if not isinstance(distracting_phrases, list) or not distracting_phrases:
                return []

            self.logger.info(f"Distractions found: {distracting_phrases}")

            distraction_areas = []
            for phrase in distracting_phrases:
                phrase_words = phrase.lower().strip().split()
                if not phrase_words: continue

                for i in range(len(ocr_data['text']) - len(phrase_words) + 1):
                    ocr_phrase_segment = [ocr_data['text'][i + j].lower() for j in range(len(phrase_words))]
                    if " ".join(phrase_words) in " ".join(ocr_phrase_segment):
                        x = ocr_data['left'][i]
                        y = ocr_data['top'][i]
                        w = (ocr_data['left'][i + len(phrase_words) - 1] + ocr_data['width'][i + len(phrase_words) - 1]) - x
                        h = max(ocr_data['height'][k] for k in range(i, i + len(phrase_words)))
                        distraction_areas.append(DistractionArea(x, y, w, h, 1.0, phrase))
                        break
            return distraction_areas
        except json.JSONDecodeError as e:
            self.logger.warning(f"Could not parse JSON from API response: {response_text}. Error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error processing screenshot: {e}")
            return []

    def configure_api_from_settings(self):
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
    
    def test_api(self):
        """Saves current settings and then tests the API connection."""
        self._save_settings_from_ui(show_success_popup=False)
        self.configure_api_from_settings()
        
        if self.api_manager.test_connection():
            self.ui.show_message("info", "Success", "API connection successful!")
        else:
            self.ui.show_message("error", "Failed", "Could not connect to API. Check your key and network.")

    def _save_settings_from_ui(self, show_success_popup=True):
        """
        Gathers settings from all UI tabs and saves them to the config file.
        """
        try:
            # Get data from the settings tab using its public helper method
            settings_data = self.ui.settings_tab.get_settings_data()
            for key, value in settings_data.items():
                self.config.set(key, value)

            # Get data from the distraction tab
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
        try:
            keyboard.add_hotkey('ctrl+shift+s', self.toggle_monitoring)
            self.logger.info("Global keyboard shortcut 'Ctrl+Shift+S' registered.")
        except Exception as e:
            self.logger.warning(f"Failed to register global hotkey: {e}. Try running as administrator.")

    def _setup_tray_icon(self):
        image = Image.new('RGB', (64, 64), 'black')
        menu = pystray_Menu(
            pystray_MenuItem('Show', self.show_from_tray, default=True),
            pystray_MenuItem('Toggle Monitoring', self.toggle_monitoring),
            pystray_Menu.SEPARATOR,
            pystray_MenuItem('Quit', self.quit_app)
        )
        self.tray_icon = pystray_Icon("FocusSuite", image, "FocusSuite", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self):
        self.root.withdraw()
        self.logger.info("Application hidden to system tray.")

    def show_from_tray(self):
        self.root.deiconify()

    def quit_app(self):
        self.logger.info("Quit command received. Shutting down.")
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        self.root.quit()

    def check_for_updates(self):
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