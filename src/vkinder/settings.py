from os.path import isfile
import json
from db import normalize
from itertools import product


class Settings:

    def __init__(self, user_id):
        self.user_id = user_id
        self.search = {}
        self.match = []

    @staticmethod
    def from_dict(settings: dict) -> tuple:
        return (
            settings.get('search'),
            settings.get('match'),
        )

    @staticmethod
    def to_dict(search, match) -> dict:
        return {
            'search': search,
            'match': match,
        }

    def load_from_file(self) -> bool:
        file_name = f'settings_{self.user_id}.json'
        if not isfile(file_name):
            return False
        with open(file_name, mode='r', encoding='utf-8') as file:
            self.search, self.match = self.from_dict(json.load(file))
            return True

    def save_to_file(self):
        file_name = f'settings_{self.user_id}.json'
        with open(file_name, mode='w', encoding='utf-8') as file:
            json.dump(
                self.to_dict(self.search, self.match),
                file, ensure_ascii=False, indent=4)

    def load_from_vk(self, vk_user: dict) -> bool:
        vk_user['sex'] = {1: 2, 2: 1}.get(vk_user['sex'], 0)

        search_fields = {
            'city', 'country', 'hometown',
            'sex', 'has_photo', 'religion'
        }
        search_fields_with_fix = {
            'universities': 'university',
            'schools': 'school',
            'career': 'company'
        }
        match = {
            'universities', 'schools', 'status', 'activities',
            'interests', 'music', 'movies', 'tv', 'books',
            'games', 'about', 'quotes', 'career', 'military', 'langs',
            'verified', 'sex', 'city', 'country', 'home_town', 'has_photo',
            'has_mobile', 'common_count', 'occupation', 'relation',
            'can_post', 'can_see_all_posts', 'can_see_audio',
            'can_write_private_message', 'can_send_friend_request',
            'is_hidden_from_feed', 'blacklisted', 'blacklisted_by_me',
            'political', 'religion', 'inspired_by', 'people_main',
            'life_main', 'smoking', 'alcohol'
        }

        search_params = {
            field: value for field, value in vk_user.items()
            if field in search_fields
            }

        for field, alias in search_fields_with_fix.items():
            if field in vk_user and len(vk_user[field]) == 1:
                search_params[alias] = vk_user[field][0]

        self.search = search_params.copy()

        self.match = [
            (field, value) for field, value in vk_user.items()
            if field in match and value
        ]

    def load_settings(self, vk):
        if self.load_from_file():
            return
        user = vk.get_user(self.user_id)
        normalize.normalize(user)
        self.load_from_vk(user)

    def make_flat_searc_params(self, searc_params=None):
        if searc_params is None:
            searc_params = self.search
        arrays = [
            product([key], value) for key, value in searc_params.items()
            if isinstance(value, (list, tuple))
            ]
        result = []
        for iteam in map(dict, product(*arrays)):
            new_iteam = searc_params.copy()
            new_iteam.update(iteam)
            result.append(new_iteam)
        return result

    def add_settings(self):
        new_settings = {
            'sort': [0, 1],
            'online': [0, 1]
        }
        self.search.update(new_settings)

    def get_base_searc(self):
        return {
            'sex': self.search.get('sex', [0, 1, 2]),
            'age_from': self.search.get('age_from', 18),
            'age_to': self.search.get('age_to', 25),
            'country': self.search.get('country', 1),
        }
