import pygame
import random
import time

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Whack-a-Mole game inside the provided surface.

    :param surface: The Pygame surface where the game is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (169, 169, 169)  # Color for the fade effect when mole is clicked

    symbols = ['4', '7', '?', '#', '$']

    # Load the gold coin image (ensure the file is present in the correct directory)

    # Mole settings
    MOLE_SIZE = 50
    MOLE_APPEAR_TIME = 1.2  # initial time mole stays on screen
    MOLE_MIN_TIME = 1       # minimum time mole stays on screen
    SPEED_INCREASE_RATE = 0.85  # Mole appear time decreases by this factor after each mole

    # Fonts
    font = pygame.font.Font(None, 50)

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
            "1. Multiple symbols will be displayed. Pay attention to when the $ sign appears",
            "2. When the $ symbol appears, blink or press eneter to hit the symbol",
            "3. Do not blink or press enter when any other symbols show"
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Proceed to the next screen
                        running = False
                # if any mouse button is pressed, proceed to the next screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

            # Update the screen
            pygame.display.flip()

    # Game variables
    running = True
    mole_appeared_time = 0
    next_mole_time = 0
    max_attempts = max_attempts_arg
    attempts = 0
    weights = [2, 3, 5] # Weights for different levels of difficulty
    results = [0, 0, 0]


    # Clock
    clock = pygame.time.Clock()

    instruction_screen(surface, win_width, win_height)
    symbol = None
    surface.fill(BLACK)

    start_time = time.time()

    # Define global flag
    enter_pressed = False  # Flag to track Enter key state

    while running and attempts < max_attempts:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if not enter_pressed:  # Only trigger if not already pressed
                    enter_pressed = True  # Set flag to prevent retriggering
                
                # Check if the mole (coin) was clicked
                if symbol == '$':
                    results[attempts] = weights[attempts]
                    symbol = None
                    MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
                    if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
                        MOLE_APPEAR_TIME = MOLE_MIN_TIME

                else:
                    results[attempts] = 0
                    symbol = None
                    MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
                    if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
                        MOLE_APPEAR_TIME = MOLE_MIN_TIME

                attempts +=1
                surface.fill(BLACK)

            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                enter_pressed = False  # Reset flag when key is released

        # Spawn a new mole if there is none on the screen
        if symbol is None and current_time >= next_mole_time:
            # Ensure mole doesn't spawn in the top reserved area (RESERVED_HEIGHT)
            symbol = random.choice(symbols)
            render_text(surface, symbol, pygame.font.SysFont(None, 100), WHITE, 350, 200, 600)
            mole_appeared_time = current_time

        # Remove mole if time exceeded
        if symbol != None and current_time - mole_appeared_time >= MOLE_APPEAR_TIME:
            MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
            if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
                MOLE_APPEAR_TIME = MOLE_MIN_TIME
            if symbol == '$':
                results[attempts] = 0
                attempts += 1  # Increment attempts when a mole times out

            symbol = None
            surface.fill(BLACK)
            next_mole_time = current_time + 0.5  # wait 0.5 seconds before next mole


        pygame.display.flip()
        clock.tick(60)

    # Display final stats before exiting
    surface.fill(WHITE)
    pygame.display.update()

    end_time = time.time()-start_time

    print("result:", results, end_time)
    return results, end_time


def render_text_simple(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))