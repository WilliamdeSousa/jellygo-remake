from game.presets import *
from math import atan2, sin, cos, dist

def tangent_point(A: Coordinate, B: Coordinate, radius: float) -> Coordinate:
    angle = atan2(B[1] - A[1], B[0] - A[0])
    x = cos(angle) * radius + A[0]
    y = sin(angle) * radius + A[1]
    return (x, y)

def line_tangent(A: Coordinate, B: Coordinate, bipolar: bool) -> Coordinate:
    if bipolar:
        return tangent_point(A, B, SELECT_RADIUS), tangent_point(B, A, SELECT_RADIUS)
    else:
        return tangent_point(A, B, SELECT_RADIUS), B

def mouse_colide(obj):
    return dist(pg.mouse.get_pos(), obj.position.xy) <= SELECT_RADIUS

def rect_two_dots(A: Coordinate, B: Coordinate) -> Rect:
    width = abs(B[0] - A[0])
    height = abs(B[1] - A[1])
    x = min(A[0], B[0])
    y = min(A[1], B[1])
    return Rect(x, y, width, height)

def is_select(cell, rect):
    return rect_collidepoint(rect, cell.position) or rect_contains(rect, cell.rect) or rect_contains(cell.rect, rect)