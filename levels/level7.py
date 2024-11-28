import pygame
import sys
import threading
import speech_recognition as sr

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Image Description Game with Speech and Scoring inside the provided surface.

    :param surface: The Pygame surface where the game level is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Load the image (make sure it exists or replace with your image file)
    try:
        image = pygame.image.load('images/level7/img1.png')
    except pygame.error:
        print("Unable to load image. Please ensure the file exists.")
        pygame.quit()
        sys.exit()

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
            "1. You will be shown an image on the screen.",
            "2. Look at the image and describe verbally what you see."
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

            # Update the screen
            pygame.display.flip()


    # Scale the image to fit the screen if necessary
    image = pygame.transform.scale(image, (400, 300))
    image_rect = image.get_rect(center=(level_width // 2, level_height // 2 - 50))

    # Define keywords (do not display these to the player)
    keywords = ["sunset", "ocean", "reflection", "colors", "horizon"]

    # Set up fonts
    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 48)

    # Variables for speech recognition
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    speech_text = ''
    listening = False
    error_message = ''
    score = None
    matched_keywords = []
    max_attempts = max_attempts_arg
    attempts = 0
    clock = pygame.time.Clock()

    # display the instruction screen
    instruction_screen(surface, win_width, win_height)

    # Function to handle speech recognition in a separate thread
    def recognize_speech():
        nonlocal speech_text, listening, error_message, score, matched_keywords
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                print("Processing...")
                speech_text = recognizer.recognize_google(audio)
                print("You said:", speech_text)
                # Check for keywords in the speech text
                check_keywords()
                update_score_callback(score)
            except sr.WaitTimeoutError:
                error_message = "Listening timed out. Please try again."
                print(error_message)
            except sr.UnknownValueError:
                error_message = "Could not understand audio. Please try again."
                print(error_message)
            except sr.RequestError as e:
                error_message = f"Could not request results; {e}"
                print(error_message)
            listening = False

    # Function to check for keywords in the speech text
    def check_keywords():
        nonlocal score, matched_keywords
        matched_keywords = []
        words_in_speech = speech_text.lower().split()
        for keyword in keywords:
            if keyword.lower() in words_in_speech:
                matched_keywords.append(keyword)
        score = len(matched_keywords)

    running = True

    while running and attempts < max_attempts:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not listening:
                    # Start speech recognition
                    listening = True
                    error_message = ''
                    speech_text = ''
                    score = None
                    matched_keywords = []
                    threading.Thread(target=recognize_speech).start()

        # Clear the surface
        surface.fill((30, 30, 30))

        # Draw the image
        surface.blit(image, image_rect)

        # Instructions
        instruction_text = font.render("Press SPACE to start speaking.", True, pygame.Color('yellow'))
        surface.blit(instruction_text, (50, level_height - 100))

        # Display listening status or errors
        if listening:
            listening_text = font.render("Listening...", True, pygame.Color('green'))
            surface.blit(listening_text, (50, level_height - 70))
        elif error_message:
            error_text = font.render(error_message, True, pygame.Color('red'))
            surface.blit(error_text, (50, level_height - 70))
        elif speech_text:
            # Display the player's description
            description_heading = font.render("Your Description:", True, pygame.Color('white'))
            surface.blit(description_heading, (50, level_height - 220))
            description_lines = []
            words = speech_text.split(' ')
            line = ''
            for word in words:
                if font.size(line + word)[0] < level_width - 100:
                    line += word + ' '
                else:
                    description_lines.append(line)
                    line = word + ' '
            description_lines.append(line)

            y_text = level_height - 190
            for line in description_lines:
                desc_text = font.render(line, True, pygame.Color('white'))
                surface.blit(desc_text, (60, y_text))
                y_text += 25

            # Display the score
            score_text = big_font.render(f"Score: {score}/{len(keywords)}", True, pygame.Color('cyan'))
            surface.blit(score_text, (50, level_height - 250))

            # Optionally, display which keywords were matched
            matched_text = font.render(f"Keywords used: {', '.join(matched_keywords)}", True, pygame.Color('lightgreen'))
            surface.blit(matched_text, (50, level_height - 160))

        # Update the display
        pygame.display.flip()
        clock.tick(30)

        # If a description has been provided, count it as an attempt
        if not listening and speech_text:
            attempts += 1
            speech_text = ''  # Reset speech text after displaying results

    # Display final score before quitting
    surface.fill((30, 30, 30))
    final_score_text = f'Final Score: {score if score is not None else 0}'
    render_text(surface, final_score_text, big_font, pygame.Color('cyan'), level_width // 2, level_height // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

    return score if score is not None else 0, attempts

def render_text(surface, text, font, color, x, y):
    """Helper function to render text to the Pygame surface."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)

# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.
