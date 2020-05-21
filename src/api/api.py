import vk_api
import time

all_fields = 'verified, sex, bdate, city, country, home_town, has_photo, domain, has_mobile, contacts, education, universities, schools, status, last_seen, common_count, occupation, nickname, relation, personal, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_hidden_from_feed, career, military, blacklisted, blacklisted_by_me'
search_params = [
    'q', 'sort', 'city', 'country', 'hometown', 'university_country', 'university',\
    'university_year', 'university_faculty', 'university_chair', 'sex', 'status',\
    'age_from', 'age_to', 'birth_day', 'birth_month', 'birth_year', 'online','has_photo',\
    'school_country', 'school_city', 'school_class', 'school', 'school_year', 'religion',\
    'company', 'position', 'group_id', 'from_list'
    ]


def too_many_rps_handler(error):
        time.sleep(0.5)
        return error.try_method()

class VK:

    def __init__(self, token):
        self.sesion = vk_api.VkApi(token=token)
        self.sesion.too_many_rps_handler = too_many_rps_handler
        self.tools = vk_api.tools.VkTools(self.sesion)

    def resolve_screen_name(self, screen_name):
        try:
            return int(screen_name)
        except ValueError:
            _id = self.sesion.method('utils.resolveScreenName', values={'screen_name': screen_name})
            if _id and _id['type'] == 'user':
                return _id['object_id']
  
    def get_user(self, _id):
        return self.sesion.method('users.get', {'user_ids': _id, 'fields': all_fields})[0]

    def get_groups(self, _id):
        return self.tools.get_all(
            'groups.get', max_count=1000, 
            values={'user_id': _id}
            )['items']

    def search(self, **params):
        params = {key: value for key, value in params.items() if key in search_params}
        params.update({'fields': all_fields, 'count': 1000})
        return self.sesion.method('users.search', values=params)['items']

    
    def get_top_three_profile_photos(self, _id):
        params = {
            'owner_id': _id,
            'album_id': 'profile',
            'extended': 1
        }
        photos = self.sesion.method('photos.get', values=params)['items']
        return sorted(
            photos,
            key=lambda value: value['likes']['count'],
            reverse=True)[:3]
