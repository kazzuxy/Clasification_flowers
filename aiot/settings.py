from pathlib import Path
from typing import Dict

# Paths
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "exports" / "best_datatrash_model.keras"
DEFAULT_CLASSES = ROOT / "exports" / "class_names.json"

# Inference and Control Settings
CONFIDENCE_THRESHOLD = 0.60
SEND_COOLDOWN_SECONDS = 0.75

# Four-relay demo mapping.
SERIAL_COMMANDS: Dict[str, bytes] = {
    "daisy": b"0",
    "dandelion": b"0",
    "lily": b"0",
    "orchid": b"1",      # Relay 1
    "rose": b"2",        # Relay 2
    "tulip": b"3",       # Relay 3
    "sunflower": b"4",   # Relay 4
}
