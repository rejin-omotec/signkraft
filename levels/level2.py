import pygame
import random
import time

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Cause and Effect MCQ game inside the provided surface.

    :param surface: The Pygame surface where the game is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)

    # Fonts
    FONT = pygame.font.Font(None, 36)

    # Cause-Effect pairs
    cause_effect_pairs = [
        ("Dark clouds gathered in the sky.", "It started raining."),
        ("They received plenty of sunlight and water.", "The plants grew tall."),
        ("The battery was dead.", "The car wouldn't start."),
        ("Someone turned off the light.", "The room became dark."),
        ("It was set to go off at 7 AM.", "The alarm clock rang."),
        ("The temperature increased.", "The ice melted."),
        ("It was left in the oven too long.", "The cake burned."),
        ("There was a lot of smoke in the air.", "People were coughing."),
        ("There was a power outage.", "The computer shut down unexpectedly."),
        ("It was dropped on the ground.", "The phone's screen cracked.")
    ]
    random.shuffle(cause_effect_pairs)

    # Game variables
    current_index = 0
    score = 0
    selected_option = None
    options = []
    option_rects = []
    options_generated = False
    show_feedback = False
    feedback = ""
    feedback_time = 0
    attempts = 0
    max_attempts = max_attempts_arg
    weights = [1.0, 1.5, 2.0]  # Increasing weights for each attempt
    results = []

    # Helper function to generate options
    def generate_options(correct_cause, all_causes, num_options=4):
        options = [correct_cause]
        distractors = [cause for cause in all_causes if cause != correct_cause]
        random.shuffle(distractors)
        options.extend(distractors[:num_options - 1])
        random.shuffle(options)
        return options

    clock = pygame.time.Clock()
    running = True

    # Prepare all causes for option generation
    all_causes = [pair[0] for pair in cause_effect_pairs]

    while running and attempts < max_attempts:
        start_time = time.time()  # Start timing the attempt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Translate mouse position to the subsurface coordinates
                x, y = event.pos

                # Get the position of the subsurface relative to the main window
                surface_rect = surface.get_abs_offset()

                # Adjust the mouse click coordinates relative to the subsurface
                x -= surface_rect[0]
                y -= surface_rect[1]

                if current_index < len(cause_effect_pairs):
                    if not show_feedback:
                        for idx, option_rect in enumerate(option_rects):
                            if option_rect.collidepoint(x, y):
                                selected_option = options[idx]
                                # Check the user's answer
                                correct_cause, effect = cause_effect_pairs[current_index]
                                time_taken = time.time() - start_time  # Calculate time taken

                                if selected_option == correct_cause:
                                    feedback = "Correct!"
                                    score += 1
                                    update_score_callback(1)  # Update global score
                                    results.append(["Cause and Effect", weights[attempts], 1, time_taken, 60])
                                else:
                                    feedback = f"Incorrect! The correct cause was: {correct_cause}"
                                    results.append(["Cause and Effect", weights[attempts], 0, time_taken, 60])

                                show_feedback = True
                                feedback_time = pygame.time.get_ticks()
                                attempts += 1  # Increment the number of attempts
                                break

        # Clear the surface
        surface.fill(WHITE)

        if current_index < len(cause_effect_pairs):
            # Display the current effect
            correct_cause, effect = cause_effect_pairs[current_index]
            effect_surface = FONT.render("Effect: " + effect, True, BLACK)
            surface.blit(effect_surface, (50, 50))

            # Generate options only once per question
            if not options_generated:
                options = generate_options(correct_cause, all_causes)
                option_rects = []
                for idx, option in enumerate(options):
                    rect = pygame.Rect(50, 150 + idx * 60, level_width - 100, 50)
                    option_rects.append(rect)
                options_generated = True  # Set the flag to True after generating options

            # Display the options
            for idx, option in enumerate(options):
                rect = option_rects[idx]
                pygame.draw.rect(surface, LIGHT_GRAY, rect)
                option_surface = FONT.render(option, True, BLACK)
                surface.blit(option_surface, (rect.x + 10, rect.y + 10))

            # Display feedback for 2 seconds
            if show_feedback:
                feedback_surface = FONT.render(feedback, True, BLACK)
                surface.blit(feedback_surface, (50, level_height - 100))
                if pygame.time.get_ticks() - feedback_time > 2000:
                    show_feedback = False
                    current_index += 1
                    options_generated = False  # Reset the flag for the next question
                    selected_option = None
                    if current_index >= len(cause_effect_pairs):
                        running = False
        else:
            # End the game
            running = False

        # Check if the attempt has exceeded 60 seconds
        if time.time() - start_time > 60 and not show_feedback:
            # Record timeout as an incorrect attempt
            results.append(["Cause and Effect", weights[attempts], 0, 60, 60])
            attempts += 1
            current_index += 1
            options_generated = False

        pygame.display.update()
        clock.tick(30)

    # Return detailed results for each attempt
    return results
