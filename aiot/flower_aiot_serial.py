"""Real-time flower CNN inference with Serial control for NodeMCU relays.

This script turns the trained flower classifier into the "digital brain" for an
AIoT demo. It reads webcam frames, runs the exported TensorFlow/Keras model,
and sends a compact command to a NodeMCU only when the confident prediction
changes. The state-change debounce prevents serial buffer spam at webcam FPS.

Example:
    python aiot/flower_aiot_serial.py --serial-port COM3
    python aiot/flower_aiot_serial.py --serial-port /dev/ttyUSB0 --camera 0
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
import serial
import tensorflow as tf

from settings import (
    DEFAULT_MODEL,
    DEFAULT_CLASSES,
    CONFIDENCE_THRESHOLD,
    SEND_COOLDOWN_SECONDS,
    SERIAL_COMMANDS,
)


def load_class_names(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def preprocess(frame: np.ndarray, image_size: Tuple[int, int]) -> np.ndarray:
    resized = cv2.resize(frame, image_size)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    return np.expand_dims(rgb.astype("float32"), axis=0)


def predict_frame(model: tf.keras.Model, frame: np.ndarray, class_names: list[str]) -> tuple[str, float]:
    height, width = model.input_shape[1], model.input_shape[2]
    predictions = model.predict(preprocess(frame, (width, height)), verbose=0)[0]
    index = int(np.argmax(predictions))
    return class_names[index], float(predictions[index])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CNN flower detection to NodeMCU relay commands")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL, help="Path to Keras model")
    parser.add_argument("--classes", type=Path, default=DEFAULT_CLASSES, help="Path to class_names.json")
    parser.add_argument("--serial-port", default="sim", help="NodeMCU port (e.g. COM3). Use 'sim' for simulation mode.")
    parser.add_argument("--baudrate", type=int, default=115200, help="Serial baud rate")
    parser.add_argument("--camera", type=int, default=0, help="OpenCV camera index")
    parser.add_argument("--width", type=int, default=640, help="Camera capture width")
    parser.add_argument("--height", type=int, default=480, help="Camera capture height")
    parser.add_argument("--threshold", type=float, default=CONFIDENCE_THRESHOLD, help="Minimum confidence")
    return parser.parse_args()


class DummySerial:
    def write(self, data: bytes):
        pass
    def flush(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def main() -> None:
    args = parse_args()
    class_names = load_class_names(args.classes)
    
    # Patch for 'quantization_config' compatibility in Keras 3
    original_dense_init = tf.keras.layers.Dense.__init__
    def patched_dense_init(self, *args, **kwargs):
        kwargs.pop("quantization_config", None)
        original_dense_init(self, *args, **kwargs)
    tf.keras.layers.Dense.__init__ = patched_dense_init
            
    model = tf.keras.models.load_model(args.model)

    camera = cv2.VideoCapture(args.camera)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    if not camera.isOpened():
        raise RuntimeError(f"Camera index {args.camera} cannot be opened")

    last_sent_class = ""
    last_sent_at = 0.0

    if args.serial_port.lower() == "sim":
        serial_ctx = DummySerial()
        print("Running in SIMULATION mode. No real serial commands will be sent.")
    else:
        serial_ctx = serial.Serial(args.serial_port, args.baudrate, timeout=1)

    with serial_ctx as node_mcu:
        if args.serial_port.lower() != "sim":
            time.sleep(2)  # allow NodeMCU reset after USB serial connection
        print("Press 'q' in the preview window to stop.")

        while True:
            ok, frame = camera.read()
            if not ok:
                break

            label, confidence = predict_frame(model, frame, class_names)
            display = f"{label}: {confidence:.0%}"

            current_time = time.monotonic()
            confident = confidence >= args.threshold
            changed = label != last_sent_class
            cooled_down = current_time - last_sent_at >= SEND_COOLDOWN_SECONDS

            if confident and changed and cooled_down:
                command = SERIAL_COMMANDS.get(label, b"0")
                node_mcu.write(command)
                node_mcu.flush()
                last_sent_class = label
                last_sent_at = current_time
                print(f"Sent {command.decode()} for {display}")
            elif not confident and last_sent_class != "none" and cooled_down:
                node_mcu.write(b"0")
                node_mcu.flush()
                last_sent_class = "none"
                last_sent_at = current_time
                print(f"Sent 0 because confidence is low ({display})")

            color = (0, 180, 0) if confident else (0, 0, 255)
            cv2.putText(frame, display, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            cv2.imshow("Flower AIoT Serial Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
