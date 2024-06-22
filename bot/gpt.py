import openai
import json 
from typing import Any, List
from datetime import datetime
from bot.message_dto import Message
from bot.db_service import DBService
from bot.tts import Tts


MODEL_ENGINE = 'gpt-4-turbo'   #  --> ('gpt-4o') 4o new update 
MODEL_WHISPER = 'whisper-1'
WHISPER_LANGUAGE = 'pt'
MODEL_TTS_ENGINE = "tts-1-hd" # "tts-1" testando se o pt-br fica melhor
VOICE = "nova"

class GptApi(object):
    def __init__(self, api_key: str, db_service: DBService) -> None:
        self.client = openai.OpenAI(api_key=api_key)
        self.messages = []
        self.instructions = json.load(open('bot/setup.json', "r", encoding='utf-8'))
        self.db_service = db_service
        self.tts = Tts()

        for i in self.instructions["instrucoes"]:
            print (i)

    def send(self, messages: List) -> str:
        print (messages)
        res = self.client.chat.completions.create(
                            model=MODEL_ENGINE,
                            messages=messages)
        print (res)
        return res.choices[0].message.content


    def process(self, message: str, user_id: str) -> Message:

        self.messages =  [self.update_initial_prompt(user_id=user_id)]

        for m in self.db_service.get_last_four_messages(user_id=user_id):
            self.messages.append(m)

        self.messages.append({"role": "user", "content": message})


        # separar a mensagem do json neste momento

        content = self.send(messages=self.messages)

        obj_message = Message(content, user_message=message)


        if obj_message.action == 'X':
            # por enquanto, faz uma tentativa de ajuste no JSON
            self.messages.append({"role": "assistant", "content": obj_message.message_text})
            self.messages.append({"role": "user", "content": 'Você não seguiu a instrução correta. Seu JSON não pode ser parseado. Verifique a sua resposta e as instruções!'})
            content = self.send(messages=self.messages)
            obj_message = Message(content, user_message=message)
            if obj_message.action == 'X':
                obj_message.action = 'N'
                obj_message.message_text = 'Ocorreu um erro. Por favor, tente reformular sua mensagem.'


        self.messages = []

        return obj_message


    def transcript(self, audio_file: Any) -> str:
        transc = self.client.audio.transcriptions.create(model=MODEL_WHISPER, file=audio_file, language=WHISPER_LANGUAGE).text
        print(f'OpenAI transcription: {str(transc)} \n')
        return transc
    
    def tts(self, audio_file_name: str, message: str) -> None:
        response_tts = self.client.audio.speech.create(
            model=MODEL_TTS_ENGINE,
            voice=VOICE,
            input=message,
        )
        
        response_tts.stream_to_file(audio_file_name)
        response_tts.close()

    def tts_google(self, audio_file_name: str, message: str) -> None:
        self.tts.generate(text = message, response_filename = audio_file_name)

    def vision_process(self, user_id: str, message: str, file_url: str) -> Message:

        self.messages =  [self.update_initial_prompt(user_id=user_id)]
        for m in self.db_service.get_last_four_messages(user_id=user_id):
            self.messages.append(m)

        msg = {
            "role": "user",
            "content": [
                {"type": "text", "text": message},
                {
                "type": "image_url",
                "image_url": {
                    "url": file_url,
                },
                },
            ],
        }
        
        self.messages.append(msg)

        print (self.messages)

        res = self.client.chat.completions.create(
                            model=MODEL_ENGINE,
                            messages=self.messages )
        
        print (res)
        content =  res.choices[0].message.content

        # separar a mensagem do json neste momento

        obj_message = Message(content, user_message=f'{message} | [imagem] ')

        self.messages = []

        return obj_message



    def update_initial_prompt(self, user_id: str) -> Any:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.instructions['data_dia'] = now
        history = self.db_service.get_diet_history(user_id=user_id)
        print (f'historico de dieta ==> {history}')            
        self.instructions['historico_dieta'] = history
        updated_prompt = f'[SEMPRE] Siga cuidadosamente as [instruções] contidas no json a seguir: {json.dumps(self.instructions)}'
        return {"role": "system", "content": updated_prompt}
    










