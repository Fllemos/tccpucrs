from typing import Any, List
from bot.util import parse_message_to_json
import json

# classes DTO utilizadas para parsear o texto das mensagens em json e converte-lo em objetos python
# para facilitar a manipulacao 
# a conversao tambem facilita a validacao das entradas

# diet item
class DietItem(object):
    def __init__(self, item: Any) -> None:
        self.item = item
        self.product = ''
        self.grams = 0
        self.calories = 0
        self.carbohydrates = 0
        self.fats = 0
        self.proteins = 0
        self.process()

    def process(self) -> None:
        self.product =  self.item.get('produto', '')
        self.grams =    self.item.get('gramas', 0)
        self.calories = self.item.get('calorias', 0)
        self.carbohydrates = self.item.get('carboidratos', 0)
        self.fats = self.item.get('gorduras', 0)
        self.proteins = self.item.get('proteinas', 0)

    def __repr__(self) -> str:
        return f'{{product={self.product} grams={self.grams} calories={self.calories} carbohydrates={self.carbohydrates} fats={self.fats} proteins={self.proteins} }}'

              


# diet register
class DietRegister(object):
    def __init__(self, register: Any) -> None:
        self.register = register
        self.id = ''
        self.description = ''
        self.created_at = ''
        self.updated_at = ''
        self.items : List[DietItem]= []
        self.process()

    def process(self) -> None:
        self.id = self.register.get('_id', '')
        self.description = self.register.get('descricao', '')
        self.created_at = self.register.get('data_criacao', None)
        items = self.register.get('itens', [])
        for i in items:
            di = DietItem(i)
            self.items.append(di)

    def __repr__(self) -> str:
        rep1 = f'| id={self.id}  description={self.description} created_at={self.created_at} items = [ \n'
        for i in self.items:
            rep1 += str(i) + '\n'
        rep1 += '] |'
        return rep1

# message parse

class Message(object):
    def __init__(self, message: str, user_message: str) -> None:
        # mensagem str que sera tratada
        self.message = message 
        self.message_text = ''
        self.user_message = user_message
        self.action = 'N'
        self.diet_registers : List[DietRegister] = []
        self.process()

    def process(self) -> Any:

        json_message = self.extract_json(self.message)
        self.message_parse(json_message=json_message)

    def extract_json(self, message: str) -> Any:
        try:
            json_obj = parse_message_to_json(message=message)
            return json_obj
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON")
    
        return {'acao': 'X', 'mensagem': message}
    
    def message_parse(self, json_message: Any) -> Any:
        json_message = json_message.get('dados', json_message)
        self.message_text = json_message.get('mensagem', "")
        self.action = json_message.get('acao', 'N')
        diet_regs_in = json_message.get('registro_dieta', [])
        print (diet_regs_in)
        if isinstance(diet_regs_in, dict):
            diet_regs_in = [diet_regs_in]
        self.diet_registers = []
        for d in diet_regs_in:
            diet_out = DietRegister(register=d)
            self.diet_registers.append(diet_out)

    def __repr__(self) -> str:
        rep1 = f'| message={self.message_text} action={self.action} diet_registers= [ \n'
        for d in self.diet_registers:
            rep1 += str(d)
        rep1 += '] | '
        return rep1


        
        