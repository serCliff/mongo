# DOCUMENTACIÓN PRÁCTICA GESTIÓN DE BASES DE DATOS NO SQL
[TOC]

En la siguiente web podremos obtener los datos que se van a utilizar sobre los taxis de madrid

[TAXIS MADRID](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=4f16216612d39410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

### REPOSITORIO - AUTOR

[Mongo - Sergio del Castillo Baranda](https://github.com/serCliff/mongo/)

## TAREAS

1. Obtener datos en json
1. Crear varias colecciones en las que se muestren
   -  Instrucciones con búsquedas y agregaciones
    - Creación de las colecciones con los diferentes datos
    - Obtención de información sobre el estado actual de los taxis
    - Concatenación de la información entre las diferentes colecciones
    - Generar generar otras tablas y trabajar con ellas
3. FUTURO
   -  Generar información en otra base de datos que se vaya actualizando
      constantemente (RSS)  
   - Crear un replicaset
   [INFO!!](https://github.com/serCliff/master_mongo/blob/master/static/documentation/replicaset.md)

# 1. EJECUCIÓN DE LA PRÁCTICA
### 1.1 INSTALACIÓN DE PAQUETES DE PYTHON NECESARIOS

Para realizar la ejecución y comprobación de los datos obtenidos hay que realizar una instalación previa de los paquetes que se van a utilizar en la práctica:

```bash
sudo apt-get udate && sudo apt-get upgrade -y sudo apt-get install python3 python3-pip -y
```

Instalación de los módulos de python requeridos:

```bash
sudo pip install -r requirements.txt
```

### 1.2 MÓDULOS UTILIZADOS

Todo el proyecto ha sido desarrollado en python. Para que esto sea posible son necesarios un conjunto de paquetes y módulos de python para poder realizar las operaciones en la base de datos de mongo, descarga de ficheros, etc. 

#### pymongo

Módulo para poder conectarse con una base de datos mongodb y hacer consultas. Más información click [aquí.](https://pypi.org/project/pandas/)

#### pandas

Módulo utilizado para el tratamiento de datos obtenidos en formato csv. Más información click [aquí.](https://pypi.org/project/pandas/)

#### unidecode

Módulo utilizado para la transformación de cadenas de caracteres en formato utf-8 suprimiendo las particularidades del idioma español. Básicamente hace una transformación de caracteres como ñ -> n suprime acentos entre otro. Más información click [aquí.](https://pypi.org/project/Unidecode/)

### ESTRUCTURA DEL PROYECTO

```
.
├── projects                            # Lista de scripts pythons ejecutables
├── static                              # Ficheros estáticos de soporte (json, csv...)
├── utils
│   ├── dataset_downloader.py           # Descargador de ficheros
│   ├── decorators.py                   # Decoradores para mostrar resultados de querys
│   ├── mongo.py                        # Scripts para facilitar uso de mongo
│   └── utils.py                        # Scripts de soporte general
├── __main__.py							# Menú de ejecución del proyecto
├── requirements.txt
└── README.md
```

#### projects

En esta carpeta se encuentran los ejecutables de todas las tareas realizadas en clase y la práctica final, se ejecutarán desde el menú de operaciones de la práctica

#### static

En esta carpeta se encuentra la parte de la documentación de la práctica y cómo generar un dataset (no utilizado en esta práctica). 

A parte también se descargarán aquí los ficheros de soporte que sean necesarios. Estos ficheros son los json, csv, tar... que se necesitan para la ejecución del proyecto.

#### utils

##### dataset_downloader.py

Este archivo tiene los métodos que se utilizan en la práctica para descargar los datasets de cada tarea que se va a ejecutar. También se ejecutan aquí los métodos que realizan la importación en la base de datos

> Es importante destacar que no tienen en cuenta conexiones que no se realicen a un servidor mongo que no esté localizado en localhost en el puerto por defecto.

El más representativo para esta práctica de todos los que hay es:

```python
def taxi_download(download=True):
    """
    Donwload taxi files
    :param download: True to download data, False to use downloaded datasets
    :return: list of tuples ('database', 'collection') imported
    """
    
    csv_paths = dict()
    json_paths = dict()
    csv_links = dict({
        'autorizados': 'https://datos.madrid.es/egob/catalogo/207347-1-taxi-modelo-vehiculos.csv',
        'flota': 'https://datos.madrid.es/egob/catalogo/300226-0-taxi-flota-diaria.csv',
    })

    # Download and parse csv to json files
    for key, csv_link in csv_links.items():
        if download:
            json_path = csv_to_json(download_csv(csv_link))
        else:
            json_path = get_json_path(os.path.basename(csv_link).replace('csv', 'json'))
        json_paths[key] = json_path

    # Bulk Import of json files
    for key, json_path in json_paths.items():
        c = connect('practica', key)
        c.drop()
        bulk_file_import(c, json_path)

    return [('practica', key) for key in json_paths.keys()]


```

##### decorators.py

Este archivo contiene los decoradores utilizados en las diferentes ejecuciones de las querys. Facilitan la representación de la información obtenida de la base de datos.

El primer decorador muestra la cabecera de todas las querys ejecutadas

```python
def exercise_decorator(text):
    """
    Exercise decorator to show the introduction text of the query
    :param text: Text ot be shown
    """
    def execute(function):
        def query(collection):
            string_to_expand = '-'
            new_text = "**{0}**: {1}".format(collection.name, text)
            header = (string_to_expand * (int(len(new_text) / len(string_to_expand)) + 1))[:len(new_text)]
            print("\n{0}\n{1}\n".format(header, new_text))
            return function(collection)
        return query
    return execute
```

El segundo decorador muestra los resultados obtenidos tras la ejecución de una query.

```python
def print_elements(function):
    """
    Decorator used to show the documents returned by the query
    """
    def wrapper(collection):
        # input("Click Enter >> ")
        res = function(collection)
        for i in res:
            pprint(i)
        return res
    return wrapper
```

El último decorador muestra el total de docuementos obtenidos en la query.

```python
def count_decorator(function):
    """
    Decorator used to show the count of documents retuned by the query
    """
    def wrapper(collection):
        res = function(collection)
        print("\n{0} documento/s".format(res.count()))
        return res
    return wrapper
```



Estos decoradores se utilizarán indistintamente en unas y otras operaciones para mostrar los resultados de las operaciones ejecutadas en cada una de las prácticas. Se verán que operaciones utilizan unos u otros ya que aparecen justo antes de los métodos con el título del decorador precedido de el caracter @.

#### mongo.py

En este fichero se encuentran las operaciones que conectan las operaciones que se realizan en el proyecto con la base de datos mongodb.

El primero se utiliza para **conectarse a la base de datos** y realizar la ejecución de las diferentes tareas y los dos últimos realizan la **importación de dataset en la base de datos**.

```python
def connect(db, collection, host='localhost', port=27017, username=None, password=None):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db][collection]
```

El método `bulk_file_import` realiza la **importación de datos a través de un json**. Este json puede estar formado por una lista que contenga un conjunto de documentos json en su interior, para ello utiliza el método `insert_many` o por el contrario puede estar formado por un único json, en esta ocasión se utiliza el método `insert_one`.

```python
def bulk_file_import(collection, json_path):
    """
    Make a bulk import of a json in a collection
    :param collection: Collection where you want to import
    :param json_path: Path where the json was located
    """
    with open(json_path, encoding='utf-8') as f:
        file_data = json.load(f)

    if isinstance(file_data, list):
        collection.insert_many(repair_dict_keys(file_data))
    else:
        collection.insert_one(repair_dict_keys(file_data))
    print("Imported file: {0}!!!".format(os.path.basename(json_path)))
```

El método `bulk_file_mongoimport` realiza la **importación de datos a través de un fichero que contiene muchos json en su interior** para ello utiliza el comando que se utiliza en la terminal para realizar una importación `mongoimport`.

```python
def bulk_file_mongoimport(collection, json_path):
    """
    Make a bulk import of a json in a collection
    :param collection: Collection where you want to import
    :param json_path: Path where the json was located
    """
    db = collection.database
    host = db.client.address[0]
    port = db.client.address[1]
    command = 'mongoimport ' \
              '--db {0} ' \
              '--collection {1} ' \
              '--host {2} ' \
              '--port {3} ' \
              '--type json ' \
              '--drop ' \
              '--stopOnError ' \
              '--file {4}'.format(db.name, collection.name, host, port, json_path)
    os.system(command)
    print("Imported file: {0}!!!".format(os.path.basename(json_path)))
```

#### utils.py

Este fichero incluye un conjunto de operaciones generales de soporte como:

- Descargar ficheros en zip, csv y json
- Parseado de ficheros csv a json
- Reparación de las claves generadas al importar datos. Esto es necesario ya que mongodb tiene ciertas restricciones. (Ej: una clave no puede tener puntos). A mayores también reescribe las claves para que tengan un formato más fácil de comprender y trabajar con él.

#### \_\_main__.py

Este fichero contiene el menú de ejecución. Se utiliza para guiar en el conjunto de tareas realizadas en la asignatura. Tan sólo ejecutar el código y se guiará automáticamente a través de las operaciones disponibles.

#### requirements.txt

Únicamente incluye los módulos de python utilizados para la práctica. Explicados más arriba. 

```
pymongo
pandas
unidecode
```

## 1.2. EJECUCIÓN DE LA PRÁCTICA

Tras haber explicado los componentes del documento, la ejecución de la práctica se realiza como si fuera un proyecto de python, utilizar siguiente comando: 

```bash
python -m mongo
```
> Recuerda que python tiene que estar en la versión 3.6
>
> Es necesario tener internet para poder descargar los documentos que se utilizarán en la práctica

# 2. MENÚ DE OPCIONES

Para conducir la ejecución de las operaciones se ha creado un menú que ayuda a la selección de los ejercicios disponibles. Tan sólo introducir el número que se desee para ejecutar una tarea.

```bash
Bienvenido,

Selecciona la ejecución deseada:

1. PRÁCTICA FINAL
2. Ejercicios día 1 (arts)
3. Ejercicios día 2 (restaurant)
4. Ejercicios día 3 (tweet)
5. Ejercicios día 4 (full-primer_dataset)
6. Ejercicios día 5 (inventory)
7. Ejercicios día 6 (full-primer_dataset)

8. Quitar

 >>  							# <--- Insertar número aquí para ejecutar
```

# 3. EJECUCIÓN DE LA PRÁCTICA
Tras seleccionar la ejecución de la PRÁCTICA FINAL lo primero que se hace es la descarga los csv con el dataset y transformarlos a json. A continuación los importa en la base de datos mongo. Mirar utils/dataset_downloader.py (taxi_downloader) para más información.

```
CSV downloaded: 207347-1-taxi-modelo-vehiculos.csv
CSV parsed to JSON 207347-1-taxi-modelo-vehiculos.csv -> 207347-1-taxi-modelo-vehiculos.json

CSV downloaded: 300226-0-taxi-flota-diaria.csv
CSV parsed to JSON 300226-0-taxi-flota-diaria.csv -> 300226-0-taxi-flota-diaria.json

Imported file: 207347-1-taxi-modelo-vehiculos.json!!!
Imported file: 300226-0-taxi-flota-diaria.json!!!
```

## 3.1 OPERACIONES

### 3.1.1 CORRECCIÓN DE LAS BASES DE DATOS
En primer lugar es útil ejecutar un método para corregir la base de datos.

En la base de datos se ha introducido un coche que tiene como combustible 'NO' lo cual significa que el dato es incorrecto o incompleto, para suprimirlo utilizo el método `delete_one`

---------------------------------------
#### **FLOTA**: Coches con combustible -> NO

La representación de información se realiza con una proyección obtenida con el método `find`, en concreto para obtener los vehículos cuyo combustible es igual a 'NO'

```python
@exercise_decorator("Coches con combustible -> NO")
@count_decorator
@print_elements
def coches_no(collection):
    return collection.find({'combustible': 'NO'})
```

El resultado de esta ejecución obtiene como resultado


```json
{'_id': ObjectId('5da8948861c54b3ad69cf1f1'),
 'cilindrada': None,
 'clasificacion_medioambiental': 'NO',
 'codigo': 'BV2L',
 'combustible': 'NO',
 'eurotaxi': None,
 'fecha': None,
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': None,
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': 'GASOLINA TRANSFORMADO GLP',
 'index': 9939,
 'marca': '1597',
 'matricula': 'ECO',
 'modelo': '94.1',
 'numero_de_plazas': '16/10/2019',
 'potencia': None,
 'regimen_especial_de_eurotaxi': None,
 'tipo': '5',
 'variante': '16/09/2019'}
```
1 documento/s

Obtenemos un único documento en el que podemos observar como el combustible que dispone es 'NO'

---------------------------------------------------
#### **FLOTA**: Suprimir documento con combustible -> NO

A continuación procedo a la supresión de dicho documento, el comando `delete_one` utiliza un filtrado similar al método `find`

```python
@exercise_decorator("Suprimir documento con combustible -> NO")
def suprimir_no(collection):
    return collection.delete_one({'combustible': 'NO'})
```
--------------------------------------------
#### **FLOTA**: Coches con combustible -> NO

En esta ocasión ejecutamos de nuevo el mismo método y no obtenemos ningún resultado.

> El resultado de la ejecución en esta ocasión no representa ninguna información

0 documento/s

### 3.1.2 EJERCICIOS CON FLOTA

-----------------------------------
#### **FLOTA**: Total de documentos

En primer lugar visualizaremos el total de documentos que tenemos en flota. Para ello ejecutamos el siguiente método. Podemos ver como la cuenta ha sido realizada posteriormente con el decorador `@count_decorator`

```python
@exercise_decorator("Total de documentos")
@count_decorator
def documentos_disponibles(collection):
    return collection.find({})
```

> El resultado de la ejecución en esta ocasión no representa ninguna información

15621 documento/s

----------------------------------------------------------------------------------
#### **FLOTA**: Añadir tiempo que tardan en dar la licencia desde la matriculación

El conjunto de métodos que visualizaremos a continuación busca obtener información sobre qué tipos de vehículos son los más comunes en la flota de taxis de madrid. 

Vamos a diferenciarlos por el combustible que utilizan para saber cuales compensa más comprarse en función del tiempo que se tarda en obtener una licencia para poder comenzar con el trabajo como taxista.

Esto lo vamos a contrastar con los  vehículos que hay actualmente operativos para obtener conclusiones.

El método ejecutado en esta ocasión es:

```python
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
```

Este método realiza una agregación para obtener los días que se han tardado en obtener las licencias para cada vehículo. 

El primer operador que se utiliza sobre el framework de agregación es `$addFields`, permite **generar un campo nuevo** en el documento. 

El campo generado `dias_en_obtener_licencia` es resultado de la resta entre la `fecha_inicio_de_prestacion_del_servicio_de_taxi` y la `fecha_matriculacion`. 

Pero aquí nos econtramos con un problema, ambos campos han sido registrados como `String`, para poder hacer la resta entre una fecha y otra, tenemos que **transformar la cadena de caracteres por una fecha**, para ello se utiliza el operador `$dateFromString` que tras pasarle el formato en el que tenemos registrada la fecha nos devuelve un objeto `Date` con el que ya podemos trabajar.

**Para hacer la resta** se emplea el operador `$subtract`, a este operador se le puede pasar una lista de elementos y este los restará en orden. 

Cómo estamos trabajando con objetos `Date` al realizar la resta obtenemos el conjunto de milésimas de segundo que separan una fecha de la otra. Para obtener los días a los que corresponde el resultado obtenido utilizamos el operador `$divide`  que **realiza la división** entre 3600000 (milésimas de segundo que corresponde una hora) * 24 (horas del día).

Finalmente, se utiliza el operador `$out` que nos permite **actualizar la colección** cuyo nombre es  como argumento. 

> El resultado de la ejecución en esta ocasión no representa ninguna información

--------------------------------------
#### **FLOTA**: 10 primeros documentos

En esta ejecución podemos observar las operaciones realizadas en la anterior ejecución.

```json
{'_id': ObjectId('5da8bab6efca49026ee9a3e3'),
 'cilindrada': 0.0,
 'clasificacion_medioambiental': None,
 'codigo': '1020144',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 3.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '16/12/2005',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '13/12/2005',
 'index': 0,
 'marca': 'SKODA',
 'matricula': '2239DTJ',
 'modelo': 'OCTAVIA',
 'numero_de_plazas': None,
 'potencia': '12',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': None,
 'variante': None}
{'_id': ObjectId('5da8bab6efca49026ee9a3e4'),
 'cilindrada': 0.0,
 'clasificacion_medioambiental': None,
 'codigo': '550115',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 6.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '14/01/2010',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '08/01/2010',
 'index': 1,
 'marca': 'SKODA',
 'matricula': '4249GST',
 'modelo': 'OCTAVIA',
 'numero_de_plazas': None,
 'potencia': '12',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': None,
 'variante': None}
{'_id': ObjectId('5da8bab6efca49026ee9a3e5'),
 'cilindrada': 0.0,
 'clasificacion_medioambiental': None,
 'codigo': '550214',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 522.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '03/08/2012',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '28/02/2011',
 'index': 2,
 'marca': 'SKODA',
 'matricula': '6296HBZ',
 'modelo': 'OCTAVIA',
 'numero_de_plazas': None,
 'potencia': '11,64',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': '1Z',
 'variante': 'AACAYCX01/NFM5'}
{'_id': ObjectId('5da8bab6efca49026ee9a3e6'),
 'cilindrada': 0.0,
 'clasificacion_medioambiental': None,
 'codigo': '550241',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 878.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '10/01/2013',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '16/08/2010',
 'index': 3,
 'marca': 'VOLKSWAGEN',
 'matricula': '9097GYH',
 'modelo': 'PASSAT',
 'numero_de_plazas': None,
 'potencia': '13',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': '3C',
 'variante': 'AACBBBX0/FM6FM6*******'}
{'_id': ObjectId('5da8bab6efca49026ee9a3e7'),
 'cilindrada': 1991.0,
 'clasificacion_medioambiental': 'B',
 'codigo': '1182347',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 2.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '04/02/2010',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '02/02/2010',
 'index': 4,
 'marca': 'CHEVROLET',
 'matricula': '5440GTD',
 'modelo': 'EPICA',
 'numero_de_plazas': '5',
 'potencia': '110',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': 'KLAL',
 'variante': 'LV3/134'}
{'_id': ObjectId('5da8bab6efca49026ee9a3e8'),
 'cilindrada': 1991.0,
 'clasificacion_medioambiental': 'B',
 'codigo': '1181262',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 6.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '20/01/2010',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '14/01/2010',
 'index': 5,
 'marca': 'CHEVROLET',
 'matricula': '9246GSV',
 'modelo': 'EPICA',
 'numero_de_plazas': '5',
 'potencia': '110',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': 'KLAL',
 'variante': 'LV3/134'}
{'_id': ObjectId('5da8bab6efca49026ee9a3e9'),
 'cilindrada': 1560.0,
 'clasificacion_medioambiental': 'C',
 'codigo': '1385946',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 4.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '13/07/2015',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '09/07/2015',
 'index': 6,
 'marca': 'CITROEN',
 'matricula': '6871JGV',
 'modelo': 'C4 PICASSO',
 'numero_de_plazas': '5',
 'potencia': '88',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': '3',
 'variante': '3DBHZ*'}
{'_id': ObjectId('5da8bab6efca49026ee9a3ea'),
 'cilindrada': 1560.0,
 'clasificacion_medioambiental': 'C',
 'codigo': '1469525',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 31.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '05/04/2017',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '05/03/2017',
 'index': 7,
 'marca': 'CITROEN',
 'matricula': '9700JXY',
 'modelo': 'CITROEN C-ELYSEE',
 'numero_de_plazas': '5',
 'potencia': '73',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': 'D',
 'variante': 'DBHY'}
{'_id': ObjectId('5da8bab6efca49026ee9a3eb'),
 'cilindrada': 1587.0,
 'clasificacion_medioambiental': 'ECO',
 'codigo': '1508730',
 'combustible': 'GLP / GASOLINA',
 'dias_en_obtener_licencia': 2.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '23/03/2018',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '21/03/2018',
 'index': 8,
 'marca': 'CITROEN',
 'matricula': '6807KJK',
 'modelo': 'CITROEN C-ELYSEE eco-glv',
 'numero_de_plazas': '5',
 'potencia': '85',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': 'F',
 'variante': 'FECE'}
{'_id': ObjectId('5da8bab6efca49026ee9a3ec'),
 'cilindrada': 1997.0,
 'clasificacion_medioambiental': 'C',
 'codigo': '1376586',
 'combustible': 'DIESEL',
 'dias_en_obtener_licencia': 7.0,
 'eurotaxi': 'NO',
 'fecha': '16/10/2019',
 'fecha_fin_regimen_especial_eurotaxi': None,
 'fecha_inicio_de_prestacion_del_servicio_de_taxi': '24/03/2015',
 'fecha_inicio_regimen_especial_eurotaxi': None,
 'fecha_matriculacion': '17/03/2015',
 'index': 9,
 'marca': 'CITROEN',
 'matricula': '6995JDF',
 'modelo': 'C4 PICASSO',
 'numero_de_plazas': '5',
 'potencia': '110',
 'regimen_especial_de_eurotaxi': 'NO',
 'tipo': '3',
 'variante': '3DAHR*'}
```

15621 documento/s

------------------------------------------------------------------------------
#### **FLOTA**: Media de días que se tarda en obtener licencia por combustible

Siguiendo con el objetivo de saber si hay alguna relación entre el tipo de combustible de un vehículo y los días que se tarda en obtener una licencia realizamos una operación para obtener la media de días que se tarda en obtener una licencia agrupando por el combustible utilizado.

Se realiza de nuevo una agregación en la que **descartamos todos los documentos de los que no sabemos su combustible** mediante el operador `$match` que siendo utilizado junto con el operador `$ne`  nos permite realizar dicho filtrado.

Para la agrupación utilizamos el operador `$group` que nos permite **obtener los documentos agrupados por combustible**.

La **media de días en obtener la licencia**, se realiza con el operador `$avg` y a continuación realizamos una **suma de** todos aquellos **documentos** que se concuerda con la agrupación realizada con el operador `$sum`. Finalmente los **ordenamos** la media obtenida de menor a mayor con `$sort `.

```python
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
```

El resultado obtenido es el siguiente. En él podemos observar que hay una diferencia notable entre los vehículos que utilizan `GASOLINA` como combustible. Tambíen podemos observar como únicamente hay 5 vehículos que utilicen dicho combustible.

A mayores podemos observar como el combustible más utilizado es de vehículos que utilizan `DIESEL` y lo cual lo hace una apuesta muy interesante ya que es el segundo combustible que menos se tarda en obtener una licencia.

```json
{'Media': 3.6, 'Total': 5, '_id': 'GASOLINA'}
{'Media': 16.41263157894737, 'Total': 6175, '_id': 'DIESEL'}
{'Media': 17.805825242718445, 'Total': 206, '_id': 'GASOLINA TRANSFORMADO GLP'}
{'Media': 18.74442379182156, 'Total': 3228, '_id': 'GLP / GASOLINA'}
{'Media': 26.03846153846154, 'Total': 26, '_id': 'ELECTRICO'}
{'Media': 31.696894409937887, 'Total': 805, '_id': 'GASOLINA - GAS NATURAL'}
{'Media': 62.0, 'Total': 1, '_id': 'DIESEL TRANSFORMADO A GLP'}
{'Media': 84.27049497293116, 'Total': 5172, '_id': 'GASOLINA-ELECTRICIDAD'}
```

### 3.1.3 EJERCICIOS CON AUTORIZADOS

-----------------------------------------------------------
#### **AUTORIZADOS**: Vehículos autorizados por combustible

Los vehículos anteriormente mostrados son todos aquellos que han obtenido una licencia a lo largo del tiempo, sin embargo no son todos los vehículos que actualmente circulan por madrid. Estos los obtenemos de otra colección.

```python
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
```

Con esta nueva agregación obtenemos, de la colección de vehículos autorizados una agrupación también por combustible del conjunto de vehículos que hay circulando por la ciudad de Madrid actualmente. 

Podemos observar que efectivamente los vehículos que más se utilizan son aquellos cuyo combustible es el diesel. 

Otra conclusión que podemos obtener es que el hecho de obtener una licencia rápidamente no es condición indispensable para la gente para decantarse por un vehículo de modo que tendremos que fijarnos en otros factores que nos ayuden en nuestra compra.

```json
{'VehIculos': 120, '_id': 'DIESEL'}
{'VehIculos': 39, '_id': 'ELECTRICO'}
{'VehIculos': 22, '_id': 'GLP / GASOLINA'}
{'VehIculos': 20, '_id': 'GASOLINA-ELECTRICIDAD'}
{'VehIculos': 12, '_id': 'GASOLINA - GAS NATURAL'}
{'VehIculos': 9, '_id': 'GASOLINA'}
{'VehIculos': 9, '_id': 'GASOLINA TRANSFORMADO GLP'}
{'VehIculos': 1, '_id': 'DIESEL-ELECTRICIDAD'}
```
-------------------------------------------------------------
#### **AUTORIZADOS**: Creación de nuevo documento 'vehículos'

El objetivo ahora es saber concretamente que vehículo deseamos comprarnos, pero la información ahora está demasiado dispersa. Para agrupar los resultados vamos a obtener el conjunto de vehículos por marca y combustible que están en circulación.

```python
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
```

Inicialmente generamos un nuevo documento en el que agrupamos los vehículos por su marca y modelo. Para ello, introducimos cada uno de los documentos que se obtienen en la agrupación de un vehículo por combustible con el operador `$push`. El cual nos permite ingresar la lista de modelos que tiene cada marca en un campo `modelos`. Para poder trabajar con estos datos generamos una nueva colección `vehiculos` donde trabajaremos estos datos.

> El resultado de la ejecución en esta ocasión no representa ninguna información

-------------------------------------------
#### **VEHICULOS**: Vehículos de cada marca

El documento resultante de la anterior operación nos permite obtener una salida similar a la siguiente.

```json
{'marca': 'FORD',
 'modelos': [{'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TRANSIT CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'DIESEL', 'modelo': 'FORD TOURNEO CONNECT'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO'}],
 'vehiculos': 71}
{'marca': 'VOLKSWAGEN',
 'modelos': [{'combustible': 'GASOLINA', 'modelo': 'TRANSPORTER o. CA'},
             {'combustible': 'GASOLINA', 'modelo': 'TRANSPORTER o. CA'},
             {'combustible': 'GASOLINA', 'modelo': 'CADDY'},
             {'combustible': 'GLP / GASOLINA', 'modelo': 'CADDY'},
             {'combustible': 'GLP / GASOLINA', 'modelo': 'CADDY'},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': 'TRANSPORTER o. CA'},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': 'TRANSPORTER o. CA'},
             {'combustible': 'GASOLINA - GAS NATURAL', 'modelo': 'PASSAT'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'GASOLINA - GAS NATURAL', 'modelo': 'CADDY'},
             {'combustible': 'GASOLINA - GAS NATURAL', 'modelo': 'CADDY'},
             {'combustible': 'GASOLINA - GAS NATURAL', 'modelo': 'CADDY'},
             {'combustible': 'GASOLINA - GAS NATURAL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'CADDY'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'},
             {'combustible': 'DIESEL', 'modelo': 'KOMBI CARAVELLE'}],
 'vehiculos': 37}
```
---------------------------------------------------------------------------
#### **VEHICULOS**: Aplanado y corrección de modelos de vehículos repetidos

Tenemos demasiada información equivalente de cada modelo repetida. Para organizar un poco esta información realizaremos una agrupación de los modelos de cada marca almacenando el total de ocurrencias del mismo.

```python
@exercise_decorator("Aplanado y corrección de modelos de vehículos repetidos")
@print_elements
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
```

Dicho resultado lo obtenemos realizando una agrupación del modelo y proyectándolo todo en un **documento aplanado** que obtenemos utilizando el operador `$unwind` sobre los modelos de la lista de documentos anteriormente obtenida.

>El documento aplanado podría haberse obtenido con la colección de autorizados pero con esta ejecución se utiliza el operador unwind.

> El resultado de la ejecución en esta ocasión no representa ninguna información

--------------------------------------------------------
#### **VEHICULOS**: Corrección de 'modelos' de vehículos

Lo que buscamos es que en el campo modelos de vehiculos tengamos una lista de cada modelo de cada vehículo diferenciando su combustible e indicando el total de registros existentes del mismo.

```python
@exercise_decorator("Corrección de \'modelos\' de vehículos")
@print_elements
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
```

Para ello esta ejecución nos permite hacer la **unión de colecciones** utilizando el operador `$lookup`de los resultados agrupados de la colección de vehículos aplanados junto con las marcas de los vehículos existentes en la colección de vehículos. Para hacer dicho almacenamiento la proyección obtenida se actualiza directamente sobre la colección de vehículos.

> El resultado de la ejecución en esta ocasión no representa ninguna información
------------------------------------
#### **VEHICULOS**: Primer documento

El resultado obtenido en la anterior ejecución tiene el siguiente aspecto.

```json
{'_id': 'FORD',
 'modelos': [{'_id': ObjectId('5da8cacd414897e400f27e06'),
              'combustible': 'GASOLINA-ELECTRICIDAD',
              'marca': 'FORD',
              'modelo': 'MONDEO HIBRIDO',
              'total': 9},
             {'_id': ObjectId('5da8cacd414897e400f27e08'),
              'combustible': 'DIESEL',
              'marca': 'FORD',
              'modelo': 'FORD TOURNEO CONNECT',
              'total': 8},
             {'_id': ObjectId('5da8cacd414897e400f27e10'),
              'combustible': 'DIESEL',
              'marca': 'FORD',
              'modelo': 'FORD CUSTOM',
              'total': 48},
             {'_id': ObjectId('5da8cacd414897e400f27e1b'),
              'combustible': 'DIESEL',
              'marca': 'FORD',
              'modelo': 'FORD TRANSIT CONNECT',
              'total': 6}],
 'vehiculos': 71}
```
--------------------------------------------------------------
#### **VEHICULOS**: Supresión campos innecesarios en vehículos

Con esta collección podemos trabajar sin problemas pero hay información que no es necesaria en absoluto como son el campo `$_id`y el campo `modelo`. 

```python
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
```

La **supresión de campos** la realizamos con el operador `$unset`, aparentemente debería ser inmediato pero al trabajar con un conjunto grande de elementos utilizamos el método `update_many` que nos permite **actualizar muchos documentos** a la vez. Nos apoyamos del operador `$[]`que ayuda a recorrer los registros existentes en documentos embebidos.

> El resultado de la ejecución en esta ocasión no representa ninguna información

------------------------------------------
#### **VEHICULOS**: 10 primeros documentos

Ahora la información que tenemos es mucho más clara. Podemos observar el conjunto de modelos que tiene cada vehículo, así como el conjunto de vehículos autorizados de cada modelo teniendo en cuenta sus combustibles.

```json
{'_id': 'FORD',
 'modelos': [{'combustible': 'DIESEL',
              'modelo': 'FORD TRANSIT CONNECT',
              'total': 6},
             {'combustible': 'DIESEL', 'modelo': 'FORD CUSTOM', 'total': 48},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'MONDEO HIBRIDO',
              'total': 9},
             {'combustible': 'DIESEL',
              'modelo': 'FORD TOURNEO CONNECT',
              'total': 8}],
 'vehiculos': 71}
{'_id': 'VOLKSWAGEN',
 'modelos': [{'combustible': 'DIESEL',
              'modelo': 'KOMBI CARAVELLE',
              'total': 16},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': 'TRANSPORTER o. CA',
              'total': 2},
             {'combustible': 'DIESEL', 'modelo': 'CADDY', 'total': 9},
             {'combustible': 'GLP / GASOLINA', 'modelo': 'CADDY', 'total': 2},
             {'combustible': 'GASOLINA - GAS NATURAL',
              'modelo': 'CADDY',
              'total': 4},
             {'combustible': 'GASOLINA - GAS NATURAL',
              'modelo': 'PASSAT',
              'total': 1},
             {'combustible': 'GASOLINA', 'modelo': 'CADDY', 'total': 1},
             {'combustible': 'GASOLINA',
              'modelo': 'TRANSPORTER o. CA',
              'total': 2}],
 'vehiculos': 37}
{'_id': 'MERCEDES-BENZ',
 'modelos': [{'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'E200 familiar',
              'total': 1},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': 'VIANO',
              'total': 4},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': '3.5',
              'total': 2},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'E200 berlina',
              'total': 1},
             {'combustible': 'DIESEL', 'modelo': 'VITO TOURER', 'total': 12},
             {'combustible': 'GASOLINA', 'modelo': 'VIANO', 'total': 4},
             {'combustible': 'GASOLINA - GAS NATURAL',
              'modelo': 'E200 NATURAL GAS',
              'total': 2},
             {'combustible': 'GASOLINA', 'modelo': '3.5', 'total': 2},
             {'combustible': 'DIESEL', 'modelo': 'CLASE V220', 'total': 6},
             {'combustible': 'DIESEL-ELECTRICIDAD',
              'modelo': 'E300de berlina',
              'total': 1}],
 'vehiculos': 35}
{'_id': 'TESLA',
 'modelos': [{'combustible': 'ELECTRICO', 'modelo': 'MODEL S', 'total': 21}],
 'vehiculos': 21}
{'_id': 'NISSAN',
 'modelos': [{'combustible': 'ELECTRICO',
              'modelo': 'NISSAN LEAF 40 KWH',
              'total': 2},
             {'combustible': 'ELECTRICO',
              'modelo': 'NISSAN e-NV200',
              'total': 9},
             {'combustible': 'ELECTRICO',
              'modelo': 'NISSAN LEAF 62 KWH',
              'total': 1},
             {'combustible': 'ELECTRICO',
              'modelo': 'NISSAN LEAF 30 kW',
              'total': 2},
             {'combustible': 'ELECTRICO', 'modelo': 'NISSAN LEAF', 'total': 4}],
 'vehiculos': 18}
{'_id': 'TOYOTA',
 'modelos': [{'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'PRIUS PLUS',
              'total': 3},
             {'combustible': 'GASOLINA-ELECTRICIDAD',
              'modelo': 'PRIUS',
              'total': 2},
             {'combustible': 'DIESEL', 'modelo': 'PROACE VERSO', 'total': 4}],
 'vehiculos': 9}
{'_id': 'FIAT',
 'modelos': [{'combustible': 'DIESEL', 'modelo': 'FIAT DOBLO', 'total': 1},
             {'combustible': 'GLP / GASOLINA',
              'modelo': 'FIAT TIPO',
              'total': 2},
             {'combustible': 'DIESEL', 'modelo': 'TALENTO', 'total': 5},
             {'combustible': 'GASOLINA - GAS NATURAL',
              'modelo': 'FIAT DOBLO',
              'total': 1}],
 'vehiculos': 9}
{'_id': 'CITROEN',
 'modelos': [{'combustible': 'GLP / GASOLINA',
              'modelo': 'CITROEN C-ELYSEE eco-glv',
              'total': 8}],
 'vehiculos': 8}
{'_id': 'DACIA',
 'modelos': [{'combustible': 'GLP / GASOLINA', 'modelo': 'LODGY', 'total': 3},
             {'combustible': 'GASOLINA TRANSFORMADO GLP',
              'modelo': 'LODGY',
              'total': 1},
             {'combustible': 'GLP / GASOLINA',
              'modelo': 'LOGAN MCV',
              'total': 2}],
 'vehiculos': 6}
{'_id': 'RENAULT',
 'modelos': [{'combustible': 'DIESEL',
              'modelo': 'RENAULT KANGOO TPMR',
              'total': 1},
             {'combustible': 'DIESEL', 'modelo': 'TRAFIC', 'total': 4}],
 'vehiculos': 5}
```
16 documento/s

### 3.1.4 EJERCICIOS CON VEHICULOS APLANADO

-----------------------------------------
#### **AUTORIZADOS**: Total de documentos

> El resultado de la ejecución en esta ocasión no representa ninguna información

232 documento/s

--------------------------------------------------
#### **VEHICULOS_APLANADO**: Vehículo más comprado

Finalmente la información que más clara podemos obtener es saber cuál es el vehículo más seleccionado por los 232 taxis autorizados en Madrid de los que tenemos información. 

```python
@exercise_decorator("Vehículo más comprado")
@print_elements
def vehiculo_mas_comprado(collection):
    return collection.find({}).sort('total', -1).limit(1)
```

El vehículo más utilizado es el siguiente. Obtenido haciendo una búsqueda entre el total de elementos y **ordenando** con el método `sort`y  **limitando el conjunto de elementos obtenidos** con el método`limit` que podemos concatenar con el método `find`.

```json
{'_id': ObjectId('5da8cc1f414897e400f28055'),
 'combustible': 'DIESEL',
 'marca': 'FORD',
 'modelo': 'FORD CUSTOM',
 'total': 48}
```

