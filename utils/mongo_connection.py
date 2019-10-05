from pymongo import MongoClient


def connect(db, collection, host='localhost', port=27017, username=None, password=None):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db][collection]