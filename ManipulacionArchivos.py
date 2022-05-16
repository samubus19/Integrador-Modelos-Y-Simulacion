import json
from operator import index
import os
import pandas as pd
class Manipulador_archivos:
    
    def __init__(self):
        pass
        
    def leer_json(self):
        archivo_json = {}
        ruta_archivo = os.path.join(os.getcwd(), os.path.join('pruebas', 'prueba.json'))
        with open(ruta_archivo, 'r') as file:
            archivo_json = json.load(file)
        return archivo_json
    
    def exportar_resultado(self, dataframe):
        dataframe.to_excel('resultado.xlsx')
        dataframe.to_csv('resultado.csv', index=False, sep='-')
        




