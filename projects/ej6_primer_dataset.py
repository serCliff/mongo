from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from mongo.utils.dataset_downloader import full_primer_dataset_download
from pprint import pprint


def reset_dataset():
    return full_primer_dataset_download()[0]


@exercise_decorator("Ej1: Media de puntuaciones de restaurante de comida italiana")
@print_elements
def ej1(collection):
    return collection.aggregate(
        [
            {'$match': {'cuisine': 'Italian'}},
            {'$unwind': '$grades'},
            {'$group': {
                '_id': '$cuisine',
                'media': {'$avg': '$grades.score'},
            }},
        ]
    )


if __name__ == "__main__":
    res = reset_dataset()
    coll = connect(res[0], res[1])
    ej1(coll)


