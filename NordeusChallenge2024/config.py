import screeninfo

monitor = screeninfo.get_monitors()[0]
M = 30
N = 30
FIELDSIZE = 16
TITLE = "Guess the island"
WIDTH = N * FIELDSIZE
HEIGHT = M * FIELDSIZE
SCREEN_WIDTH = monitor.width
SCREEN_HEIGHT = monitor.height
PANEL_HEIGHT = 60

URL = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"

BOTTOM = 1 << 0
RIGHT = 1 << 1
TOP = 1 << 2
LEFT = 1 << 3

# color scheme
BGCOLOR = (40,40,40)
OFFWHITE = (242, 242, 242)
WRONG_SELECTION_COLOR = (182, 81, 47)
SUCCESS_COLOR = (53, 118, 255)

WATER_COLOR = (142, 219, 245)
LAND_COLORS = [
    (224, 216, 202),
    (194, 163, 109),
    (255, 209, 130),
    (145, 217, 151),
    (108, 212, 117),
    (58, 161, 67),
    (49, 72, 51),
    (138, 131, 84),
    (112, 110, 95),
    (181, 177, 148)
]

BORDER_WIDTH = 1
BORDER_COLOR = OFFWHITE
