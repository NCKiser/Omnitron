import pygame
import time
import random

from enemy import Enemy

screen_width = 640
screen_height = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


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
        self.rect.center = w/2, h-h/10


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

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(WHITE)
    # Draw targetting array
    w, h = pygame.display.get_surface().get_size()
    line_end_loc = h - (2 * h / 10)
    pygame.draw.line(screen, RED, (0, line_end_loc,), (w, line_end_loc))
    for i in range(0, KEYS):
        pygame.draw.circle(screen, RED, (w/KEYS*(i+.5), line_end_loc), radius=h/screen_height*TOLERANCE)
        pygame.draw.circle(screen, WHITE, (w / KEYS * (i + .5), line_end_loc), radius=h / screen_height * TOLERANCE-1)
    for enemy in enemy_list:
        enemy.appear()
    enemy_list.update()
    laser_sprites.update()
    all_sprites_list.update()
    all_sprites_list.draw(screen)


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()

pygame.display.flip()
