import telebot
from logging import Logger
from typing import Any
from bot.gpt import GptApi
from bot.db_service import DBService
from bot.audio import Audio
from repository.models import User
from bot.report import Report
from bot.util import parse_date_range, may_come_in, MessageActions 
from telebot import types

class TelegramBot:
    def __init__(self, api_key: str, openai_api_key: str, logger: Logger) -> None:
        self.bot = telebot.TeleBot(api_key)
        self.db_service = DBService()
        self.gpt = GptApi(api_key=openai_api_key, db_service=self.db_service)
        self.logger = logger

    def start_bot(self):
        def router(message: str) -> bool:
            return len(message.text) > 0
        

        def send_message_with_button(user_id: int, text: str):
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text='Visualizar dieta hoje', callback_data='dieta_hoje')
            markup.add(button)
            self.bot.send_message(user_id, text, reply_markup=markup)


        def handle_message_text(user_id: str, first_name: str, username: str, message_txt: str) -> MessageActions:
            obj_message = self.gpt.process(message=message_txt, user_id=user_id) # Message
            if self.db_service.process_messages(user_id=user_id, message=obj_message) == 'update':
                return MessageActions(updated=True, message=obj_message.message_text)
            return MessageActions(updated=False, message=obj_message.message_text)
        
        def handle_message_photo(user: User, message_txt: str, file_url: str) -> str:
            obj_message = self.gpt.vision_process(user_id=user.user_id, message=message_txt, file_url=file_url) # Message PHOTO
            if self.db_service.process_messages(user_id=user.user_id, message=obj_message) == 'update':
                return MessageActions(updated=True, message=obj_message.message_text)
            return MessageActions(updated=False, message=obj_message.message_text)
        
        def validate_user(message: Any) -> User: 
            user_id = message.from_user.id
            self.logger.debug (user_id)
            user = self.db_service.find_user(user_id=user_id)
            if not user:
                first_name = message.from_user.first_name
                username = message.from_user.username
                user = User(user_id=user_id, first_name=first_name, username=username, created_at=None, id=None)
            return user

        def validate_user_id(user_id: int) -> User: 
            self.logger.debug (user_id)
            user = self.db_service.find_user(user_id=user_id)
            if not user:
                first_name = f'user_id={user_id}'
                username = first_name
                user = User(user_id=user_id, first_name=first_name, username=username, created_at=None, id=None)
            return user


        @self.bot.message_handler(commands=['start'])
        def send_welcome(message: str):
            self.bot.reply_to(message, "Olá. Seja bem vindo ao Vita!")


        @self.bot.message_handler(commands=['dieta'])
        def handle_command_dieta(message):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

            text = message.text.strip()
            date_range = parse_date_range(text)
            if date_range:
                date_start, date_end = date_range

                report = Report(diet_history=self.db_service.get_diet_history_by_range(user.user_id, date_start=date_start, date_end=date_end))

                self.bot.reply_to(message, report.mark_down(), parse_mode='Markdown')
            else:
                self.bot.reply_to(message, "Formato inválido. Use DD/MM/AAAA para uma data, DD/MM/AAAA DD/MM/AAAA para um intervalo, ou uma das palavras 'hoje', 'ontem', 'semana', 'mês'.")

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            user_id = call.message.chat.id
            user : User = validate_user_id(user_id=user_id)
            if not user.id:
                self.bot.reply_to(call.message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

            if call.data == 'dieta_hoje':
                date_range = parse_date_range('dieta hoje')
                if date_range:
                    date_start, date_end = date_range
                    report = Report(diet_history=self.db_service.get_diet_history_by_range(user.user_id, date_start=date_start, date_end=date_end))
                    self.bot.send_message(user.user_id, report.mark_down(), parse_mode='Markdown')
                self.bot.answer_callback_query(call.id)  # notificar o telegram sobre o feedback da call

        @self.bot.message_handler(commands=['cadastrar'])
        def handle_command_cadastro(message):
            text = message.text.strip()
            if not may_come_in(message_text=text):
                self.bot.reply_to(message, f'**{text}**. Mensagem inválida. Informe a palavra correta para participar da conversa!', parse_mode='Markdown')
                return

            user : User = validate_user(message=message)
            if user.id:
                self.bot.reply_to(message, f'**{user.first_name}**, você já possui autorização para conversar comigo!', parse_mode='Markdown')
                return


            user = self.db_service.insert_user(user=user)

            self.bot.reply_to(message, f'**{user.first_name}**, muito bem! Agora você e eu podemos conversar sobre saúde e bem-estar. Fique à vontade para cadastrar sua dieta e tirar dúvidas.\nO Comando /ajuda pode ser útil para saber sobre minhas funcionalidades.', parse_mode='Markdown')



        @self.bot.message_handler(commands=['excel'])
        def handle_command_excel(message):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

            text = message.text.strip()
            date_range = parse_date_range(text)
            if date_range:
                date_start, date_end = date_range

                report = Report(diet_history=self.db_service.get_diet_history_by_range(user.user_id, date_start=date_start, date_end=date_end))
                excel_file = report.to_excel()
                self.bot.reply_to(message, 'Um momento. Construindo o arquivo...', parse_mode='Markdown')
                self.bot.send_document(message.chat.id, ('histórico_dieta.xlsx', excel_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))    
                
            else:
                self.bot.reply_to(message, "Formato inválido. Use DD/MM/AAAA para uma data, DD/MM/AAAA DD/MM/AAAA para um intervalo, ou uma das palavras 'hoje', 'ontem', 'semana', 'mês'.")


        @self.bot.message_handler(commands=['json'])
        def handle_command_json(message):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

            text = message.text.strip()
            date_range = parse_date_range(text)
            if date_range:
                date_start, date_end = date_range
                report = Report(diet_history=self.db_service.get_diet_history_by_range(user.user_id, date_start=date_start, date_end=date_end))
                self.bot.reply_to(message, report.to_json(), parse_mode='Markdown')
                
            else:
                self.bot.reply_to(message, "Formato inválido. Use DD/MM/AAAA para uma data, DD/MM/AAAA DD/MM/AAAA para um intervalo, ou uma das palavras 'hoje', 'ontem', 'semana', 'mês'.")


        @self.bot.message_handler(func=router)
        def default(message: Any):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 
            response : MessageActions = handle_message_text(user_id=user.user_id, first_name=user.first_name, username=user.username, message_txt=message.text)
            if response.updated:
                send_message_with_button(user_id=user.user_id, text=response.message)
                return
            
            self.bot.reply_to(message, response.message)

        
        @self.bot.message_handler(content_types=['voice'])
        def handle_audio(message: Any):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

            file_info = self.bot.get_file(message.voice.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)

            audio = Audio(name=str(message.voice.file_id))
            mp3_file = audio.get_mp3(audio_file=downloaded_file)
            message_text = self.gpt.transcript(audio_file=mp3_file)
                                                                                                    # -> texto enviado ao gpt
            response : MessageActions = handle_message_text(user_id=user.user_id, first_name=user.first_name, username=user.username, message_txt=message_text)
            if response.updated:
                send_message_with_button(user_id=user.user_id, text=response.message)
            else:
                self.bot.reply_to(message, response.message)

            # fazer resposta em audio -> por enquanto, tts google
            self.gpt.tts_google(audio_file_name=audio.response_filename_ogg, message=response.message)

            with open(audio.response_filename_ogg, 'rb') as audio_response:
                self.bot.send_voice(user.user_id, audio_response)

        @self.bot.message_handler(content_types=['sticker'])
        def handle_sticker(message):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 

        @self.bot.message_handler(content_types=['photo'])
        def photo(message):
            user : User = validate_user(message=message)
            if not user.id:
                self.bot.reply_to(message, 'Usuário inválido', parse_mode='MarkdownV2')
                return 
            
            self.logger.debug ('message.photo =', message.photo)
            cap = message.caption
            self.logger.debug ('Texto na foto' + cap)
            file_id = message.photo[-1].file_id
            self.logger.debug ('fileID =', file_id)
            file = self.bot.get_file(file_id)
            self.logger.debug('file.file_path =', file.file_path)
            #downloaded_file = BOT.download_file(file.file_path)
            file_url = self.bot.get_file_url(file_id)
            self.logger.debug (file_url)
            response : MessageActions = handle_message_photo(user=user, message_txt=cap, file_url=file_url)
            if response.updated:
                send_message_with_button(user_id=user.user_id, text=response.message)
                return 
            
            self.bot.reply_to(message, response.message)


    def run(self):
        self.bot.polling()
