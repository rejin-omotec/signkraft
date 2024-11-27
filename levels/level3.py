import pygame
import sys
import random

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height):
    """
    Runs the Cause and Effect MCQ game inside the provided surface.

    :param surface: The Pygame surface where the game level is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fonts
    FONT_SIZE = 24
    hindi_font = pygame.font.Font('Nirmala.ttf', FONT_SIZE)  # Replace with your font file
    small_font = pygame.font.Font('Nirmala.ttf', 20)

    # Cause-Effect pairs (questions)
    questions = [
        {
            "question": "किसान के पास कौन सा जानवर था?",
            "options": ["गाय", "मुर्गी", "बकरी", "भेड़"],
            "answer": "मुर्गी"
        },
        {
            "question": "मुर्गी कैसे अंडे देती थी?",
            "options": ["साधारण अंडे", "सुनहरे अंडे", "चाँदी के अंडे", "हीरे के अंडे"],
            "answer": "सुनहरे अंडे"
        },
        {
            "question": "किसान ने मुर्गी के साथ क्या किया?",
            "options": ["उसे बेचा", "उसे मार दिया", "उसे खाना दिया", "उसे छोड़ दिया"],
            "answer": "उसे मार दिया"
        },
        {
            "question": "कहानी से हमें क्या शिक्षा मिलती है?",
            "options": ["लालच बुरी बला है", "मेहनत का फल मीठा होता है", "समय अमूल्य है", "दोस्तों की मदद करें"],
            "answer": "लालच बुरी बला है"
        }
    ]

    random.shuffle(questions)

    # Global variables for the game
    score = 0
    attempts = 0
    current_question = 0
    max_attempts = 3
    selected_option = -1
    clock = pygame.time.Clock()
    running = True

    def render_text(text, font, color, x, y):
        """Render text to the surface."""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (x, y + i * (FONT_SIZE + 5)))

    def display_question(index, selected_option):
        """Display the current question and options."""
        surface.fill(WHITE)
        q = questions[index]
        render_text(q["question"], hindi_font, BLACK, 50, 50)

        # Display options
        for i, option in enumerate(q["options"]):
            color = BLACK
            if selected_option == i:
                color = (0, 128, 0)  # Highlight selected option
            option_text = f"{i + 1}. {option}"
            text_surface = hindi_font.render(option_text, True, color)
            surface.blit(text_surface, (70, 150 + i * 40))

        submit_button = small_font.render("जमा करें (Enter)", True, BLACK)
        surface.blit(submit_button, (50, level_height - 50))
        pygame.display.update()

    def display_score():
        """Display the final score."""
        surface.fill(WHITE)
        score_text = f"आपका स्कोर है: {score}/{len(questions)}"
        render_text(score_text, hindi_font, BLACK, 50, 50)
        pygame.display.update()

    while running and attempts < max_attempts:
        if current_question < len(questions):
            display_question(current_question, selected_option)
        else:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Translate mouse position to the subsurface coordinates
                x, y = event.pos

                # Get the position of the subsurface relative to the main window
                surface_rect = surface.get_abs_offset()

                # Adjust the mouse click coordinates relative to the subsurface
                x -= surface_rect[0]
                y -= surface_rect[1]

            elif event.type == pygame.KEYDOWN:
                if current_question < len(questions):
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        selected_option = 0
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        selected_option = 1
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        selected_option = 2
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        selected_option = 3
                    elif event.key == pygame.K_RETURN:
                        if selected_option == -1:
                            # No option selected, do nothing
                            continue
                        else:
                            # Check answer
                            if questions[current_question]["options"][selected_option] == questions[current_question]["answer"]:
                                score += 1
                                update_score_callback(1)  # Update global score
                            attempts += 1
                            current_question += 1
                            selected_option = -1
                            if attempts >= max_attempts:
                                running = False

    # Display final score
    display_score()
    pygame.time.wait(3000)

    return score, attempts
