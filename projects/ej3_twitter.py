from mongo.utils.mongo_connection import connect
from pprint import pprint
import os
import json


def reset_restaurants(collection):
    path = os.path.join(os.getcwd(), 'static/json/restaurants.json')
    print(path)
    # collection.delete_many({})
    # file = open(path, 'r')
    #
    # for line_data in file:
    #     collection.insert_many(line_data)

    # pprint(json_data)


def ej1(collection):
    print("======================================================")
    print("Ej1: Filtrar por cocinas americanas\n")
    result = collection.find({'cuisine': 'Japanese'})
    print("Ej1: "+str(result.count())+" elements\n")


if __name__ == "__main__":
    coll = connect('clase', 'restaurant')
    reset_restaurants(coll)
    ej1(coll)

