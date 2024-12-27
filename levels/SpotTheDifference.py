import pygame
import random
import sys
import time
import queue
from mods.blink_detect import BlinkDetectionThread  # Assuming this is the same BlinkDetectionThread used in Level 2
from mods.audio_detect import SpeechRecognitionThread  # Replace with your actual module name


def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):


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

    # Define questions, options, and correct answers
    # Define questions, options, and correct answers
    questions = [
        {
            "question_images": ["images/SpotTheDifference/11.png", "images/SpotTheDifference/12.png"],
            "options": ["images/SpotTheDifference/1.jpg", "images/SpotTheDifference/3.jpg", "images/SpotTheDifference/4.jpg", "images/SpotTheDifference/6.jpg"],
            "correct_index": 0
        },
        {
            "question_images": ["images/SpotTheDifference/21.png", "images/SpotTheDifference/22.png"],
            "options": ["images/SpotTheDifference/5.jpg", "images/SpotTheDifference/1.jpg", "images/SpotTheDifference/2.jpg", "images/SpotTheDifference/3.jpg"],
            "correct_index": 2
        },
        {
            "question_images": ["images/SpotTheDifference/31.png", "images/SpotTheDifference/32.png"],
            "options": ["images/SpotTheDifference/6.jpg", "images/SpotTheDifference/2.jpg", "images/SpotTheDifference/4.jpg", "images/SpotTheDifference/3.jpg"],
            "correct_index": 3
        },
        {
            "question_images": ["images/SpotTheDifference/41.png", "images/SpotTheDifference/42.png"],
            "options": ["images/SpotTheDifference/4.jpg", "images/SpotTheDifference/1.jpg", "images/SpotTheDifference/5.jpg", "images/SpotTheDifference/3.jpg"],
            "correct_index": 0
        },
        {
            "question_images": ["images/SpotTheDifference/51.png", "images/SpotTheDifference/52.png"],
            "options": ["images/SpotTheDifference/2.jpg", "images/SpotTheDifference/5.jpg", "images/SpotTheDifference/6.jpg", "images/SpotTheDifference/4.jpg"],
            "correct_index": 1
        },
        {
            "question_images": ["images/SpotTheDifference/61.png", "images/SpotTheDifference/62.png"],
            "options": ["images/SpotTheDifference/5.jpg", "images/SpotTheDifference/6.jpg", "images/SpotTheDifference/2.jpg", "images/SpotTheDifference/1.jpg"],
            "correct_index": 1
        },
    ]

    random.shuffle(questions)   

    def load_images(image_paths):
        try:
            return [pygame.transform.scale(pygame.image.load(path), (150, 150)) for path in image_paths]
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            sys.exit()

    for q in questions:
        q["question_images"] = load_images(q["question_images"])
        q["options"] = load_images(q["options"])

    
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


    def render_question(surface, question):
        """Display the current question images forming the analogy."""
        image_positions = [(225, 50), (225, 50)]

        for i, img in enumerate(question["question_images"]):
            surface.fill(WHITE)
            surface.blit(img, image_positions[i])
            pygame.display.update()
            pygame.time.wait(100)
            surface.fill(WHITE)
            pygame.display.update()
            pygame.time.wait(100)

    def render_options(surface, question, selected_option):
        """Display the current question's options with a border around the selected option."""
        positions = [
            (30, 300),  # Top-left
            (230, 300),  # Top-right
            (430, 300),  # Bottom-left
            (630, 300),  # Bottom-right
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
            # Colors and Fonts
            WHITE = (255, 255, 255)
            BLUE = (0, 0, 255)
            BLACK = (0, 0, 0)
            RED = (255, 0, 0)

            title_font = pygame.font.SysFont(None, 50)
            text_font = pygame.font.SysFont(None, 30)

            # Instruction text
            instructions = (
                "1. You will be shown two images with pauses in between.",
                "2. Between the two pictures, something will have changed.",
                "3. Four images will appear as possible answers.",
                "4. Blink to select the correct option.",
                
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


    # Game variables
    running = True
    game_state = "question"
    selected_option = 0  # Start with the first option selected
    max_attempts = max_attempts_arg
    attempts = 0
    results = [0, 0, 0]
    weights = [2, 3, 5]

    # Display the instruction screen
    instruction_screen(surface, win_width, win_height)

    clock = pygame.time.Clock()
    start_time = time.time()

    while running:
        surface.fill(WHITE)

        if game_state == "question":
            render_question(surface, questions[attempts])
            game_state = "question_shown"
            selected_option = 0

        if game_state == "question_shown":
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



            # Keyboard Control
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
                            game_state = "question"
                        else:
                            running = False
        
        pygame.display.flip()
        clock.tick(30)

    end_time = time.time()-start_time

    return results, end_time
