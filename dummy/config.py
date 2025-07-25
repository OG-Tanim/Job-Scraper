#heloper funciton to load companies from json file
import json
from pathlib import Path 

COMPANIES_FILE = Path(__file__).parent / "companies.json"

def load_companies():
    with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)