import pygame
import settings

import globals

pygame.mixer.init()
pygame.mixer.set_num_channels(128)

class Enemy(pygame.sprite.Sprite):
    TOLERANCE = 500
    DEFAULT_SPEED = 2
    POINTS = 100

    def __init__(self, appear_time, player_key, duration=1, sprite_option='A', note='piano/g', music_only=False):
        self.appear_time = appear_time
        self.play_time = self.appear_time + settings.VISIBLE_TIME
        self.end_time = self.play_time + (duration * settings.TEMPO)
        self.duration = duration
        self.player_key = player_key  # 1-8
        self.sprite_option = sprite_option.upper()  # a-d
        self.present = False
        self.image = None
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/enemy" + self.sprite_option + ".png")
        w, h = pygame.display.get_surface().get_size()
        channel_size = w / 8
        self.rect = self.image.get_rect()
        self.rect.center = (channel_size * self.player_key + channel_size / 2, -self.image.get_rect()[0])
        self.played = False
        self.note = pygame.mixer.Sound("assets/"+note+".wav")
        self.dead = False
        self.music_only = music_only
        if music_only:
            self.image = pygame.image.load("assets/clear.png")

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
                    globals.score -= 50
                self.kill()

    def play(self):
        print("PLAYING NOTE")
        self.note.play()

    def shot_attempt(self, shot_time):
        pts = 0  # lose points for missing
        globals.earned = 0
        if self.present and (self.play_time - self.TOLERANCE <= shot_time) and (shot_time <= self.end_time + self.TOLERANCE):
            globals.earned = 100 * (1 - abs(self.play_time - shot_time) / self.TOLERANCE)
            globals.score += globals.earned
            #print(pts)
            self.appear_time = shot_time
            #print(self.play_time - self.TOLERANCE, shot_time, self.end_time + self.TOLERANCE)
            #self.kill()
            self.image = pygame.image.load("assets/clear.png")
            self.dead = True
        return pts
