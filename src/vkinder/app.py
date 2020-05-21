from db import model, normalize
from api import api
from datetime import datetime
import json
from itertools import product
import webbrowser
from os import path


class APP:

    def __init__(self, token, _id):
        self.vk = api.VK(token)
        self.user_id = str(self.vk.resolve_screen_name(_id))
        self.db = model.DB(self.user_id)

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
            print(
                f'{name} [{"*"*p_bar + " "*(bar_len - p_bar)}] {i} of {data_len} {datetime.now() - start}\r',
                end=''
                )
            if one:
                func(value)
            else:
                result.extend(func(**value))
        print(f'{name} [{"*"*bar_len}] {data_len} of {data_len} {datetime.now() -start} done')
        return result

    def settings_to_dict(self):
        return {
            'search': tuple(self.search_params.items())
            if isinstance(self.search_params, dict) else self.search_params,
            'match': tuple(self.match_params.items())
            if isinstance(self.match_params, dict) else self.match_params,
            'intersection': tuple(self.intersection_params.items())
            if isinstance(self.intersection_params, dict)
            else self.intersection_params
                }

    def save_settings_to_file(self):
        with open(f'profile_{self.user_id}.json', mode='w', encoding='utf-8') as file:
            json.dump(
                self.settings_to_dict(),
                file, indent=4,
                ensure_ascii=False
                )

    def save_settings_to_db(self):
        self.db.save_settings_to_db(self.settings_to_dict())

    def load_settings(self):
        self.load_settings_from_file() or\
            self.load_settings_from_db() or\
            self.load_settings_from_vk()

    def load_settings_from_file(self):
        file_name = f'profile_{self.user_id}.json'
        if not path.isfile(file_name):
            file_name = 'profile.json'
        if not path.isfile(file_name):
            return False
        with open(file_name, mode='r', encoding='utf-8') as file:
            profile = json.load(file)
            self.search_params = dict(profile.get('search', {}))
            self.match_params = profile.get('match', [])
            self.intersection_params = profile.get('intersection', [])
            return True
        return False

    def load_settings_from_db(self):
        profile = self.db.load_settings_from_db()
        if profile:
            self.search_params = dict(profile.get('search', {}))
            self.match_params = profile.get('match', [])
            self.intersection_params = profile.get('intersection', [])
            print(self.intersection_params)
            return True
        return False

    def load_settings_from_vk(self):
        settings = self.vk.get_user(self.user_id)
        normalize.normalize(settings)
        settings['sex'] = {1: 2, 2: 1}.get(settings['sex'], 0)

        search_fields = [
            'city', 'country', 'hometown',
            'sex', 'has_photo', 'religion'
            ]
        search_fields_with_fix = {
            'universities': 'university',
            'schools': 'school',
            'career': 'company'
            }
        intersection_fields = [
            'universities', 'schools', 'status', 'activities',
            'interests', 'music', 'movies', 'tv', 'books',
            'games', 'about', 'quotes', 'career', 'military', 'langs'
            ]
        match_fields = [
            'verified', 'sex', 'city', 'country', 'home_town', 'has_photo',
            'has_mobile', 'common_count', 'occupation', 'relation',
            'can_post', 'can_see_all_posts', 'can_see_audio',
            'can_write_private_message', 'can_send_friend_request',
            'is_hidden_from_feed', 'blacklisted', 'blacklisted_by_me',
            'political', 'religion', 'inspired_by', 'people_main',
            'life_main', 'smoking', 'alcohol'
            ]

        search_params = {
            field: value for field, value in settings.items()
            if field in search_fields
            }

        for field, alias in search_fields_with_fix.items():
            if field in settings and len(settings[field]) == 1:
                search_params[alias] = settings[field][0]

        match_params = {
            field: value for field, value in settings.items()
            if field in match_fields and field not in search_params
            }

        intersection_params = {
            field: value for field, value in settings.items()
            if field in intersection_fields and value
            and field not in search_params
            }

        self.search_params = search_params
        self.match_params = list(match_params.items())
        self.intersection_params = list(intersection_params.items())
        return True

    def get_top_three_profile_photos(self, _id):
        try:
            photos = self.vk.get_top_three_profile_photos(_id)
        except:
            return 'Профиль закрыт'

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

    def out_html(self, users):
        file_name = f'out_{self.user_id}.html'
        with open(file_name, mode='w', encoding='utf-8') as file:
            for user in users:
                href = f"https://vk.com/{user['domain']}"
                file.write(f'<a href="{href}"><h1>{user["domain"]}</h1></a>\n')
                photos = self.get_top_three_profile_photos(user['id'])
                if not isinstance(photos, list):
                    continue
                for photo in photos:
                    # print(photo)
                    file.write('<img src="' + photo + '" width="800">')

    def check_settings(self):
        obligatory_search_params = [
            'age_from', 'age_to', 'sex', 'country', 'city'
        ]
        for param in obligatory_search_params:
            if param not in self.search_params:
                self.search_params[param] =\
                    input(f'Нехватает {param}. Введите значение: ')
        if 'group_id' not in self.search_params:
            load = input('Введите id групп через запятую или "load" для загрузки.')
            if load == 'load':
                self.search_params['group_id'] =\
                    self.vk.get_groups(self.user_id)
            else:
                self.search_params['group_id'] = load.split(', ')

    def make_flat_searc_params(self):
        arrays = [
            product([key], value) for key, value in self.search_params.items()
            if isinstance(value, (list, tuple))
            ]
        result = []
        for iteam in map(dict, product(*arrays)):
            new_iteam = self.search_params.copy()
            new_iteam.update(iteam)
            result.append(new_iteam)
        return result
