import pygame as pg
from pygame.locals import *


# TYPE ALIASES
color = pg.Color
Rect = pg.Rect
Vector2 = pg.Vector2
Coordinate = tuple[int, int] | list[int, int] | Vector2

rect_contains = Rect.contains
rect_collidepoint = Rect.collidepoint


# COLORS
YELLOW = color('yellow')
PURPLE = color('purple')
WHITE = color('white')
BLACK = color('black')
GREEN = color('green')
BLUE = color('blue')
GRAY = color('gray')
RED = color('red')


# GAME CONTANTS
TIME_CONSTANT = 0.025
BALL_SPEED = 1
MAX_LEVEL = 5
CUST_UPGRADE = (5, 10, 15, 20, 25, 30)
MAX_POINTS   = (5, 10, 20, 30, 40, 50)

RADIUS_CELLS = 50
SELECT_RADIUS = RADIUS_CELLS * 1.3
SELECT_WIDTH = 2
SELECT_COLOR = WHITE
TARGET_COLOR = GRAY

SCORE_COLOR = WHITE

BG_COLOR = BLACK


# WINDOWS CONSTANTS
SIZE = (1280, 720)
WIDTH = SIZE[0]
HEIGHT = SIZE[1]
WINDOW_NAME = 'Remake Jelly Go!'


# PRESETS
pg.init()
pg.font.init()
screen = pg.display.set_mode(SIZE)
pg.display.set_caption(WINDOW_NAME)
clock = pg.time.Clock()
running = True