# rules/rules_loader.py
"""
Load and validate rules.json for the explainable rule engine.

Expected schema:
{
  "version": "1.0",
  "metadata": {...},
  "rules": {
    "fever": {"Condition A": 3, "Condition B": 1},
    ...
  }
}
"""

import json
from pathlib import Path
from typing import Dict, Optional

DEFAULT_RULES_PATH = Path("rules.json")

class RulesLoadError(Exception):
    pass

def load_rules(path: Optional[str] = None) -> Dict[str, Dict[str, int]]:
    p = DEFAULT_RULES_PATH if path is None else Path(path)
    if not p.exists():
        raise RulesLoadError(f"Rules file not found at {p.resolve()}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise RulesLoadError(f"Failed to parse JSON: {e}")
    if "rules" not in data or not isinstance(data["rules"], dict):
        raise RulesLoadError("Invalid rules file: missing 'rules' dict")
    cleaned = {}
    for token, mapping in data["rules"].items():
        if not isinstance(mapping, dict):
            raise RulesLoadError(f"Invalid mapping for token '{token}'")
        token_key = str(token).lower().strip()
        inner = {}
        for cond, weight in mapping.items():
            if not isinstance(weight, int) or weight <= 0:
                raise RulesLoadError(f"Weight for '{token}' -> '{cond}' must be a positive integer")
            inner[str(cond).strip()] = int(weight)
        cleaned[token_key] = inner
    return cleaned

if __name__ == "__main__":
    try:
        r = load_rules()
        print(f"Loaded {len(r)} tokens")
    except Exception as e:
        print("Error:", e)
