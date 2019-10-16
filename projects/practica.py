from mongo.utils.mongo import connect
from mongo.utils.dataset_downloader import taxi_download
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator
from pprint import pprint
import pdb


def reset_database(download=True):
    mas_cuestiones = 'https://datos.gob.es/en/catalogo/l01280796-taxi-tarifas-suplementos-municipios-paradas-eventuales-regimen-de-descanso-y-duracion-del-servicio'
    return taxi_download(download)


@exercise_decorator("Total de documentos")
@count_decorator
def documentos_disponibles(collection):
    return collection.find({})


@exercise_decorator("Total de documentos")
@count_decorator
@print_elements
def mostrar_10_documentos(collection):
    return collection.find({}).limit(10)


@exercise_decorator("Coches con combustible -> NO")
@count_decorator
@print_elements
def coches_no(collection):
    return collection.find({'combustible': 'NO'})


@exercise_decorator("Suprimir combustible -> NO")
def suprimir_no(collection):
    return collection.delete_one({'combustible': 'NO'})


@exercise_decorator("Combustible de los coches")
@print_elements
def combustibles(collection):
    return collection.aggregate([
        {
            '$group': {
                '_id': '$combustible',
                'Total': {'$sum': 1},
            }
        },
        {
            '$sort': {'combustible': 1}
        }
    ])


@exercise_decorator("Añadir tiempo que tardan en dar la licencia desde la matriculaciOn")
def tiempo_licencias(collection):
    return collection.aggregate([
        {'$addFields':
            {'dias_en_obtener_licencia':
                {'$divide':
                    [{'$subtract':
                        [
                            {'$dateFromString':
                                 {'dateString': '$fecha_inicio_de_prestacion_del_servicio_de_taxi',
                                  'format': "%d/%m/%Y"
                                  }
                             },
                            {'$dateFromString':
                                 {'dateString': '$fecha_matriculacion',
                                  'format': "%d/%m/%Y"
                                  }
                             },
                        ]},
                        3600000 * 24
                    ]
                },
            },
        },
        {'$out': collection.name},
    ])


@exercise_decorator("Media obtenciOn licencia")
@print_elements
def media_obtencion_licencias(collection):
    return collection.aggregate([
        {
            '$group':
             {
               '_id': "$index",

               'media': { '$avg': "dias_en_obtener_licencia" }
             }
         }
    ])


def execute():
    res = reset_database(download=False)

    # Conexiones a todas las bases de datos, para ver que incluye el resultado descomentar la siguiente lInea
    # pprint(res)
    reserva_paradas = connect(res[0][0], res[0][1])
    autorizados = connect(res[1][0], res[1][1])
    objetos_perdidos = connect(res[2][0], res[2][1])
    tarifas = connect(res[3][0], res[3][1])
    flota = connect(res[4][0], res[4][1])

    # 1. CORRECCION DE ELEMENTOS INCORRECTOS
    # coches_no(flota)
    suprimir_no(flota)
    # coches_no(flota)

    # 2. OPERACIONES CON FLOTA
    documentos_disponibles(flota)
    tiempo_licencias(flota)
    media_obtencion_licencias(flota)  # TODO: Obtener una agrupaciOn de todo y sacar la media
    # combustibles(flota)
    # combustibles(autorizados)


if __name__ == '__main__':
    execute()
