import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Recall Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define shapes and their positions
shapes = ['circle', 'square', 'triangle']
shape_positions = {
    'circle': (150, 300),
    'square': (300, 300),
    'triangle': (450, 300)
}

def draw_shape(shape, color):
    if shape == 'circle':
        pygame.draw.circle(WIN, color, shape_positions['circle'], 50)
    elif shape == 'square':
        pygame.draw.rect(WIN, color, pygame.Rect(250, 250, 100, 100))
    elif shape == 'triangle':
        pygame.draw.polygon(WIN, color, [
            (450, 250),
            (400, 350),
            (500, 350)
        ])

def show_sequence(sequence):
    for shape in sequence:
        WIN.fill(BLACK)
        draw_shape(shape, WHITE)
        pygame.display.update()
        time.sleep(1)
        WIN.fill(BLACK)
        pygame.display.update()
        time.sleep(0.5)

def get_player_input(sequence_length):
    input_sequence = []
    while len(input_sequence) < sequence_length:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check which shape was clicked
                for shape in shapes:
                    sx, sy = shape_positions[shape]
                    if shape == 'circle':
                        distance = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
                        if distance <= 50:
                            input_sequence.append('circle')
                    elif shape == 'square':
                        rect = pygame.Rect(250, 250, 100, 100)
                        if rect.collidepoint(x, y):
                            input_sequence.append('square')
                    elif shape == 'triangle':
                        # Simple bounding box check for triangle
                        if 400 <= x <= 500 and 250 <= y <= 350:
                            input_sequence.append('triangle')
        # Redraw shapes
        WIN.fill(BLACK)
        for shape in shapes:
            draw_shape(shape, WHITE)
        pygame.display.update()
    return input_sequence

def main():
    initial_sequence_length = 3  # Starting sequence length
    sequence_length = initial_sequence_length
    sequence = [random.choice(shapes) for _ in range(sequence_length)]
    score = 0

    while True:
        # Show the sequence to the player
        show_sequence(sequence)

        # Display prompt to the player
        WIN.fill(BLACK)
        font = pygame.font.SysFont(None, 35)
        text = font.render("Now it's your turn! Repeat the sequence.", True, WHITE)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

        # Display clickable shapes
        for shape in shapes:
            draw_shape(shape, WHITE)
        pygame.display.update()

        # Get player's input
        player_input = get_player_input(len(sequence))

        # Check if the player's input matches the sequence
        if player_input == sequence:
            score += 1
            sequence_length += 1
            sequence.append(random.choice(shapes))
            font = pygame.font.SysFont(None, 55)
            text = font.render("Correct!", True, GREEN)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            time.sleep(1)
        else:
            font = pygame.font.SysFont(None, 55)
            text = font.render("Incorrect! Starting over...", True, RED)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            pygame.display.update()
            time.sleep(2)
            # Reset the game variables
            sequence_length = initial_sequence_length
            sequence = [random.choice(shapes) for _ in range(sequence_length)]
            score = 0

if __name__ == "__main__":
    main()