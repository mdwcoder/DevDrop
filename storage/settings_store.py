import json
import os
from typing import Any

SETTINGS_FILE = "settings.json"

class SettingsStore:
    @staticmethod
    def load() -> dict[str, Any]:
        if not os.path.exists(SETTINGS_FILE):
            return {}
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def save(settings: dict[str, Any]):
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")
