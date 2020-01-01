import constants as const
import pygame as pg
import pygame.gfxdraw as gfxdraw
import numpy as np


class Dot:
    def __init__(self, color, column):
        self.color = color
        self.columns = column

    def draw(self, screen, point_locations, size=const.POINT_SIZE):
        pg.draw.circle(screen, self.color, point_locations, size)


class Line:
    def __init__(self, color, columns):
        self.color = color
        self.columns = columns

    def draw(self, screen, point_locations):
        gfxdraw.line(screen, *point_locations[:, 0], *point_locations[:, 1], self.color)


class Side:
    def __init__(self, color, columns):
        self.color = color
        self.columns = columns

    def draw(self, screen, point_locations):
        pg.draw.polygon(
            screen,
            self.color,
            (
                point_locations[:, 0],
                point_locations[:, 1],
                point_locations[:, 2],
                point_locations[:, 3],
            ),
        )


class DrawManager:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.S = None
        self.handle_mouseclick = False

    def set_screen_locations(self, new_locations):
        self.S = new_locations

    def add_dot(self, color, column):
        dot = Dot(color, column)
        self.objects.append(dot)

    def add_line(self, color, columns):
        line = Line(color, columns)
        self.objects.append(line)

    def add_side(self, color, columns):
        side = Side(color, columns)
        self.objects.append(side)

    def draw_all_objects(self):
        for draw_object in self.objects:
            point_locations = self.S[:, draw_object.columns]
            draw_object.draw(self.screen, point_locations)

    def get_mouse_dot(self, mouse_pos):
        square = np.power(self.S - mouse_pos, 2)
        dists = np.sqrt(square[0, :] + square[1, :])
        mouse_cols = np.where(np.isclose(dists, 0, atol=10))[0]
        if mouse_cols.size > 1:
            mouse_cols = mouse_cols[:1]
        return mouse_cols
