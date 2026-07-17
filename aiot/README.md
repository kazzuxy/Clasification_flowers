# Flower AIoT Serial Relay Demo

This folder adds a mid-project AIoT integration path for the trained flower CNN.
The laptop runs inference, sends serial commands to a NodeMCU, and the NodeMCU
activates one relay output for confident detections.

## Architecture

```text
Webcam -> CNN Python -> PySerial -> USB -> NodeMCU -> Relay module -> LED/DC lamp
```

## Class-to-relay rules

| CNN class | Serial command | Relay action |
| --- | --- | --- |
| daisy | `1` | Relay 1 ON |
| dandelion | `2` | Relay 2 ON |
| lily | `3` | Relay 3 ON |
| orchid | `4` | Relay 4 ON |
| rose, sunflower, tulip | `0` | All relays OFF |

The Python controller only sends commands when the confidence is at least 60%
and the detected class changes. This state-change debounce keeps the serial link
stable even when the webcam produces many frames per second.

## Run the Python controller

Install runtime dependencies if they are not already available:

```bash
pip install tensorflow opencv-python pyserial numpy
```

Run on Windows:

```bash
python aiot/flower_aiot_serial.py --serial-port COM3
```

Run on Linux/macOS:

```bash
python aiot/flower_aiot_serial.py --serial-port /dev/ttyUSB0
```

Press `q` in the camera preview window to stop.

## Upload the Arduino sketch

1. Open `aiot/arduino/FlowerRelaySerial/FlowerRelaySerial.ino` in Arduino IDE.
2. Select the correct NodeMCU ESP8266/ESP32 board and USB port.
3. Upload the sketch.
4. Open Serial Monitor at `115200` baud to verify command acknowledgements.

## Wiring summary

Use the diagram in `aiot/diagrams/flower_aiot_serial_wiring.svg` as the project
schematic. For a NodeMCU ESP8266 demo:

| NodeMCU pin | Relay input | Suggested load |
| --- | --- | --- |
| D1 / GPIO5 | IN1 | LED/DC lamp 1 |
| D2 / GPIO4 | IN2 | LED/DC lamp 2 |
| D5 / GPIO14 | IN3 | LED/DC lamp 3 |
| D6 / GPIO12 | IN4 | LED/DC lamp 4 |
| 5V/VU | VCC | Relay VCC |
| GND | GND | Common ground |

> Safety: demonstrate with LEDs, small DC lamps, or other low-voltage 5V-12V
> loads only. Do not connect classroom prototypes to 220V AC mains.
