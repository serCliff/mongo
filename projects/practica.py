from mongo.utils.mongo import connect
from mongo.utils.dataset_downloader import taxi_download
from mongo.utils.decorators import exercise_decorator, print_elements, count_decorator


def reset_database(download=True):
    mas_info = 'https://datos.gob.es/en/catalogo/l01280796-taxi-tarifas-suplementos-municipios-paradas-eventuales-regimen-de-descanso-y-duracion-del-servicio'
    connect('practica', 'vehiculos').drop()
    connect('practica', 'vehiculos_aplanado').drop()
    return taxi_download(download)


@exercise_decorator("Total de documentos")
@count_decorator
def documentos_disponibles(collection):
    return collection.find({})


@exercise_decorator("Primer documento")
@count_decorator
@print_elements
def mostrar_1_documento(collection):
    return collection.find({}).limit(1)


@exercise_decorator("10 primeros documentos")
@count_decorator
@print_elements
def mostrar_10_documentos(collection):
    return collection.find({}).limit(10)


@exercise_decorator("Coches con combustible -> NO")
@count_decorator
@print_elements
def coches_no(collection):
    return collection.find({'combustible': 'NO'})


@exercise_decorator("Suprimir documento con combustible -> NO")
def suprimir_no(collection):
    return collection.delete_one({'combustible': 'NO'})


@exercise_decorator("Añadir tiempo que tardan en dar la licencia desde la matriculación")
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


@exercise_decorator("Media de días que se tarda en obtener licencia por combustible")
@print_elements
def media_obtencion_licencias(collection):
    return collection.aggregate([
        {'$match': {'combustible': {'$ne': None}}},
        {'$group':
            {
               '_id': '$combustible',
               'Media': {'$avg': '$dias_en_obtener_licencia'},
               'Total': {'$sum': 1},
            },
         },
        {'$sort': {'Media': 1}}
    ])


@exercise_decorator("Vehículos autorizados por combustible")
@print_elements
def autorizados_combustible(collection):
    return collection.aggregate([
        {'$group':
            {
               '_id': '$combustible',
               'VehIculos': {'$sum': 1},
            },
         },
        {'$sort': {'VehIculos': -1}}
    ])


@exercise_decorator("Creación de nuevo documento \'vehículos\'")
def creacion_vehiculos(collection):
    return collection.aggregate([
        {'$group':
            {
                '_id': '$marca',
                'vehiculos': {'$sum': 1},
                'modelos': {'$push': {'modelo': '$modelo', 'combustible': '$combustible'}}
            },
         },
        {'$sort': {'vehiculos': -1}},
        {'$out': 'vehiculos'},
    ])


@exercise_decorator("Vehículos de cada marca")
@print_elements
def vehiculos_por_marca(collection):
    return collection.aggregate([
        {'$project':
            {
                '_id': 0,
                'marca': '$_id',
                'vehiculos': 1,
                'modelos': 1,
                'combustible': 1,
            },
         },
        {'$limit': 2}
    ])


@exercise_decorator("Aplanado y corrección de modelos de vehículos repetidos")
def aplanado_modelos(collection):
    return collection.aggregate([
        {'$unwind': '$modelos'},
        {'$group': {
            '_id': {
                'modelo': '$modelos.modelo',
                'marca': '$_id',
                'combustible': '$modelos.combustible',
            },
            'total': {'$sum': 1},
        }},
        {'$project':
             {
                 '_id': 0,
                 'marca': '$_id.marca',
                 'modelo': '$_id.modelo',
                 'total': '$total',
                 'combustible': '$_id.combustible',
             }
         },
        {'$out': 'vehiculos_aplanado'}
    ])


@exercise_decorator("Corrección de \'modelos\' de vehículos")
def actualizacion_vehiculos(collection):
    return collection.aggregate([
        {'$lookup':
            {
                'from': "vehiculos_aplanado",
                'localField': "_id",
                'foreignField': "marca",
                'as': "modelos_a"
             }
         },
        {'$project':
             {
                 '_id': 1,
                 'modelos': '$modelos_a',
                 'vehiculos': 1,
             }
         },
        {'$out': 'vehiculos'}
    ])


@exercise_decorator("Supresión campos innecesarios en vehículos")
def limpieza_modelos_vehiculos(collection):
    return collection.update_many(
        {'modelos._id': {'$exists': True}},
        {'$unset':
            {
                'modelos.$[]._id': True,
                'modelos.$[].marca': True
            },
        },
    )


@exercise_decorator("Vehículo más comprado")
@print_elements
def vehiculo_mas_comprado(collection):
    return collection.find({}).sort('total', -1).limit(1)


def execute(download=True):
    res = reset_database(download)

    # Conexiones a todas las bases de datos, para ver que incluye el resultado descomentar la siguiente lInea
    # pprint(res)
    autorizados = connect(res[0][0], res[0][1])
    flota = connect(res[1][0], res[1][1])

    # 1. CORRECCION DE ELEMENTOS ERRoNEOS
    coches_no(flota)
    suprimir_no(flota)
    coches_no(flota)

    # 2. OPERACIONES flota
    documentos_disponibles(flota)
    tiempo_licencias(flota)
    mostrar_10_documentos(flota)
    media_obtencion_licencias(flota)

    # 3. OPERACIONES autorizados
    autorizados_combustible(autorizados)
    creacion_vehiculos(autorizados)

    # 4. OPERACIONES vehiculos
    vehiculos = connect(res[0][0], 'vehiculos')
    vehiculos_por_marca(vehiculos)
    aplanado_modelos(vehiculos)
    vehiculos_aplanado = connect(res[0][0], 'vehiculos_aplanado')
    actualizacion_vehiculos(vehiculos)
    mostrar_1_documento(vehiculos)
    limpieza_modelos_vehiculos(vehiculos)
    mostrar_10_documentos(vehiculos)
    documentos_disponibles(autorizados)
    vehiculo_mas_comprado(vehiculos_aplanado)


if __name__ == '__main__':
    execute(False)
