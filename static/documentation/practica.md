# DATOS DE LA PRÁCTICA 1
En la siguiente web podremos obtener datos sobre los taxis de madrid

[TAXIS MADRID](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=4f16216612d39410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

[OTRA WEB](https://datos.gob.es/en/catalogo/l01280796-taxi-tarifas-suplementos-municipios-paradas-eventuales-regimen-de-descanso-y-duracion-del-servicio)


## TAREAS
1. Obtener datos en json
1. Crear varias colecciones en las que se muestren
    - Instrucciones sobre que son cada uno de los datos
    - Creación de las colecciones con los diferentes datos
    - Obtención de información sobre el estado actual de los taxis
    - Obtención en tiempo real sobre los taxis
    - Concatenación de la información entre las diferentes colecciones
    - Buscar la necesidad de generar unwinds y generar otras tablas, trabajar con ellas y suprimirlas en tiempo real
1. Generar información en otra base de datos que se vaya actualizando constantemente (RSS)
1. Crear un replicaset [INFO!!](https://github.com/serCliff/master_mongo/blob/master/static/documentation/replicaset.md)

# 1. EJECUCIÓN DE LA PRÁCTICA
Para realizar la ejecución y comprobación de la información se realiza
con el siguiente comando: 
```bash
python -m mongo
```
> Recuerda que python tiene que estar en la versión 3.6

# 2. MENÚ DE OPCIONES

# 3. EJECUCIÓN DE LA PRÁCTICA
Tras seleccionar la ejecución de la práctica 1 lo primero que hace es
descargarse los csv, transformarlos a json y a continuación los importa
en la base de datos mongo
```
Imported file: 208094-1-reserva-paradas-taxis.json!!!
Imported file: 207347-1-taxi-modelo-vehiculos.json!!!
Imported file: 300224-0-taxi-objetos-perdidos.json!!!
Imported file: 300171-0-taxi-recursos.json!!!
Imported file: 300226-0-taxi-flota-diaria.json!!!
```

## 3.1 OPERACIONES

### 3.1.2 CORRECCIÓN DE LAS BASES DE DATOS
Ejecuta unos cuantos métodos para corregir la base de datos

-------------------------------------------------
[flota]: Suprimir documento con combustible -> NO



----------------------------
[flota]: Total de documentos


15622 documento/s

---------------------------------------------------------------------------
[flota]: Añadir tiempo que tardan en dar la licencia desde la matriculaciOn


-------------------------------------------------
[flota]: Media obtenciOn licencia por combustible
```json
{'Media': 17.78048780487805, 'Total': 205, '_id': 'GASOLINA TRANSFORMADO GLP'}
{'Media': 84.45687148672224, 'Total': 5159, '_id': 'GASOLINA-ELECTRICIDAD'}
{'Media': 62.0, 'Total': 1, '_id': 'DIESEL TRANSFORMADO A GLP'}
{'Media': 26.03846153846154, 'Total': 26, '_id': 'ELECTRICO'}
{'Media': 32.05926860025221, 'Total': 793, '_id': 'GASOLINA - GAS NATURAL'}
{'Media': 3.6, 'Total': 5, '_id': 'GASOLINA'}
{'Media': 18.75031017369727, 'Total': 3224, '_id': 'GLP / GASOLINA'}
{'Media': 16.332903641637124, 'Total': 6206, '_id': 'DIESEL'}
{'Media': 15.0, 'Total': 3, '_id': None}
```