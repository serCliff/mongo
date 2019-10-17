# PRACTICA BASES DE DATOS NO SQL MASTER - BIG DATA & BLOCKCHAIN

### ÍNDICE

1. [ Descripción ](#desc)
1. [ Requisitos ](#requirements)
1. [ Instalación ](#installation)
1. [ Estructura ](#structure)
1. [ Proyectos ](#projects)


<a name="desc"></a>
## DESCRIPCIÓN

Proyecto creado con objeto de manejar bases de datos para mongo desde
python.

<a name="requirements"></a>
## REQUISITOS
Para poder utilizar este proyecto lo único que se necesita es tener una
máquina que pueda ejecutar scripts de python3. 

No obstante el tutorial está enfocado en ser utilizado con: 
- Ubuntu 18.04
- Python 3.6


<a name="installation"></a>
## INSTALACIÓN

Instalación de paquetes necesarios para poder trabajar con este
proyecto.
```
sudo apt-get udate && sudo apt-get upgrade -y 
sudo apt-get install python3 python3-pip -y
```

Instalación de módulos de python requeridos. 
``` 
sudo pip install -r requirements.txt
```


<a name="structure"></a>
## ESTRUCTURA

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


<a name="projects"></a>
## PROYECTOS

### ej1-6_*.py
Ejercicios realizados en clase

### practica.py
Ejercicios generados para resolver los requisitos de la práctica. [Más
info aquí.](https://github.com/serCliff/mongo/blob/master/static/documentation/practica.md)

