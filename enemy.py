import io
import os

import pygame
import settings

pygame.mixer.init()
pygame.mixer.set_num_channels(2048)
settings.drawM = True
settings.drawP = False
settings.drawG = False
settings.drawE = False
settings.drawPe = False


def load_image(imagename):
    if imagename not in settings.media:
        print("loading {}".format(imagename))

        # https://stackoverflow.com/questions/44358334/play-video-and-sound-in-python-with-ram-cache
        settings.media[imagename] = pygame.image.load(imagename)
    return settings.media[imagename]


def load_sound(soundname):
    if soundname not in settings.media:
        print("loading {}".format(soundname))
        # https://stackoverflow.com/questions/44358334/play-video-and-sound-in-python-with-ram-cache
        settings.media[soundname] = pygame.mixer.Sound(soundname)
    return settings.media[soundname]


def play_sound(soundname):
    settings.media[soundname].play()


class EnemyPrototype:

    def __init__(self, appear_time, player_key, duration=1, sprite_option='A', instrument='piano', note='g4',
                 music_only=False):
        self.appear_time = appear_time
        self.play_time = self.appear_time + settings.VISIBLE_TIME
        self.end_time = self.play_time + (duration * settings.tempo)
        self.duration = duration
        self.player_key = player_key  # 1-8
        self.sprite_option = sprite_option.upper()  # a-d
        load_image("assets/enemy" + self.sprite_option + ".png")
        # print("Note: " + os.path.join(instrument, note) + ".wav")
        try:
            self.sound_name = ("assets/" + os.path.join(instrument, note) + ".wav")
            load_sound(self.sound_name)
        except FileNotFoundError:
            self.sound_name = ("assets/electric_piano/" + note + ".wav")
            load_sound(self.sound_name)
        self.music_only = music_only


class Enemy(pygame.sprite.Sprite):
    TOLERANCE = 300
    DEFAULT_SPEED = 2
    POINTS = 100

    def __init__(self, ep):
        self.appear_time = ep.appear_time
        self.play_time = self.appear_time + settings.VISIBLE_TIME
        self.end_time = self.play_time + (ep.duration * settings.tempo)
        self.duration = ep.duration
        self.player_key = ep.player_key  # 1-8
        self.sprite_option = ep.sprite_option.upper()  # a-d
        self.present = True
        self.image = None
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(load_image("assets/enemy" + self.sprite_option + ".png"), 180)
        w, h = pygame.display.get_surface().get_size()
        channel_size = w / 8
        self.rect = self.image.get_rect()
        self.rect.center = (channel_size * self.player_key + channel_size / 2, -self.image.get_rect()[0])
        self.played = False
        self.sound_name = ep.sound_name
        self.dead = False
        self.music_only = ep.music_only

    def update(self, current_time):
        if self.present:
            w, h = pygame.display.get_surface().get_size()
            line_end_loc = h - (2 * h / 10)
            dy = line_end_loc / settings.VISIBLE_TIME
            pos = dy * (current_time-self.appear_time)
            # speed = h / 600 * self.DEFAULT_SPEED
            self.rect.center = (self.rect.center[0], pos)
            x, y = self.rect.center

            if y >= line_end_loc and not self.played:
                self.play()
                self.played = True
            if y > h:
                if not self.dead and not self.music_only:
                    settings.score -= 250
                self.kill()

    def play(self):
        print("PLAYING NOTE")
        play_sound(self.sound_name)

    def shot_attempt(self, shot_time):
        pts = 0  # lose points for missing
        settings.earned = 0
        settings.drawM = True
        print(shot_time)
        print(type(shot_time))
        if self.present and (self.play_time - self.TOLERANCE <= shot_time) and (
                shot_time <= self.end_time + self.TOLERANCE):
            settings.earned = 100 * (1 - abs(self.play_time - shot_time) / self.TOLERANCE)
            settings.score += settings.earned
            if 0 < settings.earned < 51:
                settings.drawM = False
                settings.drawP = True
                settings.drawG = False
                settings.drawE = False
                settings.drawPe = False
            if 50 < settings.earned < 86:
                settings.drawM = False
                settings.drawP = False
                settings.drawG = True
                settings.drawE = False
                settings.drawPe = False
            if 85 < settings.earned < 100:
                settings.drawM = False
                settings.drawP = False
                settings.drawG = False
                settings.drawE = True
                settings.drawPe = False
            if settings.earned == 100:
                settings.drawM = False
                settings.drawP = False
                settings.drawG = False
                settings.drawE = False
                settings.drawPe = True
            # print(pts)
            self.appear_time = shot_time
            # print(self.play_time - self.TOLERANCE, shot_time, self.end_time + self.TOLERANCE)
            # self.kill()
            self.image = pygame.image.load("assets/clear.png")
            self.dead = True
        return pts
