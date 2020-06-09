import pytest
from db import normalize


@pytest.mark.parametrize(
    'text, lems',
    [
        ('кот коты', ['кот']),
        ('кот собака', ['кот', 'собака']),
        ('Кот, коты!', ['кот']),
        ('', [])
    ]
)
def test_lemmatize(text, lems):
    assert set(normalize.lemmatize(text)) == set(lems)


def test_normalize_lemmatize_fields():
    exist_field = normalize.lemmatize_fields[0]
    exist_data = 'коты'
    data = {exist_field: exist_data}
    normalize.normalize(data)
    for field in normalize.lemmatize_fields:
        if field == exist_field:
            assert data[field] == normalize.lemmatize(exist_data)
        else:
            assert data[field] == []


@pytest.mark.parametrize(
    'data, expected, field',
    [
        (
            {'career': [{'company': 1}, {'company': 2}]},
            [1, 2],
            'career'
        ),
        (
            {'city': {'id': 5}},
            5,
            'city'
        )
    ]
)
def test_normalize_obj_fields(data, expected, field):
    normalize.normalize(data)
    assert data[field] == expected


def test_normalize_array_fields():
    data = {
        'schools': [{'id': 5}, {'id': 7}]
    }
    normalize.normalize(data)
    assert data['schools'] == [5, 7]
    assert data['universities'] == []


def test_normalize_personal():
    data = {
        'personal': {
            'personal_field': 'personal_dta',
            'some': 'thing'
            }
    }
    normalize.normalize(data)
    assert 'personal' in data
    assert data['personal_field'] == 'personal_dta'
    assert data['some'] == 'thing'


def test_normalize_occupation():
    data = {
        'occupation': {
            "type": "university",
            "id": 227,
            "name": "МГППУ"
        }
    }
    normalize.normalize(data)
    assert data['occupation'] == 'МГППУ'
