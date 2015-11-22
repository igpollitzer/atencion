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
PERIODO = 300
VELOCIDAD_INIT = 2

dist_jugadores = PERIODO_INIT / NUMERO_JUGADORES

class jugador(object):
    def __init__(self, desfasaje):
        self.arco = 0
        self.desfasaje = desfasaje
        self.posicion = self.get_pos(self.arco)

    def get_pos(self, arco):
        x = RADIO_GIRO * np.sin((arco + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[0]
        y = RADIO_GIRO * np.cos((arco + self.desfasaje) * 2 * np.pi / PERIODO) + CENTRO_GIRO[1]
        return np.array((x, y))

