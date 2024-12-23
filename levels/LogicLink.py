import pygame
import random
import sys

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height, max_attempts_arg):
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

    def render_options(surface, question):
        """Display the current question's options."""
        positions = [
            (100, 300),  # Top-left
            (300, 300),  # Top-right
            (500, 300),  # Bottom-left
            (700, 300),  # Bottom-right
        ]

        for i, img in enumerate(question["options"]):
            surface.blit(img, positions[i])

    def check_answer(mouse_pos, question):
        """Check if the clicked image is the correct answer."""
        positions = [
            pygame.Rect(100, 300, 150, 150),  # Top-left
            pygame.Rect(300, 300, 150, 150),  # Top-right
            pygame.Rect(500, 300, 150, 150),  # Bottom-left
            pygame.Rect(700, 300, 150, 150),  # Bottom-right
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
            "1. You will be shown an incomplete analogy.",
            "2. Four images will appear as possible answers.",
            "3. Blink to select the option."
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
    current_question_index = 0

    clock = pygame.time.Clock()

    # Display instructions
    instruction_screen(surface, win_width, win_height)

    while running:
        surface.fill(WHITE)

        if game_state == "question":
            render_question(surface, questions[current_question_index])
            render_options(surface, questions[current_question_index])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        is_correct = check_answer(event.pos, questions[current_question_index])
                        if is_correct:
                            score += 1
                            update_score_callback(1)  # Update score in the main menu
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

    return score
