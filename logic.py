import tweepy
import config
import json
import datetime
import time
import gdata.youtube.service as gys
from tweepy.streaming import StreamListener
import urlparse
import os
import platform
import thread

continuar            = True
tiempo_inicio        = 0
duracion             = 0
hay_video            = False
habilitado           = True
cola_de_videos       = []
cola_admin_de_videos = []
cantidad_sacalos     = 0
yt_service = gys.YouTubeService()
my_graphic           = None

class listener(StreamListener):
    def on_data(self,data):
        print data
        videodata = json.loads(data)
        llego_tweet(videodata)
    def on_error(self,status):
        print status


def start(graphic):
    global my_graphic
    my_graphic = graphic
    thread.start_new_thread(setup,())

def setup():

    auth = tweepy.OAuthHandler(config.API_KEY,config.API_SECRET)

    auth.set_access_token(config.ACCESS_TOKEN,config.ACCESS_TOKEN_SECRET)

    stream = tweepy.Stream(auth,listener())

    stream.filter(track=[ ("@"+config.usuario) ])

def update():
    global tiempo_inicio
    global duracion
    global hay_video
    global cantidad_sacalos

    if not hay_video:
        video = next_video()
        if video:
            print "Reproduciendo el video que sigue de la cola ..."
            thread.start_new_thread( open_link, (video["link"],) )
            tiempo_inicio = time.time()
            duracion = video["duration"]
            print "Duracion: "+str(duracion / 60)+":"+str(duracion%60)+" minutos"
            cantidad_sacalos = 0
            hay_video = True
            if my_graphic:
                my_graphic.call_start_video()
    elif hay_video:
        if time.time() - tiempo_inicio > duracion + config.margen_cargar: #si terminamos
            print "Se termino de reproducir el video"
            if my_graphic:
                del cola_de_videos[0]
                my_graphic.call_end_video()
            hay_video = False
            close_all()
        else:
            my_graphic.update_time(duracion - (time.time() - tiempo_inicio) + config.margen_cargar)

def llego_tweet(data):
    print "HOLA"
    global habilitado
    global cantidad_sacalos

    nombre_escritor  = data["user"]["screen_name"]
    id_escritor      = data["id"]
    texto            = data["text"]

    print "Nos nombraron!"
    print nombre_escritor + "( "+ str(id_escritor) + ") :"
    print "-------------------"
    print texto

    admin = es_admin(nombre_escritor)

    if admin:
        if texto.find(config.palabra_clave_prender) != -1:
            if my_graphic:
                my_graphic.call_enabled()
            print "se activara el sistema por peticion de admin"
            habilitado = True
        elif texto.find(config.palabra_clave_apagar) != -1:
            if my_graphic:
                my_graphic.call_disabled()
            print "se desactivara el sistema por peticion de admin"
            habilitado = False
    if texto.find(config.palabra_clave_malo) != -1:
        cantidad_sacalos += 1
        if cantidad_sacalos >= config.cantidad_malo or admin:
            abort_video()
    if admin or (habilitado and cumple_horarios() ):
        url = None
        cadena = "http://www.youtube.com"
        cadena2 = "https://www.youtube.com"
        urls = data["entities"]["urls"]
        for urlact in urls:
            urlac = urlact["expanded_url"]
            if urlac[:len(cadena)] == cadena or urlac[:len(cadena2)] == cadena2:
                url = urlac
                break
        if url:
            duration = int(get_video_duration(url))
            video = {"link":url,"duration":duration,"title":get_video_title(url)}
            print "Link detectado! :" +  url

            #if is_music(url):
            print "Se agrega a la cola"

            if texto.find(config.palabra_clave_admin) != -1 and admin:
                cola_admin_de_videos.append(video)
            else:
                cola_de_videos.append(video)
                if my_graphic:
                    my_graphic.call_video_added(video)
            #else:
            #    print "El link no es una cancion"
        else:
            print "No se detecto ningun link"
    else:
        print "El servicio no esta habilitado o no se cumplen los horarios, por lo que no se reproduce el video"
def eliminar(id):
    print "Se ha eliminado el video ",id
    del cola_de_videos[id]

def es_admin(usuario):
    for x in range(len(config.master_admins)):
        if config.master_admins[x] == usuario:
            return True
    return False

def cumple_horarios():
    if (not config.activar_filtro_horario):
        return True
    son_las = datetime.datetime.now()
    hora = son_las.hour
    minuto = son_las.minute

    for x in range(len(config.horarios_disponibles)):
        posibilidad_inicio   = config.horarios_disponibles[x][0]
        posibilidad_fin      = config.horarios_disponibles[x][1]
        hora_inicio   = posibilidad_inicio[0]
        minuto_inicio = posibilidad_inicio[1]
        hora_fin      = posibilidad_fin[0]
        minuto_fin    = posibilidad_fin[1]

        neta_a = hora_inicio * 60 + minuto_inicio
        neta_b = hora_fin * 60 + minuto_fin
        neta_c = hora * 60 + minuto

        if neta_a <= neta_c <= neta_b:
            return True
    return False

def get_video_id(url):
    urldata = urlparse.urlparse(url)
    query = urlparse.parse_qs(urldata.query)
    return query["v"][0]

def get_video_duration(url):
    global yt_service
    ID = get_video_id(url)
    act = yt_service.GetYouTubeVideoEntry(video_id = ID)
    print act.media.duration.seconds
    duration = act.media.duration.seconds
    return duration

def get_video_title(url):
    global yt_service
    ID = get_video_id(url)
    act = yt_service.GetYouTubeVideoEntry(video_id = ID)
    return act.media.title.text

def is_music(url):
    ID = get_video_id(url)
    act = yt_service.GetYouTubeVideoEntry(video_id = ID)
    category = act.category
    print category
    for q in category:
        if q == "Music":
           return True
    return True # por ahora

def open_link(url):
    so = platform.system()
    if so == "Windows":
        os.system("chrome "+url)
    elif so == "Linux":
        os.system("google-chrome "+url)
    else:
        os.system("open "+url)

def next_video():
    if len(cola_admin_de_videos) > 0:
        video =  cola_admin_de_videos[0]
        del cola_admin_de_videos[0]
        return video
    if not cumple_horarios():
        return 0
    if len(cola_de_videos) > 0:
        video = cola_de_videos[0]
        #del cola_de_videos[0]
        return video
    return 0

def close_all():
    so = platform.system()
    if so == "Linux":
        os.system("pkill chrome")
    elif so == "Windows":
        os.system("taskkill /IM chrome.exe")

def buscar_video(keyword):
    pass

def enrocar(x,y):
    print "Enrocando ",x," con ",y
    p = cola_de_videos[x]
    cola_de_videos[x] = cola_de_videos[y]
    cola_de_videos[y] = p

def abort_video():
    if len(cola_de_videos) == 0:
        return 0

    del cola_de_videos[0]
    if my_graphic:
        my_graphic.call_bad_video()
    print "Se termino de reproducir el video por peticion"
    hay_video = False
    close_all()
    global duracion
    duracion = 0

if __name__ == "__main__":
    main()
