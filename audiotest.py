import time
import random
import pygame
import pygame.midi
import mido
import io


screen_width = 640
screen_height = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
# print(pygame.mixer.init())


screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED, 32)

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

state = 0
level_loading = 0

playhead = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(WHITE)
    if state == 0:
        # MENU
        if pygame.mouse.get_pressed():
            print("Mouse Clicked")
            state = 1
            level_loading = 1
    if state == 1:
        if level_loading == 1:
            print("LOADING LEVEL")
            audio_track = mido.MidiFile("music/abridge_d.mid").tracks[1]
            playhead = 0
            level_loading = 0
        else:
            pass
            if playhead < len(audio_track):
                print(audio_track[playhead])

                playhead += 1
            else:
                print("Audio track ended")



    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()

pygame.display.flip()
