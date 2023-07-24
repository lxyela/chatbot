import threading
import signal
from microphone_recoder import MicrophoneRecorder
from speech_recognize import SpeechRecognizer

global stop_thread
stop_thread = threading.Event()

def signal_handler(signum, frame):
    stop_thread.set()

record = MicrophoneRecorder(save_audio=True, stream_data=False, event=stop_thread)
transcribe = SpeechRecognizer(audio_folder="/Users/lohithyelamanchi/chatbot/audio_logs/", event=stop_thread)
signal.signal(signal.SIGINT, signal_handler)
record_thread = threading.Thread(target=record.record_microphone,)
transcribe_thread = threading.Thread(target=transcribe.whisper_speech_recognition,)
record_thread.start()
transcribe_thread.start()
record_thread.join()
transcribe_thread.join()