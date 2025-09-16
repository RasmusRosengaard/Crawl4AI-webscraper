import json
from pathlib import Path


class Config:

    def __init__(self):
        CONFIG_PATH = Path(__file__).parent /"config.json"
        with open(CONFIG_PATH, "r") as f:
            CONFIG = json.load(f)

        self.url = CONFIG.get("Url", [])
        self.mode = CONFIG.get("Mode", "Crawl")




      


