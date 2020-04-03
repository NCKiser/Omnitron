import io
import os

import pygame
import settings

import globals

pygame.mixer.init()
pygame.mixer.set_num_channels(2048)
globals.drawM = True
globals.drawP = False
globals.drawG = False
globals.drawE = False
globals.drawPe = False


def load_sound(soundname):
    if soundname not in globals.media:
        # https://stackoverflow.com/questions/44358334/play-video-and-sound-in-python-with-ram-cache
        globals.media[soundname] = pygame.mixer.Sound(soundname)
    print("loading {}".format(soundname))
    return globals.media[soundname]


def play_sound(soundname):
    globals.media[soundname].play()


class Enemy(pygame.sprite.Sprite):
    TOLERANCE = 500
    DEFAULT_SPEED = 2
    POINTS = 100

    def __init__(self, appear_time, player_key, duration=1, sprite_option='A', instrument='piano', note='g4',
                 music_only=False):
        self.appear_time = appear_time
        self.play_time = self.appear_time + settings.VISIBLE_TIME
        self.end_time = self.play_time + (duration * settings.TEMPO)
        self.duration = duration
        self.player_key = player_key  # 1-8
        self.sprite_option = sprite_option.upper()  # a-d
        self.present = False
        self.image = None
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load("assets/enemy" + self.sprite_option + ".png"), 180)
        w, h = pygame.display.get_surface().get_size()
        channel_size = w / 8
        self.rect = self.image.get_rect()
        self.rect.center = (channel_size * self.player_key + channel_size / 2, -self.image.get_rect()[0])
        self.played = False
        print("Note: " + note + ".wav")
        try:
            self.sound_name = ("assets/" + os.path.join(instrument, note) + ".wav")
            load_sound(self.sound_name)
        except FileNotFoundError:
            self.sound_name = ("assets/piano/" + note + ".wav")
            load_sound(self.sound_name)
        self.dead = False
        self.music_only = music_only

    def appear(self):
        self.present = True

    def update(self, d_time):
        if self.present:
            w, h = pygame.display.get_surface().get_size()
            line_end_loc = h - (2 * h / 10)
            distance = line_end_loc * d_time / settings.VISIBLE_TIME
            # speed = h / 600 * self.DEFAULT_SPEED
            self.rect = self.rect.move(0, distance)
            x, y = self.rect.center

            if y >= line_end_loc and not self.played:
                self.play()
                self.played = True
            if y > h:
                if not self.dead and not self.music_only:
                    globals.score -= 250
                self.kill()

    def play(self):
        print("PLAYING NOTE")
        play_sound(self.sound_name)

    def shot_attempt(self, shot_time):
        pts = 0  # lose points for missing
        globals.earned = 0
        globals.drawM = True
        if self.present and (self.play_time - self.TOLERANCE <= shot_time) and (
                shot_time <= self.end_time + self.TOLERANCE):
            globals.earned = 100 * (1 - abs(self.play_time - shot_time) / self.TOLERANCE)
            globals.score += globals.earned
            if globals.earned > 0 and globals.earned < 51:
                globals.drawM = False
                globals.drawP = True
                globals.drawG = False
                globals.drawE = False
                globals.drawPe = False
            if globals.earned > 50 and globals.earned < 86:
                globals.drawM = False
                globals.drawP = False
                globals.drawG = True
                globals.drawE = False
                globals.drawPe = False
            if globals.earned > 85 and globals.earned < 100:
                globals.drawM = False
                globals.drawP = False
                globals.drawG = False
                globals.drawE = True
                globals.drawPe = False
            if globals.earned == 100:
                globals.drawM = False
                globals.drawP = False
                globals.drawG = False
                globals.drawE = False
                globals.drawPe = True
            # print(pts)
            self.appear_time = shot_time
            # print(self.play_time - self.TOLERANCE, shot_time, self.end_time + self.TOLERANCE)
            # self.kill()
            self.image = pygame.image.load("assets/clear.png")
            self.dead = True
        return pts
