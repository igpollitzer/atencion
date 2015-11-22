# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:51:08 2015

@author: igpollitzer
"""

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
PERIODO_INIT = 300
VELOCIDAD_INIT = 10

dist_jugadores = PERIODO_INIT / NUMERO_JUGADORES

class cuerpo(object):
    
    def __init__(self, posicion):
        self.posicion = posicion
        self.velocidad = np.array((0,0))
        self.aceleracion = np.array((0,0))
    
    def update(self):
        self.posicion = self.posicion + self.velocidad
        self.velocidad = self.velocidad + self.aceleracion
        pg.draw.circle(screen, (255, 255, 255), self.posicion.astype(int), 30, 30)

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS, SCREEN_DEPTH)
relos = pg.time.Clock()

carlos = cuerpo((SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
carlos.velocidad = np.array((4,0))

modulo = np.linalg.norm(np.subtract(CENTRO_GIRO, carlos.posicion))

cuanto = 0

while True:

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
                pass
#                carlos.aceleracion = (np.array(pg.mouse.get_pos()) - carlos.posicion) /100.


    screen.fill(SCREEN_COLOR)

    acentrip = np.divide(np.power(np.linalg.norm(carlos.velocidad), 2), modulo)
    rcentrip = np.divide(np.subtract(CENTRO_GIRO, carlos.posicion), modulo)

    carlos.aceleracion = np.multiply(acentrip, rcentrip)

#    print np.subtract(carlos.posicion, CENTRO_GIRO)
#    print modulo
#    print acentrip
#    print rcentrip

#**************CONCLUSION: CARLOS SE ME VA AL CUERNO*********************


    carlos.update()

    pg.display.update()

    cuanto = cuanto + 1

    relos.tick(FPS)   