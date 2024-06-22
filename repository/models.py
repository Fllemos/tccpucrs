from datetime import datetime

class User:
    def __init__(self, user_id, first_name, username, created_at=None, id=None):
        self.id = id
        self.user_id = user_id
        self.first_name = first_name
        self.username = username
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = datetime.now() if self.id else None

    def to_dict(self):
        return {
            "userId": self.user_id,
            "firstName": self.first_name,
            "username": self.username,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }


    def __repr__(self) -> str:
        return f'id: {self.id} userId: {self.user_id}, first_name: {self.first_name}, username: {self.username}, createdAt: {self.created_at}, updatedAt: {self.updated_at}'

class Message:
    def __init__(self, user_id, role, content, created_at=None):
        self.user_id = user_id
        self.role = role
        self.content = content
        self.created_at = created_at if created_at else datetime.now()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "role": self.role,
            "content": self.content,
            "createdAt": self.created_at
        }
    def to_short_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }

class DietRegister:
    def __init__(self, user_id, description, items=[], id=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.description = description
        self.items = items
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = datetime.now() if self.id else None

    def to_dict(self):
        return {
            "userId": self.user_id,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }

    def to_dict_plain(self):
        return {
            "_id": self.id,
            "userId": self.user_id,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
            "createdAt": self.created_at.strftime('%d/%m/%Y %H:%M')
        }


class DietItem:
    def __init__(self, product, grams, calories, carbohydrates, fats, proteins):
        self.product = product
        self.grams = grams
        self.calories = calories
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.proteins = proteins

    def to_dict(self):
        return {
            "product": self.product,
            "grams": self.grams,
            "calories": self.calories,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
            "proteins": self.proteins
        }

