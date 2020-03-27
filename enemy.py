import pygame
import settings


class Enemy(pygame.sprite.Sprite):
    TOLERANCE = 100
    DEFAULT_SPEED = 2
    POINTS = 100

    def __init__(self, press_time, player_key, duration=1, sprite_option='A'):
        self.appear_time = press_time
        self.end_time = press_time + duration * settings.TEMPO
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
        self.rect.center = (channel_size * self.player_key - channel_size / 2, -self.image.get_rect()[0])

    def appear(self):
        self.present = True

    def update(self):
        if self.present:
            w, h = pygame.display.get_surface().get_size()
            speed = h / settings.SCREEN_HEIGHT * settings.VISIBLE_TIME / 1000
            # speed = h / 600 * self.DEFAULT_SPEED
            self.rect = self.rect.move(0, speed)
            x, y = self.rect.center
            if y > h - (2 * h / 10):
                self.kill()

    def shot_attempt(self, shot_time):
        pts = -100  # lose points for missing
        if self.appear_time - self.TOLERANCE <= shot_time <= self.end_time + self.TOLERANCE:
            pts = 100 * (1 - abs(self.appear_time - shot_time) / self.TOLERANCE)
            self.appear_time = shot_time

        self.kill()
        return pts
