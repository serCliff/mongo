from mongo.utils.mongo import connect
from pymongo import MongoClient
from pprint import pprint
import os
import json
import pdb


def reset_dataset(collection):
    collection.drop()
    collection.insert_many([
           {'item': "journal", 'instock': [{'warehouse': "A", 'qty': 5}, {'warehouse': "C", 'qty': 15}]},
           {'item': "notebook", 'instock': [{'warehouse': "C", 'qty': 5}]},
           {'item': "paper", 'instock': [{'warehouse': "A", 'qty': 60}, {'warehouse': "B", 'qty': 15}]},
           {'item': "planner", 'instock': [{'warehouse': "A", 'qty': 40}, {'warehouse': "B", 'qty': 5}]},
           {'item': "postcard", 'instock': [{'warehouse': "B", 'qty': 15}, {'warehouse': "C", 'qty': 35}]}
    ])


def ej1(collection):
    print("======================================================")
    print("Ej1: Cantidad instock entre 10 y 20\n")
    result = collection.find({
        'instock.qty': {'$gte': 10, '$lte': 20},
        })

    for i in result:
        pprint(i)
        print()

    print("Ej1: "+str(result.count())+" elements\n")


def ej2_1(collection):
    print("======================================================")
    print("Ej2.1: Cantidad instock entre 10 y 20 o 40\n")
    result = collection.find({
        'instock': {
            '$all': [
                {'$elemMatch':
                    {'qty': {'$gte': 10, '$lte': 20}, },
                 },
                {'$elemMatch':
                    {'qty': {'$eq': 40}}
                 },
                ]
            }
        })

    for i in result:
        pprint(i)
        print()

    print("Ej2.1: "+str(result.count())+" elements\n")


def ej2_2(collection):
    print("======================================================")
    print("Ej2.2: Cantidad instock entre 10 y 20 o 40\n")
    result = collection.find({
        '$or': [{
            'instock': {
                '$elemMatch': {
                    'qty': {'$gte': 10, '$lte': 20},
                    }
                }
            },
            {'instock.qty': 40}
            ]
        })

    for i in result:
        pprint(i)
        print()

    print("Ej2.2: "+str(result.count())+" elements\n")


if __name__ == "__main__":
    coll = connect('clase', 'inventory')
    reset_dataset(coll)
    ej1(coll)
    ej2_1(coll)
    ej2_2(coll)


