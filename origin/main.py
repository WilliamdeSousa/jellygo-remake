# imports
import pygame as pg
from pygame.locals import *
import game

# pg setups
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

# game configs
blue_team = game.Team('blue', True)
red_team = game.Team('red')

blue_cell = game.Cell(blue_team, 3, 'default', [500, 275])
blue_cel2 = game.Cell(blue_team, 1, 'default', [500, 425])
red_cell = game.Cell(red_team, 2, 'default', [800, 350])

# main loop
while running:

    # check events
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            game.mouse_pressed()
        if event.type == MOUSEBUTTONUP:
            game.check_click()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                game.select_all()

    # background
    game.background(screen)

    # render game
    game.render(screen)

    # show the game
    pg.display.flip()
    
    clock.tick(60) # limite FPS to 60
