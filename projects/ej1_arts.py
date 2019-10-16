from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from pprint import pprint
import os
import json


def reset_arts(collection):
    print("======================================================")
    print("Reloading data")
    collection.delete_many({})
    collection.insert_many([
         {"title": "The Pillars of Society", "artist": "Grosz", "year": 1926, "price": 199.99},
         {"title": "Melancholy III", "artist": "Munch", "year": 1902, "price": 280.00},
         {"title": "Dancer", "artist": "Miro", "year": 1925, "price": "76.04"},
         {"title": "The Great Wave off Kanagawa", "artist": "Hokusai", "price": 167.30},
         {"title": "The Persistence of Memory", "artist": "Dali", "year": 1931, "price": 483.00},
         {"title": "Composition VII", "artist": "Kandinsky", "year": 1913, "price": 385.00},
         {"title": "The Scream", "artist": "Munch", "year": 1893},
         {"title": "Blue Flower", "artist": "O'Keefe", "year": 1918, "price": 118.42}])


@exercise_decorator("Ej1: Obtener registros con año superior a 1920 y precio superior a 200")
@count_decorator
@print_elements
def ej1(collection):
    return collection.find({'year': {'$gt': 1920}, 'price': {'$gt': 200}})


@exercise_decorator("Ej2: Obtener campos que no tengan año establecido")
@count_decorator
@print_elements
def ej2(collection):
    return collection.find({'year': {'$exists': False}})


@exercise_decorator("Ej3: Añadir campo año a los registros que no lo tengan")
def ej3(collection):
    return collection.update_many({'year': {'$exists': False}}, {'$set': {'year': None}})


@exercise_decorator("Ej4: Sacar las tres siguienes filas a las 3 primeras")
@count_decorator
@print_elements
def ej4(collection):
    return collection.find({}).limit(3).skip(3)


@exercise_decorator("Ej5: Sacar las tres siguienes filas a las 3 primeras ordenado por fecha de forma descendente")
@count_decorator
@print_elements
def ej5(collection):
    return collection.find({}).sort('year', -1).limit(3).skip(3)


def execute():
    coll = connect('clase', 'arts')
    reset_arts(coll)
    ej1(coll)
    ej2(coll)
    ej3(coll)
    ej2(coll)
    ej4(coll)
    ej5(coll)
