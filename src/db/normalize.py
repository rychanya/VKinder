from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

lemmatize_fields = [
    'status', 'activities', 'interests',
    'music', 'movies', 'tv', 'books',
    'games', 'about', 'quotes'
]

obj_fields = {
    'career': 'company',
    'city': 'id',
    'country': 'id',
    'education': 'university',
    'last_seen': 'time',
    'military': 'unit_id',
    'occupation': 'name'
}

array_fields = ['schools', 'universities']


def lemmatize(text):
    lm = Mystem()
    rus_stopwords = stopwords.words('russian')
    tokens = lm.lemmatize(text.lower())
    tokens = [
        token for token in tokens if token not in rus_stopwords
        and token != ' ' and token.strip() not in punctuation
            ]
    return list(set(tokens))


def normalize_lemmatize_fields(data):
    for key in lemmatize_fields:
        data[key] = lemmatize(data.get(key, ''))


def normalize_obj_fields(data):
    def get_target(value, targets):
        if not isinstance(targets, list):
            return value.get(targets)
        for target in targets:
            try:
                return value[target]
            except KeyError:
                continue

    for key, target in obj_fields.items():
        if key in data:
            if isinstance(data[key], dict):
                data[key] = get_target(data[key], target)
            elif isinstance(data[key], list):
                data[key] = [get_target(value, target) for value in data[key]]


def normalize_array_fields(data):
    for key in array_fields:
        if key in data:
            data[key] = [value['id'] for value in data[key]]
        else:
            data[key] = []


def normalize_special_fields(data):
    if 'personal' in data:
        for key, value in data['personal'].items():
            data[key] = value
    if 'occupation' in data:
        data['occupation'] = str(data['occupation'])


def normalize(data: dict):
    normalize_lemmatize_fields(data)
    normalize_obj_fields(data)
    normalize_array_fields(data)
    normalize_special_fields(data)
