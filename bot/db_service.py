import os
from typing import Any, List
from datetime import datetime
from repository.mongo import Repository
from repository.models import User
from repository.models import Message, DietRegister, DietItem 
from bot.message_dto import Message as MessageDto
from collections import deque

class DBService(object):
    def __init__(self) -> None:
        self.repository = Repository(os.getenv("MONGODB_CONNECTION"))

    def ensure_user(self, user_id: str, first_name: str, username: str) -> Any:
        user = self.repository.find_user(user_id)
        if not user:
            user = User(user_id=user_id, first_name=first_name, username=username)
            self.repository.add_user(user)
        else:
            print (f'usuario existente na base = {user}')
        return user

    def insert_user(self, user: User) -> User:
        if (not user) or user.id:
            return user
        u = self.repository.add_user(user)
        if u:
            return User(user_id=u['userId'], first_name=u['firstName'], username=u['username'], created_at=u['createdAt'],  id=u['_id'])
        return None

    def find_user(self, user_id: str) -> User:
        print (f'procurando usuario na base -> {user_id}')
        user = self.repository.find_user(user_id)
        print (f'Usuario = {user}')
        if user:
            return User(user_id=user['userId'], first_name=user['firstName'], username=['username'], created_at=user['createdAt'],  id=user['_id'])
        return None


    def process_messages(self, user_id: str, message: MessageDto) -> str:

        # definir a principal acao que ocorreu no metodo
        action = 'no_op'

        # mensagem em texto
        # processamento da mensagem em texto. gravacao dela no banco de dados
        # primeiro a user_message

        user_message = Message(user_id=user_id, role="user", content=message.user_message)
        self.repository.add_message(user_message)


        # agora vem o processamento dos itens de dieta que precisam ser inseridos ou atualizados na base


        print ('inserindo registers')

        print (f'tenho registers aqui => registers={message.diet_registers}')

        for dr in message.diet_registers:
            action = 'update'
            items = []
            for di in dr.items:
                items.append(DietItem(product=di.product, grams=di.grams, calories=di.calories, carbohydrates=di.carbohydrates, fats=di.fats, proteins=di.proteins))
            
            mdr = DietRegister(user_id=user_id, description=dr.description, items=items, id=dr.id if len(dr.id) > 5 else None, created_at=dr.created_at if len(dr.id) > 5 else None)

            print (f'register montado. vai inserir => register={mdr}')

            # incluir ou alterar registro
            print (self.repository.save_diet_register(diet_register=mdr))

        # verificando inclusao dos registros de dieta

        for dr in self.repository.list_diet_registers(user_id=user_id):
            print (dr)


        #somente ao final de tudo inclui a mensagem do assistente. 
        #para nao ficar no mesmo timestamp do user
        assistant_message = Message(user_id=user_id, role="assistant", content=message.message_text)
        self.repository.add_message(assistant_message)

        # testando apenas se as mensagens estao sendo atualizadas no sistema
        for m in self.repository.list_messages(user_id=user_id):
            print (m)

        return action



    # refatorar aqui para ajustar o ID
    def get_diet_history(self, user_id: str) -> List[Any]:
        history = []
        for h in self.repository.list_recent_diet_registers(user_id=user_id):
            h['_id'] = str(h['_id']) 
            if 'createdAt' in h and h['createdAt']:
                h['createdAt'] = h['createdAt'].isoformat()
            if 'updatedAt' in h and h['updatedAt']:
                h['updatedAt'] = h['updatedAt'].isoformat()            
            history.append(h)
        return history

    def get_diet_history_by_range(self, user_id: int, date_start: datetime, date_end: datetime) -> List[DietRegister]:
        history = []
        for h in self.repository.list_diet_registers_by_range(user_id=user_id, date_start=date_start, date_end=date_end):
            print (h)
            diet_items = []
            for i in h['items']:
                diet_items.append(DietItem(product=i['product'], grams=i['grams'], calories=i['calories'], carbohydrates=i['carbohydrates'], fats=i['fats'], proteins=i['proteins']))

            dr = DietRegister(user_id=h['userId'], description=h['description'], items=diet_items, id=str(h['_id']), created_at=h['createdAt'])
            history.append(dr)

        print (f'recuperado histórico de dietas => {history}')
        return history

    def get_last_four_messages(self, user_id: str) -> List[Message]:
        last_messages = deque(maxlen=4) 
        for message in self.repository.get_last_four_messages(user_id=user_id):
            m = Message(user_id=message['userId'], role=message['role'], content=message['content'])
            last_messages.appendleft(m.to_short_dict()) 

        return list(last_messages) 
    


