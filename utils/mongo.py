from pymongo import MongoClient
import json


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
    collection.insert_one(file_data)


