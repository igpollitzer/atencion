# -*- coding: utf-8 -*-

import numpy as np
import pygame as pg
from pygame.locals import *
from sys import exit
from random import randrange
from random import random

from sandals import *

LEFT_BUTTON = 1
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (110, 110, 110)
GRIS_CLARO = (160, 160, 160)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

SCREEN_SIZE = (1280, 720)
SCREEN_WIDTH = SCREEN_SIZE[0]
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_DEPTH = 32
SCREEN_FLAGS = 0
SCREEN_COLOR = GRIS
FPS = 60
DIST_INIT = 50
DIST_PASO = 5
PERIODO_PASO = 5

RADIO_GIRO = SCREEN_HEIGHT / 2.5
CENTRO_GIRO = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
PERIODO = 100

class Parametros(object):
    def __init__(self):
        self.nro_jugadores = 8
        self.pases = 0
        self.numero = 0
        self.cuanto = 0
        self.mensaje_tiempo = 1
        self.mensaje_transparencia = 25
        self.pase_tiempo = 0.5
        self.pase_minimo = 0.75
        self.pase_maximo = 1

globales = Parametros()


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
        self.color = ROJO

        #para cuando vuele
        self.partida = 0
        self.destino = (0, 0)        
        self.paso = 0        

    def pasar(self, jugador):
        self.posicion = self.get_pos(globales.cuanto)
        self.partida = globales.cuanto
        arribo = globales.cuanto + globales.pase_tiempo
        self.destino = jugador.get_pos(arribo)
        self.paso = (self.destino - self.posicion) / float(globales.pase_tiempo)
        self.desfasaje = jugador.desfasaje
        self.estado = Pelota.VOLANDO
    
    def get_pos(self, tiempo):
    
        salida = np.array((0, 0))
    
        if self.estado is Pelota.GIRANDO:
    
            x = int(RADIO_GIRO * np.sin((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[0])
            y = int(RADIO_GIRO * np.cos((tiempo + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[1])
            salida = np.array((x, y))

        if self.estado is Pelota.VOLANDO:

            self.posicion = self.posicion + self.paso

            if np.linalg.norm(self.posicion - self.destino) < 1:
            
                self.posicion = self.destino
                self.estado = Pelota.GIRANDO
                self.color = ROJO

            salida = np.array((int(self.posicion[0]), int(self.posicion[1])))
        return salida
            



def get_jugadores(cant_jugadores):
    jugadores = []
    for pos in range(cant_jugadores):
        #if (pos + 1) % 2 == 1:
        if random() > 0.5:
            next_color = BLANCO
        else:
            next_color = NEGRO
        jugadores.append(Jugador(pos * PERIODO / cant_jugadores, next_color))
    return jugadores

def programa():

    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS, SCREEN_DEPTH)
    relos = pg.time.Clock()

    jugadores = get_jugadores(globales.nro_jugadores)
    pelota = Pelota()
    globales.cuanto = 0
    arroja = randrange(globales.pase_minimo, globales.pase_maximo, 1)
    globales.pases = 0

    globales.numero = str(randrange(101, 999, 1))

    texto_fondo = randrange(240, 360, 1)
    texto = pg.font.SysFont("monospace", 200, True)
    mensaje = texto.render(globales.numero, 0, GRIS_CLARO)
    mensaje.set_alpha(0)
    mensaje_flag = 0

    while globales.cuanto >= 0:

        screen.fill(SCREEN_COLOR)
        screen.blit(mensaje, (SCREEN_WIDTH/3, SCREEN_HEIGHT/3))


        for event in pg.event.get():
            if event.type is QUIT:
                pg.quit()
                return
            if event.type is KEYDOWN:
                if event.key is K_ESCAPE:
                    pg.quit()
                    return
                if event.key is K_UP:
                    if pelota.estado is Pelota.GIRANDO:
                        rand = randrange(0, globales.nro_jugadores, 1)
                        while jugadores[rand].desfasaje is pelota.desfasaje:
                            rand = randrange(0, globales.nro_jugadores, 1)
                        pelota.pasar(jugadores[rand])
                if event.key is K_DOWN:
                    pelota.__init__()
                if event.key is K_LEFT:
                    pass
                if event.key is K_RIGHT:
                    pass
            if event.type is MOUSEBUTTONDOWN:
                if event.button is LEFT_BUTTON:
                    pass
        # de cada fuente...
        for jugador in jugadores:
            pg.draw.circle(screen, jugador.color, jugador.get_pos(globales.cuanto), 40, 10)

        pg.draw.circle(screen, pelota.color, pelota.get_pos(globales.cuanto), 30, 30)

        if globales.cuanto >= arroja and pelota.estado is not pelota.VOLANDO:
            rand = randrange(0, globales.nro_jugadores, 1)
            while jugadores[rand].desfasaje is pelota.desfasaje:
                rand = randrange(0, globales.nro_jugadores, 1)
            pelota.pasar(jugadores[rand])
            arroja = globales.cuanto + randrange(globales.pase_minimo, globales.pase_maximo, 1)
            if jugadores[rand].color is BLANCO:
                globales.pases = globales.pases + 1

        if globales.cuanto > texto_fondo:
            if mensaje_flag is 0 and mensaje.get_alpha() < globales.mensaje_transparencia:
                mensaje.set_alpha(mensaje.get_alpha() + 1)
            if mensaje_flag is 1:
                mensaje.set_alpha(mensaje.get_alpha() - 1)
                if mensaje.get_alpha() is 0:
                    mensaje_flag = 2
            if globales.cuanto == texto_fondo + globales.mensaje_tiempo:
                mensaje_flag = 1
                
        pg.display.update()

        globales.cuanto = globales.cuanto + 1
        relos.tick(FPS)
        if globales.cuanto > 601 and pelota.estado is Pelota.GIRANDO:
            pg.quit()


with window("Atención"):
    label("Bienvenido!")

    with flow(padx=10):
        set_jugadores = editBox(globales.nro_jugadores)
        label(" jugadores.")

    with flow(padx=10):
        set_tiempo = editBox(globales.mensaje_tiempo)
        label(" segundos.")

    with flow(padx=10):
        set_transparencia = editBox(globales.mensaje_transparencia)
        label("% de transparencia.")

    with flow(padx=10):
        set_pase = editBox(globales.pase_tiempo)
        label(" segundos de pase.")

    with flow(padx=10):
        set_minimo = editBox(globales.pase_minimo)
        label(" segundos mínimo.")

    with flow(padx=10):
        set_maximo = editBox(globales.pase_maximo)
        label(" segundos máximo.")

    @button("Cómo fue?")
    def boton_rta():
        showInfo(message = ("Se realizaron ", globales.pases, " pases, y el número fué el ", globales.numero, "."))

    @button("Arranca!")
    def boton_arranca():
        globales.nro_jugadores=int(set_jugadores.text)
        globales.mensaje_tiempo=int(set_tiempo.text) * FPS
        globales.mensaje_transparencia=int(int(set_transparencia.text) * 2.55)
        globales.pase_tiempo=int(float(set_pase.text) * FPS)
        globales.pase_minimo=int(float(set_minimo.text) * FPS)
        globales.pase_maximo=int(float(set_maximo.text) * FPS)
		
        programa()
