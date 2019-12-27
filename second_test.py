import pygame as pg
import numpy as np
import sys 

W, H = 600, 600
CX, CY = W//2, H//2
SCREEN_CENTER = np.array([[CX], [CY]])

FOCAL_LENGTH = 200

screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()

# Columns -> positions 1 to 7

def get_starting_locations():
    return np.array([
        [-1, 1, -1, 1, -1, 1, -1, 1],
        [1, 1, -1, -1, 1, 1, -1, -1],
        [1, 1, 1, 1, -1, -1, -1, -1]
    ], dtype=float)

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


class Engine:
    def __init__(self, position):
        self.P = position

    def apply_movement(self):
        pass

    def apply_rotation(self):
        pass

    def get_screen_location(self):
        pos_float = SCREEN_CENTER + FOCAL_LENGTH/self.P[2,:] * self.P[:2, :]
        return np.rint(pos_float).astype(int)


def main_loop(locs, lines):
    # Move back starting position slightly
    locs = locs + np.array([[0], [0], [3]], dtype=float)
    engine = Engine(locs)

    while True:
        dt = clock.tick() / 1000

        # Find exit event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Find key events
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            pass
        if keys[pg.K_DOWN]:
            pass
        if keys[pg.K_LEFT]:
            pass
        if keys[pg.K_RIGHT]:
            pass    

        # Calculate new positions

        # Draw all items
        screen.fill((255, 255, 255))
        L = engine.get_screen_location()

        for col in L.T:
            pg.draw.circle(screen, (0,0,0), col, 6)

        for p1, p2 in lines:
            pg.draw.line(screen, (0,0,0), L[:,p1], L[:,p2], 3)

        pg.display.flip()


def main():
    locs = get_starting_locations()
    lines = get_starting_lines()
    main_loop(locs, lines)


if __name__ == "__main__":
    main()