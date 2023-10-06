import pygame as pg
from math import atan2, sin, cos

pg.font.init()

SIZE = 50
SELECTION_SIZE = SIZE * 1.3

cells = []
cells_player = []
select_cells = 0
mouse_pos_initial = None
selection_rect = None
target_cell = None
selection = False

Coordinate = tuple[int, int] | list[int, int] | pg.math.Vector2

class Position:
    def __init__(self, center) -> None:
        self.center = center
        self.x = center[0]
        self.y = center[1]
    
class Team:
    def __init__(self, color, player = False) -> None:
        self.color = color
        self.player = player

class Score(pg.font.Font):
    def __init__(self, name: None, size: int) -> None:
        super().__init__(name, size)
        self.color = 'white'
        

class Cell:
    def __init__(self, team: Team, level: int, _class: str, position: Coordinate) -> None:
        self.team = team
        self.level = level
        self._class = _class
        self.limit = level * 10

        self.position = Position(position)
        self.select = False
        self.rect = [0, 0, 0, 0]
        self.points = 0
        self.growth_rate = 0.8
        self.score = Score(None, 50)

        cells.append(self)
        if self.team.player:
            cells_player.append(self)

    def render(self, screen: pg.Surface) -> None:

        self.rect = pg.draw.circle(screen, self.team.color, self.position.center, SIZE)

        # SELECTION
        mouse = pg.mouse.get_pos()
        center = self.position.center
        
        if self.select:
            pg.draw.circle(screen, 'white', center, SELECTION_SIZE, 2)

            ### LINE
            if self.get_distance(mouse) >= SELECTION_SIZE:
                attack_destine = mouse if target_cell is None else tangent_point(target_cell.position.center, center, SELECTION_SIZE)
                source = tangent_point(center, attack_destine, SELECTION_SIZE)
                pg.draw.line(screen, 'white', source, attack_destine, 2)
        
        ## TARGET
        if selection and self.get_distance(mouse) <= SELECTION_SIZE or select_cells > 1 and self.get_distance(mouse):
            pg.draw.circle(screen, 'gray', center, SELECTION_SIZE, 2)

        # SCORE
        score = self.score.render(f'{int(self.points)}', False, self.score.color)
        size = score.get_size()
        position = [self.position.x - (size[0] // 2), self.position.y - (size[1] // 2)]
        screen.blit(score, position)

    def update(self):
        # UPDATING POINTS
        if self.points <= self.limit:
            self.score.color = 'white'
            self.points += self.growth_rate * 0.025
        else:
            self.score.color = 'yellow'
        
        # UPDATING TARGETS
        if self.get_distance(pg.mouse.get_pos()) <= SELECTION_SIZE:
            global target_cell
            target_cell = self

    def get_distance(self, obj: Coordinate) -> float:
        return distance(self.position.center, obj)


# BASIC FUNCTIONS

## RENDER

def background(screen: pg.Surface):
    screen.fill('black')

def render(screen: pg.Surface):
    global mouse_pos_initial, target_cell
    target_cell = None
    for cell in cells:
        cell.update()

    for cell in cells:
        cell.render(screen)
    
    if pg.mouse.get_pressed()[0]:
        global selection_rect
        selection_rect = pg.Rect(rect(mouse_pos_initial, pg.mouse.get_pos()))
        pg.draw.rect(screen, 'white', selection_rect, 1)

## BASICS

def distance(A: Coordinate, B: Coordinate) -> float:
    """Distance beteween two points, A and B."""
    return ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** (1/2)

def tangent_point(A: Coordinate, B: Coordinate, radius: float) -> Coordinate:
    angle = atan2(B[1] - A[1], B[0] - A[0])
    x = cos(angle) * radius + A[0]
    y = sin(angle) * radius + A[1]
    return (x, y)

def rect(A: Coordinate, B: Coordinate) -> float:
    """Return a rect with two points"""
    left = A[0] if A[0] < B[0] else B[0]
    top = A[1] if A[1] < B[1] else B[1]
    width = abs(B[0] - A[0])
    height = abs(B[1] - A[1])
    return (left, top, width, height)

# GAME FUNCTIONS

## KEYBOARD

def select_all():
    """Select all your cells."""
    global selection
    selection = True
    for cell in cells_player:
        cell.select = True
    
## MOUSE

def check_click():
    global mouse_pos_initial, selection_rect, selection
    
    if target_cell is not None and (select_cells > 1 or not target_cell.select):
        print('atacando o bisho')
    
    mouse_pos = pg.mouse.get_pos()
    selection = False
    if distance(mouse_pos, mouse_pos_initial) < 5:
        for cell in cells_player:
            if cell.get_distance(mouse_pos) <= SIZE:
                cell.select = True
                selection = True
            else:
                cell.select = False
    else:
        for cell in cells_player:
            if pg.Rect.contains(selection_rect, cell.rect) or pg.Rect.contains(cell.rect, selection_rect) or pg.Rect.collidepoint(selection_rect, cell.position.center):
                cell.select = True
                selection = True
            else:
                cell.select = False


    mouse_pos_initial = None
    selection_rect = None

def mouse_pressed():
    global mouse_pos_initial
    mouse_pos_initial = pg.mouse.get_pos()
