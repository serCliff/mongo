import requests
import os
import pdb


def get_json_path(file):
    path = os.path.join(os.getcwd().replace('projects', 'static'), 'json')
    file_json = os.path.join(path, str(file))
    return file_json


def donwload_json():
    # TODO: DEscargar estos csv parsear a json y sacar las operaciones disponibles
    reservas_paradas = 'https://datos.madrid.es/egob/catalogo/208094-1-reserva-paradas-taxis.csv'
    autorizados = 'https://datos.madrid.es/egob/catalogo/207347-1-taxi-modelo-vehiculos.csv'
    o_perdidos = 'https://datos.madrid.es/egob/catalogo/300224-0-taxi-objetos-perdidos.csv'
    tarifas = 'https://datos.madrid.es/egob/catalogo/300171-0-taxi-recursos.csv'
    flota = 'https://datos.madrid.es/egob/catalogo/300226-1-taxi-flota-diaria.xls'
    mas_cuestiones = 'https://datos.gob.es/en/catalogo/l01280796-taxi-tarifas-suplementos-municipios-paradas-eventuales-regimen-de-descanso-y-duracion-del-servicio'
    link_json = ''
    r = requests.get(link_json, allow_redirects=True)
    # Create the file
    file_path = get_json_path()
    open(file_path, 'wb').write(r.content)
    return file_path

