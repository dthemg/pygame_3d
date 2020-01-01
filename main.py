from engine import Engine
from drawing import DrawManager

import constants as const

import pygame as pg
import numpy as np
import sys


screen = pg.display.set_mode((const.W, const.H))
clock = pg.time.Clock()


def setup_engine():
    # Move back starting position slightly
    locs = const.STARTING_LOCATIONS + np.array([[0], [0], [10]], dtype=float)
    engine = Engine(locs)

    for p1, p2 in const.STARTING_EDGES:
        # Base length of all edge connections is 2
        engine.add_connection(p1, p2, 2, const.C, const.K)

    for p1, p2 in const.STARTING_DIAGS:
        # Base length of all diag connections is sqrt(2)*2
        engine.add_connection(p1, p2, np.sqrt(2) * 2, const.C, const.K)

    # TODO: work on boundary checks & gravitational pull
    engine.add_boundary(1, 3, 4, 5)
    engine.set_rotation(const.BASE_ROT_X, const.BASE_ROT_Y, const.BASE_ROT_Z)

    return engine


def setup_draw_manager():
    draw_manager = DrawManager(screen)
    for i, side_columns in enumerate(const.STARTING_SIDES):
        if i == 5:
            draw_manager.add_side(const.ORANGE, side_columns)
    for line_columns in const.STARTING_EDGES:
        draw_manager.add_line(const.WHITE, line_columns)
    for line_columns in const.STARTING_DIAGS:
        draw_manager.add_line(const.GRAY, line_columns)
    for dot_columns in const.STARTING_DOTS:
        draw_manager.add_dot(const.WHITE, dot_columns)

    return draw_manager


def main_loop():
    engine = setup_engine()
    draw_manager = setup_draw_manager()

    handle_mouseclick = False
    mouse_drag = False
    drag_column = None

    while True:
        dt = clock.tick() / 50

        # Find exit event and mouse presses
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_mouseclick = True
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    mouse_pos = np.array([[mouse_x], [mouse_y]], dtype=int)
                    pg.mouse.get_rel()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    engine.set_rotation(
                        const.BASE_ROT_X, 
                        const.BASE_ROT_Y, 
                        const.BASE_ROT_Z)
                    
                    mouse_drag = False

        # Handle key presses
        camera_movement = np.array([[0], [0], [0]], dtype=float)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            camera_movement += MV_FWD
        if keys[pg.K_DOWN]:
            camera_movement += MV_BCK
        if keys[pg.K_LEFT]:
            camera_movement += MV_LEFT
        if keys[pg.K_RIGHT]:
            camera_movement += MV_RIGHT

        # Calculate new positions
        engine.apply_movement(camera_movement)
        engine.apply_rotation()
        if mouse_drag:
            mouse_move = np.array(pg.mouse.get_rel(), dtype=float)
            engine.apply_vertex_shift(drag_column, mouse_move)
        else:
            engine.calc_contraction()
            engine.calc_boundaries()

        draw_manager.set_screen_locations(engine.get_screen_location())

        if handle_mouseclick:
            mouse_col = draw_manager.get_mouse_dot(mouse_pos)
            if mouse_col.size > 0:
                mouse_drag = True
                drag_column = mouse_col[0]
                engine.set_rotation(0, 0, 0)
            handle_mouseclick = False

        # Draw all items
        screen.fill(const.BLACK)

        draw_manager.draw_all_objects()

        pg.display.flip()


def main():
    main_loop()


if __name__ == "__main__":
    main()
