import re
from db import model

def get_id_or_domain_from_user():
    print('Привет, давай попробуем найти тебе пару!')
    return input('Введи совой id или короткое имя: ')

def get_settings_from_user_profile(_id):
    return {'id': _id}

def get_settings(_id):
    setttings = model.load_settings_from_db(_id)
    if setttings:
        print('Загружаем настройки из БД')
        return setttings
    else:
        print('Инфориации о вас нет в БД')
        setttings = get_settings_from_user_profile(_id)
        db_id = model.save_settings_from_db(setttings)
        setttings.update({'_id': db_id})
        return setttings
        


