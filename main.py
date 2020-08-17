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

class listener(StreamListener):
    def on_data(self,data):
        print data
        videodata = json.loads(data)
        llego_tweet(videodata)
	def on_error(self,status):
		print status

def main():
    auth = tweepy.OAuthHandler(config.API_KEY,config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN,config.ACCESS_TOKEN_SECRET)

    thread.start_new_thread(main_check,())

    stream = tweepy.Stream(auth,listener())
    stream.filter(track=[ ("@"+config.usuario) ])

def main_check():
    global continuar
    loops = 0
    while continuar:
        loop()
            #if loops == 1000000:
            #    data = {'contributors': None, 'truncated': False, 'text': '@arielnowik https://t.co/S4DeBgNVdh', 'in_reply_to_status_id': None, 'id': 488387306127388672, 'favorite_count': 0, 'source': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'retweeted': False, 'coordinates': None, 'entities': {'user_mentions': [{'id': 209841894, 'indices': [0, 11], 'id_str': '209841894', 'screen_name': 'arielnowik', 'name': 'ariel nowik'}], 'symbols': [], 'trends': [], 'hashtags': [], 'urls': [{'url': 'https://t.co/S4DeBgNVdh', 'indices': [12, 35], 'expanded_url': 'https://www.youtube.com/watch?v=OLyf1D7cFU4', 'display_url': 'youtube.com/watch?v=OLyf1D\u2026'}]}, 'in_reply_to_screen_name': 'arielnowik', 'id_str': '488387306127388672', 'retweet_count': 0, 'in_reply_to_user_id': 209841894, 'favorited': False, 'user': {'follow_request_sent': None, 'profile_use_background_image': True, 'default_profile_image': True, 'id': 2617799809, 'verified': False, 'profile_image_url_https': 'https://abs.twimg.com/sticky/default_profile_images/default_profile_2_normal.png', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'followers_count': 1, 'profile_sidebar_border_color': 'C0DEED', 'id_str': '2617799809', 'profile_background_color': 'C0DEED', 'listed_count': 0, 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'utc_offset': None, 'statuses_count': 24, 'description': None, 'friends_count': 4, 'location': '', 'profile_link_color': '0084B4', 'profile_image_url': 'http://abs.twimg.com/sticky/default_profile_images/default_profile_2_normal.png', 'following': None, 'geo_enabled': False, 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'name': 'GranDT', 'lang': 'es', 'profile_background_tile': False, 'favourites_count': 0, 'screen_name': 'elgrandt11', 'notifications': None, 'url': None, 'created_at': 'Fri Jul 11 18:08:48 +0000 2014', 'contributors_enabled': False, 'time_zone': None, 'protected': False, 'default_profile': True, 'is_translator': False}, 'geo': None, 'in_reply_to_user_id_str': '209841894', 'possibly_sensitive': False, 'lang': 'und', 'created_at': 'Sun Jul 13 18:19:42 +0000 2014', 'filter_level': 'medium', 'in_reply_to_status_id_str': None, 'place': None}
            #    llego_tweet(data)
        loops += 1

def loop():
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

    elif hay_video:
        if time.time() - tiempo_inicio > duracion + config.margen_cargar: #si terminamos
            print "Se termino de reproducir el video"
            hay_video = False
            close_all()

def llego_tweet(data):
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
            print "se activara el sistema por peticion de admin"
            habilitado = True
        elif texto.find(config.palabra_clave_apagar) != -1:
            print "se desactivara el sistema por peticion de admin"
            habilitado = False
    if texto.find(config.palabra_clave_malo) != -1:
        cantidad_sacalos += 1
        if cantidad_sacalos >= config.cantidad_malo or admin:
            print "Se termino de reproducir el video por peticion"
            hay_video = False
            close_all()
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
            video = {"link":url,"duration":duration}
            print "Link detectado! :" +  url

            if is_music(url):
                print "Se agrega a la cola"

                if texto.find(config.palabra_clave_admin) != -1 and admin:
                    cola_admin_de_videos.append(video)
                else:
                    cola_de_videos.append(video)
            else:
                print "El link no es una cancion"
        else:
            print "No se detecto ningun link"
    else:
        print "El servicio no esta habilitado o no se cumplen los horarios, por lo que no se reproduce el video"

def es_admin(usuario):
    for x in range(len(config.master_admins)):
        if config.master_admins[x] == usuario:
            return True
    return False

def cumple_horarios():
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
    if len(cola_de_videos) > 0:
        video = cola_de_videos[0]
        del cola_de_videos[0]
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

if __name__ == "__main__":
    main()
