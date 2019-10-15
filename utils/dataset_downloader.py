from mongo.utils.utils import download_json, download_csv, download_zip, csv_to_json, get_json_path, get_zip_path
from mongo.utils.mongo import connect, bulk_file_import, bulk_file_mongoimport
import zipfile
import os
import pdb


def twitter_download():
    """
    Dataset of twitter downloader
    :return: list of tuples ('database', 'collection') imported
    """
    link_zip = 'https://drive.google.com/uc?export=download&id=1aqZUFkAm1EW9H8skKnhfAeAhIO28TZjl'
    json_path = get_json_path('twitter.json')

    zip_path = download_zip(link_zip)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(get_json_path())

    c = connect('clase', 'twitter')
    c.drop()
    bulk_file_mongoimport(c, json_path)

    return [('clase', 'twitter')]


def restaurants_download():
    """
    Dataset of restaurants downloader
    :return: list of tuples ('database', 'collection') imported
    """
    link_zip = 'https://drive.google.com/uc?export=download&id=1qUgzM5JHvnH2d1Ayh8oES9BIZPj03Nol'
    json_path = get_json_path('restaurants.json')

    zip_path = download_zip(link_zip)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(get_json_path())

    c = connect('clase', 'restaurant')
    c.drop()
    bulk_file_mongoimport(c, json_path)

    return [('clase', 'restaurant')]


def full_primer_dataset_download():
    """
    Dataset of full_primer-dataset downloader
    :return: list of tuples ('database', 'collection') imported
    """
    link_zip = 'https://drive.google.com/uc?export=download&id=1WswYNzSv-R7ultIs7CB-xsO9WepT-YQT'
    json_path = get_json_path('full_primer-dataset.json')

    zip_path = download_zip(link_zip)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(get_json_path())

    c = connect('clase', 'primer')
    c.drop()
    bulk_file_mongoimport(c, json_path)

    return [('clase', 'primer')]


def incidences_download():
    """
    Dataset of incidences downloader
    :return: list of tuples ('database', 'collection') imported
    """
    link_json = 'https://datosabiertos.jcyl.es/web/jcyl/risp/es/transporte/incidencias_carreteras/1284212099243.json'

    json_path = download_json(link_json)
    c = connect('datos_abiertos', 'incidencias')
    c.drop()
    bulk_file_import(c, json_path)

    return [('datos_abiertos', 'incidencias')]


def taxi_download(download=True):
    """
    Donwload taxi files
    :return: list of tuples ('database', 'collection') imported
    """

    csv_paths = dict()
    json_paths = dict()
    csv_links = dict({
        'reserva_paradas': 'https://datos.madrid.es/egob/catalogo/208094-1-reserva-paradas-taxis.csv',
        'autorizados': 'https://datos.madrid.es/egob/catalogo/207347-1-taxi-modelo-vehiculos.csv',
        'objetos_perdidos': 'https://datos.madrid.es/egob/catalogo/300224-0-taxi-objetos-perdidos.csv',
        'tarifas': 'https://datos.madrid.es/egob/catalogo/300171-0-taxi-recursos.csv',
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













