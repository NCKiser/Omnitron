import pygame
import time
import random

screen_width = 640
screen_height = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

enemyList = ['enemyA', 'enemyB', 'enemyC', 'enemyD']


class Block(pygame.sprite.Sprite):
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
        self.rect.y = self.rect.y + 1
        if (self.rect.center[1] > screen_height):
            self.rect.center = (self.rect.center[0], self.rect.center[1] - screen_height)
        if (self.rect.center[1] < 0):
            self.rect.center = (self.rect.center[0], self.rect.center[1] + screen_height)


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

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(50):
    # This represents a block
    block = Block(enemyList[random.randint(0, len(enemyList) - 1)] + '.png')

    # Set a random location for the block

    block.image = pygame.transform.rotate(block.image, 180)
    block.rect = block.image.get_rect()

    block.rect.center = (random.randrange(screen_width), random.randrange(screen_height))

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

player = Block('mainShip.png')
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(WHITE)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()

    if (pygame.mouse.get_pressed()[0]):
        laser = Laser()
        laser.rect.center = player.rect.center
        laser_sprites.add(laser)
        all_sprites_list.add(laser)

    # Fetch the x and y out of the list,
    # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    player.rect.center = pos

    block_list.update()
    laser_sprites.update()
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()

pygame.display.flip()
