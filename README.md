# Flower Classification & AIoT Integration

This project is an end-to-end machine learning pipeline for classifying different species of flowers using a Convolutional Neural Network (CNN) built with TensorFlow/Keras. The project also features an AIoT (Artificial Intelligence of Things) integration where the trained model acts as a "digital brain" to control hardware relays (via a NodeMCU/Arduino) based on real-time webcam detection.

## Features

- **Flower Classification Model**: A CNN trained to classify various flower species (Daisy, Dandelion, Lily, Orchid, Rose, Sunflower, Tulip).
- **Real-Time Webcam Inference**: Live detection using a webcam, predicting the flower presented in front of the camera.
- **AIoT Hardware Control**: Communicates via serial port with a NodeMCU to control hardware relays. For example, showing a Daisy triggers Relay 1, a Dandelion triggers Relay 2, etc.
- **Simulation Mode**: Run the live inference without physical hardware connected by utilizing the built-in simulation mode.

## Project Structure

- `aiot/`: Contains the AIoT integration scripts and Arduino sketches.
  - `flower_aiot_serial.py`: The main script to run real-time inference and send serial commands.
  - `settings.py`: Configuration file for the AIoT script.
  - `arduino/`: Arduino sketches for the NodeMCU to receive serial commands and toggle relays.
  - `diagrams/`: Wiring diagrams for connecting the NodeMCU to relays.
- `exports/`: Contains the trained `.keras` model and the `class_names.json` file.
- `models/`: Scripts/notebooks used for training and evaluating the model.
- `requirements.txt`: Python dependencies needed to run the project.

## Quick Start

### 1. Installation

Ensure you have Python 3 installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Running in Simulation Mode

If you don't have a NodeMCU connected, you can run the AIoT script in simulation mode to test the webcam inference:

```bash
python aiot/flower_aiot_serial.py
```
*(Press `q` in the camera preview window to stop)*

### 3. Running with NodeMCU Hardware

Connect your NodeMCU to your computer via USB and specify the COM port (Windows) or TTY USB port (Linux/macOS):

**Windows:**
```bash
python aiot/flower_aiot_serial.py --serial-port COM3
```

**Linux / macOS:**
```bash
python aiot/flower_aiot_serial.py --serial-port /dev/ttyUSB0
```

> **Note**: For more details regarding the hardware setup and wiring, please refer to the [AIoT README](aiot/README.md).
