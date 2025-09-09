import json
import logging
import threading
import time

import numpy as np
import pytesseract
from PIL import ImageGrab
from skimage.metrics import structural_similarity as ssim

from core.models import DistractionArea
from utils import windows_utils


class FocusMonitorManager:
    """
    Manages the entire screen distraction monitoring feature.
    This class encapsulates the state, logic, and processing loop for identifying
    and reporting on-screen distractions.
    """
    def __init__(self, root, config, api_manager, overlay_manager, ui_callbacks, logger):
        self.root = root
        self.config = config
        self.api_manager = api_manager
        self.overlay_manager = overlay_manager
        self.ui_callbacks = ui_callbacks 
        self.logger = logger

        self.monitoring = False
        self.monitor_thread = None
        self.focus_topic = ""

    def start_monitoring(self, focus_topic: str):
        """Validates inputs and starts the monitoring loop in a background thread."""
        if not focus_topic:
            self.ui_callbacks['show_message']('warning', "Input Required", "Please enter a focus topic.")
            return
        if not self.api_manager.is_available():
            self.ui_callbacks['show_message']('error', "API Error", "API is not configured or offline. Cannot start.")
            return

        self.focus_topic = focus_topic
        self.config.set('last_focus_topic', self.focus_topic)
        self.config.save()
        self.monitoring = True

        if self.ui_callbacks.get('on_start'):
            self.ui_callbacks['on_start']() 

        self.logger.info(f"Monitoring started for topic: '{self.focus_topic}'")
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stops the monitoring loop and cleans up."""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        self.overlay_manager.hide()
        
        if self.ui_callbacks.get('on_stop'):
            self.ui_callbacks['on_stop']()

        self.logger.info("Monitoring stopped.")

    def toggle_monitoring(self, get_focus_topic_func):
        """Toggles the monitoring state."""
        if self.monitoring:
            self.stop_monitoring()
        else:
            topic = get_focus_topic_func()
            self.start_monitoring(topic)
            
    def _monitor_loop(self):
        """The main loop that captures, compares, and processes screenshots."""
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
            
    def _process_screenshot(self, screenshot: 'Image.Image') -> list[DistractionArea]:
        """
        Performs OCR on the screenshot, sends text to the AI for analysis,
        and maps distracting phrases back to their coordinates.
        """
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
            return distraction_areas
        except json.JSONDecodeError as e:
            self.logger.warning(f"Could not parse JSON from API response: {response_text}. Error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error processing screenshot: {e}")
            return []