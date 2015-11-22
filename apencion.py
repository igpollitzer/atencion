import numpy as np
import pygame as pg
from pygame.locals import *
from sys import exit
from random import randrange

LEFT_BUTTON = 1
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CYAN = (110, 110, 110)
#CYAN = (0, 255, 255)
#PRUEBA = (125, 125, 125)
PRUEBA = (160, 160, 160)

ROJO = (255, 0, 0)
SCREEN_SIZE = (1280, 720)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_DEPTH = 32
SCREEN_FLAGS = 0
SCREEN_COLOR = CYAN
FPS = 60
DIST_INIT = 50
DIST_PASO = 5
PERIODO_PASO = 5

NUMERO_JUGADORES = 8
RADIO_GIRO = SCREEN_HEIGHT / 2.5
CENTRO_GIRO = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
PERIODO = 100

class Jugador(object):
    def __init__(self, desfasaje, color):
        self.arco = 0
        self.desfasaje = desfasaje
        self.posicion = self.get_pos(self.arco)
        self.color = color
    def get_pos(self, tiempo):
        x = int(RADIO_GIRO * np.sin((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[0])
        y = int(RADIO_GIRO * np.cos((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[1])
        return np.array((x, y))

class Pelota(object):
    GIRANDO, VOLANDO = range(2)

    def __init__(self):
        self.arco = 0
        self.desfasaje = 0
        self.estado = Pelota.GIRANDO
        self.posicion = self.get_pos(self.arco)

        #para cuando vuele
        self.partida = 0
        self.destino = (0, 0)        
        self.paso = 0        

    def pasar(self, jugador):
        self.posicion = self.get_pos(cuanto)
        self.partida = cuanto
        # este arreglo de 35 esta horrible, pero sirve para 7 jugadores
        arribo = cuanto + 35
        self.destino = jugador.get_pos(arribo)
        self.paso = (self.destino - self.get_pos(cuanto)) / 240.
        self.desfasaje = jugador.desfasaje
        self.estado = Pelota.VOLANDO

    def get_pos(self, tiempo):
    
        salida = np.array((0, 0))
    
        if self.estado == Pelota.GIRANDO:
    
            x = int(RADIO_GIRO * np.sin((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[0])
            y = int(RADIO_GIRO * np.cos((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[1])
            salida = np.array((x, y))

        if self.estado == Pelota.VOLANDO:

            self.posicion = self.posicion + self.paso

            if np.linalg.norm(self.posicion - self.destino) < 1:
            
                self.posicion = self.destino
                self.estado = Pelota.GIRANDO

            salida = np.array((int(self.posicion[0]), int(self.posicion[1])))
        return salida
            



def get_jugadores(cant_jugadores):
    jugadores = []
    for pos in range(cant_jugadores):
        if (pos + 1) % 2 == 1:
            next_color = BLANCO
        else:
            next_color = NEGRO
        jugadores.append(Jugador(pos * PERIODO / cant_jugadores, next_color))
    return jugadores


pg.init()
screen = pg.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS, SCREEN_DEPTH)
relos = pg.time.Clock()

jugadores = get_jugadores(NUMERO_JUGADORES)
pelota = Pelota()
cuanto = 0
arroja = randrange(10, 20, 1)
pases = 0

numero = str(randrange(101, 999, 1))

texto_fondo = randrange(240, 360, 1)
texto = pg.font.SysFont("monospace", 200, True)
mensaje = texto.render(numero, 0, PRUEBA)
mensaje.set_alpha(0)
mensaje_flag = 0

while cuanto < 601:

        screen.fill(SCREEN_COLOR)
        screen.blit(mensaje, (SCREEN_WIDTH/3, SCREEN_HEIGHT/3))


        for event in pg.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_UP:
                    if pelota.estado == Pelota.GIRANDO:
                        print "volando"
                        rand = randrange(0, NUMERO_JUGADORES, 1)
                        while jugadores[rand].desfasaje == pelota.desfasaje:
                            rand = randrange(0, NUMERO_JUGADORES, 1)
                        print rand
                        print pelota.get_pos(cuanto)
                        arribo = 60
                        print jugadores[rand].get_pos(arribo)
                        pelota.pasar(jugadores[rand])
                if event.key == K_DOWN:
                    pelota.__init__()
                if event.key == K_LEFT:
                    pass
                if event.key == K_RIGHT:
                    pass
            if event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT_BUTTON:
                    pass
        # de cada fuente...
        for jugador in jugadores:
            pg.draw.circle(screen, jugador.color, jugador.get_pos(cuanto), 40, 10)
            pg.draw.circle(screen, (255, 0, 0), pelota.get_pos(cuanto), 30, 30)

        if cuanto == arroja:
            rand = randrange(0, NUMERO_JUGADORES, 1)
            while jugadores[rand].desfasaje == pelota.desfasaje:
                rand = randrange(0, NUMERO_JUGADORES, 1)
            arribo = 60
            pelota.pasar(jugadores[rand])
            arroja = cuanto + randrange(45, 60, 1)
            if jugadores[rand].color == BLANCO:
                pases = pases + 1
                print pases


#        if cuanto > texto_fondo:
#            if mensaje_flag == 0:
#                mensaje.set_alpha(mensaje.get_alpha() + 1)
#            elif mensaje_flag == 1:
#                mensaje.set_alpha(mensaje.get_alpha() - 1)

#            print mensaje.get_alpha()

#            if cuanto > texto_fondo + 30:
#                mensaje_flag = 1
#                print "apago"
#            if cuanto > texto_fondo + 90:
#                mensaje_flag = 2
#                print "listo" 
#            if cuanto > texto_fondo + 121:
#                mensaje_flag = 3

#            if cuanto > texto_fondo + 61:
#                mensaje_flag = 2

        # muestro la pantalla

        pg.display.update()

        cuanto = cuanto + 1

        relos.tick(FPS)
