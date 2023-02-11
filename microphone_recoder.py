from queue import Queue
import pyaudio
import wave
from utils import get_time_stamp, create_log_dir
import sys

# class to store the audio frames and control the recording process
class MicrophoneRecorder:
    def __init__(self, channels='default', frame_rate='default', record_seconds=10, chunk_size=512, stream_data=False, stream_queue=None, save_audio=True, audio_folder=None, event=None):
        self.messages = event
        self.stream_data = stream_data
        self.stream_queue = stream_queue

        # stream queue validations
        if self.stream_data == True and self.stream_queue != None:
            if isinstance(stream_queue, Queue):
                self.stream_queue = stream_queue
            else:
                print("The object is not of type queue.")
                sys.exit()

        self.save_audio = save_audio
        if self.save_audio:
            if audio_folder == None:
                print("No audio folder provided to save the audio.\nNow creating a audio folder")
                self.audio_folder = create_log_dir()
            else:
                self.audio_folder = create_log_dir(audio_folder)

        self.p = pyaudio.PyAudio()
        self.microphone_info = self.p.get_default_input_device_info()
        if channels == 'default':
            self.channels = int(self.microphone_info['maxInputChannels'])
        if frame_rate == 'default':
            self.frame_rate = int(self.microphone_info['defaultSampleRate'])
        self.record_seconds = record_seconds
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.sample_size = 2

    def write_wave_file(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.frame_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def record_microphone(self):
        self.frames = []
        self.counter = 0
        while not self.messages.is_set():
            self.stream = self.p.open(format=self.format,
                                channels=self.channels,
                                rate=self.frame_rate,
                                input=True,
                                frames_per_buffer=self.chunk_size
                                )

            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

            if len(self.frames) >= (self.frame_rate * self.record_seconds) / self.chunk_size:
                if self.stream_data:
                    self.stream_queue.put(self.frames.copy())
                
                if self.save_audio:
                    filename = f"{self.audio_folder}/unproc_rec_{self.counter}_{get_time_stamp()}.wav"
                    self.write_wave_file(filename)

                self.frames = []
                self.counter += 1

        if len(self.frames):
            filename = f"{self.audio_folder}/unproc_rec_{self.counter}_{get_time_stamp()}.wav"
            self.write_wave_file(filename)

        print("teminating before the program")
        self.stop()
        print("teminating the program")