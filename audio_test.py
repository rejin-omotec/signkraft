import queue
import time
from mods.audio_detect import SpeechRecognitionThread  # Replace with your actual module name

# Queue for recognized speech
speech_queue = queue.Queue(maxsize=10)

# Prompt user for language selection
language = input("Choose language (english/hindi): ").strip().lower()

# Start the speech recognition thread for the selected language
speech_thread = SpeechRecognitionThread(audio_queue=speech_queue, language=language)
speech_thread.start()

print(f"Listening for commands in {language}... Speak into the microphone!")

try:
    while True:
        # Check for speech commands
        try:
            if not speech_queue.empty():
                command = speech_queue.get(block=False)
                print(f"Recognized command: {command}")
        except queue.Empty:
            pass

        time.sleep(0.1)  # Small delay to avoid busy waiting

except KeyboardInterrupt:
    print("\nStopping speech recognition...")
    speech_thread.stop()
    speech_thread.join()
    print("Speech recognition stopped.")
