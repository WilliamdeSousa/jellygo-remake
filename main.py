from game.game import *

while running:

    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            game.control.mouse_down()
        if event.type == MOUSEBUTTONUP:
            game.control.mouse_up()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                game.control.select_all()
    
    game.run()