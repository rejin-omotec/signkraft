import pygame
import sys
import random
import time

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height):
    """
    Runs the Memory Sequence Game inside the provided surface.

    :param surface: The Pygame surface where the game level is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Define colors
    WHITE = (255, 255, 255)
    RED = (220, 20, 60)
    GREEN = (34, 139, 34)
    BLUE = (30, 144, 255)
    YELLOW = (255, 215, 0)
    BLACK = (0, 0, 0)

    # Define shapes with positions and colors
    shapes = [
        {'color': RED, 'rect': pygame.Rect(50, 50, 200, 200), 'sound': 'asset/game5/sound1.wav'},
        {'color': GREEN, 'rect': pygame.Rect(level_width - 250, 50, 200, 200), 'sound': 'asset/game5/sound2.wav'},
        {'color': BLUE, 'rect': pygame.Rect(50, level_height - 250, 200, 200), 'sound': 'asset/game5/sound3.wav'},
        {'color': YELLOW, 'rect': pygame.Rect(level_width - 250, level_height - 250, 200, 200), 'sound': 'asset/game5/sound4.wav'},
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
        """Draw the shapes on the subsurface."""
        for shape in shapes:
            pygame.draw.rect(surface, shape['color'], shape['rect'])
        pygame.display.flip()

    def play_sequence(sequence, speed=0.5):
        """Play the sequence of shapes and sounds."""
        for index in sequence:
            shape = shapes[index]
            # Highlight the shape
            pygame.draw.rect(surface, WHITE, shape['rect'])
            pygame.display.flip()
            # Play the sound
            shape['tone'].play()
            time.sleep(speed)
            # Redraw the shape in its original color
            pygame.draw.rect(surface, shape['color'], shape['rect'])
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
                    # Adjust the mouse click coordinates to the subsurface coordinates
                    x, y = event.pos
                    surface_rect = surface.get_abs_offset()
                    x -= surface_rect[0]
                    y -= surface_rect[1]

                    for idx, shape in enumerate(shapes):
                        if shape['rect'].collidepoint((x, y)):
                            # Flash the shape
                            pygame.draw.rect(surface, WHITE, shape['rect'])
                            pygame.display.flip()
                            shape['tone'].play()
                            time.sleep(0.3)
                            pygame.draw.rect(surface, shape['color'], shape['rect'])
                            pygame.display.flip()
                            input_sequence.append(idx)
                            # Check if the input is correct so far
                            if input_sequence[-1] != sequence[len(input_sequence)-1]:
                                return False
            pygame.display.flip()
        return True

    # Main game loop
    sequence = []
    level = 1
    max_attempts = 3
    attempts = 0
    running = True

    while running and attempts < max_attempts:
        surface.fill(BLACK)
        draw_shapes()
        pygame.display.flip()
        pygame.time.wait(1000)

        # Add a new random shape to the sequence
        next_shape = random.randint(0, len(shapes) - 1)
        sequence.append(next_shape)

        # Play the sequence
        play_sequence(sequence, speed=max(0.1, 0.5 - level * 0.02))

        # Get player's input
        correct = get_player_input(sequence)

        if not correct:
            # Game Over
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over!', True, WHITE)
            surface.blit(text, (level_width // 2 - text.get_width() // 2, level_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        else:
            level += 1
            update_score_callback(1)  # Increase score by 1 for each successful sequence
            pygame.time.wait(500)

        attempts += 1

    # Display final stats before exiting
    surface.fill(BLACK)
    final_score_text = f"Final Level Reached: {level - 1}"
    render_text(surface, final_score_text, pygame.font.Font(None, 36), WHITE, 50, 50)
    pygame.display.flip()
    pygame.time.wait(2000)

    return level - 1, attempts

def render_text(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.
