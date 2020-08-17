__author__ = 'newtonis'

import pygame
import datetime
import config

pygame.init()

class Icon:
    def __init__(self,title,duration,x,y,sbx = 0,sby = 0):
        self.title    = title
        self.duration = duration
        self.x = x
        self.y = y
        self.sbx = sbx
        self.sby = sby
        self.surface = generate_surface_area(title+"  ("+add0(str(duration/60))+":"+add0(str(duration%60))+")")
        self.w , self.h = self.surface.get_size()
        self.sxp = 0
        self.syp = 0
        self.lastselected = False

    def update(self,mousex,mousey,pressed):
        global sometextsel

        selected = False

        if self.lastselected and pressed:
            selected = True
        elif sometextsel:
            if self.lastselected:
                sometextsel = False
        elif mousex > self.x and mousex < self.x + self.w and mousey > self.y and mousey < self.y + self.h and pressed:
            selected = True
            if not self.lastselected:
                self.sxp = mousex - self.x
                self.syp = mousey - self.y
            self.lastselected = True
        elif self.lastselected:
            sometextsel = False

        if not selected:
            self.lastselected = False
            self.x += float(self.sbx - self.x)/10.0
            self.y += float(self.sby - self.y)/10.0
        else:
            self.x = mousex - self.sxp
            self.y = mousey - self.syp

        if selected:
            global diamond
            diamond = True
            sometextsel = True

    def draw(self,corrimento = 0):
        screen.blit(self.surface,(self.x + corrimento,self.y))
    def update_time(self,time):
        self.surface = generate_surface_area(self.title+"  ("+add0(str(int(time/60)))+":"+add0(str(int(time%60)))+")")
class Config_icon:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w , self.h = image_config.get_size()
        self.color_background = 0
    def draw(self,corrimento = 0):
        screen.blit(surface_aplhaB,(self.x+corrimento,self.y))
        screen.blit(image_config,(self.x+corrimento,self.y))
    def update(self,pressed,mousex,mousey):
        if mousex > self.x and mousex < self.x + self.w and mousey > self.y and mousey < self.y + self.h:
            self.focused()
            if pressed:
                self.ifpressed()
        else:
            self.color_background = 0
        surface_aplhaB.set_alpha(self.color_background)
    def ifpressed(self):
        if corrimiento != 0:
            return 0
        show_message_loading("Entrando en configuracion")
        global estado
        estado = CONFIGURACION
    def focused(self):
        global diamond
        diamond = True
        if self.color_background < 255:
            self.color_background += 3

class Flechaid_icon(Config_icon):
    def __init__(self,x,y):
        Config_icon.__init__(self,x,y)
    def draw(self,corrimento = 0):
        screen.blit(surface_aplhaB,(self.x+corrimento,self.y))
        screen.blit(image_flechaid,(self.x+corrimento,self.y))
    def ifpressed(self):
        if corrimiento != 800:
            return 0
        show_message_loading("Volviendo ...")
        global estado
        estado = RETURN_APLICATION

class Bin_icon:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w , self.h = bin.get_size()
        self.color_background = 0
        self.isfocused = False

    def draw(self,corrimiento = 0):
        screen.blit(surface_aplhaB,(self.x + corrimiento,self.y))
        screen.blit(bin,(self.x + corrimiento,self.y))
    def update(self,mousex,mousey):
        if mousex > self.x and mousex < self.x + self.w and mousey > self.y and mousey < self.y + self.h:
            self.focused()
            self.isfocused = True
        else:
            self.color_background = 0
            self.isfocused = False
        surface_aplhaB.set_alpha(self.color_background)
    def focused(self):
        global diamond
        diamond = True
        if self.color_background < 255:
            self.color_background += 3

