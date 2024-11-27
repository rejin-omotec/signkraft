import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape Orientation Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Load or define the shape (we'll use a simple arrow shape)
def create_arrow_surface(color):
    surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.polygon(surface, color, [(50, 0), (100, 50), (75, 50), (75, 100), (25, 100), (25, 50), (0, 50)])
    return surface

# Function to rotate surface around its center
def rot_center(image, angle):
    rotated_image = pygame.transform.rotozoom(image, -angle, 1)  # Negative angle to rotate correctly
    rotated_rect = rotated_image.get_rect(center=(0, 0))
    return rotated_image, rotated_rect

# Create reference and user shapes
reference_shape = create_arrow_surface(GRAY)
user_shape = create_arrow_surface(BLACK)

# Random reference angle
reference_angle = random.randint(0, 359)

# User angle starts at 0
user_angle = 0

# Game font
font = pygame.font.SysFont(None, 48)

# Game loop
running = True
while running:
    clock.tick(60)  # Limit to 60 frames per second

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        user_angle = (user_angle + 2) % 360
    if keys[pygame.K_RIGHT]:
        user_angle = (user_angle - 2) % 360
    if keys[pygame.K_SPACE]:
        # Check if the user's angle matches the reference angle within a tolerance
        angle_difference = abs((user_angle - reference_angle) % 360)
        if angle_difference <= 5 or angle_difference >= 355:
            message = font.render("Correct!", True, (0, 255, 0))
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 50))
            pygame.display.flip()
            pygame.time.wait(2000)  # Pause for 2 seconds
            # Reset for next round
            reference_angle = random.randint(0, 359)
            user_angle = 0
        else:
            message = font.render("Try Again!", True, (255, 0, 0))
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 50))
            pygame.display.flip()
            pygame.time.wait(1000)  # Pause for 1 second

    # Drawing
    screen.fill(WHITE)

    # Draw reference shape
    ref_rotated_image, ref_rotated_rect = rot_center(reference_shape, reference_angle)
    ref_rect = ref_rotated_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
    screen.blit(ref_rotated_image, ref_rect)

    # Draw user-controlled shape
    user_rotated_image, user_rotated_rect = rot_center(user_shape, user_angle)
    user_rect = user_rotated_image.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))
    screen.blit(user_rotated_image, user_rect)

    # Display instructions
    instructions = font.render("Match the orientation!", True, BLACK)
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 20))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
