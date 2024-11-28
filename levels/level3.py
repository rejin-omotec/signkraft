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
        """
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Wait for the audio to finish
        except pygame.error as e:
            print(f"Error loading audio: {e}")

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

    # Initialize results list
    results = []
    weights = [1.0, 1.5, 2.0]  # Example weights for increasing difficulty or attempts

    # Track story attempts
    story_attempts = 0  # Tracks the number of stories completed

    # Iterate over the stories (max 3 stories)
    for story in selected_stories:
        if story_attempts >= 3:  # Limit to 3 stories
            break

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

        # Clear the screen before showing questions
        surface.fill(WHITE)
        pygame.display.update()

        # Show questions
        score = 0
        current_question = 0

        while current_question < len(questions):
            question = questions[current_question]
            selected_option = -1  # Reset selected option for each question
            start_time = time.time()  # Start timer for the question

            while True:
                surface.fill(WHITE)
                render_text(surface, question["question"], font, BLACK, 50, 50, level_width - 50)
                for i, option in enumerate(question["options"]):
                    option_text = f"{i + 1}. {option}"
                    color = BLACK if selected_option != i else (0, 128, 0)
                    render_text(surface, option_text, font, color, 70, 150 + i * 40, level_width - 50)
                render_text(surface, "Press Enter to submit", font, BLACK, 50, level_height - 50, level_width - 50)
                pygame.display.update()

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
                            time_taken = time.time() - start_time
                            is_correct = question["options"][selected_option] == question["answer"]
                            if is_correct:
                                score += 1
                                update_score_callback(1)
                                results.append([
                                    "Story Game",
                                    weights[story_attempts],  # Weight based on story number
                                    1,
                                    0,
                                    time_taken,
                                    60
                                ])
                            else:
                                results.append([
                                    "Story Game",
                                    weights[story_attempts],
                                    0,
                                    1,
                                    time_taken,
                                    60
                                ])
                            current_question += 1
                            break
                else:
                    continue
                break

        # Increment story attempts after completing questions
        story_attempts += 1

        # Display final score for the story
        surface.fill(WHITE)
        final_score = f"Your score for this story: {score}/{len(questions)}"
        render_text(surface, final_score, font, BLACK, 50, 50, level_width - 50)
        pygame.display.update()
        pygame.time.wait(2000)

    return results
