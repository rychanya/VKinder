from db import model
from api import api
from datetime import datetime
import json
import webbrowser
from vkinder.settings import Settings


class APP:

    def __init__(self, token, _id):
        self.vk = api.VK(token)
        self.user_id = str(self.vk.resolve_screen_name(_id))
        self.db = model.DB(self.user_id)
        self.settings = Settings(self.user_id)

    @staticmethod
    def user_input():
        url = 'https://oauth.vk.com/authorize?client_id=7331062&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,groups&response_type=token&v=5.103'
        webbrowser.open_new_tab(url)
        token = input('Введите токен: ')
        _id = input('Введите ваш id: ')
        return APP(token, _id)

    @staticmethod
    def progress_bar(data, func, name, one=False, bar_len=50):
        start = datetime.now()
        data_len = len(data)
        result = []
        for i, value in enumerate(data):
            p_bar = round(i / data_len * bar_len)
            bar = f'[{"*"*p_bar + " "*(bar_len - p_bar)}]'
            print(
                f'{name:^15} {bar} {i} of {data_len} {datetime.now() - start}\r',
                end=''
                )
            if one:
                func(value)
            else:
                result.extend(func(**value))
        print(f'{name} [{"*"*bar_len}] {data_len} of {data_len} {datetime.now() -start} done')
        return result

    def get_top_three_profile_photos(self, _id):
        photos = self.vk.get_top_three_profile_photos(_id)
        if not photos:
            return 'Профиль закрыт или без фото'

        def parse(photo):
            return {
                'w': 6,
                'z': 5,
                'y': 4,
                'x': 3,
                'm': 2,
                's': 1,
            }.get(photo['type'], 0)

        return [max(photo['sizes'], key=parse)['url'] for photo in photos]

    def out(self, users):
        file_name = f'out_{self.user_id}.json'
        with open(file_name, mode='w', encoding='utf-8') as file:
            json.dump(
                [
                    {f'https://vk.com/{user["domain"]}':
                        self.get_top_three_profile_photos(user['id'])}
                    for user in users
                ],
                file, ensure_ascii=False, indent=4)
            print(f'результат записан в {file_name}')

    def check_settings(self):
        obligatory_search_params = [
            'age_from', 'age_to', 'sex', 'country', 'city'
        ]
        for param in obligatory_search_params:
            if param not in self.settings.search:
                self.settings.search[param] =\
                    input(f'Нехватает {param}. Введите значение: ')
        if 'group_id' not in self.settings.search:
            load = input('Введите id групп через запятую или "load" для загрузки.')
            if load == 'load':
                self.settings.search['group_id'] =\
                    self.vk.get_groups(self.user_id)
            else:
                self.settings.search['group_id'] = load.split(', ')
