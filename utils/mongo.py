from pymongo import MongoClient
from mongo.utils.utils import repair_dict_keys
import json
import os


def connect(db, collection, host='localhost', port=27017, username=None, password=None):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db][collection]


def bulk_file_import(collection, json_path):
    """
    Make a bulk import of a json in a collection
    :param collection: Collection where you want to import
    :param json_path: Path where the json was located
    """
    with open(json_path, encoding='utf-8') as f:
        file_data = json.load(f)

    if isinstance(file_data, list):
        collection.insert_many(repair_dict_keys(file_data))
    else:
        collection.insert_one(repair_dict_keys(file_data))
    print("Imported file: {0}!!!".format(os.path.basename(json_path)))


def bulk_file_mongoimport(collection, json_path):
    """
    Make a bulk import of a json in a collection
    :param collection: Collection where you want to import
    :param json_path: Path where the json was located
    """
    db = collection.database
    host = db.client.address[0]
    port = db.client.address[1]
    command = 'mongoimport ' \
              '--db {0} ' \
              '--collection {1} ' \
              '--host {2} ' \
              '--port {3} ' \
              '--type json ' \
              '--drop ' \
              '--stopOnError ' \
              '--file {4}'.format(db.name, collection.name, host, port, json_path)
    os.system(command)
    print("Imported file: {0}!!!".format(os.path.basename(json_path)))


