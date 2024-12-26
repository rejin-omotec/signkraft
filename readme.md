
# Speech Recognition with Vosk and MediaPipe

This project demonstrates setting up speech recognition using the Vosk API and gesture tracking with MediaPipe.

## Prerequisites

1. Python 3.7 or higher.
2. Pip (Python package manager).

## Installation

Install the required Python libraries:

```bash
pip install vosk mediapipe pyaudio numpy
```

## Model Setup

Ensure you have the Vosk model in the `data` folder. The structure should look like this:

```
models/
└── audio_model_en
└── audio_model_hi
```

If the application does not work, check if the model exists in the `models` folder.

## Running the Application

Run the main script:

```bash
python main_menu.py
```

If you encounter issues, confirm the model is in the `data` folder and correctly configured.

## Troubleshooting

- Make sure all dependencies are installed:
  ```bash
  pip install vosk mediapipe pyaudio numpy
  ```
- Verify the `models` folder contains the required Vosk model.

Enjoy building your application!
