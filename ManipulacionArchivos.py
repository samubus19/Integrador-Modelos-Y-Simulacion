import json
import os
class Manipulador_archivos:
    
    def __init__(self):
        pass
        
    def leer_json(self):
        archivo_json = {}
        ruta_archivo = os.path.join(os.getcwd(), os.path.join('pruebas', 'prueba.json'))
        with open(ruta_archivo, 'r') as file:
            archivo_json = json.load(file)
        return archivo_json
        




