import os
import time
import whisper

# class to store the audio frames and control the recording process
class SpeechRecognizer:
    def __init__(self, audio_folder=None, event=None):
        self.event_exit = event
        self.audio_folder = audio_folder

    def whisper_speech_recognition(self):
        self.model = whisper.load_model("base.en")
        while True:
            audio_files = [f for f in os.listdir(self.audio_folder) if f.endswith(".wav")]
            audio_files.sort(key=lambda x: os.path.getctime(f"{self.audio_folder}/{x}"))  
            if audio_files: 
                for audio_file in audio_files[:]:
                    print(audio_file)
                    result = self.model.transcribe(os.path.join(self.audio_folder, audio_file), fp16=False)
                    print(result['text'])
                    audio_files.remove(audio_file)
                    os.remove(os.path.join(self.audio_folder, audio_file))
            else:
                time.sleep(1)

            if self.event_exit.is_set():
                if audio_files: 
                    for audio_file in audio_files[:]:
                        result = self.model.transcribe(os.path.join(self.audio_folder, audio_file), fp16=False)
                        print(result['text'])
                        audio_files.remove(audio_file)
                        os.remove(os.path.join(self.audio_folder, audio_file))
                print("exiting speech recognition")
                break