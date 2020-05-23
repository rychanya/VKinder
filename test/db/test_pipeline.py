import pytest
from db import pipeline
from bson import SON


def test_make_intersection_pipeline():
    assert [] == pipeline.make_intersection_pipeline([])
    pl_set, pl_sort = pipeline.make_intersection_pipeline(
        [('one', [6,7]), ('two', [7, 8])]
        )
    assert pl_set == {
        '$set': SON([
            (
                'one_w',
                {'$size': {'$setIntersection': ['$one', [6,7]]}}
            ),
            (
                'two_w',
                {'$size': {'$setIntersection': ['$two', [7, 8]]}}
            )
        ])
        }
    assert pl_sort == {
        '$sort': SON([
            (
                'one_w', -1
            ),
            (
                'two_w', - 1
            )
        ])
    }

def test_make_match_pipeline():
    pl = pipeline.make_match_pipeline([
        ('one', 1),
        ('two', [1, 2])
    ])
    assert pl == {
        '$match': {
            'one': 1,
            'two': {'$in': [1, 2]}}
    }

def test_make_pipeline():
    pl = pipeline.make_pipeline([], [])
    assert pl[-1] == {'$limit': 10}