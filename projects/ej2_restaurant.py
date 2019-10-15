from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from mongo.utils.dataset_downloader import restaurants_download
from pprint import pprint


def reset_dataset():
    return restaurants_download()[0]


@exercise_decorator("Ej1: Cuantos restaurantes de cocina japonesa tenemos")
@count_decorator
def ej1(collection):
    return collection.find({'cuisine': 'Japanese'})


@exercise_decorator("Ej2: Filtrar por las cocinas americanas")
@count_decorator
@print_elements
def ej2(collection):
    return collection.find({'cuisine': 'American'}, {'borough'}).limit(10)


if __name__ == "__main__":
    res = reset_dataset()
    coll = connect(res[0], res[1])
    ej1(coll)
    ej2(coll)

