from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
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


@exercise_decorator("Ej1: Cantidad instock entre 10 y 20")
@count_decorator
@print_elements
def ej1(collection):
    return collection.find({
        'instock.qty': {'$gte': 10, '$lte': 20},
        })


@exercise_decorator("Ej2.1: Cantidad instock entre 10 y 20 o 40")
@count_decorator
@print_elements
def ej2_1(collection):
    return collection.find({
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


@exercise_decorator("Ej2.2: Cantidad instock entre 10 y 20 o 40")
@count_decorator
@print_elements
def ej2_2(collection):
    return collection.find({
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


def execute():
    coll = connect('clase', 'inventory')
    reset_dataset(coll)
    ej1(coll)
    ej2_1(coll)
    ej2_2(coll)


