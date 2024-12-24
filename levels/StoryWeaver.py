import pygame
import sys
import random
import time
import json
import queue
from mods.blink_detect import BlinkDetectionThread  # Assuming this is the same BlinkDetectionThread used in Level 2


def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the entire game with language selection, story display, audio playback, and questions.
    """

    # Blink detection setup
    blink_queue = queue.Queue(maxsize=10)
    blink_thread = BlinkDetectionThread(blink_queue)
    blink_thread.start()  # Start the blink detection thread


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

        text_rects = []
        for line in lines:
            text_surface = font.render(line, True, color)
            rect = surface.blit(text_surface, (x, y))
            text_rects.append(rect)
            y += font.get_linesize() + 5

        return text_rects  # Return rectangles of rendered text for interaction


    def language_selection(surface, win_width, win_height):
        """Display a language selection screen with mouse and keyboard functionality, accounting for subsurface offsets."""

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        HIGHLIGHT_COLOR = (200, 200, 200)  # Light gray for highlighting
        font = pygame.font.Font('fonts/Nirmala.ttf', 20)

        surface.fill(WHITE)

        # Render text
        text_hindi = font.render("1. हिंदी", True, BLACK)
        text_english = font.render("2. English", True, BLACK)
        text_hindi_rect = text_hindi.get_rect(center=(win_width // 2, win_height // 3))
        text_english_rect = text_english.get_rect(center=(win_width // 2, win_height // 3 + 60))

        # Account for the subsurface offsets
        subsurface_offset = surface.get_abs_offset()

        selected_language = None

        def draw_screen(highlight_hindi, highlight_english):
            """Draw the language selection screen with optional highlights."""
            surface.fill(WHITE)  # Clear the surface
            # Highlight Hindi
            if highlight_hindi:
                pygame.draw.rect(surface, HIGHLIGHT_COLOR, text_hindi_rect.inflate(10, 10))
            surface.blit(text_hindi, text_hindi_rect)

            # Highlight English
            if highlight_english:
                pygame.draw.rect(surface, HIGHLIGHT_COLOR, text_english_rect.inflate(10, 10))
            surface.blit(text_english, text_english_rect)

            pygame.display.update()

        while selected_language is None:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Adjust mouse position to subsurface coordinates
            adjusted_mouse_pos = (mouse_pos[0] - subsurface_offset[0], mouse_pos[1] - subsurface_offset[1])

            # Check if the adjusted mouse position is over any text
            mouse_over_hindi = text_hindi_rect.collidepoint(adjusted_mouse_pos)
            mouse_over_english = text_english_rect.collidepoint(adjusted_mouse_pos)

            draw_screen(mouse_over_hindi, mouse_over_english)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_language = "Hindi"
                    elif event.key == pygame.K_2:
                        selected_language = "English"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_over_hindi:
                        selected_language = "Hindi"
                    elif mouse_over_english:
                        selected_language = "English"

        return selected_language


    
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
            "1. Select your preferred language: English or Hindi.",
            "2. Listen carefully to the story narrated in your chosen language.",
            "3. Answer questions based on details from the story.",
            "4. Blink to select the options and submit the answers."
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
                # if any mouse button is pressed, proceed to the next screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Proceed to the next screen
                        running = False

            # Update the screen
            pygame.display.flip()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fonts
    FONT_SIZE = 24
    hindi_font = pygame.font.Font('fonts/Nirmala.ttf', FONT_SIZE)
    english_font = pygame.font.Font(None, FONT_SIZE)
    
    instruction_screen(surface, win_width, win_height)

    # Language Selection
    selected_language = language_selection(surface, win_width, win_height)

    stories = load_stories("data/level3_stories.json")

    # Filter stories by selected language
    selected_stories = [story for story in stories if story["language"] == selected_language]
    random.shuffle(selected_stories)  # Shuffle the filtered stories in-place

    # Initialize results list
    results = []
    weights = [1.0, 1.5, 2.0]  # Example weights for increasing difficulty or attempts
    HIGHLIGHT_COLOR = (200, 200, 200)
    GREEN = (0, 128, 0)

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
        # play_audio(audio)

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

        subsurface_offset = surface.get_abs_offset()

        while current_question < len(questions):
            question = questions[current_question]
            selected_option = -1  # Reset selected option for each question
            start_time = time.time()  # Start timer for the question

            # Initialize hovered_option before the loop
            hovered_option = None  # Tracks the currently highlighted option (None if no option is hovered)

            while True:
                # Clear the surface once
                surface.fill(WHITE)

                # Render the question
                render_text(surface, question["question"], font, BLACK, 50, 50, level_width - 50)

                # Render options and track their rectangles
                option_rects = []
                for i, option in enumerate(question["options"]):
                    option_text = f"{i + 1}. {option}"
                    color = BLACK if hovered_option != i else GREEN  # GREEN for highlighted option
                    rects = render_text(surface, option_text, font, color, 70, 150 + i * 40, level_width - 50)
                    option_rects.append(rects[-1])  # Get the rectangle of the last line of the option text

                # Render submit instruction
                render_text(surface, "Press Enter to submit", font, BLACK, 50, level_height - 50, level_width - 50)

                # Get mouse position and adjust for subsurface offset
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (
                    mouse_pos[0] - subsurface_offset[0],
                    mouse_pos[1] - subsurface_offset[1]
                )

                # Check mouse hover over options
                mouse_hovered_option = None
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(adjusted_mouse_pos):
                        mouse_hovered_option = i

                # Update hovered_option from mouse
                if mouse_hovered_option is not None:
                    hovered_option = mouse_hovered_option

                # Draw highlight for hovered option
                if hovered_option is not None:
                    highlight_rect = option_rects[hovered_option].inflate(10, 10)
                    pygame.draw.rect(surface, HIGHLIGHT_COLOR, highlight_rect)
                    render_text(
                        surface,
                        f"{hovered_option + 1}. {question['options'][hovered_option]}",
                        font,
                        BLACK,
                        option_rects[hovered_option].x,
                        option_rects[hovered_option].y,
                        level_width - 50
                    )

                pygame.display.update()

                # Handle events
                try:
                    blink_message = blink_queue.get_nowait()
                    if blink_message == "SINGLE_BLINK":
                        print("Single Blink Detected")
                        if hovered_option is None:
                            hovered_option = 0  # Default to the first option if none is highlighted
                        else:
                            hovered_option = (hovered_option + 1) % len(question["options"])  # Move to next option
                    elif blink_message == "DOUBLE_BLINK" and hovered_option is not None:
                        print("Double Blink Detected")
                        selected_option = hovered_option  # Select the current option
                        time_taken = time.time() - start_time
                        is_correct = question["options"][selected_option] == question["answer"]
                        if is_correct:
                            score += 1
                            results.append({
                                "Game": "Story Game",
                                "Weight": weights[story_attempts],
                                "Correct": 1,
                                "Incorrect": 0,
                                "Time Taken": time_taken,
                                "Max Time": 60
                            })
                        else:
                            results.append({
                                "Game": "Story Game",
                                "Weight": weights[story_attempts],
                                "Correct": 0,
                                "Incorrect": 1,
                                "Time Taken": time_taken,
                                "Max Time": 60
                            })
                        current_question += 1
                        break
                except queue.Empty:
                    pass

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_DOWN, pygame.K_UP]:
                            if hovered_option is None:
                                hovered_option = 0  # Default to the first option if none is highlighted
                            else:
                                if event.key == pygame.K_DOWN:
                                    hovered_option = (hovered_option + 1) % len(question["options"])
                                elif event.key == pygame.K_UP:
                                    hovered_option = (hovered_option - 1) % len(question["options"])
                        elif event.key == pygame.K_RETURN and hovered_option is not None:
                            selected_option = hovered_option
                            time_taken = time.time() - start_time
                            is_correct = question["options"][selected_option] == question["answer"]
                            if is_correct:
                                score += 1
                                results.append({
                                    "Game": "Story Game",
                                    "Weight": weights[story_attempts],
                                    "Correct": 1,
                                    "Incorrect": 0,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                                })
                            else:
                                results.append({
                                    "Game": "Story Game",
                                    "Weight": weights[story_attempts],
                                    "Correct": 0,
                                    "Incorrect": 1,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                                })
                            current_question += 1
                            break
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                        if mouse_hovered_option is not None:
                            selected_option = mouse_hovered_option
                            time_taken = time.time() - start_time
                            is_correct = question["options"][selected_option] == question["answer"]
                            if is_correct:
                                score += 1
                                results.append({
                                    "Game": "Story Game",
                                    "Weight": weights[story_attempts],
                                    "Correct": 1,
                                    "Incorrect": 0,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                                })
                            else:
                                results.append({
                                    "Game": "Story Game",
                                    "Weight": weights[story_attempts],
                                    "Correct": 0,
                                    "Incorrect": 1,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                                })
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

    return results, score
