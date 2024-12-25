import pygame
import sys
import random
import math
import queue
import time
from mods.audio_detect import SpeechRecognitionThread  # Replace with your actual module name


def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Shape Orientation Game inside the provided surface.

    :param surface: The Pygame surface where the game level is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """

    # speech detection setup
    speech_queue = queue.Queue(maxsize=10)
    speech_thread = SpeechRecognitionThread(audio_queue=speech_queue, language="english")
    speech_thread.start()

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Define colors
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    BLACK = (0, 0, 0)

    # Load or define the shape (arrow shape)
    def create_arrow_surface(color):
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color, [(50, 0), (100, 50), (75, 50), (75, 100), (25, 100), (25, 50), (0, 50)])
        return surface

    # Function to rotate surface around its center
    def rot_center(image, angle):
        rotated_image = pygame.transform.rotozoom(image, -angle, 1)  # Negative angle to rotate correctly
        return rotated_image
    
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
            "1. Try to ensure that the object on the left-hand side is in the same orientation as the target image."
        )

        # Flag to keep the screen running
        running = True

        while running:
            surface.fill(WHITE)

            # Title
            title_text = title_font.render("Game Instructions", True, BLUE)
            surface.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

            # Render the instruction
            y_offset = 150  # Starting y position for the instructions
            render_text(surface, instructions, text_font, BLACK, 50, y_offset, screen_width - 100)

            # Navigation instructions
            nav_text = text_font.render("Press ENTER to proceed.", True, RED)
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


    # Create reference and user shapes
    reference_shape = create_arrow_surface(GRAY)
    user_shape = create_arrow_surface(BLACK)

    # Random reference angle
    reference_angle = random.randint(0, 359)

    # User angle starts at 0
    user_angle = 0

    # Game font
    font = pygame.font.SysFont(None, 48)

    # Limit the number of attempts
    max_attempts = max_attempts_arg
    attempts = 0
    score = 0
    results = []  # JSON-compatible results
    weights = [1.0, 1.5, 2.0]  # Scoring weights


    # display instructions
    instruction_screen(surface, win_width, win_height)

    # Game loop
    running = True

    # Define button properties dynamically based on font size
    button_width = max(100, font.size("Submit")[0] + 20)
    button_height = 50
    button_margin = 20

    # Button positions relative to the subsurface
    left_button_rect = pygame.Rect(
        level_width // 4 - button_width // 2,
        level_height - button_height - button_margin,
        button_width,
        button_height
    )
    right_button_rect = pygame.Rect(
        3 * level_width // 4 - button_width // 2,
        level_height - button_height - button_margin,
        button_width,
        button_height
    )
    submit_button_rect = pygame.Rect(
        level_width // 2 - button_width // 2,
        level_height - button_height - 2 * button_margin - button_height,
        button_width,
        button_height
    )

    # Get the subsurface offset for proper mouse handling
    subsurface_offset = surface.get_abs_offset()

    while running and attempts < max_attempts:
        clock.tick(60)  # Limit to 60 frames per second
        start_time = time.time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Adjust mouse position for subsurface
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (
                    mouse_pos[0] - subsurface_offset[0],
                    mouse_pos[1] - subsurface_offset[1]
                )

                # Check for button clicks
                if left_button_rect.collidepoint(adjusted_mouse_pos):
                    user_angle = (user_angle + 2) % 360
                elif right_button_rect.collidepoint(adjusted_mouse_pos):
                    user_angle = (user_angle - 2) % 360
                elif submit_button_rect.collidepoint(adjusted_mouse_pos):
                    # Check if the user's angle matches the reference angle within a tolerance
                    angle_difference = abs((user_angle - reference_angle) % 360)
                    if angle_difference <= 5 or angle_difference >= 355:
                        # Player got it correct
                        message = font.render("Correct!", True, (0, 255, 0))
                        surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Pause for 2 seconds
                        score += 1
                        elapsed_time = time.time() - start_time
                        results.append({
                            "Game": "Shape Orientation",
                            "Weight": weights[attempts],
                            "Success": 1,
                            "Failure": 0,
                            "Time Taken": elapsed_time,
                            "Max Time": 60
                        })
                    else:
                        # Player got it wrong
                        message = font.render("Try Again!", True, (255, 0, 0))
                        surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Pause for 1 second
                        elapsed_time = time.time() - start_time
                        results.append({
                            "Game": "Shape Orientation",
                            "Weight": weights[attempts],
                            "Success": 0,
                            "Failure": 1,
                            "Time Taken": elapsed_time,
                            "Max Time": 60
                        })

                    # Reset for next round
                    reference_angle = random.randint(0, 359)
                    user_angle = 0
                    attempts += 1

        # Key states for rotating the user shape
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            user_angle = (user_angle + 2) % 360
        if keys[pygame.K_RIGHT]:
            user_angle = (user_angle - 2) % 360
        if keys[pygame.K_SPACE]:
            # Check if the user's angle matches the reference angle within a tolerance
            angle_difference = abs((user_angle - reference_angle) % 360)
            if angle_difference <= 5 or angle_difference >= 355:
                # Player got it correct
                message = font.render("Correct!", True, (0, 255, 0))
                surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                pygame.display.flip()
                pygame.time.wait(2000)  # Pause for 2 seconds
                score += 1
                elapsed_time = time.time() - start_time
                results.append({
                    "Game": "Shape Orientation",
                    "Weight": weights[attempts],
                    "Success": 1,
                    "Failure": 0,
                    "Time Taken": elapsed_time,
                    "Max Time": 60
                })
            else:
                # Player got it wrong
                message = font.render("Try Again!", True, (255, 0, 0))
                surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                pygame.display.flip()
                pygame.time.wait(1000)  # Pause for 1 second
                elapsed_time = time.time() - start_time
                results.append({
                    "Game": "Shape Orientation",
                    "Weight": weights[attempts],
                    "Success": 0,
                    "Failure": 1,
                    "Time Taken": elapsed_time,
                    "Max Time": 60
                })

            # Reset for next round
            reference_angle = random.randint(0, 359)
            user_angle = 0
            attempts += 1

        # Speech Control
        try:
            if not speech_queue.empty():
                command = speech_queue.get(block=False)
                print(f"Recognized command: {command}")
                if command == "left":
                    user_angle = (user_angle + 2) % 360
                elif command == "right":
                    user_angle = (user_angle - 2) % 360
                elif command == "select":
                    angle_difference = abs((user_angle - reference_angle) % 360)
                    if angle_difference <= 5 or angle_difference >= 355:
                        # Player got it correct
                        message = font.render("Correct!", True, (0, 255, 0))
                        surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Pause for 2 seconds
                        score += 1
                        elapsed_time = time.time() - start_time
                        results.append({
                            "Game": "Shape Orientation",
                            "Weight": weights[attempts],
                            "Success": 1,
                            "Failure": 0,
                            "Time Taken": elapsed_time,
                            "Max Time": 60
                        })
                    else:
                        # Player got it wrong
                        message = font.render("Try Again!", True, (255, 0, 0))
                        surface.blit(message, (level_width // 2 - message.get_width() // 2, level_height - 50))
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Pause for 1 second
                        elapsed_time = time.time() - start_time
                        results.append({
                            "Game": "Shape Orientation",
                            "Weight": weights[attempts],
                            "Success": 0,
                            "Failure": 1,
                            "Time Taken": elapsed_time,
                            "Max Time": 60
                        })
        except queue.Empty:
            pass

        # Drawing
        surface.fill(WHITE)

        # Draw reference shape
        ref_rotated_image = rot_center(reference_shape, reference_angle)
        ref_rect = ref_rotated_image.get_rect(center=(level_width // 4, level_height // 2))
        surface.blit(ref_rotated_image, ref_rect)

        # Draw user-controlled shape
        user_rotated_image = rot_center(user_shape, user_angle)
        user_rect = user_rotated_image.get_rect(center=(3 * level_width // 4, level_height // 2))
        surface.blit(user_rotated_image, user_rect)

        # Draw buttons
        pygame.draw.rect(surface, (200, 200, 200), left_button_rect)  # Left button
        pygame.draw.rect(surface, (200, 200, 200), right_button_rect)  # Right button
        pygame.draw.rect(surface, (200, 200, 200), submit_button_rect)  # Submit button

        # Add button text
        left_text = font.render("Left", True, BLACK)
        right_text = font.render("Right", True, BLACK)
        submit_text = font.render("Submit", True, BLACK)

        surface.blit(left_text, (left_button_rect.centerx - left_text.get_width() // 2, left_button_rect.centery - left_text.get_height() // 2))
        surface.blit(right_text, (right_button_rect.centerx - right_text.get_width() // 2, right_button_rect.centery - right_text.get_height() // 2))
        surface.blit(submit_text, (submit_button_rect.centerx - submit_text.get_width() // 2, submit_button_rect.centery - submit_text.get_height() // 2))

        # Display instructions
        instructions = font.render("Match the orientation!", True, BLACK)
        surface.blit(instructions, (level_width // 2 - instructions.get_width() // 2, 20))

        # Update display
        pygame.display.flip()

    # Display final score before quitting the level
    surface.fill(WHITE)
    final_score_text = f'Final Score: {score}/{max_attempts}'
    render_text_1(surface, final_score_text, font, BLACK, level_width // 2, level_height // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

    return results, score


def render_text_1(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)

# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.