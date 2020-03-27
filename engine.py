import pygame
import time
import random

from enemy import Enemy

screen_width = 640
screen_height = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pressed = ' '


class Ship(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, image):
        """ Constructor. Pass in the color of the block,
        and its size. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('assets/' + image)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        w, h = pygame.display.get_surface().get_size()
        self.rect.center = w / 2, h - h / 10
        if pressed == ' ':
            self.rect.center = w / 2, h - h / 10
        if pressed == 'APressed':
            self.rect.center = w / 16, h - h / 10
        if pressed == 'SPressed':
            self.rect.center = w / 5.3, h - h / 10
        if pressed == 'DPressed':
            self.rect.center = w / 3.2, h - h / 10
        if pressed == 'FPressed':
            self.rect.center = w / 2.275, h - h / 10
        if pressed == 'JPressed':
            self.rect.center = w / 1.77, h - h / 10
        if pressed == 'KPressed':
            self.rect.center = w / 1.45, h - h / 10
        if pressed == 'LPressed':
            self.rect.center = w / 1.225, h - h / 10
        if pressed == 'SCPressed':
            self.rect.center = w / 1.065, h - h / 10

class Laser(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its size. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('assets/' + 'singleLaser.png')

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)

    def update(self):
        self.rect.y = self.rect.y - 2
        if self.rect.center[1] < 0:
            self.kill()


pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED, 32)

enemy_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    enemy = Enemy(press_time=0, player_key=1)

    # Add the block to the list of objects
    enemy_list.add(enemy)
    all_sprites_list.add(enemy)

player = Ship('mainShip.png')
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

reloading = False
KEYS = 8
TOLERANCE = 10
TIME_TO_RELOAD = 1
firing_a = False
firing_s = False
firing_d = False
firing_f = False
firing_j = False
firing_k = False
firing_l = False
firing_SC = False

KEYMAP = {97: 1, 115: 2, 100: 3, 102: 4, 106: 5, 107: 6, 108: 7, 59: 8}

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_a:
                pressed = 'APressed'
                firing_a = True
            if event.key == pygame.K_s:
                pressed = 'SPressed'
                firing_s = True
            if event.key == pygame.K_d:
                pressed = 'DPressed'
                firing_d = True
            if event.key == pygame.K_f:
                pressed = 'FPressed'
                firing_f = True
            if event.key == pygame.K_j:
                pressed = 'JPressed'
                firing_j = True
            if event.key == pygame.K_k:
                pressed = 'KPressed'
                firing_k = True
            if event.key == pygame.K_l:
                pressed = 'LPressed'
                firing_l = True
            if event.key == pygame.K_SEMICOLON:
                pressed = 'SCPressed'
                firing_SC = True
        if event.type == pygame.KEYUP:
            print(event.key)
            if event.key == pygame.K_a:
                firing_a = False
            if event.key == pygame.K_s:
                firing_s = False
            if event.key == pygame.K_d:
                firing_d = False
            if event.key == pygame.K_f:
                firing_f = False
            if event.key == pygame.K_j:
                firing_j = False
            if event.key == pygame.K_k:
                firing_k = False
            if event.key == pygame.K_l:
                firing_l = False
            if event.key == pygame.K_SEMICOLON:
                firing_SC = False
        if event.type == pygame.QUIT:
            done = True

    if firing_a or firing_s or firing_d or firing_f or firing_j or firing_k or firing_l or firing_SC:
        laser = Laser()
        laser.rect.center = player.rect.center
        laser.rect.y = laser.rect.y - 20
        laser.rect.x = laser.rect.x - 11
        laser_sprites.add(laser)
        all_sprites_list.add(laser)
            
    # Clear the screen
    screen.fill(WHITE)
    # Draw targetting array
    w, h = pygame.display.get_surface().get_size()
    line_end_loc = h - (2 * h / 10)
    pygame.draw.line(screen, RED, (0, line_end_loc,), (w, line_end_loc))
    for i in range(0, KEYS):
        pygame.draw.circle(screen, RED, (w / KEYS * (i + .5), line_end_loc), radius=h / screen_height * TOLERANCE)
        pygame.draw.circle(screen, WHITE, (w / KEYS * (i + .5), line_end_loc), radius=h / screen_height * TOLERANCE - 1)
    for enemy in enemy_list:
        enemy.appear()
    enemy_list.update()
    laser_sprites.update()
    all_sprites_list.update()
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what wfdafdae've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()

pygame.display.flip()
