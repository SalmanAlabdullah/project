# dinosaur-game

import random
import sys
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dino_image = pygame.image.load("dino.png")
cactus_image = pygame.image.load("cactus.png")

# Game variables
dino_x, dino_y = 50, HEIGHT - 70
cactus_x = WIDTH
cactus_y = HEIGHT - 70
score = 0
jumping = False
jump_count = 10

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True

    if jumping:
        if jump_count >= -10:
            neg = 1 if jump_count >= 0 else -1
            dino_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    cactus_x -= 10
    if cactus_x < -50:
        cactus_x = WIDTH
        score += 1

    # Collision detection
    if (dino_x + 50 > cactus_x) and (dino_x < cactus_x + 50) and (dino_y + 50 > cactus_y):
        print("Game Over! Your score was:", score)
        pygame.quit()
        sys.exit()

    # Draw the dinosaur and cactus
    screen.blit(dino_image, (dino_x, dino_y))
    screen.blit(cactus_image, (cactus_x, cactus_y))

    # Update the display
    pygame.display.update()

pygame.quit()