class tick_select:
    def __init__(self,text,x,y,state):
        self.ticked = state
        self.x = x
        self.y = y
        self.w , self.h = tickimage.get_size()
        self.lastpressed = False
        self.surfacetext = ka1.render(text,1,(0,0,0))
        self.obtained = True
    def draw(self,corrimiento = 0):
        screen.blit(self.surfacetext , (self.x+corrimiento,self.y))
        if self.ticked:
            screen.blit(tickimage , (self.x+corrimiento + self.surfacetext.get_size()[0] + 30 ,self.y))
        else:
            screen.blit(tickimageB,(self.x+corrimiento + self.surfacetext.get_size()[0] + 30 ,self.y))
    def newstate(self):
        if self.obtained == False:
            self.obtained = True
            return self.ticked
        else:
            return -1
    def update(self,pressed,mousex,mousey):
        if mousex > self.x + self.surfacetext.get_size()[0] + 30  and mousex < self.x + self.w + self.surfacetext.get_size()[0] + 30 and mousey > self.y and mousey < self.y + self.h:
            if pressed:
                if not self.lastpressed:
                    self.ticked = not self.ticked
                    self.obtained = False
                self.lastpressed = True
        if not pressed:
            self.lastpressed = False


class Message:
    def __init__(self,message,loading):
        self.image = generateMessageImage(message)
        self.y = -self.image.get_size()[1]
        self.enabled = True
        self.timeup  = 0
    def show(self):
        screen.blit(self.image,(0,self.y))
    def update(self):
        if self.enabled:
            if self.y < 0:
                self.y += 1
            else:
                self.timeup += 1
                if self.timeup > 100:
                    self.enabled = False
                    self.timeup   = 0
        else:
            if self.y > -self.image.get_size()[1]:
                self.y -= 1
class Red_button:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w , self.h = buttonred.get_size()
        self.backgroundcolor = 0
        self.lastpressed     = False
    def update(self,pressed,mousex,mousey):
        if mousex > self.x and mousex < self.x + self.w and mousey > self.y and mousey < self.y + self.w:
            self.focused()
            if pressed:
                if not self.lastpressed:
                    abort_current()
                self.lastpressed = True
            else:
                self.lastpressed = False
        else:
            self.backgroundcolor = 0
            self.lastpressed = False
    def focused(self):
        global diamond
        diamond = True
        self.backgroundcolor += 4
        if self.backgroundcolor > 255:
            self.backgroundcolor = 255

    def draw(self,corrimiento):
        screen.blit(buttonred,(self.x+corrimiento,self.y))
        redcover.set_alpha(self.backgroundcolor)
        screen.blit(redcover,(self.x+corrimiento,self.y))


### DECLARACION DE ESTADOS ###
PRESENTACION_ORT , \
PRESENTACION_ALPICACION,  \
APPLICATION, \
CONFIGURACION, \
RETURN_APLICATION = range(5)

screen       = pygame.display.set_mode((800,600))
estado       = APPLICATION
my_logic     = None
image_logo   = pygame.image.load("imagenes/titulo.png")
ort_logo     = pygame.image.load("imagenes/ort.png")
ort_logo_cel = pygame.image.load("imagenes/ort_celeste.png")
image_config = pygame.image.load("imagenes/config.png")
image_flechaid=pygame.image.load("imagenes/flechaid.png")

flecha       = pygame.image.load("imagenes/flecha.png")
bin          = pygame.image.load("imagenes/bin.png")

diamond      = False
sometextsel  = False
enabled      = True

fontApache    = pygame.font.Font("fonts/AldotheApache.ttf",30)
fontApache20  = pygame.font.Font("fonts/AldotheApache.ttf",20)
fontLittleDays= pygame.font.Font("fonts/Little days.ttf",20)
fontClubLand  = pygame.font.Font("fonts/Clubland.ttf",10)
display007    = pygame.font.Font("fonts/LiquidCrystal-Bold.ttf",35)
ka1           = pygame.font.Font("fonts/ka1.ttf",20)

