import os
from typing import Any
from pydub import AudioSegment
import shutil

AUDIO_BASE_PATH = 'audio/'
AUDIO_RESPONSE_PATH = 'audio/response/'

class Audio(object):
    def __init__(self, name: str) -> None:
        self.filename_ogg = f'{AUDIO_BASE_PATH}{name}.ogg' 
        self.filename_mp3 = f'{AUDIO_BASE_PATH}{name}.mp3' 
        self.response_filename_ogg = f'{AUDIO_RESPONSE_PATH}r-{name}.ogg' 
        self.create_directories()

    def get_mp3(self, audio_file: Any) -> Any:
        return self.convert(audio_file=audio_file)
        
    def convert(self, audio_file: Any) -> Any:
        # salva primeiro o obb para exportar
        with open(self.filename_ogg, 'wb') as f:
            f.write(audio_file)

        AudioSegment.from_file(self.filename_ogg).export(self.filename_mp3, format="mp3")

        mp3_file = open(self.filename_mp3, 'rb')

        return mp3_file
    
    def create_directories(self) -> None:
        os.makedirs(AUDIO_BASE_PATH, exist_ok=True)
        os.makedirs(AUDIO_RESPONSE_PATH, exist_ok=True)    

    
    def clear_audio_directory(self) -> None:
        shutil.rmtree(AUDIO_BASE_PATH)  
        self.create_directories() 


