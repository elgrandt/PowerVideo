
from key import *

#---- Los master admins ---#
master_admins = [ "arielnowik" ]

activar_filtro_horario = False

palabra_clave_prender = "activar"
palabra_clave_apagar  = "desactivar"
palabra_clave_admin   = "lo quiero ya"
palabra_clave_malo    = "sacalo"
cantidad_malo         = 2 #minima cantidad de malos mensajes para abortar

margen_cargar         = 20 #en segundos

usuario               = "arielnowik"


#---- Disponibilidad horaria ---#
horarios_disponibles = [  \
                        ( (7 ,30) , ( 7,45) ), \
                        ( (8 ,05) , ( 9,20) ), \
                        ( (10,40) , (10,55) ), \
                        ( (12,15) , ( 1,10) ), \
                        ( (14 ,30), (14,40) ), \
                        ( (16,00) , (16,10) ), \
                        ( (17,30) , (24,00) ), \
                        ]
