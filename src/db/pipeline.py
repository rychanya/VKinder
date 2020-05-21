from bson import SON


def make_intersection_pipeline(criterions):
    def size_pipline(name, value):
        return (
            f'{name}_w',
            {'$size': {'$setIntersection': [f'${name}', value]}}
            )
    if not criterions:
        return []
    return [{
        '$set': SON([size_pipline(name, value) for name, value in criterions])
        },
        {
            '$sort': SON([(f'{name}_w', -1) for name, _ in criterions])
        }]


def make_match_pipeline(criterions):
    if not criterions:
        return []
    return {
        '$match': {
            name: {'$in': value} if isinstance(value, list)
            else value for name, value in criterions
            }
    }


def make_pipeline(match_criterions, intersection_criterions):
    pipeline = []
    copy_match_criterions = match_criterions.copy()
    copy_match_criterions.append(('skip', {'$exists': False}))
    pipeline.append(make_match_pipeline(copy_match_criterions))
    pipeline.extend(make_intersection_pipeline(intersection_criterions))
    pipeline.append({'$limit': 10})
    return pipeline
