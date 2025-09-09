# handles loading and saving of application settings from a json file

import json
import logging
from utils.constants import SETTINGS_FILE

logger = logging.getLogger(__name__)

class ConfigManager:
    # Handles loading and saving of application settings. 
    def __init__(self, file_path=SETTINGS_FILE):
        self.file_path = file_path
        self.settings = self.load()

    def load(self):
        # Loads settings from the JSON file, returning an empty dict on failure. 
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Settings file not found or corrupt, creating new one. Error: {e}")
            return {}
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading settings: {e}")
            return {}

    def save(self):
        # Saves the current settings to the JSON file
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.settings,f,indent=4)
        except IOError as e:
            logger.error(f"Could not save settings to {self.file_path}.Error: {e}")

    def get(self, key, default=None):
        # Get a value from settings, returning a default if not found.
        return self.settings.get(key,default)

    def set(self, key, value):
        #Sets a value in the settings.
        self.settings[key] = value
