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

# PASOS
1. Conexion al rss de taxi
1. Obtención de los csv
1. Parseo a json
1. Generación de las colecciones