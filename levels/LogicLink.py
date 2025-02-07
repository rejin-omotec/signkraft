import pygame
import random
import sys
import time
import queue
from mods.blink_detect import BlinkDetectionThread  # Assuming this is the same BlinkDetectionThread used in Level 2
from mods.audio_detect import SpeechRecognitionThread  # Replace with your actual module name


def initialize_questions():
    """Load all images for questions and options and return the updated questions."""
    # Define questions, options, and correct answers
    questions = [
        {
            "question_images": ["images/level9/question_1/Sun.png", "images/level9/question_1/Day.png", "images/level9/question_1/Moon.png"],
            "options": ["images/level9/question_1/Star.png", "images/level9/question_1/Sky.png", "images/level9/question_1/Night.png", "images/level9/question_1/Cloud.png"],
            "correct_index": 2
        },
        {
            "question_images": ["images/level9/question_2/Pen.png", "images/level9/question_2/Paper.png", "images/level9/question_2/Paintbrush.png"],
            "options": ["images/level9/question_2/Easel.png", "images/level9/question_2/Canvas.png", "images/level9/question_2/Palette.png", "images/level9/question_2/Wall.png"],
            "correct_index": 1
        },
        {
            "question_images": ["images/level9/question_3/Monkey.png", "images/level9/question_3/Banana.png", "images/level9/question_3/Cow.png"],
            "options": ["images/level9/question_3/Milk.png", "images/level9/question_3/Cheese.png", "images/level9/question_3/Carrot.png", "images/level9/question_3/Grass.png"],
            "correct_index": 3
        },
        {
            "question_images": ["images/level9/question_4/Ball.png", "images/level9/question_4/Bat.png", "images/level9/question_4/Shuttlecock.png"],
            "options": ["images/level9/question_4/Racket.png", "images/level9/question_4/Net.png", "images/level9/question_4/Player.png", "images/level9/question_4/Court.png"],
            "correct_index": 0
        },
        {
            "question_images": ["images/level9/question_5/Musician.png", "images/level9/question_5/Guitar.png", "images/level9/question_5/Photographer.png"],
            "options": ["images/level9/question_5/Reel.png", "images/level9/question_5/Tripod.png", "images/level9/question_5/Camera.png", "images/level9/question_5/Studio.png"],
            "correct_index": 2
        },
        {
            "question_images": ["images/level9/question_6/Bread.png", "images/level9/question_6/Baker.png", "images/level9/question_6/Book.png"],
            "options": ["images/level9/question_6/Writer.png", "images/level9/question_6/Reader.png", "images/level9/question_6/Librarian.png", "images/level9/question_6/Teacher.png"],
            "correct_index": 0
        },
    ]   

    def load_images(image_paths):
        try:
            return [pygame.transform.scale(pygame.image.load(path), (150, 150)) for path in image_paths]
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            sys.exit()

    for q in questions:
        q["question_images"] = load_images(q["question_images"])
        q["options"] = load_images(q["options"])

    return questions

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Image-Based Analogy Game inside the provided surface.

    :param surface: The Pygame surface where the game is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    :param max_attempts_arg: Maximum number of attempts for the game.
    """

    
    # Blink detection setup
    blink_queue = queue.Queue(maxsize=10)
    blink_thread = BlinkDetectionThread(blink_queue)
    blink_thread.start()  # Start the blink detection thread

    # speech detection setup
    speech_queue = queue.Queue(maxsize=10)
    speech_thread = SpeechRecognitionThread(audio_queue=speech_queue, language="english")
    speech_thread.start()


    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 255)

    # Fonts
    FONT = pygame.font.Font(None, 48)
    FONT_SMALL = pygame.font.Font(None, 36)

    # Load questions and images
    questions = initialize_questions()

    def render_question(surface, question):
        """Display the current question images forming the analogy."""
        image_positions = [(150, 50), (350, 50), (550, 50)]

        for i, img in enumerate(question["question_images"]):
            surface.blit(img, image_positions[i])

        # Render text symbols
        symbols = [":", "->", "?"]
        font = pygame.font.Font(None, 64)
        colon_position = (image_positions[0][0] + 150 + 25, image_positions[0][1] + 50)
        arrow_position = (image_positions[1][0] + 150 + 25, image_positions[1][1] + 50)
        question_mark_position = (image_positions[2][0] + 150 + 25, image_positions[2][1] + 50)

        colon_surface = font.render(symbols[0], True, BLACK)
        arrow_surface = font.render(symbols[1], True, BLACK)
        question_mark_surface = font.render(symbols[2], True, BLACK)

        surface.blit(colon_surface, colon_position)
        surface.blit(arrow_surface, arrow_position)
        surface.blit(question_mark_surface, question_mark_position)

    def render_options(surface, question, selected_option):
        """Display the current question's options with a border around the selected option."""
        positions = [
            (100, 300),  # Top-left
            (300, 300),  # Top-right
            (500, 300),  # Bottom-left
            (700, 300),  # Bottom-right
        ]

        for i, img in enumerate(question["options"]):
            surface.blit(img, positions[i])
            if i == selected_option:
                pygame.draw.rect(surface, BLUE, pygame.Rect(positions[i][0], positions[i][1], 150, 150), 5)

    def check_answer(selected_option, question):
        """Check if the selected option is the correct answer."""
        return selected_option == question["correct_index"]

    def instruction_screen(surface, screen_width, screen_height):
        """
        Displays the instruction screen.

        :param surface: The Pygame surface where the instructions will be displayed.
        :param screen_width: The width of the screen.
        :param screen_height: The height of the screen.
        """
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        title_font = pygame.font.SysFont(None, 50)
        text_font = pygame.font.SysFont(None, 30)

        instructions = (
            "1. You will be shown an incomplete analogy.",
            "2. Four images will appear as possible answers.",
            "3. Use the arrow keys to select the correct option.",
            "4. Press Enter to confirm your choice."
        )

        running = True

        while running:
            surface.fill(WHITE)

            title_text = title_font.render("Game Instructions", True, BLUE)
            surface.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

            y_offset = 150
            for line in instructions:
                text_surface = text_font.render(line, True, BLACK)
                surface.blit(text_surface, (50, y_offset))
                y_offset += text_font.get_linesize() + 20

            nav_text = text_font.render("Press ENTER to proceed.", True, RED)
            surface.blit(nav_text, (screen_width // 2 - nav_text.get_width() // 2, screen_height - 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            pygame.display.flip()

    running = True
    selected_option = 0  # Start with the first option selected
    max_attempts = max_attempts_arg
    attempts = 0
    weights = [2, 3, 5]
    results = [0, 0, 0]

    clock = pygame.time.Clock()

    instruction_screen(surface, win_width, win_height)
    start_time = time.time()


    while running:
        surface.fill(WHITE)

        render_question(surface, questions[attempts])
        render_options(surface, questions[attempts], selected_option)
        pygame.display.flip()


        # Blink Control
        try:
            blink_message = blink_queue.get_nowait()
            if blink_message == "SINGLE_BLINK":
                print("Single Blink Detected - Pygame")
                selected_option = (selected_option + 1) % 4
            elif blink_message == "DOUBLE_BLINK":
                print("Double Blink Detected - Pygame")
                is_correct = check_answer(selected_option, questions[attempts])
                if is_correct:
                    results[attempts] = weights[attempts]

                attempts += 1
                if attempts < max_attempts:
                    selected_option = 0  # Reset selection for the next question
                    game_state = "question"
                else:
                    running = False
        except queue.Empty:
            pass
        
        # Speech Control
        try:
            if not speech_queue.empty():
                command = speech_queue.get(block=False)
                print(f"Recognized command: {command}")
                if command == "next":
                    selected_option = (selected_option + 1) % 4
                elif command == "revious":
                    selected_option = (selected_option - 1) % 4
                elif command == "select":
                    is_correct = check_answer(selected_option, questions[attempts])
                if is_correct:
                    results[attempts] = weights[attempts]

                attempts += 1
                if attempts < max_attempts:
                    selected_option = 0  # Reset selection for the next question
                    game_state = "question"
                else:
                    running = False
        except queue.Empty:
            pass

        # keybaord and mouse contorl
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % 4
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % 4
                elif event.key == pygame.K_RETURN:
                    is_correct = check_answer(selected_option, questions[attempts])
                    if is_correct:
                        results[attempts] = weights[attempts]

                    attempts += 1
                    if attempts < max_attempts:
                        selected_option = 0  # Reset selection for the next question
                    else:
                        running = False

        clock.tick(30)

    end_time = time.time()-start_time

    print("Results: ", results, "Time: ", end_time)
    return results, end_time
