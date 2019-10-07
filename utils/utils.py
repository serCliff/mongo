import pandas as pd
import csv
import json
import os
import pdb
import urllib
import urllib.request
import requests


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


def get_csv_path(file):
    return _get_path(file, 'csv')


def get_json_path(file):
    return _get_path(file, 'json')


def _get_path(file, folder):
    path = os.path.join(os.getcwd().replace('projects', 'static'), folder)
    file_json = os.path.join(path, str(file))
    return file_json


def repair_dict_keys(dict_frame):
    """
    Repair keys corrections to be useful to mongod
    :param dict_frame: frame to be repaired
    :return: same dict_frame corrected
    """

    def dict_correction(dict_for_correction):
        new_dict_frame = dict()
        for key, value in dict_for_correction.items():
            new_dict_frame[key.replace('.', '')] = value
        return new_dict_frame

    if isinstance(dict_frame, list):
        returned_value = list()
        for dict_value in dict_frame:
            returned_value.append(dict_correction(dict_value))
        return returned_value
    else:
        return dict_correction(dict_frame)
