from typing import List, Any
from pymongo import MongoClient
from bson import ObjectId
from repository.models import User, Message, DietRegister
from datetime import datetime, timedelta

class Repository:
    def __init__(self, con_string: str) -> None:
        self.client = MongoClient(con_string)
        self.db = self.client['vita']
        self.users_collection = self.db['users']
        self.messages_collection = self.db['messages']
        self.diet_registers_collection = self.db['diet_registers']

    def add_user(self, user: User):
        result = self.users_collection.insert_one(user.to_dict())
        if result.inserted_id:
            return self.users_collection.find_one({'_id': result.inserted_id})
        return None

    def add_message(self, message: Message):
        return self.messages_collection.insert_one(message.to_dict())
    
    def list_messages(self, user_id: str) -> List[Any]:
        return self.messages_collection.find({"userId": user_id}).sort("createdAt", -1).limit(12)
    
    def get_last_four_messages(self, user_id: str) -> Any:
        return self.messages_collection.find({"userId": user_id}).sort("createdAt", -1).limit(4)
        

    def save_diet_register(self, diet_register: DietRegister):
        if diet_register.id:
            return self.diet_registers_collection.update_one(
                    {"_id": ObjectId(diet_register.id)}, 
                    {"$set": diet_register.to_dict()},
                    upsert=True
                )
        else:
            return self.diet_registers_collection.insert_one(diet_register.to_dict())        

    def list_diet_registers(self, user_id: str) -> List[Any]:
        return self.diet_registers_collection.find({"userId": user_id})

    def list_recent_diet_registers(self, user_id: str) -> Any:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today 
        return self.diet_registers_collection.find({
            "userId": user_id,
            "createdAt": {
                "$gte": yesterday,  
                "$lt": today + timedelta(days=1)  
            }
        })
    
    def list_diet_registers_by_range(self, user_id: str, date_start: datetime, date_end: datetime) -> Any:
        return self.diet_registers_collection.find({
            "userId": user_id,
            "createdAt": {
                "$gte": date_start,
                "$lt": date_end + timedelta(days=1)
            },
            "description": {
                "$ne": ""  
            },
            "items": {
                "$exists": True, 
                "$not": {"$size": 0}  
            }
        })   
    
    def find_user(self, user_id):
        return self.users_collection.find_one({"userId": user_id})
    
    def update_user(self, user: User):
        return self.users_collection.update_one(
            {"userId": user.user_id}, 
            {"$set": user.to_dict()}, 
            upsert=True
        )
