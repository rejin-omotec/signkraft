import pyaudio
from vosk import Model, KaldiRecognizer

# Load the model from the specified path
model = Model("data/audio_model_en")
recognizer = KaldiRecognizer(model, 16000)

# Audio settings
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

print("Listening... Speak something!")

# Variable to track the last printed partial result
last_partial = ""

# Recognition loop
try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        if len(data) == 0:
            continue

        # Process partial results
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result).get("text", "")
            if text:  # Print final result only if non-empty
                print(f"Final Recognized: {text}")
            last_partial = ""  # Reset partial result tracker
        else:
            partial = eval(recognizer.PartialResult()).get("partial", "")
            if partial != last_partial:  # Only print if partial has changed
                print(f"Partial Recognized: {partial}")
                last_partial = partial

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
