import pygame
import random
import sys
import time

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

    # update_score_callback = None

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)

    # Fonts
    FONT = pygame.font.Font(None, 48)
    FONT_SMALL = pygame.font.Font(None, 36)

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

    # Load images for all questions
    def load_images(image_paths):
        try:
            return [pygame.transform.scale(pygame.image.load(path), (150, 150)) for path in image_paths]
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
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

    for q in questions:
        q["question_images"] = load_images(q["question_images"])
        q["options"] = load_images(q["options"])

    def render_question(surface, question):
        """Display the current question images forming the analogy."""
        image_positions = [(225, 50), (225, 50)]

        for i, img in enumerate(question["question_images"]):
            surface.fill(WHITE)
            surface.blit(img, image_positions[i])
            pygame.display.update()
            pygame.time.wait(2000)
            surface.fill(WHITE)
            pygame.display.update()
            pygame.time.wait(3000)

    def render_options(surface, question):
        """Display the current question's options."""
        positions = [
            (30, 300),  # Top-left
            (230, 300),  # Top-right
            (430, 300),  # Bottom-left
            (630, 300),  # Bottom-right
        ]

        for i, img in enumerate(question["options"]):
            surface.blit(img, positions[i])

    def check_answer(mouse_pos, question):
        """Check if the clicked image is the correct answer."""
        positions = [
            pygame.Rect(30, 300, 150, 150),  # Top-left
            pygame.Rect(230, 300, 150, 150),  # Top-right
            pygame.Rect(430, 300, 150, 150),  # Bottom-left
            pygame.Rect(630, 300, 150, 150),  # Bottom-right
        ]
        for i, rect in enumerate(positions):
            if rect.collidepoint(mouse_pos):
                return i == question["correct_index"]
        return False
    
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
    score = 0
    weights = [1.0, 1.0, 1.5, 1.5, 2.0, 2.0]
    selected_option = -1
    results = []
    current_question_index = 0

    clock = pygame.time.Clock()

    # Display instructions
    instruction_screen(surface, win_width, win_height)

    while running:
        surface.fill(WHITE)

        if game_state == "question":
            render_question(surface, questions[current_question_index])
            game_state = "question_shown"
            selected_option = -1
        if game_state == "question_shown":
            render_options(surface, questions[current_question_index])
            pygame.display.flip()
            start_time = time.time()

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
                    if selected_option != -1:
                        time_taken = time.time() - start_time
                        is_correct = selected_option == questions[current_question_index]["correct_index"]
                        if is_correct:
                            score += 1
                            results.append({
                                    "Game": "SpotTheDifference",
                                    "Weight": weights[current_question_index],
                                    "Correct": 1,
                                    "Incorrect": 0,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                            })
                        else:
                            results.append({
                                    "Game": "SpotTheDifference",
                                    "Weight": weights[current_question_index],
                                    "Correct": 0,
                                    "Incorrect": 1,
                                    "Time Taken": time_taken,
                                    "Max Time": 60
                            })
                        current_question_index += 1
                        if current_question_index < len(questions):
                            game_state = "question"
                        else:
                            game_state = "end"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click

                        time_taken = time.time() - start_time
                        

                        is_correct = check_answer(event.pos, questions[current_question_index])

                        results.append({
                            "Game": 'QuickTap',
                            "Weight": weights[current_question_index],
                            "Correct": 1 if is_correct else 0,
                            "Incorrect": 0 if is_correct else 1,
                            "Time Taken": time_taken,
                            "Max Time": 60
                        })

                    if is_correct:
                        score += 1
                                # update_score_callback(1)  # Update score in the main menu
                    current_question_index += 1
                    if current_question_index < len(questions):
                        game_state = "question"
                    else:
                        game_state = "end"

        elif game_state == "end":
            # Display final score
            result_text = f"You scored {score} out of {len(questions)}!"
            result_surface = FONT.render(result_text, True, BLACK)
            result_rect = result_surface.get_rect(center=(level_width // 2, level_height // 2))
            surface.blit(result_surface, result_rect)

            quit_surface = FONT_SMALL.render("Press any key to quit.", True, BLACK)
            quit_rect = quit_surface.get_rect(center=(level_width // 2, level_height // 2 + 50))
            surface.blit(quit_surface, quit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False

        pygame.display.flip()
        clock.tick(30)

    return results, score


