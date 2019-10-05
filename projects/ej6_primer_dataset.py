from mongo.utils.mongo import connect
from pymongo import MongoClient
from pprint import pprint
import os
import json
import pdb


def reset_dataset(collection):
    current_file = os.path.basename(os.path.realpath(__file__))
    print(current_file)

    # path = os.path.join(os.getcwd(), 'static/json/full_primer-dataset.json')
    # collection.delete_many({})
    # file = open(path, 'r')
    #
    # for line_data in file:
    #     collection.insert_many(line_data)
    # pprint(json_data)


def ej1(collection):
    print("======================================================")
    print("Ej1: Media de puntuaciones de restaurante de comida italiana\n")
    result = collection.aggregate(
        [
            {'$match': {'cuisine': 'Italian'}},
            {'$unwind': '$grades'},
            {'$group': {
                '_id': '$cuisine',
                'media': {'$avg': '$grades.score'},
            }},
        ]
    )
    for i in result:
        pprint(i)


if __name__ == "__main__":
    coll = connect('clase', 'primer')
    reset_dataset(coll)
    ej1(coll)


