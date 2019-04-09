import pygame,sys
from pygame.locals import *
from random import randint
import time
ancho=900
alto=480
listaEnemigo=[]


#newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()


class Boton(pygame.sprite.Sprite):
    def __init__(self, imagen1, imagen2, x=200, y=200):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, pantalla, cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else:
            self.imagen_actual = self.imagen_normal

        pantalla.blit(self.imagen_actual, self.rect)
#newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww


class score(pygame.sprite.Sprite):
    def __init__(self,sco):
        pygame.sprite.Sprite.__init__(self)
        self.num=sco
        self.num1='0000'
        self.fuente=pygame.font.Font(None,30)
        self.puntaje=self.fuente.render('Score:'+self.num1,0,(255,250,250))
    def escribir(self,superficie):
        superficie.blit(self.puntaje,(750,450))
    def sumpun(self,puj):
        self.num=self.num+puj
        if(self.num<100):
            self.num1='00'+str(self.num)
        elif self.num>=100 and self.num<1000:
            self.num1='0'+str(self.num)
        else:
            self.num=str(self.num)
        self.puntaje=self.fuente.render('Score:'+self.num1,0,(255,250,250))
class naveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave=pygame.image.load("imagenes/nave.png")
        self.ImagenExplosion=pygame.image.load("imagenes/explosion.png")
        self.rect=self.ImagenNave.get_rect()
        self.rect.centerx=ancho/2
        self.rect.centery=alto-30
        self.velocidad=20
        #poner la ruta del archivo de sonido del disparo
        #self.sonidoDisparo = pygame.mixer.Sound()
        #self.sonidoExplosion=pygame.mixer.Sound()
        self.Vida=True
        self.listaDisparo=[]
    def movimientoDerecha(self):
        self.rect.right+=self.velocidad
        self.movimiento()
    def movimientoIzquierda(self):
        self.rect.left-=self.velocidad
        self.movimiento()
    def movimiento(self):
        if self.Vida==True:
            if self.rect.left<=0:
               self.rect.left=0
            elif self.rect.right>=870:
                self.rect.right=870
    def disparar(self,x,y):
        proy=Proyectil(x,y,"imagenes/disparoa.png",True,10)
        self.listaDisparo.append(proy)
        #self.sonidoDisparo.play()
    def destruccion(self):
        #self.sonidoExplosion.play()
        self.Vida=False
        self.velocidad=0
        self.ImagenNave=self.ImagenExplosion

    def dibujar(self,superficie):
        superficie.blit(self.ImagenNave,self.rect)
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,personaje,aux):
        pygame.sprite.Sprite.__init__(self)
        self.imageProyectil=pygame.image.load(ruta)
        self.rect=self.imageProyectil.get_rect()
        self.velocidadDisparo=aux
        self.rect.top=posy
        self.rect.left=posx
        self.disparoPersonaje =personaje
    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top=self.rect.top-self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo
    def dibujar(self,superficie):
        superficie.blit(self.imageProyectil,self.rect)
class Invasor(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagenUno,imagenDos,imagenTres,imagenCuatro,velinv):
        pygame.sprite.Sprite.__init__(self)
        self.imagenA = pygame.image.load(imagenUno)
        self.imagenB = pygame.image.load(imagenDos)
        self.imagenC = pygame.image.load(imagenTres)
        self.imagenD = pygame.image.load(imagenCuatro)
        self.listaImagenes=[self.imagenA, self.imagenB,self.imagenC,self.imagenD]
        self.posImagen=0
        self.imagenInvasor=self.listaImagenes[self.posImagen]
        self.rect=self.imagenInvasor.get_rect()
        self.listaDisparo=[]
        self.velocidad=velinv
        self.rect.top=posy
        self.rect.left=posx
        self.rangoDisparo=1
        self.tiempoCambio=1
        self.conquista=False
        self.derecha=True
        self.contador=0
        self.Maxdescenso=self.rect.top+40
        self.limiteDerecha=posx+distancia
        self.limiteIzquierda=posx-distancia
    def dibujar(self,superficie):
        self.imagenInvasor=self.listaImagenes[self.posImagen]
        superficie.blit(self.imagenInvasor, self.rect)

    def comportamiento(self,tiempo,ata):
        if self.conquista==False:
            self._movimientos()
            self._ataque(ata)
        if self.tiempoCambio == tiempo:
              self.posImagen +=+1
              self.tiempoCambio +=+1
              if self.posImagen >len(self.listaImagenes)-1:
                  self.posImagen=0
        self._ataque(ata)
        self._movimientos()
    def _ataque(self,ata):
        if (randint(0,ata)<self.rangoDisparo):
           self._disparo()
    def _disparo(self):
        x,y =self.rect.center
        miProyectil=Proyectil(x,y,"imagenes/disparob.png",False,2)
        self.listaDisparo.append(miProyectil)
    def _movimientos(self):
        if self.contador<3:
            self._movimientoLateral()
        else:
            self._descenso()
    def _descenso(self):
        if self.Maxdescenso== self.rect.top:
            self.contador=0
            self.Maxdescenso= self.rect.top+40
        else:
            self.rect.top +=1

    def _movimientoLateral(self):
        if self.derecha ==True:
            self.rect.left=self.rect.left+self.velocidad
            if self.rect.left>self.limiteDerecha:
                self.derecha=False
                self.contador+=1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left <self.limiteIzquierda:
                self.derecha = True

def detenerTodo():
    for enemigo in  listaEnemigo:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
        enemigo.conquista=True