textoCola    = fontApache.render("Cola de videos",1,(0,0,0))
textoNada    = fontApache20.render("No hay ningun video",1,(0,0,0))
bar_image    = pygame.image.load("imagenes/bar.png")
points       = [ pygame.image.load("imagenes/points_0.png") , pygame.image.load("imagenes/points_1.png") , pygame.image.load("imagenes/points_2.png") ]

buttonred    = pygame.image.load("imagenes/rojo.png")
redcover     = pygame.surface.Surface((64,64))
tickimage    = pygame.image.load("imagenes/tick.png")
tickimageB   = pygame.image.load("imagenes/tick2.png")

boton_image  = pygame.image.load("imagenes/boton.png")
boton_image_hover  = pygame.image.load("imagenes/boton1.png")

redcover.fill((231, 17, 0))

surface_alpha = pygame.surface.Surface(screen.get_size())
surface_aplhaB= pygame.surface.Surface(image_config.get_size())
surface_alpha .fill((0,0,0))
surface_aplhaB.fill((0,0,0))
lastsecond    = -1

videoqueue    = []


end_value  = False

#presentacion ort
time_ort_logo = 0
sub_time_ort_logo = 0
screen_fill_color = 0

#presentacion aplicacino
time_aplicacion = 0

#aplicacion
config_icon = Config_icon(screen.get_size()[0]-image_config.get_size()[0]-10,10)
bin_icon    = Bin_icon(10,screen.get_size()[1]-bin.get_size()[1]-10)
abort_button= Red_button(30,83)
videoplaying= True #por ahora
lastabort   = False
nowabort    = False
surfacetime = 0
corrimiento = 0

#message
loading_message = False
message_structure = None

#config
tickFiltroHorario = tick_select("Activar filtro horario",100,100,config.activar_filtro_horario)
flechaid          = Flechaid_icon(screen.get_size()[0]-image_config.get_size()[0]-10,10)



def generate_surface_area(title):
    mysurface = flecha.copy()
    surfacetext = fontLittleDays.render(title,1,(0,0,0))
    mysurface.blit(surfacetext,(10,mysurface.get_size()[1]/2 - surfacetext.get_size()[1]/2))
    return mysurface

def generateMessageImage(message):
    base_surface = bar_image.copy()
    message_surface = fontClubLand.render(message,1,(0,0,0))
    base_surface.blit(message_surface,(10,base_surface.get_size()[1]/2-message_surface.get_size()[1]/2))
    return base_surface

def add0(strnumber):
    if len(str(strnumber)) == 1:
        return "0"+str(strnumber)
    else:
        return str(strnumber)

def start(logic):
    pygame.display.set_caption("Power Video")
    global my_logic
    my_logic = logic
    print "start"
    #for x in range(10):
    #    call_video_added({"link":"here it is some url "+str(x),"duration":600})

def get_center(surfaceA,surfaceB):
    return surfaceA.get_size()[0] / 2 - surfaceB.get_size()[0] / 2 , surfaceA.get_size()[1] / 2 - surfaceB.get_size()[1] / 2

def end():
    global end_value
    return end_value

