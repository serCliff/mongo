import requests
import os
import pdb


def get_json_path():
    path = os.path.join(os.getcwd().replace('projects', 'static'), 'json')
    file_json = os.path.join(path, 'incidencias_carreteras.json')
    return file_json


def donwload_json():
    link_json = 'https://datosabiertos.jcyl.es/web/jcyl/risp/es/transporte/incidencias_carreteras/1284212099243.json'
    r = requests.get(link_json, allow_redirects=True)
    # Create the file
    file_path = get_json_path()
    open(file_path, 'wb').write(r.content)
    return file_path

