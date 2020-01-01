import numpy as np

import constants as const

# REDO SOON - project onto vector instead
class Boundary:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def through_boundary(x, y, z):
        return self.a * x + self.b * y + self.c * z + d > 0


class Connection:
    def __init__(self, column1, column2, base_length, damp_const, string_const):
        self.col1 = column1
        self.col2 = column2
        self.l = base_length
        self.c = damp_const
        self.k = string_const


class Engine:
    def __init__(self, position):
        # P defines current 3d positions of vertices
        self.P = position
        # M defines vertex movement
        self.M = np.zeros_like(self.P)
        # con defines connections between vertices
        self.connections = []
        self.boundaries = []
        self.cog = self.calc_center_of_gravity(self.P)
        self.screen_center = np.array([[const.CX], [const.CY]])

    def add_connection(self, *args):
        self.connections.append(Connection(*args))

    def add_boundary(self, *args):
        self.boundaries.append(Boundary(*args))

    def calc_contraction(self):
        A = np.zeros_like(self.P)
        for conn in self.connections:
            # Spring force acceleration
            vec = self.P[:, conn.col1] - self.P[:, conn.col2]
            dist = np.linalg.norm(vec)
            stretch = dist - conn.l
            A[:, conn.col1] -= vec * stretch * conn.k
            A[:, conn.col2] += vec * stretch * conn.k
            # Dampening effect
            A[:, conn.col1] -= conn.c * self.M[:, conn.col1]
            A[:, conn.col2] -= conn.c * self.M[:, conn.col2]

        self.M += A
        self.P += self.M

    def calc_boundaries(self):
        for boundary in self.boundaries:
            pass

    def calc_center_of_gravity(self, M):
        n_points = np.ma.size(M, 1)
        return (1 / n_points * np.sum(M, 1)).reshape(3, 1)

    def apply_movement(self, move_vec):
        self.P += move_vec
        self.cog = self.calc_center_of_gravity(self.P)

    def apply_vertex_shift(self, column, move_vec):
        # Movement occurs in xy plane
        move_vec = np.append(move_vec, 0)
        self.P[:, column] += move_vec * 0.005

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

    def get_screen_location(self):
        pos_float = (
            self.screen_center + const.FOCAL_LENGTH / self.P[2, :] * self.P[:2, :]
        )
        return np.rint(pos_float).astype(int)