def update():
    global diamond
    diamond = False

    global estado
    screen.fill((255,255,255))

    if estado == PRESENTACION_ORT:

        global time_ort_logo
        global sub_time_ort_logo
        sub_time_ort_logo += 1
        if sub_time_ort_logo >= 2:
            sub_time_ort_logo = 0
            time_ort_logo += 1
        if time_ort_logo < 50:
            maxshow = 1
        elif time_ort_logo < 50+10:
            maxshow = (time_ort_logo - 50)
        elif time_ort_logo < 50+10+50:
            maxshow = 10
        else:
            maxshow = 10
            global screen_fill_color
            screen_fill_color += 4

            if screen_fill_color >= 255:
                screen_fill_color = 255
                estado = PRESENTACION_ALPICACION


        for v in range(maxshow):
            x,y = get_center(screen,ort_logo)
            x += maxshow
            y -= maxshow
            if v != maxshow-1:
                screen.blit(ort_logo_cel, (x-v,y+v))
            else:
                screen.blit(ort_logo, (x-v,y+v))


    elif estado == PRESENTACION_ALPICACION:
        global time_aplicacion

        screen.blit(image_logo,get_center(screen,image_logo))
        if time_aplicacion < 255:
            screen_fill_color -= 2
            if screen_fill_color < 0:
                screen_fill_color = 0
        elif time_aplicacion < 255+50:
            pass
        elif time_aplicacion < 256+50+256:
            screen_fill_color += 2
        else:
            estado = APPLICATION

        time_aplicacion += 1
    elif estado == APPLICATION:
        aplicacion()
        if screen_fill_color > 0:
            screen_fill_color -= 2
        else:
            screen_fill_color = 0

    elif estado == CONFIGURACION:
        global corrimiento
        if corrimiento <= 779:
            aplicacion()
            configuracion()
            corrimiento -= float(- 800.0 + corrimiento) / 20.0
            time_aplicacion += 1
        else:
            corrimiento = 800
            screen.fill((144, 199, 214))
            configuracion()
    elif estado == RETURN_APLICATION:
        corrimiento += float( - corrimiento ) / 20.0
        aplicacion()
        configuracion()
        if corrimiento <= 1:
            corrimiento = 0
            estado = APPLICATION
        pass
    surface_alpha.set_alpha(screen_fill_color)
    screen.blit(surface_alpha,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global end_value
            end_value = True

    if not diamond:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    if message_structure:
        message_structure.update()
    pygame.display.update()

### START CALLBACK FUNCTIONS ###

def update_time(newtime):
    if len(videoqueue) == 0:
        return 0
    global videoplaying
    if not videoplaying:
        return 0
    videoqueue[0].update_time( newtime )

def call_video_added(video):
    pass

def call_start_video():
    global videoplaying
    videoplaying = True
    show_message_loading("Se esta comenzando a reproducir un nuevo video")

def call_end_video():
    global videoplaying
    show_message_loading("Se ha terminado de reproducir el video")
    videoplaying = False
    if len(videoqueue) > 0:
        del videoqueue[0]
    else:
        print "Error de los peores"
def call_enabled():
    global enabled
    enabled = True

def call_disabled():
    global enabled
    enabled = False

def call_bad_video():
    global videoqueue
    if len(videoqueue) > 0:
        del videoqueue[0]

def call_video_added(video):
    show_message_loading("Nuevo video recibido ! ")
    videoqueue.append( Icon(video["title"],video["duration"],300,1000) )

### END CALLBACK FUNCTIONS ###

def update_cola():
    global videoplaying
    global videoqueue
    for x in range(len(videoqueue)):
        videoqueue[x].sby = 90+x * 60
        if videoplaying and x == 0:
            videoqueue[x].sbx = 150
        else:
            videoqueue[x].sbx = 100

def enrocar(x,y):
    p = videoqueue[x]
    videoqueue[x] = videoqueue[y]
    videoqueue[y] = p
    update_cola()
    my_logic.enrocar(x,y)

def aplicacion():
    screen.fill((144, 199, 214))
    screen.blit(get_time_surface() , (70,20))

    global videoqueue
    global videoplaying
    global corrimiento

    update_cola()
    screen.blit(textoCola,(screen.get_size()[0]/2-textoCola.get_size()[0]/2 + corrimiento,30))
    if len(videoqueue) == 0:
        screen.blit(textoNada,(screen.get_size()[0]/2-textoNada.get_size()[0]/2+ corrimiento,200))
    mousex,mousey = pygame.mouse.get_pos()
    pressed       = pygame.mouse.get_pressed()[0]

    for x in range(len(videoqueue)):
        if videoqueue[x].lastselected and not (videoplaying and x == 0):
            if not pressed:
                if bin_icon.isfocused:
                    show_message_loading("Video eliminado !")
                    del videoqueue[x]
                    my_logic.eliminar(x)
                    global sometextsel
                    sometextsel = False
                    break
                for y in range(len(videoqueue)):
                    if y != x:
                        if mousex > videoqueue[y].x and mousex < videoqueue[y].x + videoqueue[y].w and mousey > videoqueue[y].y and mousey < videoqueue[y].y + videoqueue[y].h:
                            enrocar(x,y)

        videoqueue[x].update(mousex,mousey,pressed)
        videoqueue[x].draw(corrimiento)


    config_icon.update(pressed,mousex,mousey)
    config_icon.draw(corrimiento)
    bin_icon.update(mousex,mousey)
    bin_icon.draw(corrimiento)
    abort_button.update(pressed,mousex,mousey)
    abort_button.draw(corrimiento)

class boton:
    def __init__(self, text):
        self.x = 0
        self.y = 0
        self.text = text
        self.surface = boton_image
        self.render = ka1.render(text,1,(0,0,0))
    def set_x(self, X):
        self.x = X
    def set_y(self, Y):
        self.y = Y
    def update(self, mouse_x, mouse_y, pressed):
        if self.focused(mouse_x,mouse_y):
            self.surface = boton_image_hover
        if self.clicked(mouse_x,mouse_y,pressed):
            self.render = ka1.render(self.text,1,(0,0,255))
        fina_surface = self.surface
        final_surface.blit(self.render,(self.surface.get_size()[0]/2-self.render.get_size()[0]/2,self.surface.get_size()[1]/2-self.render.get_size()[1]/2));
    def focused(self, x, y):
        w,h = self.surface.get_size()
        return (x > self.x) and (y > self.y) and (x < self.x+w) and (x < self.y+h)
    def clicked(self,x,y,pressed):
        return self.focused(x,y,pressed) and pressed
    def get_surface(self):
        return self.surface;

def configuracion():
    #------ ACTUALIZAR RELOJ ------#
    screen.blit(get_time_surface() , (70,20))
    global corrimiento
    
    #------ OBTENER DATOS DE PRESIONADO Y POSICION DE MOUSE ------#
    pressed = pygame.mouse.get_pressed()[0]
    mousex, mousey = pygame.mouse.get_pos()

    ###  HABILITAR HORARIOS  ###
    tickFiltroHorario.update(pressed,mousex,mousey)
    tickFiltroHorario.draw(800-corrimiento)
    if tickFiltroHorario.newstate() != -1:
        replace_line("config.py",6,"activar_filtro_horario = " + str(tickFiltroHorario.ticked) +"\n")
        show_message_loading("Actualizado conf.py")
        config.activar_filtro_horario = not tickFiltroHorario.ticked
    flechaid.update(pressed,mousex,mousey)
    flechaid.draw(800-corrimiento)
    ###  HABILITAR HORARIOS  ###

    ###  VER HORARIOS ADMITIDOS  ###
    #boton_horarios_admitidos = boton()
    ###  VER HORARIOS ADMITIDOS  ###

def get_time_surface():

    global lastsecond

    son_las = datetime.datetime.now()
    hours   = son_las.hour
    minutes = son_las.minute
    seconds = son_las.second
    stringtime  = add0(hours) + ":" + add0(minutes) + ":" + add0(seconds)

    global surfacetime
    if lastsecond != seconds or lastsecond == -1:
        if not config.activar_filtro_horario:
            color = (24, 34, 87)
        elif my_logic.cumple_horarios():
            color = (39, 118, 80)
        else:
            color = (168, 56, 59)
        surfacetime = display007.render(stringtime,1,color)
        lastsecond = seconds
    return surfacetime

def show_message_loading(message):
    global message_structure
    message_structure = Message(message,False)

def abort_current():
    if len(videoqueue) > 0:
        show_message_loading("Se ha abortado el video")
    global my_logic
    my_logic.abort_video()

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()