from pathlib import Path
from typing import Dict

# Paths
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "exports" / "best_datatrash_model.keras"
DEFAULT_CLASSES = ROOT / "exports" / "class_names.json"

# Inference and Control Settings
CONFIDENCE_THRESHOLD = 0.60
SEND_COOLDOWN_SECONDS = 0.75

# Four-relay demo mapping. The classifier has seven flower labels, so the
# remaining classes are routed to "0" (all relays off) unless expanded.
SERIAL_COMMANDS: Dict[str, bytes] = {
    "daisy": b"1",
    "dandelion": b"2",
    "lily": b"3",
    "orchid": b"4",
    "rose": b"0",
    "sunflower": b"0",
    "tulip": b"0",
}
