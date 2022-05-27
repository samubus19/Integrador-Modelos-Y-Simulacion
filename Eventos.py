from dataclasses import dataclass
from datetime import datetime, timedelta, date
import Configuracion
import pandas as pd

from ManipulacionArchivos import Manipulador_archivos
class Eventos:
    
    def __init__(self):
        self.data1                  = []
        self.data                   = []
        config                      = Configuracion.Configuracion()
        arreglos                    = config.cargar_ultima_configuracion()
        self.arreglo_eventos        = arreglos[0]
        # print(arreglos[0])
        self.arreglo_variables      = dict(arreglos[1])
        self.intervalo_por_cliente  = timedelta(seconds=self.arreglo_variables['tiempo_llegada'])
        self.duracion_servicio      = timedelta(seconds=self.arreglo_variables['duracion_servicio'])
        self.duracion_descanso      = timedelta(seconds=self.arreglo_variables['duracion_descanso'])
        self.tiempo_trabajo         = timedelta(seconds=self.arreglo_variables['tiempo_trabajo'])
        self.tiempo_abandono        = timedelta(minutes=self.arreglo_variables['tiempo_abandono'])
        self.ps                     = self.arreglo_variables['PS']
        self.cola                   = self.arreglo_variables['Q']
        self.s                      = self.arreglo_variables['S']
        self.hora_actual            = self.convertir_fecha(self.arreglo_variables['hora_actual'])
        self.hora_fin_servicio      = self.convertir_fecha(self.arreglo_variables['hora_fin_servicio'])
        self.hora_llegada_cliente   = self.convertir_fecha(self.arreglo_variables['hora_llegada'])
        self.hora_comienzo_descanso = self.convertir_fecha(self.arreglo_variables['hora_comienzo_descanso'])
        self.hora_vuelta_trabajo    = self.convertir_fecha(self.arreglo_variables['hora_vuelta_trabajo'])
        self.hora_abandono          = self.convertir_fecha(self.arreglo_variables['hora_abandono'])
        self.horas_abandono         = [] 
        
        #* Flags
        self.hora_fin_servicio_flag      = True
        self.hora_comienzo_descanso_flag = True
        self.hora_vuelta_trabajo_flag    = True
        self.hora_abandono_flag          = True
         
    def simular(self):
        for i in self.arreglo_eventos:
            self.data.append([self.convertir_fecha(i['hora']), 
                         i['nombreEvento']])
            
        # if (self.hora_comienzo_descanso == '-----' or self.hora_comienzo_descanso == self.convertir_fecha('23:59:59') ):
        #     self.hora_comienzo_descanso_flag = False
        #     self.hora_vuelta_trabajo_flag = True
        # else:
        #     self.hora_comienzo_descanso_flag = True
        #     self.hora_vuelta_trabajo_flag = False

        for i in range(509):
 
            
            hora_lleg_cliente_aux      = ('-----' if self.hora_llegada_cliente   == '-----' else self.hora_llegada_cliente.time() )
            hora_fin_servicio_aux      = ('-----' if self.fin_de_servicio        == '-----' or not self.hora_fin_servicio_flag else self.hora_fin_servicio.time())
            hora_comienzo_descanso_aux = ('-----' if self.hora_comienzo_descanso == '-----' or not self.hora_comienzo_descanso_flag else self.hora_comienzo_descanso.time())
            hora_vuelta_trabajo_aux    = ('-----' if self.hora_vuelta_trabajo    == '-----' or not self.hora_vuelta_trabajo_flag else self.hora_vuelta_trabajo.time())
            hora_abandono_aux          = ('-----' if self.hora_abandono          == '-----' or not self.hora_abandono_flag else self.hora_abandono.time())

            
            self.data1.append(
                [self.hora_actual.time(),
                 hora_lleg_cliente_aux,
                 hora_fin_servicio_aux,
                 hora_comienzo_descanso_aux,
                 hora_vuelta_trabajo_aux,
                 hora_abandono_aux,
                 self.cola,
                 self.ps,
                 self.s
                 ]
            ) 
            
            hora_minima = self.obtener_minimo(self.data)

            if(hora_minima[1] == 'llegada_cliente'):
                self.llegada_cliente()

            if(hora_minima[1] == 'fin_servicio'):
                self.fin_de_servicio()
                
            if(hora_minima[1] == 'comienzo_descanso'):
                self.comienzo_descanso()
            
            if(hora_minima[1] == 'vuelta_trabajo'):
                self.vuelta_al_trabajo()
            
            if(hora_minima[1] == 'abandono_cola'):
                self.abandono_de_cola()

        my_dataframe = pd.DataFrame(self.data1, columns=['Hs Actual', 'Hs Llegada', 'Hora Fin', 'Hs ini descanso', 'Hs ini trabajo', 'Hs abandono' ,'Q', 'PS', 'S'])
        print(my_dataframe)
        manipulador_archivos = Manipulador_archivos().exportar_resultado(my_dataframe)

        
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
            if self.comprobar_evento_abandono_cola():
                self.horas_abandono.append(self.hora_llegada_cliente + self.tiempo_abandono)
                
                self.hora_abandono = self.horas_abandono[0]
                self.data[4] = [self.hora_abandono, 'abandono_cola']
        
        self.hora_llegada_cliente  += self.intervalo_por_cliente
        self.data[0] = [self.hora_llegada_cliente, 'llegada_cliente']
        self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
        self.hora_fin_servicio_flag = True
         
                
    def fin_de_servicio(self):
        self.hora_actual            = self.hora_fin_servicio
        self.ps = 0
        if(self.cola > 0):
            self.ps                 = 1
            self.cola              -= 1
            self.hora_fin_servicio += self.duracion_servicio
            self.data[1] = [self.hora_fin_servicio, 'fin_servicio']
            if self.comprobar_evento_abandono_cola():
                if(len(self.horas_abandono) > 0):
                    self.horas_abandono.remove(self.horas_abandono[0])
                    if(len(self.horas_abandono) > 0):
                        self.hora_abandono = self.horas_abandono[0]
                        self.data[4]       = [self.hora_abandono, 'abandono_cola']
        else:
            #? Preguntar que hacer con la hora de fin de servicio
            #? le asgino un valor grande a hora de fin de servicio para que se ejecute el otro evento
            self.hora_fin_servicio      += timedelta(hours=10)
            self.hora_fin_servicio_flag  = False
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
        self.hora_comienzo_descanso_flag = False
        self.hora_vuelta_trabajo_flag    = True
        self.data[2] = [self.hora_comienzo_descanso, 'comienzo_descanso']
        
    def vuelta_al_trabajo(self):
        self.hora_actual               = self.hora_vuelta_trabajo
        self.s                         = 1   
        # self.duracion_trabajo          = datetime.timedelta(seconds=random.randint(self.intervalo_duracion_trabajo_min, self.intervalo_duracion_trabajo_max)) 
        self.hora_comienzo_descanso    = self.hora_actual + self.tiempo_trabajo
        self.data[2] = [self.hora_comienzo_descanso, 'comienzo_descanso']
        self.hora_vuelta_trabajo      += timedelta(hours=10)
        self.hora_comienzo_descanso_flag = True
        self.hora_vuelta_trabajo_flag    = False
        self.data[3] = [self.hora_vuelta_trabajo, 'vuelta_trabajo']
    
    def abandono_de_cola(self):
        self.hora_actual = self.hora_abandono
        self.cola       -= 1
        if(len(self.horas_abandono) > 0):
            self.horas_abandono.remove(self.horas_abandono[0])
            if(len(self.horas_abandono) > 0):
                self.hora_abandono = self.horas_abandono[0]    
                self.data[4]       = [self.hora_abandono, 'abandono_cola']        
        
    def convertir_fecha(self, fecha_string):
        if(fecha_string == '-----'):
            return fecha_string
        return datetime.combine(date.today(), datetime.strptime(fecha_string, '%H:%M:%S').time()) 

    def comprobar_evento_abandono_cola(self):
        for evento in self.data:
             if evento[1] == 'abandono_cola' and evento[0] != '-----':
                 return True
        return False
    
    def obtener_minimo(self, datos):
        aux = []
        for dato in datos:
            if(dato[0] != '-----'):
               aux.append(dato) 
        minimo = min(aux)
        return minimo