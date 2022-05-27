import ManipulacionArchivos

class Configuracion:
    def __init__(self) -> None:
        self.arreglo_eventos = []
        self.datos_json      = {}
        self.variables       = []
        
    def cargar_ultima_configuracion(self):
        manipulador_archivos = ManipulacionArchivos.Manipulador_archivos()
        self.datos_json      = manipulador_archivos.leer_json()
        self.variables       = self.datos_json['variables']
        
        self.arreglo_eventos.clear()
        # Preguntar si quiere leer de un archivo o ingresar a mano
        a = input("Quiere repetir la última simulación? s/n: ")
        if(a == 's'):
            if(self.datos_json['eventos']['llegada_cliente']):
                self.arreglo_eventos.append({
                    'nombreEvento': 'llegada_cliente',
                    'tiempo'      : self.datos_json['variables']['tiempo_llegada'],
                    'hora'        : self.datos_json['variables']['hora_llegada']})
            else:
                self.arreglo_eventos.append({
                    'nombreEvento': 'llegada_cliente',
                    'tiempo'      : '-----',
                    'hora'        : '-----'})
                self.variables['hora_llegada'] = '-----'
                
            if(self.datos_json['eventos']['fin_servicio']):
                self.arreglo_eventos.append({
                    'nombreEvento' : 'fin_servicio',
                    'tiempo'       : self.datos_json['variables']['duracion_servicio'],
                    'hora'         : self.datos_json['variables']['hora_fin_servicio']})
            else:
                self.arreglo_eventos.append({
                    'nombreEvento': 'fin_servicio',
                    'tiempo'      : '-----',
                    'hora'        : '-----'})
                self.variables['hora_fin_servicio'] = '-----'
           
            if(self.datos_json['eventos']['comienzo_descanso']):
                self.arreglo_eventos.append({
                    'nombreEvento' : 'comienzo_descanso',
                    'tiempo'       : self.datos_json['variables']['duracion_descanso'],
                    'hora'         : self.datos_json['variables']['hora_comienzo_descanso']})
            else:
                self.arreglo_eventos.append({
                    'nombreEvento': 'comienzo_descanso',
                    'tiempo'      : '-----',
                    'hora'        : '-----'})
                self.variables['hora_comienzo_descanso'] = '-----'
                
            if(self.datos_json['eventos']['vuelta_trabajo']):
                self.arreglo_eventos.append({
                    'nombreEvento' : 'vuelta_trabajo',
                    'tiempo'       : self.datos_json['variables']['tiempo_trabajo'],
                    'hora'         : self.datos_json['variables']['hora_vuelta_trabajo']})
            else:
                self.arreglo_eventos.append({
                    'nombreEvento': 'vuelta_trabajo',
                    'tiempo'      : '-----',
                    'hora'        : '-----'})
                self.variables['hora_vuelta_trabajo'] = '-----'
                
            if(self.datos_json['eventos']['abandono_cola']):
                self.arreglo_eventos.append({
                    'nombreEvento' : 'abandono_cola',
                    'tiempo'       : self.datos_json['variables']['tiempo_abandono'],
                    'hora'         : self.datos_json['variables']['hora_abandono']})
            else:
                self.arreglo_eventos.append({
                    'nombreEvento': 'abandono_cola',
                    'tiempo'      : '-----',
                    'hora'        : '-----'})
                self.variables['hora_abandono'] = '-----'
                
                
            return [self.arreglo_eventos, self.variables]
            
        

    
