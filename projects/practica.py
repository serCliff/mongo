from mongo.utils.mongo import connect, bulk_file_import
from mongo.utils.incidences_downloader import donwload_json
from pprint import pprint
import pdb


def reset_database():
    file = donwload_json()
    c = connect('practica', 'incidencias')
    c.drop()
    bulk_file_import(c, file)

def operation1():
    pass


if __name__ == "__main__":
    reset_database()
