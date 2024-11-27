import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Sequence Game")

# Define colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# Define shapes with positions and colors
shapes = [
    {'color': RED, 'rect': pygame.Rect(50, 50, 200, 200), 'sound': 'asset\game5\sound1.wav'},
    {'color': GREEN, 'rect': pygame.Rect(350, 50, 200, 200), 'sound': 'asset\game5\sound2.wav'},
    {'color': BLUE, 'rect': pygame.Rect(50, 350, 200, 200), 'sound': 'asset\game5\sound3.wav'},
    {'color': YELLOW, 'rect': pygame.Rect(350, 350, 200, 200), 'sound': 'asset\game5\sound4.wav'},
]

# Load sounds
for shape in shapes:
    try:
        shape['tone'] = pygame.mixer.Sound(shape['sound'])
    except pygame.error as e:
        print(f"Error loading sound {shape['sound']}: {e}")
        pygame.quit()
        sys.exit()

def draw_shapes():
    """Draw the shapes on the screen."""
    for shape in shapes:
        pygame.draw.rect(screen, shape['color'], shape['rect'])
    pygame.display.flip()

def play_sequence(sequence, speed=0.5):
    """Play the sequence of shapes and sounds."""
    for index in sequence:
        shape = shapes[index]
        # Highlight the shape
        pygame.draw.rect(screen, WHITE, shape['rect'])
        pygame.display.flip()
        # Play the sound
        shape['tone'].play()
        time.sleep(speed)
        # Redraw the shape in its original color
        pygame.draw.rect(screen, shape['color'], shape['rect'])
        pygame.display.flip()
        time.sleep(0.2)

def get_player_input(sequence):
    """Get and validate the player's input."""
    input_sequence = []
    while len(input_sequence) < len(sequence):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, shape in enumerate(shapes):
                    if shape['rect'].collidepoint(pos):
                        # Flash the shape
                        pygame.draw.rect(screen, WHITE, shape['rect'])
                        pygame.display.flip()
                        shape['tone'].play()
                        time.sleep(0.3)
                        pygame.draw.rect(screen, shape['color'], shape['rect'])
                        pygame.display.flip()
                        input_sequence.append(idx)
                        # Check if the input is correct so far
                        if input_sequence[-1] != sequence[len(input_sequence)-1]:
                            return False
        pygame.display.flip()
    return True

def main():
    """Main game loop."""
    sequence = []
    level = 1
    running = True

    while running:
        screen.fill(BLACK)
        draw_shapes()
        pygame.display.flip()
        pygame.time.wait(1000)

        # Add a new random shape to the sequence
        next_shape = random.randint(0, len(shapes)-1)
        sequence.append(next_shape)

        # Play the sequence
        play_sequence(sequence, speed=max(0.1, 0.5 - level * 0.02))

        # Get player's input
        correct = get_player_input(sequence)

        if not correct:
            # Game Over
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over!', True, WHITE)
            screen.blit(text, (150, 250))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        else:
            level += 1
            pygame.time.wait(500)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
