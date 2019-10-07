from mongo.utils.mongo import connect
from mongo.utils.dataset_downloader import taxi_donwload, incidences_download
from pprint import pprint
import pdb


def reset_database():

    mas_cuestiones = 'https://datos.gob.es/en/catalogo/l01280796-taxi-tarifas-suplementos-municipios-paradas-eventuales-regimen-de-descanso-y-duracion-del-servicio'

    res = taxi_donwload()
    # res = incidences_download()


def operation1():
    pass


if __name__ == "__main__":
    reset_database()

