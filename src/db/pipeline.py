from bson import SON


def chose_project_method(name, value):

    def match(name, value):
        return {'$eq': [f'${name}', value]}

    def intersection(name, value):
        return {'$size':  {'$setIntersection': [f'${name}', value]}}

    if isinstance(value, (list, tuple, set)):
        return intersection(name, value)
    else:
        return match(name, value)


def make_pipeline(criterions):
    if not criterions:
        return [
            {
                '$match': {'skip': {'$exists': False}}
            },
            {
                '$limit': 10
            }
        ]
    return [
        {
            '$match': {'skip': {'$exists': False}}
        },
        {
            '$project': SON(
                [(name, chose_project_method(name, value))
                    for name, value in criterions] + [('id', 1), ('domain', 1)]
                    )
        },
        {
            '$sort': SON(
                [(name, -1) for name, value in criterions]
                )
        },
        {
            '$limit': 10
        }
    ]
