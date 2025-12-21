from pathlib import Path 
import json

BASE_DIR = Path(__file__).resolve().parent
LAN_RU = BASE_DIR / "language" / "ru.json"   
LAN_EN = BASE_DIR / "language" / "en.json"

class LanguageManager:
    def __init__(self, default_path):
        self.current_lang_code = "ru"
        self.data = {}
        self.load(default_path)

    def load(self, path, lang_code=None):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}
        if lang_code:
            self.current_lang_code = lang_code

    def t(self, key: str):
        cur = self.data
        for part in key.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return key
        return cur if isinstance(cur, str) else key

LANG = LanguageManager(LAN_RU)

def t(key: str) -> str:
    return LANG.t(key)
