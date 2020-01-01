import numpy as np

# Physics constants
C = 0.005  # Dampening constant
K = 0.001  # Spring constant
G = 1  # Grativational constant

# Drawing constants
POINT_SIZE = 6

# Camera settings
delta = 0.1
FOCAL_LENGTH = 1000
MV_FWD = delta * np.array([[0], [0], [-1]], dtype=float)
MV_BCK = delta * np.array([[0], [0], [1]], dtype=float)
MV_RIGHT = delta * np.array([[-1], [0], [0]], dtype=float)
MV_LEFT = delta * np.array([[1], [0], [0]], dtype=float)

# Screen constants
W, H = 1200, 1200
CX, CY = W // 2, H // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
ORANGE = (252, 173, 3)
GRAY = (100, 100, 100)

# Shape initialization constants
BASE_ROT_X = 0.0004
BASE_ROT_Y = 0.0015
BASE_ROT_Z = 0.0003
STARTING_LOCATIONS = np.array(
    [
        [-1, 1, -1, 1, -1, 1, -1, 1],
        [1, 1, -1, -1, 1, 1, -1, -1],
        [1, 1, 1, 1, -1, -1, -1, -1],
    ],
    dtype=float,
)
STARTING_DOTS = [(0), (1), (2), (3), (4), (5), (6), (7)]
STARTING_DIAGS = [
    (0, 3),
    (1, 7),
    (5, 6),
    (4, 2),
    (1, 4),
    (3, 6),
    (1, 2),
    (3, 5),
    (4, 7),
    (0, 6),
    (0, 5),
    (2, 7),
]
STARTING_EDGES = [
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
STARTING_SIDES = [
    (0, 1, 3, 2),
    (1, 5, 7, 3),
    (0, 1, 5, 4),
    (0, 4, 6, 2),
    (2, 6, 7, 3),
    (4, 5, 7, 6),
]
