import pygame
import random
import global_data
import time  # For time measurement

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    A quiz level that asks the user 3 random questions based on previously collected data.
    Tracks time and calculates scores.
    """
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Fonts
    TITLE_FONT = pygame.font.Font(None, 36)
    QUESTION_FONT = pygame.font.Font(None, 24)
    INPUT_FONT = pygame.font.Font(None, 20)

    # Fetch stored data
    stored_data = global_data.persistent_user_data
    if not stored_data:
        raise ValueError("No data found. Please run the first level to collect data.")

    # Randomly select 3 questions
    selected_keys = random.sample(list(stored_data.keys()), 3)
    questions = {key: stored_data[key] for key in selected_keys}

    # Input field properties
    input_field = {"value": "", "rect": pygame.Rect(level_width // 2 - 100, level_height // 2, 200, 30)}
    submit_button = pygame.Rect(level_width // 2 - 100, level_height - 70, 200, 50)

    # Game state variables
    question_index = 0
    feedback_message = ""
    total_questions = len(questions)
    score_per_question = []
    total_score = 0

    # Time tracking variables
    start_time = time.time()
    question_start_time = start_time
    total_time = 0

    running = True
    while running:
        surface.fill(WHITE)

        # Display title
        title_surface = TITLE_FONT.render("Quiz Level", True, BLACK)
        surface.blit(title_surface, (level_width // 2 - title_surface.get_width() // 2, 20))

        # Display current question
        if question_index < total_questions:
            question_key = list(questions.keys())[question_index]
            question_text = f"What is your {question_key.replace('_', ' ')}?"
            question_surface = QUESTION_FONT.render(question_text, True, BLACK)
            surface.blit(question_surface, (level_width // 2 - question_surface.get_width() // 2, level_height // 2 - 50))

            # Draw input box
            pygame.draw.rect(surface, GRAY, input_field["rect"])
            input_surface = INPUT_FONT.render(input_field["value"], True, BLACK)
            surface.blit(input_surface, (input_field["rect"].x + 5, input_field["rect"].y + 5))
        else:
            # Display final score
            score_surface = TITLE_FONT.render(f"Your Score: {total_score}/{10}", True, BLACK)
            surface.blit(score_surface, (level_width // 2 - score_surface.get_width() // 2, level_height // 2 - 50))
            feedback_message = f"Time Taken: {total_time:.2f} seconds. Press ESC to exit."

        # Draw submit button
        pygame.draw.rect(surface, GREEN, submit_button)
        submit_text = QUESTION_FONT.render("Submit", True, WHITE)
        surface.blit(submit_text, (submit_button.x + 70, submit_button.y + 10))

        # Display feedback message
        if feedback_message:
            feedback_surface = QUESTION_FONT.render(feedback_message, True, RED)
            surface.blit(feedback_surface, (level_width // 2 - feedback_surface.get_width() // 2, level_height - 120))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit the game loop entirely

            if event.type == pygame.KEYDOWN:
                if question_index < total_questions:
                    if event.key == pygame.K_BACKSPACE:
                        input_field["value"] = input_field["value"][:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        input_field["value"] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the absolute offset of the subsurface
                abs_offset = surface.get_abs_offset()
                x, y = event.pos
                x -= abs_offset[0]
                y -= abs_offset[1]

                # Check if submit button was clicked
                if submit_button.collidepoint(x, y):
                    if question_index < total_questions:
                        # Validate answer
                        user_answer = input_field["value"].strip().lower()
                        correct_answer = questions[list(questions.keys())[question_index]].strip().lower()
                        if user_answer == correct_answer:
                            score_per_question.append(10 / 3)
                            feedback_message = "Correct!"
                        else:
                            score_per_question.append(0)
                            feedback_message = f"Wrong! The correct answer was: {correct_answer}"

                        # Calculate time for this question
                        question_end_time = time.time()
                        question_time = question_end_time - question_start_time
                        total_time += question_time
                        question_start_time = question_end_time

                        # Clear input for next question
                        input_field["value"] = ""
                        question_index += 1

        # Allow exit after quiz completion
        if question_index >= total_questions:
            total_score = sum(score_per_question)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.update()

    # Return the quiz results, scores, and total time
    return score_per_question, total_time
