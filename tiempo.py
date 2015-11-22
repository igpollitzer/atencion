import numpy as np
import pygame as pg
from pygame.locals import *
from sys import exit

LEFT_BUTTON = 1
NEGRO = (0, 0, 0)
CYAN = (0, 255, 255)
ROJO = (255, 0, 0)
SCREEN_SIZE = (1280, 720)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_DEPTH = 32
SCREEN_FLAGS = 0
SCREEN_COLOR = CYAN
FPS = 60
FUENTES_X = 100
FUENTES_TAM = 3
FUENTES_COLOR = ROJO
ONDAS_ANCHO = 1
ONDAS_COLOR = NEGRO
DIST_INIT = 50
DIST_PASO = 5
PERIODO_PASO = 5

NUMERO_JUGADORES = 8
RADIO_GIRO = SCREEN_HEIGHT / 3
CENTRO_GIRO = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
PERIODO = 300
VELOCIDAD_INIT = 2

dist_jugadores = PERIODO_INIT / NUMERO_JUGADORES

class jugador(object):
    CON_BOLA, SIN_BOLA = range(2)
    
    def __init__ (self, fase):
        self.fase = fase
        self.tiempo = tiempo

    def posicion(self, tiempo):
        argumento = (tiempo + fase) * 2 * np.pi / PERIODO
        return (np.sin(argumento) * RADIO_GIRO + CENTRO_GIRO[0], np.cos(argumento) * RADIO_GIRO + CENTRO_GIRO[1])

        self.posicion = posicion()



def get_jugadores(cant_jugadores, radio_circ, tiempo, periodo):
    jugadores = []
    for pos in range(cant_jugadores):



    # no me gust,a pero paso los nros a float, para hacer la division    

        radianes = 2 * np.pi * (float(pos) / cant_jugadores) + (float(tiempo) / periodo)
        jugadores.append(np.array((int(np.cos(radianes) * radio_circ), int(np.sin(radianes) * radio_circ))))
    return jugadores

class bola(object):
    GIRANDO, VOLANDO = range(2)

    def __init__ (self, position):
        self.position = position
        self.state = bola.GIRANDO
    
        

    def vuela(self, objetivo):
        self.state = bola.VOLANDO        





pg.init()
screen = pg.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS, SCREEN_DEPTH)
relos = pg.time.Clock()
periodo = PERIODO_INIT
velocidad = VELOCIDAD_INIT

jugadores = get_jugadores(NUMERO_JUGADORES, RADIO_GIRO, 0, periodo)

#dist_fuentes = DIST_INIT

#target = np.array(SCREEN_SIZE) / 2

cuanto = 0

while True:


    # Un cuanto, es un instante de tiempo, que va desde 0 hasta el periodo. Cuando llega al periodo, el dibujo se repite, por lo que el ciclo vuelve a empezar.

        screen.fill(SCREEN_COLOR)
        pg.draw.circle(screen, ONDAS_COLOR, CENTRO_GIRO, RADIO_GIRO, ONDAS_ANCHO)



        # ESC para salir, arriba y abajo cambia la distancia entre fuentes, izquierda y derecha cambia el periodo, y boton izquierdo del mouse cambia el foco.
        for event in pg.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_UP:
                    if dist_fuentes < SCREEN_HEIGHT:
                        dist_fuentes = dist_fuentes + DIST_PASO
                        fuentes = get_fuentes(dist_fuentes)
                        print dist_fuentes
                if event.key == K_DOWN:
                    if dist_fuentes > DIST_PASO:
                        dist_fuentes = dist_fuentes - DIST_PASO
                        fuentes = get_fuentes(dist_fuentes)
                        print dist_fuentes
                if event.key == K_LEFT:
                    if periodo > PERIODO_PASO:
                        periodo = periodo - PERIODO_PASO
                        print periodo
                if event.key == K_RIGHT:
                    if periodo < SCREEN_WIDTH:
                        periodo = periodo + PERIODO_PASO
                        print periodo
            if event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT_BUTTON:
                    target = pg.mouse.get_pos()
                    print target


        # de cada fuente...
        for jugador in jugadores:
            pg.draw.circle(screen, (255, 255, 255), jugador + CENTRO_GIRO, 30, 30)

        jugadores = get_jugadores(NUMERO_JUGADORES, RADIO_GIRO, cuanto * velocidad, periodo)

#            desfasaje = int(np.linalg.norm(fuente - target)) % periodo - periodo
#            # ...dibujo cada onda
#            for onda in range(SCREEN_HEIGHT * 2 / periodo):
#                if periodo * onda + cuanto + desfasaje > 0:
#                    pg.draw.circle(screen, ONDAS_COLOR, fuente, periodo * onda + cuanto + desfasaje, ONDAS_ANCHO)

        # muestro la pantalla

        pg.display.update()

        cuanto = cuanto + 1

        relos.tick(FPS)
