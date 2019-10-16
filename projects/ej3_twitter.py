from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from mongo.utils.dataset_downloader import twitter_download
from pprint import pprint


def reset_dataset():
    return twitter_download()[0]


@exercise_decorator("Mostrar 10")
@count_decorator
@print_elements
def ej1(collection):
    return collection.find({}).limit(10)


def execute():
    res = reset_dataset()
    coll = connect(res[0], res[1])
    ej1(coll)

