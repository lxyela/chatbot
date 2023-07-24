import os
import datetime
import shutil

# creating a audio logs folder where all the audio files are written to
def create_log_dir(dir=None):
    if dir is None:
        current_working_dir = os.getcwd()
        audio_folder = os.path.join(current_working_dir, "audio_logs")
    else:
        if os.path.isdir(dir):
            audio_folder = os.path.join(dir, "audio_logs")

    shutil.rmtree(audio_folder)
    os.makedirs(audio_folder)
    print(f"{audio_folder} has been created.")
    
    return audio_folder

def get_time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")