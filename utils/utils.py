import requests
import codecs
import csv
import json
import os
import pdb
import urllib
import urllib.request


def download_csv(link_csv):

    filename = os.path.basename(link_csv)
    file_path = get_csv_path(filename)
    urllib.request.urlretrieve(link_csv, file_path)
    print("CSV downloaded!!!")
    return file_path


def download_json(link_json):

    filename = os.path.basename(link_json)
    file_path = get_json_path(filename)
    urllib.request.urlretrieve(link_json, file_path)
    print("JSON downloaded!!!")
    return file_path


def csv_to_json(csv_path):
    """
    Parse csv files to json and save on /mongo/static/json/
    :param csv_path: path with csv
    :return: path of json
    """
    # Open the CSV
    csv_file = open(csv_path, 'rU', encoding='utf-8')

    #TODO: CORREGIR POR QUÉ NO PUEDO ABRIR EL PUTO CSV
    reader = csv.DictReader(csv_file)

    # Parse the CSV into JSON
    out = json.dumps([row.decode('utf-8') for row in reader])
    print("JSON parsed!")

    pdb.set_trace()

    # Save the JSON
    path_to_parsed_json = get_json_path(os.path.basename(csv_path).replace('csv', 'json'))
    f = open(path_to_parsed_json, 'w', encoding='utf-8')
    f.write(out)
    print("JSON saved!")

    return path_to_parsed_json


def get_csv_path(file):
    return _get_path(file, 'csv')


def get_json_path(file):
    return _get_path(file, 'json')


def _get_path(file, folder):
    path = os.path.join(os.getcwd().replace('projects', 'static'), folder)
    file_json = os.path.join(path, str(file))
    return file_json
