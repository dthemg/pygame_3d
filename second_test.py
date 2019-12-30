import pygame as pg
import pygame.gfxdraw as gfxdraw
import numpy as np
import sys

W, H = 1200, 1200
CX, CY = W // 2, H // 2
SCREEN_CENTER = np.array([[CX], [CY]])

FOCAL_LENGTH = 1000

delta = 0.01
MV_FWD = delta * np.array([[0], [0], [-1]], dtype=float)
MV_BCK = delta * np.array([[0], [0], [1]], dtype=float)
MV_RIGHT = delta * np.array([[-1], [0], [0]], dtype=float)
MV_LEFT = delta * np.array([[1], [0], [0]], dtype=float)

POINT_SIZE = 6
LINE_SIZE = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
ORANGE = (252, 173, 3)

screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

# Columns -> positions 1 to 7


def get_starting_locations():
    return np.array(
        [
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [1, 1, -1, -1, 1, 1, -1, -1],
            [1, 1, 1, 1, -1, -1, -1, -1],
        ],
        dtype=float,
    )


def get_starting_dots():
    return [(0), (1), (2), (3), (4), (5), (6), (7)]


def get_starting_lines():
    return [
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7),
    ]


def get_starting_sides():
    return [
        (0, 1, 3, 2),
        (1, 5, 7, 3),
        (0, 1, 5, 4),
        (0, 4, 6, 2),
        (2, 6, 7, 3),
        (4, 5, 7, 6),
    ]


class Dot:
    def __init__(self, color, column):
        self.color = color
        self.columns = column

    def draw(self, screen, point_locations):
        pg.draw.circle(screen, self.color, point_locations, POINT_SIZE)


class Line:
    def __init__(self, color, columns):
        self.color = color
        self.columns = columns

    def draw(self, screen, point_locations):
        gfxdraw.line(
            screen, *point_locations[:, 0], *point_locations[:, 1],  self.color
        )


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
            )
        )


class DrawManager:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.S = None

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


class Engine:
    def __init__(self, position):
        self.P = position
        self.cog = self.calc_center_of_gravity(self.P)

    def calc_center_of_gravity(self, M):
        n_points = np.ma.size(M, 1)
        return (1 / n_points * np.sum(M, 1)).reshape(3, 1)

    def apply_movement(self, move_vec):
        self.P += move_vec
        self.cog = self.calc_center_of_gravity(self.P)

    def apply_rotation(self, alpha, beta, gamma):
        A = np.array(
            [
                [1, 0, 0],
                [0, np.cos(alpha), np.sin(alpha)],
                [0, -np.sin(alpha), np.cos(alpha)],
            ],
            dtype=float,
        )
        B = np.array(
            [
                [np.cos(beta), 0, -np.sin(beta)],
                [0, 1, 0],
                [np.sin(beta), 0, np.cos(beta)],
            ],
            dtype=float,
        )
        C = np.array(
            [
                [np.cos(gamma), np.sin(gamma), 0],
                [-np.sin(gamma), np.cos(gamma), 0],
                [0, 0, 1],
            ],
            dtype=float,
        )
        R = np.dot(A, np.dot(B, C))
        P_center = self.P - self.cog
        P_center = np.dot(R, P_center)
        self.P = P_center + self.cog
        # self.P = np.dot(R, self.P)

    def get_screen_location(self):
        pos_float = SCREEN_CENTER + FOCAL_LENGTH / self.P[2, :] * self.P[:2, :]
        return np.rint(pos_float).astype(int)


def main_loop(dots, locs, lines, sides):
    # Move back starting position slightly
    locs = locs + np.array([[0], [0], [10]], dtype=float)
    engine = Engine(locs)

    # Draw manager setup
    draw_manager = DrawManager(screen)
    for i, side_columns in enumerate(sides):
        if i == 5:
            draw_manager.add_side(ORANGE, side_columns)
        else:
            continue
            #draw_manager.add_side(BLUE, side_columns)
    for line_columns in lines:
        draw_manager.add_line(WHITE, line_columns)
    for dot_columns in dots:
        draw_manager.add_dot(WHITE, dot_columns)

    while True:
        dt = clock.tick() / 100

        # Find exit event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Handle key presses
        movement = np.array([[0], [0], [0]], dtype=float)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            movement += MV_FWD
        if keys[pg.K_DOWN]:
            movement += MV_BCK
        if keys[pg.K_LEFT]:
            movement += MV_LEFT
        if keys[pg.K_RIGHT]:
            movement += MV_RIGHT

        # Calculate new positions
        engine.apply_movement(movement)
        engine.apply_rotation(0.0004, 0.0015, 0.0003)

        # Draw all items
        screen.fill(BLACK)
        L = engine.get_screen_location()

        draw_manager.S = L
        draw_manager.draw_all_objects()

        pg.display.flip()


def main():
    locs = get_starting_locations()
    dots = get_starting_dots()
    lines = get_starting_lines()
    sides = get_starting_sides()
    main_loop(dots, locs, lines, sides)


if __name__ == "__main__":
    main()
