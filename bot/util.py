import os
import json
from typing import Any
from datetime import datetime, timedelta
import dateutil.parser


class MessageActions(object):
    def __init__(self, updated: bool = False, message: str = '') -> None:
        self.updated = updated
        self.message = message

def parse_date_range(message_text: str) -> Any:
    parts = message_text.split()

    print (f'partes =  {parts}')
    try:
        if len(parts) == 2 and parts[1].lower() in ["hoje", "ontem", "semana", "mes", "mês"]:
            now = datetime.now()
            if parts[1].lower() == "hoje":
                date_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                date_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif parts[1].lower() == "ontem":
                yesterday = now - timedelta(days=1)
                date_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
                date_end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif parts[1].lower() == "semana":
                date_start = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
                date_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            elif parts[1].lower() in ["mes", "mês"]:
                date_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                date_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            return date_start, date_end

        if len(parts) == 2:
            date_start = dateutil.parser.parse(parts[1], dayfirst=True).replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = date_start.replace(hour=23, minute=59, second=59, microsecond=999999)
            return date_start, date_end
        
        if len(parts) == 3:
            date_start = dateutil.parser.parse(parts[1], dayfirst=True).replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = dateutil.parser.parse(parts[2], dayfirst=True).replace(hour=23, minute=59, second=59, microsecond=999999)
            return date_start, date_end
    except ValueError:
        return None
    
    return None

def parse_message_to_json(message: str) -> Any:
    parts = message.split("```json")
    msg = ''
    if len(parts[0].strip()) > 0:
        msg += f'{parts[0].strip()}.\n' 
    middle = parts[1].split("```")
    if len(middle[1].strip()) > 0:
        msg += f'| {middle[1].strip()}'
    print (f'msg={msg}')
    print (f'middle={middle[0].strip()}')
    json_str = middle[0].strip()
    json_lines = []
    print ('json retornado --> ')
    for json_line in json_str.split('\n'):
        print (json_line)
        json_lines.append(json_line.split('//')[0] + '\n')

    json_str = ''.join(json_lines)
    print ('------------ JSON STR TRATADO')
    print (json_str)
    json_obj = json.loads(json_str)
    if len(msg) > 0:
        json_obj['mensagem'] += msg 
    return json_obj

def may_come_in(message_text: str) -> bool:
    bot_secret = os.getenv("BOT_SECRET")
    parts = message_text.split()
    print (f'partes =  {parts}')
    if len(parts) == 2 and parts[1] == bot_secret:
       return True
    return False

