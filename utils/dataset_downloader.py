from mongo.utils.utils import download_json, download_csv, csv_to_json
from mongo.utils.mongo import connect, bulk_file_import
import pdb

def incidences_download():
    """
    Dataset of incidences downloader
    :return: list of tuples ('database', 'collection') imported
    """
    link_json = 'https://datosabiertos.jcyl.es/web/jcyl/risp/es/transporte/incidencias_carreteras/1284212099243.json'

    json_path = download_json(link_json)
    c = connect('datos_abiertos', 'incidencias')
    bulk_file_import(c, json_path)

    return [('datos_abiertos', 'incidencias')]


def taxi_donwload():
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
        json_path = csv_to_json(download_csv(csv_link))
        json_paths[key] = json_path

    # Bulk Import of json files
    for key, json_path in json_paths.items():
        c = connect('practica', key)
        bulk_file_import(c, json_path)

    return [('practica', key) for key in json_paths.keys()]













