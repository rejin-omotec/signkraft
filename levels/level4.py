import pygame
import random
import time

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height):
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
    max_attempts = 3
    attempts = 0

    # Clock
    clock = pygame.time.Clock()

    while running and attempts < max_attempts:
        current_time = time.time()
        surface.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Translate mouse position to the subsurface coordinates
                x, y = event.pos

                # Get the position of the subsurface relative to the main window
                surface_rect = surface.get_abs_offset()

                # Adjust the mouse click coordinates relative to the subsurface
                x -= surface_rect[0]
                y -= surface_rect[1]

                # Check if the mole was clicked
                if mole_rect and mole_rect.collidepoint((x, y)):
                    hit_time = current_time - mole_appeared_time
                    response_times.append(hit_time)
                    correct_hits += 1
                    mole_rect = None
                    MOLE_APPEAR_TIME *= SPEED_INCREASE_RATE
                    if MOLE_APPEAR_TIME < MOLE_MIN_TIME:
                        MOLE_APPEAR_TIME = MOLE_MIN_TIME

        # Spawn a new mole if there is none on the screen
        if mole_rect is None and current_time >= next_mole_time:
            x = random.randint(0, level_width - MOLE_SIZE)
            y = random.randint(0, level_height - MOLE_SIZE)
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
            attempts += 1  # Increment attempts when a mole times out

        # Draw mole
        if mole_rect:
            pygame.draw.rect(surface, BLACK, mole_rect)

        # Display stats
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            response_text = font.render(f"Avg Response Time: {avg_response_time:.2f}s", True, BLACK)
            surface.blit(response_text, (10, 10))

        accuracy = correct_hits / total_moles * 100 if total_moles > 0 else 0
        accuracy_text = font.render(f"Accuracy: {accuracy:.1f}%", True, BLACK)
        surface.blit(accuracy_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    # Display final stats before exiting
    surface.fill(WHITE)
    final_score_text = f"Final Accuracy: {accuracy:.1f}%"
    render_text(surface, final_score_text, font, BLACK, 50, 50)
    pygame.display.update()
    pygame.time.wait(2000)

    return correct_hits, attempts


def render_text(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.
