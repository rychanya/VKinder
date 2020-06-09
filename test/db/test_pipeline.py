import pytest
from db import pipeline
from bson import SON


@pytest.mark.parametrize(
    'project, expected',
    [
        (('name', 'value'), ({'$eq': ['$name', 'value']})),
        (('name', [1, 2]), ({'$size':  {'$setIntersection': ['$name', [1, 2]]}})),
        (('name', (1, 2)), ({'$size':  {'$setIntersection': ['$name', (1, 2)]}})),
        (('name', {1, 2}), ({'$size':  {'$setIntersection': ['$name', {1, 2}]}})),
        (('name', []), ({'$size':  {'$setIntersection': ['$name', []]}})),
        (('name', set()), ({'$size':  {'$setIntersection': ['$name', set()]}})),
    ]
)
def test_chose_project_method(project, expected):
    result = pipeline.chose_project_method(*project)
    assert result == expected


def test_make_pipeline_empty():
    pl = pipeline.make_pipeline([])
    assert pl[0] == {'$match': {'skip': {'$exists': False}}}
    assert pl[-1] == {'$limit': 10}


def test_make_pipeline():
    pl = pipeline.make_pipeline([('name1', 6), ('name2', [1, 2])])
    assert pl[0] == {'$match': {'skip': {'$exists': False}}}
    assert pl[-1] == {'$limit': 10}
    assert '$project' in pl[1] and len(pl[1]) == 1
    assert '$sort' in pl[2] and len(pl[2]) == 1
    assert pl[1]['$project'] == SON([
        ('name1', {'$eq': ['$name1', 6]}),
        ('name2', {'$size':  {'$setIntersection': ['$name2', [1, 2]]}}),
        ('id', 1),
        ('domain', 1)
    ])
    assert pl[2]['$sort'] == SON([
        ('name1', -1),
        ('name2', -1)
    ])
