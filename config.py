
from key import *

#---- Los master admins ---#
master_admins = [ "arielnowik" ]

activar_filtro_horario = True

palabra_clave_prender = "activar"
palabra_clave_apagar  = "desactivar"
palabra_clave_admin   = "lo quiero ya"
palabra_clave_malo    = "sacalo"
cantidad_malo         = 2 #minima cantidad de malos mensajes para abortar

margen_cargar         =33333333333333333344444444

usuario               = "" 
goautofullscreen      = False

#---- Disponibilidad horaria ---#
horarios_disponibles = [
( (2 ,2) , (2,3) ),
( (9 ,5) , (9,20) ),
( (10 ,40) , (10,55) ),
( (12 ,15) , (1,10) ),
( (14 ,30) , (14,40) ),
( (16 ,0) , (16,10) ),
( (17 ,30) , (24,0) ),
( (1 ,0) , (2,0) ),
( (0 ,0) , (0,0) ),
]