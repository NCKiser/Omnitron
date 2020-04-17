import pygame
import time
import settings
from LevelInterface import Level

settings.init()

settings.SCREEN_WIDTH = 640
settings.SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (131, 214, 62)

pressed = ' '

intro = True


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
        self.rect.center = (settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

    def update(self):
        self.rect.y = self.rect.y - 2
        if self.rect.center[1] < settings.SCREEN_HEIGHT / 1.65:
            self.kill()


font_name = pygame.font.match_font('arial')


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


SHIPSPRITE = pygame.image.load('assets/mainShip.png')


def draw_ship_title(x, y):
    screen.blit(SHIPSPRITE, (x, y))


ENEMYSPRITE = pygame.image.load('assets/enemyD.png')


def draw_enemy_title(x, y):
    screen.blit(ENEMYSPRITE, (x, y))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_text_title(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def level_cleared(level=0):
    time.sleep(5)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SCALED, 32)

enemy_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

player = Ship('mainShip.png')
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

settings.score = 0
settings.earned = -1

reloading = False

firing_a = False
firing_s = False
firing_d = False
firing_f = False
firing_j = False
firing_k = False
firing_l = False
firing_SC = False

level_state = 0
menu = 0
level_start = 0
# level_name = "TakeOnMeIntro.txt.csv"
# level_name = "moonlightSonata.txt.csv"
# level_name = "drumTest.txt.csv"
# level_name = "Storms.txt.csv"
# level_name = "DejaVu.txt.csv"
# level_name = "TitleSong.txt.csv"
level_list = ['DejaVu.txt']
tempo_list = [150]
level_number = 0
level = None
# -------- Main Program Loop -----------
while intro:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            intro = False
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill(WHITE)
    draw_ship_title(settings.SCREEN_WIDTH / 2 + 13, 350)
    draw_enemy_title(settings.SCREEN_WIDTH / 2, 160)
    TEXTTITLE = pygame.font.Font('freesansbold.ttf', 115)
    TSURF, TRECT = text_objects("Omn tron", TEXTTITLE)
    draw_text_title(screen, 'I', 100, settings.SCREEN_WIDTH / 2 + 15, 181)
    draw_text(screen, 'Press any key to continue', 18, settings.SCREEN_WIDTH / 2, 450)
    TRECT.center = ((settings.SCREEN_WIDTH / 2), (settings.SCREEN_HEIGHT / 2))
    screen.blit(TSURF, TRECT)
    pygame.display.update()

while not done:

    d_time = clock.tick(60)
    if menu:
        level_name = "level1.csv"
    else:
        if level_state == 0:
            print("Loading Level")
            level_name = level_list[level_number] + ".csv"
            settings.tempo = 1000 * 60 / 4 / tempo_list[level_number]
            print("Tempo =", settings.tempo)
            level = Level(level_name)
            d_time = clock.tick(60)  # start once loaded, as leading takes a lot of time
            level_start = pygame.time.get_ticks()
            level_state = 1
        elif level_state == 1:
            current_time = pygame.time.get_ticks() - level_start
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    level.shoot(event.key, current_time)
                    try:
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
                    except KeyError:
                        print("invalid key")
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
                # score += 63
            if level.done():
                draw_text(screen, 'Level Cleared!', 18, settings.SCREEN_WIDTH / 2, 200)
                pygame.display.flip()
                level_cleared(level_number)
                level_number = level_number + 1
                level_state = 0

            # Clear the screen
            screen.fill(WHITE)
            # Draw targetting array
            if settings.drawP is True:
                draw_text(screen, 'Poor', 18, settings.SCREEN_WIDTH / 2, 450)
            if settings.drawG is True:
                draw_text(screen, 'Good', 18, settings.SCREEN_WIDTH / 2, 450)
            if settings.drawE is True:
                draw_text(screen, 'Excellent', 18, settings.SCREEN_WIDTH / 2, 450)
            if settings.drawPe is True:
                draw_text(screen, 'Perfect', 18, settings.SCREEN_WIDTH / 2, 450)

            w, h = pygame.display.get_surface().get_size()
            line_end_loc = h - (2 * h / 10)
            pygame.draw.line(screen, RED, (0, line_end_loc,), (w, line_end_loc))
            for i in range(0, settings.KEYS):
                pygame.draw.circle(screen, RED, (w / settings.KEYS * (i + .5), line_end_loc),
                                   radius=h / settings.SCREEN_HEIGHT * settings.TOLERANCE)
                pygame.draw.circle(screen, WHITE, (w / settings.KEYS * (i + .5), line_end_loc),
                                   radius=h / settings.SCREEN_HEIGHT * settings.TOLERANCE - 1)

            player.update()
            laser_sprites.update()
            level.update(current_time)
            level.draw(screen)
            all_sprites_list.draw(screen)
            draw_text(screen, str(round(settings.score)), 18, settings.SCREEN_WIDTH / 2, 10)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second

pygame.quit()

pygame.display.flip()
