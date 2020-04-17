
LOAD_AHEAD = 10000
VISIBLE_TIME = 2000
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MAX_SPRITES = 500

KEYS = 8
TOLERANCE = 10
TIME_TO_RELOAD = 1

ENEMY_SPRITES = ['A', 'B', 'C', 'D', 'D', 'C', 'B', 'A'] # mirrored sprites for easy glancing for key
NOTES = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'co']
key_map = {97: 0, 115: 1, 100: 2, 102: 3, 106: 4, 107: 5, 108: 6, 59: 7}

PLAYER_DIFFICULTY = 2


global tempo
global media
global earned

global score

global enemy_list


def init():
    global score
    score = 0
    global earned

    global media
    media = {}

    global tempo
    tempo = 1000 * 60 / 4 / 150  # 120 bpm

