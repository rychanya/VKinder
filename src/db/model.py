from pymongo import MongoClient
from db.normalize import normalize


class DB:

    DB_NAME = 'vkinder'

    def __init__(self, user_id):
        self.user_id = user_id
        self.connection = MongoClient()

    def load_settings_from_db(self):
        return self.connection[DB.DB_NAME]['settings']\
            .find_one({'id': self.user_id})

    def save_settings_to_db(self, settings):
        settings['id'] = self.user_id
        self.connection[DB.DB_NAME]['settings']\
            .replace_one({'id': self.user_id}, settings, upsert=True)

    def is_db_empty(self):
        return self.connection[DB.DB_NAME][self.user_id]\
            .count_documents({'skip': {'$exists': False}}) == 0

    def get(self, criterions):
        return self.connection[DB.DB_NAME][self.user_id]\
            .aggregate(criterions)

    def set_skip(self, user_id):
        self.connection[DB.DB_NAME][self.user_id]\
            .update_one({'id': user_id}, {'$set': {'skip': True}})

    def save(self, data):
        normalize(data)
        self.connection[DB.DB_NAME][self.user_id]\
            .replace_one({'id': data['id']}, data, upsert=True)
