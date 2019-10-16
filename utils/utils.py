import pandas as pd
import json
import os
import pdb
import urllib
import urllib.request
from unidecode import unidecode


def download_zip(link_zip):

    filename = os.path.basename(link_zip)
    file_path = get_zip_path(filename)
    urllib.request.urlretrieve(link_zip, file_path)
    print("ZIP downloaded: {0}".format(filename))
    return file_path


def download_csv(link_csv):

    filename = os.path.basename(link_csv)
    file_path = get_csv_path(filename)
    urllib.request.urlretrieve(link_csv, file_path)
    print("CSV downloaded: {0}".format(filename))
    return file_path


def download_json(link_json):

    filename = os.path.basename(link_json)
    file_path = get_json_path(filename)
    urllib.request.urlretrieve(link_json, file_path)
    print("JSON downloaded: {0}".format(filename))
    return file_path


def csv_to_json(csv_path):
    """
    Parse csv files to json and save on /mongo/static/json/
    :param csv_path: path with csv
    :return: path of json
    """
    csv_filename = os.path.basename(csv_path)
    json_filename = csv_filename.replace('csv', 'json')

    # Download and parse the CSV into JSON
    out = pd.read_csv(csv_path, header=0, sep=";", encoding='latin1').reset_index().to_json(orient='records')
    json_document = json.loads(out)
    json_str = json.dumps(json_document)

    # Save the JSON
    path_to_parsed_json = get_json_path(json_filename)
    f = open(path_to_parsed_json, 'w', encoding='utf-8')
    f.write(json_str)

    print("CSV parsed to JSON {0} -> {1}\n".format(csv_filename, json_filename))
    return path_to_parsed_json


def get_zip_path(file=None):
    return _get_path('zip', file)


def get_csv_path(file=None):
    return _get_path('csv', file)


def get_json_path(file=None):
    return _get_path('json', file)


def _get_path(folder, file=None):
    current_path = os.path.realpath(__file__)
    current_dir = os.path.dirname(current_path)
    path = os.path.join(current_dir.replace('utils', 'static'), folder)
    if not os.path.exists(path):
        os.makedirs(path)
    if file:
        path = os.path.join(path, str(file))
    return path


def repair_dict_keys(dict_frame):
    """
    Repair keys corrections to be useful to mongod
    :param dict_frame: frame to be repaired
    :return: same dict_frame corrected
    """

    def dict_correction(dict_for_correction):
        new_dict_frame = dict()
        for key, value in dict_for_correction.items():
            new_key = key
            new_key = new_key.replace('.', '')  # Remove dots
            new_key = new_key.replace(' ', '_')  # Remove spaces
            new_key = new_key.replace(' ', '_')  # Remove spaces
            new_key = unidecode(new_key).lower()  # Remove spanish data and get lower cased
            new_dict_frame[new_key] = value
        return new_dict_frame

    if isinstance(dict_frame, list):
        returned_value = list()
        for dict_value in dict_frame:
            returned_value.append(dict_correction(dict_value))
        return returned_value
    else:
        return dict_correction(dict_frame)
