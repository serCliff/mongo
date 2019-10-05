import csv
import json
import os
import pdb


def parse_to_json(csv_path):
    """
    Parse csv files to json and save on /mongo/static/json/
    :param csv_path: path with csv
    :return: path of json
    """
    # Open the CSV
    f = open(csv_path, 'rU')
    pdb.set_trace()
    # Change each fieldname to the appropriate field name. I know, so difficult.
    reader = csv.DictReader(f, fieldnames=("fieldname0", "fieldname1", "fieldname2", "fieldname3"))

    # Parse the CSV into JSON
    out = json.dumps([row for row in reader])
    print("JSON parsed!")

    # Save the JSON
    path_to_parsed_json = '/path/to/parsed.json'
    f = open(path_to_parsed_json, 'w')
    f.write(out)
    print("JSON saved!")

    return path_to_parsed_json