def cargarEnemigos(velinv):
    posx=100
    for x in range(1,5):
        enemigo=Invasor(posx,100,40,"imagenes/marcianoA.png","imagenes/marcianoB.gif","imagenes/marcianoC.gif","imagenes/marcianoD.gif",velinv)
        listaEnemigo.append(enemigo)
        posx=posx+200
    posx=100
    for x in range(1,5):
        enemigo=Invasor(posx,0,40,"imagenes/marcianoA.png","imagenes/marcianoB.gif","imagenes/marcianoC.gif","imagenes/marcianoD.gif",velinv)
        listaEnemigo.append(enemigo)
        posx=posx+200
    posx=100
    for x in range(1,5):
        enemigo=Invasor(posx,-100,40,"imagenes/marcianoA.png","imagenes/marcianoB.gif","imagenes/marcianoC.gif","imagenes/marcianoD.gif",velinv)
        listaEnemigo.append(enemigo)
        posx=posx+200
def GameOver(venta,sco):
    go=pygame.image.load("imagenes/gameover.jpg")
    mifuenteSistema=pygame.font.SysFont(None,30)
    Pun=mifuenteSistema.render("Score: "+str(sco),1,(96,123,139))
    pres=mifuenteSistema.render("Presione enter para volver al menu....",1,(0,0,0))

    while True:
        venta.blit(go,(0,0))
        venta.blit(Pun,(100,200))
        venta.blit(pres,(100,220))
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==K_SPACE:
                   main()
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
def subniv(venta,numl,velinv,randis,sco):
    lvl=pygame.image.load("imagenes/nextlvl.jpg")
    mifuenteSistema=pygame.font.SysFont(None,30)
    numl=numl+1
    velinv=velinv+1
    randis=randis-100
    nvl=mifuenteSistema.render("Nivel "+str(numl),1,(0,0,0))
    while True:
        venta.blit(lvl,(0,0))
        venta.blit(nvl,(450,240))

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==K_SPACE:
                    SpaceInvader(numl,velinv,randis,sco)
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def SpaceInvader(numl,velinv,randis,sco):
    pygame.init()
    venta=pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Invader")
    ImagenFondo=pygame.image.load("imagenes/Fondo.jpg")
    #poner el sonido de fondo
    pygame.mixer.music.load("imagenes/Fondo.mp3")
    pygame.mixer.music.play(3)
    mifuenteSistema=pygame.font.SysFont("Arial",30)
    Texto=mifuenteSistema.render("Fin del juego",0,(150,130,120))
    Score=score(sco)
    jugador=naveEspacial()
    cargarEnemigos(velinv)
    enJuego=True
    reloj=pygame.time.Clock()
    t=True

    while True:
        reloj.tick(60)
        #jugador movimiento
        tiempo=int(pygame.time.get_ticks()/1000)
        for event in pygame.event.get():
            if enJuego==True:
                if event.type==pygame.KEYDOWN:
                    if event.key==K_LEFT:
                        jugador.movimientoIzquierda()
                    elif event.key==K_RIGHT:
                        jugador.movimientoDerecha()
                    elif event.key==K_SPACE:
                        x,y=jugador.rect.center
                        jugador.disparar(x,y)
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        venta.blit(ImagenFondo,(0,0))
        jugador.dibujar(venta)
        Score.escribir(venta)
        if len(jugador.listaDisparo)>0:
            for x in jugador.listaDisparo:
                x.dibujar(venta)
                x.trayectoria()
                if x.rect.top<-10:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            listaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(x)
                            Score.sumpun(10)

        if len(listaEnemigo)>0:
            for enemigo in listaEnemigo:
                enemigo.comportamiento(int(tiempo),randis)
                enemigo.dibujar(venta)
                if enemigo.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    enJuego = False
                    detenerTodo()
                if len(enemigo.listaDisparo)>0:
                    for x in enemigo.listaDisparo:
                        x.dibujar(venta)
                        x.trayectoria()
                        if x.rect.colliderect(jugador.rect):
                            jugador.destruccion()
                            enJuego = False
                            detenerTodo()
                        if x.rect.top>900:
                            enemigo.listaDisparo.remove(x)
                        else:
                            for disparo in jugador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(x)
        else:
            Score.sumpun(100)
            subniv(venta,numl,velinv,randis,Score.num)

        if enJuego==False:
            pygame.mixer.music.fadeout(3000)
            GameOver(venta,Score.num)

        pygame.display.update()



def main():
    pygame.init()
    venta=pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Invader")
    ImagenFondo=pygame.image.load("Fondo.png")
    #poner el sonido de fondo
    pygame.mixer.music.load("sonidos/2.mp3")
    pygame.mixer.music.play(3)

    reloj1 = pygame.time.Clock()

    rojo1 = pygame.image.load("rojo.png")
    rojo2 = pygame.image.load("rojo2.png")
    azul1 = pygame.image.load("azul.png")
    azul2 = pygame.image.load("azul2.png")

    boton1 = Boton(azul1, azul2, 400,270)
    boton2 = Boton(rojo1, rojo2, 400,370)
    cursor1 = Cursor()

    salir = False
    # LOOP PRINCIPAL
    while salir != True:
        # recorro todos los eventos producidos
        # en realidad es una lista
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    SpaceInvader(1, 1, 600, 0)

                if cursor1.colliderect(boton2.rect):
                    salir = True

            # pygame.QUIT( cruz de la ventana)
            if event.type == pygame.QUIT:
                salir = True
        venta.blit(ImagenFondo,(0,0))

        reloj1.tick(20)  # operacion para que todo corra a 20fps

        cursor1.update()
        boton1.update(venta, cursor1)
        boton2.update(venta, cursor1)

        pygame.display.update()  # actualizo el display
    pygame.quit()



main()

