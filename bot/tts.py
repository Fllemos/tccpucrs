import google
from google.cloud import texttospeech_v1

class Tts(object):
    def __init__(self) -> None:
        self.ttsclient = texttospeech_v1.TextToSpeechClient()
        self.langague_code = 'pt-BR'
        self.language_name = 'pt-BR-Neural2-C'
        self.pitch = -2
        self.voice1 = texttospeech_v1.types.VoiceSelectionParams (
            language_code=self.langague_code,
            name=self.language_name 
            )
        self.audio_config = texttospeech_v1.AudioConfig(
            audio_encoding = texttospeech_v1.AudioEncoding.OGG_OPUS, 
            pitch=self.pitch
            )


    def generate(self, text: str, response_filename: str) -> None:
         text = f'<speak>{text}</speak>'
         synth_input = texttospeech_v1.SynthesisInput(ssml=text)
         response1 = self.ttsclient.synthesize_speech(
             input= synth_input,
             voice = self.voice1,
             audio_config = self.audio_config 
             )
         
         with open(response_filename, 'wb') as output:
             output.write(response1.audio_content)  
         
         
             
         
