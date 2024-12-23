import pygame
import sys
import random
import time

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
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
        {'color': RED, 'rect': pygame.Rect(50, 50, 200, 200), 'sound': 'sounds/sound1.wav'},
        {'color': GREEN, 'rect': pygame.Rect(level_width - 250, 50, 200, 200), 'sound': 'sounds/sound2.wav'},
        {'color': BLUE, 'rect': pygame.Rect(50, level_height - 250, 200, 200), 'sound': 'sounds/sound3.wav'},
        {'color': YELLOW, 'rect': pygame.Rect(level_width - 250, level_height - 250, 200, 200), 'sound': 'sounds/sound4.wav'},
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

    def render_text(surface, text, font, color, x, y, max_width):
        """
        Helper function to render text with word wrapping.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (x, y))
            y += font.get_linesize() + 5



    def get_player_input(sequence):
        """Get and validate the player's input."""
        input_sequence = []
        start_time = time.time()

        while len(input_sequence) < len(sequence):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    surface_rect = surface.get_abs_offset()
                    x -= surface_rect[0]
                    y -= surface_rect[1]

                    for idx, shape in enumerate(shapes):
                        if shape['rect'].collidepoint((x, y)):
                            pygame.draw.rect(surface, WHITE, shape['rect'])
                            pygame.display.flip()
                            shape['tone'].play()
                            time.sleep(0.3)
                            pygame.draw.rect(surface, shape['color'], shape['rect'])
                            pygame.display.flip()
                            input_sequence.append(idx)
                            if input_sequence[-1] != sequence[len(input_sequence) - 1]:
                                return False, time.time() - start_time

        return True, time.time() - start_time
    


    def instruction_screen(surface, screen_width, screen_height):
        """
        Displays the instruction screen.

        :param surface: The Pygame surface where the instructions will be displayed.
        :param screen_width: The width of the screen.
        :param screen_height: The height of the screen.
        """
        # Colors and Fonts
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        title_font = pygame.font.SysFont(None, 50)
        text_font = pygame.font.SysFont(None, 30)

        # Instruction text
        instructions = (
            "1. Wait for a musical tone to play.",
            "2. Quickly tap the object on the screen associated with the tone."
        )

        # Flag to keep the screen running
        running = True

        while running:
            surface.fill(WHITE)

            # Title
            title_text = title_font.render("Game Instructions", True, BLUE)
            surface.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

            # Render each line of instructions
            y_offset = 150  # Starting y position for the instructions
            for line in instructions:
                render_text(surface, line, text_font, BLACK, 50, y_offset, screen_width - 100)
                y_offset += text_font.get_linesize() + 20  # Adjust spacing between lines

            # Navigation instructions
            nav_text = text_font.render("Press ENTER or CLICK to proceed.", True, RED)
            surface.blit(nav_text, (screen_width // 2 - nav_text.get_width() // 2, screen_height - 100))

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Proceed to the next screen
                        running = False
                # if any mouse button is pressed, proceed to the next screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

            # Update the screen
            pygame.display.flip()

    # Main game loop
    sequence = []
    level = 1
    max_attempts = max_attempts_arg
    attempts = 0
    running = True
    score = 0
    results = []  # JSON-compatible results

    # Display instructions
    instruction_screen(surface, win_width, win_height)

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
        correct, time_taken = get_player_input(sequence)

        if not correct:
            # Game Over
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over!', True, WHITE)
            surface.blit(text, (level_width // 2 - text.get_width() // 2, level_height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        else:
            score += 1
            results.append({
                "Game": "Memory Sequence",
                "Weight": 1.0,
                "Sequence Length": len(sequence),
                "Time Taken": time_taken
            })
            level += 1
            pygame.time.wait(500)

        attempts += 1

    # Display final stats before exiting
    surface.fill(BLACK)
    final_score_text = f"Final Level Reached: {level - 1}"
    render_text_1(surface, final_score_text, pygame.font.Font(None, 36), WHITE, 50, 50)
    pygame.display.flip()
    pygame.time.wait(2000)

    return results, score

def render_text_1(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.
