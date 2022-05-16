from dataclasses import dataclass
from datetime import datetime, timedelta, date
import Configuracion
import pandas as pd

from ManipulacionArchivos import Manipulador_archivos
class Eventos:
    
    def __init__(self):
        self.data1 = []
        self.data                 = []
        config                     = Configuracion.Configuracion()
        arreglos                   = config.cargar_ultima_configuracion()
        self.arreglo_eventos       = arreglos[0]
        self.arreglo_variables     = dict(arreglos[1])
        self.intervalo_por_cliente = timedelta(seconds=self.arreglo_variables['tiempo_llegada'])
        self.duracion_servicio     = timedelta(seconds=self.arreglo_variables['duracion_servicio'])
        self.duracion_descanso     = timedelta(seconds=self.arreglo_variables['duracion_descanso'])
        self.tiempo_trabajo        = timedelta(seconds=self.arreglo_variables['tiempo_trabajo'])
        self.ps                    = self.arreglo_variables['PS']
        self.cola                  = self.arreglo_variables['Q']
        self.s                     = self.arreglo_variables['S']
        self.hora_actual           = self.convertir_fecha(self.arreglo_variables['hora_actual'])
        self.hora_fin_servicio     = self.convertir_fecha(self.arreglo_variables['hora_fin_servicio'])
        self.hora_llegada_cliente  = self.convertir_fecha(self.arreglo_variables['hora_llegada'])
        self.hora_comienzo_descanso  = self.convertir_fecha(self.arreglo_variables['hora_comienzo_descanso'])
        self.hora_vuelta_trabajo  = self.convertir_fecha(self.arreglo_variables['hora_vuelta_trabajo'])
     
        
    def simular(self):
        
        for i in self.arreglo_eventos:
            self.data.append([self.convertir_fecha(i['hora']), 
                         i['nombreEvento']])
            
        for i in range(50):
            
            self.data1.append(
                [self.hora_actual.time(),
                 self.hora_llegada_cliente.time(),
                 self.hora_fin_servicio.time(),
                 self.hora_comienzo_descanso.time(),
                 self.hora_vuelta_trabajo.time(),
                 self.cola,
                 self.ps,
                 self.s]
            )
            
            # print("data: ", self.data1[0::3])
            hora_minima = min(self.data)
            print('data: ', self.data)
            # print('min: ', hora_minima)
            
            # print("if: ", i)
            if(hora_minima[1] =='llegada_cliente'):
                # print("id: ", i)
                self.llegada_cliente()

            if(hora_minima[1] =='fin_servicio'):
                self.fin_de_servicio()
                
            if(hora_minima[1] =='comienzo_descanso'):
                self.comienzo_descanso()
            
            if(hora_minima[1] =='vuelta_trabajo'):
                self.vuelta_al_trabajo()

        my_dataframe = pd.DataFrame(self.data1, columns=['Hs Actual', 'Hs Llegada', 'Hora Fin', 'Hs ini descanso', 'Hs ini trabajo' ,'Q', 'PS', 'S'])
        print(my_dataframe)
        manipulador_archivos = Manipulador_archivos().exportar_resultado(my_dataframe)



# #SERAN LAS HORAS Y MINS DE TRABAJO A REALIZARSE
# horas_salida = datetime.timedelta(hours=7,minutes=30)
# #OBTENEMOS UN OBJETO DATETIME DE LA SUMA DE LAS HORAS DE TRABAJO A REALIZARSE A LA HORA DE ENTRADA 
# salida = hora_entrada + horas_salida


        
    def llegada_cliente(self):
        self.hora_actual            = self.hora_llegada_cliente
        if self.ps == 0:
            self.ps                 = 1
            if self.s == 0:
                self.hora_fin_servicio  =  self.hora_vuelta_trabajo + self.duracion_servicio
            else:
                self.hora_fin_servicio  = self.hora_llegada_cliente + self.duracion_servicio
        else:
            self.cola              += 1
        
        self.hora_llegada_cliente  += self.intervalo_por_cliente
        self.data[0] = [self.hora_llegada_cliente, 'llegada_cliente']
        self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
       
        
    def fin_de_servicio(self):
        self.hora_actual            = self.hora_fin_servicio
        self.ps = 0
        if(self.cola > 0):
            self.ps                 = 1
            self.cola              -= 1
            self.hora_fin_servicio += self.duracion_servicio
            self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
        else:
            #? Preguntar que hacer con la hora de fin de servicio
            #? le asgino un valor grande a hora de fin de servicio para que se ejecute el otro evento
            self.hora_fin_servicio  += timedelta(hours=10)
            self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
            
    def comienzo_descanso(self):
        
        self.hora_actual               = self.hora_comienzo_descanso
        self.s                         = 0
        # self.duracion_descanso         = datetime.timedelta(seconds=self.arreglo_variables['duracion_descanso']) 
        self.hora_vuelta_trabajo       = self.hora_comienzo_descanso + self.duracion_descanso
        self.data[3] = [self.hora_vuelta_trabajo, 'vuelta_trabajo']
        if self.ps != 0:
            self.hora_fin_servicio    += self.duracion_descanso
            self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
        self.hora_comienzo_descanso   += timedelta(hours=10)
        self.data[2] = [self.hora_comienzo_descanso, 'comienzo_descanso']
        
    def vuelta_al_trabajo(self):
        self.hora_actual               = self.hora_vuelta_trabajo
        self.s                         = 1   
        # self.duracion_trabajo          = datetime.timedelta(seconds=random.randint(self.intervalo_duracion_trabajo_min, self.intervalo_duracion_trabajo_max)) 
        self.hora_comienzo_descanso    = self.hora_actual + self.tiempo_trabajo
        self.data[2] = [self.hora_comienzo_descanso, 'comienzo_descanso']
        self.hora_vuelta_trabajo      += timedelta(hours=10)
        self.data[3] = [self.hora_vuelta_trabajo, 'vuelta_trabajo']
    
    def convertir_fecha(self, fecha_string):
        return datetime.combine(date.today(), datetime.strptime(fecha_string, '%H:%M:%S').time())  