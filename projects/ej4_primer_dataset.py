from mongo.utils.mongo import connect
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from mongo.utils.dataset_downloader import full_primer_dataset_download
from pprint import pprint


def reset_dataset():
    connect('clase', 'datasetaplanado').drop()
    return full_primer_dataset_download()[0]


@exercise_decorator("Ej1: Filtrar por las cocinas Americanas y mostrar campo borough")
@count_decorator
@print_elements
def ej1(collection):
    return collection.find({'cuisine': 'American'}, {'_id': 0, 'borough': 1}).limit(10)


@exercise_decorator("Ej2: Filtrar por las cocinas Americanas y devolver el TOTAL de cocinas que tengan zipcode")
def ej2(collection):
    result = collection.count({'cuisine': 'American', 'address.zipcode': {'$exists': True}})
    print("Ej2: "+str(result)+" documento/s\n")


@exercise_decorator("Ej3: Aplanar collección")
def ej3(collection):
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
    print(str(connect('clase', 'datasetaplanado').count({}))+" documento/s\n")


@exercise_decorator("Ej4: Media de puntuaciones de restaurante de comida italiana, por barrio")
@print_elements
def ej4(collection):
    # collection.create_index([('name', 'text')], name='text')
    return collection.aggregate(
        [
            {'$match': {'cuisine': 'Italian'}},
            {'$group': {
                '_id': '$borough',
                'media': {'$avg': '$score'},
            }},
        ]
    )


@exercise_decorator("Ej5: Media de puntuaciones de restaurante por barrio y cocina ordenados de mayor a menor "
                    "puntuación de media y que su media se mayor a 17")
@print_elements
def ej5(collection):
    # collection.create_index([('name', 'text')], name='text')
    # result = collection.find({'$text': {'$search': 'Pizza'}})

    return collection.aggregate(
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


@exercise_decorator("Ej6: Conjunto final de operaciones (WHERE, GROUP, CALCULO, ORDENACIÓN)")
@print_elements
def ej6(collection):
    """
    //  Tipo de grade y documentos cada uno
    // WHERE -> FILTRAR POR COCINA AMERICANA , GRADO A Y PUNTUACIÓN ENTRE 8 y 12, (MAYOR MENOR IGUAL)
    // GROUP -> AGRUPANDO POR BARRIO,
    // CALCULO -> OBTENER EL NÚMERO DE DOCUMENTOS Y LA MEDIA, EL MÁXIMO Y MÍNIMO DE PUNTUACIONES
    // ORDENAR -> POR MEDIA DE FORMA DESCENDENTE
    """

    return collection.aggregate(
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


@exercise_decorator("Ej6: Concatenar calle y código postal en mayúsculas en un nuevo campo")
@print_elements
def ej7(collection):

    return collection.aggregate(
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


if __name__ == "__main__":
    res = reset_dataset()
    coll = connect(res[0], res[1])
    ej1(coll)
    ej2(coll)
    ej3(coll)
    coll2 = connect('clase', 'datasetaplanado')
    ej4(coll2)
    ej5(coll2)
    ej6(coll2)
    ej7(coll2)

