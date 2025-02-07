import threading
import queue
import pyaudio
from vosk import Model, KaldiRecognizer
import time

class SpeechRecognitionThread(threading.Thread):
    def __init__(self, audio_queue, language="english", model_paths=None):
        super().__init__()
        self.audio_queue = audio_queue  # Queue to store recognized words
        self.stop_thread = False  # Flag to stop the thread
        self.language = language.lower()

        # Default model paths
        default_model_paths = {
            "english": "data/audio_model_en",
            "hindi": "data/audio_model_hi"
        }
        
        # Determine the model path
        if model_paths is None:
            model_paths = default_model_paths

        model_path = model_paths.get(self.language)
        if not model_path:
            raise ValueError(f"Unsupported language: {language}. Supported languages are: {list(model_paths.keys())}")

        # Load the model
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

        # Audio stream settings
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        self.stream.start_stream()

        # Predefined words for each language
        self.english_words = {"up", "down", "next", "previous", "left", "right", "select", "stop", "start", "quit"}
        self.hindi_words = {"ऊपर", "नीचे", "अगला", "पिछला","बायां","दायां", "चयन ", "रोकें ", "शुरू", "छोड़ें" }

        # Tracking results
        self.last_result = ""
        self.last_result_time = time.time()
        self.result_threshold = 1.5  # Time threshold in seconds

    def run(self):
        print("Speech Recognition Started!")
        try:
            while not self.stop_thread:
                data = self.stream.read(1024, exception_on_overflow=False)

                if len(data) == 0:
                    continue

                # Process speech input
                current_time = time.time()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = eval(result).get("text", "")
                    if text and (text != self.last_result or (current_time - self.last_result_time) > self.result_threshold):
                        self.last_result = text
                        self.last_result_time = current_time
                        self.process_text(text)
                        # print(f"Final Recognized ({self.language}): {text}")
                else:
                    partial = eval(self.recognizer.PartialResult()).get("partial", "")
                    if partial and (partial != self.last_result or (current_time - self.last_result_time) > self.result_threshold):
                        self.last_result = partial
                        self.last_result_time = current_time
                        self.process_text(partial)
                        # print(f"Partial Recognized ({self.language}): {partial}")

        except Exception as e:
            print(f"Error in SpeechRecognitionThread: {e}")

        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.pyaudio_instance.terminate()
            print("Speech Recognition Stopped.")

    def process_text(self, text):
        """Process the recognized text and add it to the queue if it matches predefined words."""
        words_to_check = self.english_words if self.language == "english" else self.hindi_words
        matched_words = set(text.split()).intersection(words_to_check)

        for word in matched_words:
            try:
                # Remove the oldest item if the queue is full
                if self.audio_queue.full():
                    self.audio_queue.get()
                self.audio_queue.put(word, block=False)  # Non-blocking put
            except queue.Full:
                pass  # Ignore if the queue is full

    def stop(self):
        self.stop_thread = True
