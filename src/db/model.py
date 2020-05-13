from pymongo import MongoClient

def load_settings_from_db(_id):
    con = MongoClient()
    try:
        return con['vkinder']['settings'].find_one({'id': _id})
    finally:
        con.close()

def save_settings_from_db(settings):
    con = MongoClient()
    try:
        return con['vkinder']['settings'].insert_one(settings)
    finally:
        con.close()