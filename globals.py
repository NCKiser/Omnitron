# globals.py
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
