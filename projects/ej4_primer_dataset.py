from mongo.utils.mongo import connect
from pymongo import MongoClient
from pprint import pprint
import os
import json
import pdb


def reset_dataset(collection):
    path = os.path.join(os.getcwd(), 'static/json/full_primer-dataset.json')
    print(path)
    # collection.delete_many({})
    # file = open(path, 'r')
    #
    # for line_data in file:
    #     collection.insert_many(line_data)
    # pprint(json_data)

    connect('clase', 'datasetaplanado').drop()


def ej1(collection):
    print("======================================================")
    print("Ej1: Filtrar por las cocinas Americanas y mostrar campo borough\n")
    result = collection.find({'cuisine': 'American'}, {'_id': 0, 'borough': 1}).limit(10)
    for i in result:
        pprint(i)
        print()

    print("Ej1: "+str(result.count())+" elements\n")


def ej2(collection):
    print("======================================================")
    print("Ej2: Filtrar por las cocinas Americanas y devolver el total de cocinas que tengan zipcode\n")
    result = collection.count({'cuisine': 'American', 'address.zipcode': {'$exists': True}})
    print("Ej2: "+str(result)+" elements\n")


def ej3(collection):
    print("======================================================")
    print("Ej3: Aplanar collección\n")
    collection.aggregate(
        [{'$unwind': '$grades'},
         {'$project': {
            '_id': 0,
            'building': "$address.building",
            'street': "$address.street",
            'zipcode': '$address.zipcode',
            'borough': 1,
            'cuisine': 1,
            'date': '$address.date',
            'grade': '$grades.grade',
            'score': '$grades.score',
            'name': 1,
            'restaurant_id': 1, }, },
         {'$out': 'datasetaplanado'}, ]
        )
    print("Ej3: "+str(connect('clase', 'datasetaplanado').count({}))+" elements\n")


def ej4(collection):
    print("======================================================")
    print("Ej4: Media de puntuaciones de restaurante de comida italiana, por barrio\n")
    # collection.create_index([('name', 'text')], name='text')
    result = collection.aggregate(
        [
            {'$match': {'cuisine': 'Italian'}},
            {'$group': {
                '_id': '$borough',
                'media': {'$avg': '$score'},
            }},
        ]
    )
    for i in result:
        pprint(i)


def ej5(collection):
    print("======================================================")
    print("Ej5: Media de puntuaciones de restaurante por barrio y cocina ordenados de mayor a menor puntuación de "
          "media y que su media se mayor a 17\n")
    # collection.create_index([('name', 'text')], name='text')
    # result = collection.find({'$text': {'$search': 'Pizza'}})

    result = collection.aggregate(
        [
            {'$group': {
                '_id': {
                    'barrio': '$borough',
                    'cocina': '$cuisine',
                },
                'media': {'$avg': '$score'},
            }},
            {'$match': {'media': {'$gt': 17}}},
            {'$sort': {'media': -1}},
        ],

    )

    for i in result:
        pprint(i)


def ej6(collection):
    """
    //  Tipo de grade y documentos cada uno
    // WHERE -> FILTRAR POR COCINA AMERICANA , GRADO A Y PUNTUACIÓN ENTRE 8 y 12, (MAYOR MENOR IGUAL)
    // GROUP -> AGRUPANDO POR BARRIO,
    // CALCULO -> OBTENER EL NÚMERO DE DOCUMENTOS Y LA MEDIA, EL MÁXIMO Y MÍNIMO DE PUNTUACIONES
    // ORDENAR -> POR MEDIA DE FORMA DESCENDENTE
    """
    print("======================================================")
    print("Ej6: Conjunto final de operaciones (WHERE, GROUP, CALCULO, ORDENACIÓN)\n")

    result = collection.aggregate(
        [

            {'$match': {'cuisine': 'American', 'grade': 'A', 'score': {'$gte': 8, '$lte': 12}}},
            {'$group': {
                '_id': '$borough',
                'media': {'$avg': '$score'},
                'documentos': {'$sum': 1},
                'maximo': {'$max': '$score'},
                'minimo': {'$min': '$score'},
            }},
            {'$sort': {'media': -1}},
        ],

    )

    for i in result:
        pprint(i)


def ej7(collection):
    print("======================================================")
    print("Ej6: Concatenar calle y código postal en mayúsculas en un nuevo campo\n")

    result = collection.aggregate(
        [
            {'$project': {
                '_id': 0,
                'building': 1,
                'calle/zip': {'$concat': ['$street', ', ', '$zipcode']},
                'borough': 1,
                'cuisine': 1,
                'date': 1,
                'grade': 1,
                'score': 1,
                'name': 1,
                'restaurant_id': 1,
            }},
            {'$limit': 10},
        ],

    )

    for i in result:
        pprint(i)


if __name__ == "__main__":
    coll = connect('clase', 'primer')
    reset_dataset(coll)
    ej1(coll)
    ej2(coll)
    ej3(coll)
    coll2 = connect('clase', 'datasetaplanado')
    ej4(coll2)
    ej5(coll2)
    ej6(coll2)
    ej7(coll2)

