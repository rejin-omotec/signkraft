import pygame
import sys
import random
import time
import json


def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the entire game with language selection, story display, audio playback, and questions.
    """

    # Load the JSON file
    def load_stories(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def play_audio(audio):
        """
        Play the audio narration of the story.
        Audio files should be saved with names matching the story title (e.g., 'The Farmer and the Hen.mp3').

        :param title: The title of the story, used to load the corresponding audio file.
        """
        try:
            pygame.mixer.init()
            audio_file = audio  # Replace 'audio/' with your actual audio file directory
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Wait for the audio to finish
        except pygame.error as e:
            print(f"Error loading audio for '{title}': {e}")

        
    def render_text(surface, text, font, color, x, y, max_width):
        """
        Helper function to render text with word wrapping.
        
        :param surface: The Pygame surface where the text is rendered.
        :param text: The text to render.
        :param font: The Pygame font used for rendering the text.
        :param color: The color of the text.
        :param x: The x-coordinate to start rendering the text.
        :param y: The y-coordinate to start rendering the text.
        :param max_width: The maximum width for the text block.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check if the word can fit in the current line
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                # Add the current line to lines and start a new line
                lines.append(current_line)
                current_line = word + " "

        # Add the last line
        if current_line:
            lines.append(current_line)

        # Render each line
        for line in lines:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (x, y))
            y += font.get_linesize() + 5  # Move to the next line


    def language_selection(surface, win_width, win_height):
        """Display a language selection screen."""
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        font = pygame.font.Font('fonts/Nirmala.ttf', 20)

        surface.fill(WHITE)
        text_hindi = font.render("1. हिंदी", True, BLACK)
        text_english = font.render("2. English", True, BLACK)

        surface.blit(text_hindi, (win_width // 2 - 100, win_height // 3))
        surface.blit(text_english, (win_width // 2 - 100, win_height // 3 + 60))

        pygame.display.update()

        selected_language = None
        while selected_language is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_language = "Hindi"
                    elif event.key == pygame.K_2:
                        selected_language = "English"
        return selected_language


    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fonts
    FONT_SIZE = 24
    hindi_font = pygame.font.Font('fonts/Nirmala.ttf', FONT_SIZE)
    english_font = pygame.font.Font(None, FONT_SIZE)

    # Language Selection
    selected_language = language_selection(surface, win_width, win_height)

    stories = load_stories("data/level3_stories.json")

    # Filter stories by selected language
    selected_stories = [story for story in stories if story["language"] == selected_language]
    random.shuffle(selected_stories)  # Shuffle the filtered stories in-place


    # Iterate over the stories
    for story in selected_stories:
        title = story["title"]
        audio = story["audio"]
        content = story["content"]
        questions = story["questions"]

        # Display story title and content
        font = hindi_font if selected_language == "Hindi" else english_font
        surface.fill(WHITE)
        render_text(surface, title, font, BLACK, 50, 50, level_width - 100)
        render_text(surface, content, font, BLACK, 50, 100, level_width - 100)
        continue_text = font.render("Press Enter to continue...", True, BLACK)
        surface.blit(continue_text, (50, level_height - 50))
        pygame.display.update()

        # Play audio narration
        play_audio(audio)

        # Wait for user to proceed after audio playback
        story_read = False
        while not story_read:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    story_read = True

        # Clear the screen before showing options
        surface.fill(WHITE)
        pygame.display.update()

        # Show questions (same as before)
        score = 0
        attempts = 0
        current_question = 0
        max_attempts = max_attempts_arg

        while current_question < len(questions) and attempts < max_attempts:
            question = questions[current_question]
            selected_option = -1  # Reset selected option for each question

            while True:  # Wait until the user submits their answer
                # Clear the screen for each update
                surface.fill(WHITE)

                # Render the question with wrapping
                render_text(surface, question["question"], font, BLACK, 50, 50, level_width - 50)

                # Render the options, ensuring each fits within `level_width - 50`
                for i, option in enumerate(question["options"]):
                    option_text = f"{i + 1}. {option}"
                    color = BLACK if selected_option != i else (0, 128, 0)  # Highlight selected option
                    render_text(surface, option_text, font, color, 70, 150 + i * 40, level_width - 50)

                # Render the "submit" text
                render_text(surface, "Press Enter to submit", font, BLACK, 50, level_height - 50, level_width - 50)

                pygame.display.update()

                # Handle events for options
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_KP1]:
                            selected_option = 0
                        elif event.key in [pygame.K_2, pygame.K_KP2]:
                            selected_option = 1
                        elif event.key in [pygame.K_3, pygame.K_KP3]:
                            selected_option = 2
                        elif event.key in [pygame.K_4, pygame.K_KP4]:
                            selected_option = 3
                        elif event.key == pygame.K_RETURN and selected_option != -1:
                            # Check the selected answer
                            if question["options"][selected_option] == question["answer"]:
                                score += 1
                                update_score_callback(1)  # Update global score
                            attempts += 1
                            current_question += 1
                            break
                else:
                    # Continue the loop if no valid input is provided
                    continue
                # Break the outer loop when a valid selection is submitted
                break

        # Display score after questions
        surface.fill(WHITE)
        final_score = f"Your score: {score}/{len(questions)}"
        render_text(surface, final_score, font, BLACK, 50, 50, level_width - 50)
        pygame.display.update()
        pygame.time.wait(2000)