import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Mole settings
MOLE_SIZE = 50
MOLE_APPEAR_TIME = 2.0  # initial time mole stays on screen
MOLE_MIN_TIME = 0.5     # minimum time mole stays on screen
SPEED_INCREASE_RATE = 0.95  # Mole appear time decreases by this factor after each mole

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
running = True
mole_rect = None
mole_appeared_time = 0
next_mole_time = 0
response_times = []
correct_hits = 0
total_moles = 0

# Clock
clock = pygame.time.Clock()

# Main game loop
while running:
    current_time = time.time()
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mole_rect and mole_rect.collidepoint(event.pos):
                hit_time = current_time - mole_appeared_time
                response_times.append(hit_time)
                correct_hits += 1
                mole_rect = None
                MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
                if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
                    MOLE_APPEAR_TIME = MOLE_MIN_TIME

    # Spawn a new mole if there is none on the screen
    if mole_rect is None and current_time >= next_mole_time:
        x = random.randint(0, WIDTH - MOLE_SIZE)
        y = random.randint(0, HEIGHT - MOLE_SIZE)
        mole_rect = pygame.Rect(x, y, MOLE_SIZE, MOLE_SIZE)
        mole_appeared_time = current_time
        total_moles += 1

    # Remove mole if time exceeded
    if mole_rect and current_time - mole_appeared_time >= MOLE_APPEAR_TIME:
        mole_rect = None
        next_mole_time = current_time + 0.5  # wait 0.5 seconds before next mole
        MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
        if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
            MOLE_APPEAR_TIME = MOLE_MIN_TIME

    # Draw mole
    if mole_rect:
        pygame.draw.rect(screen, BLACK, mole_rect)

    # Display stats
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        response_text = font.render(f"Avg Response Time: {avg_response_time:.2f}s", True, BLACK)
        screen.blit(response_text, (10, 10))

    accuracy = correct_hits / total_moles * 100 if total_moles > 0 else 0
    accuracy_text = font.render(f"Accuracy: {accuracy:.1f}%", True, BLACK)
    screen.blit(accuracy_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
