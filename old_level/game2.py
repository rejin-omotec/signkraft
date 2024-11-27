import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
FONT = pygame.font.Font(None, 36)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cause and Effect MCQ Game")

# List of cause-effect pairs
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

# Shuffle the cause-effect pairs
random.shuffle(cause_effect_pairs)

# Game variables
current_index = 0
score = 0
selected_option = None

# Initialize options and flags
options = []
option_rects = []
options_generated = False

def generate_options(correct_cause, all_causes, num_options=4):
    options = [correct_cause]
    distractors = [cause for cause in all_causes if cause != correct_cause]
    random.shuffle(distractors)
    options.extend(distractors[:num_options - 1])
    random.shuffle(options)
    return options

def main():
    global current_index, score, selected_option, options_generated

    clock = pygame.time.Clock()
    running = True
    show_feedback = False
    feedback = ''
    feedback_time = 0  # Time when feedback was shown

    # Prepare all causes for option generation
    all_causes = [pair[0] for pair in cause_effect_pairs]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_index < len(cause_effect_pairs):
                    if not show_feedback:
                        for idx, option_rect in enumerate(option_rects):
                            if option_rect.collidepoint(event.pos):
                                selected_option = options[idx]
                                # Check the user's answer
                                correct_cause, effect = cause_effect_pairs[current_index]
                                if selected_option == correct_cause:
                                    feedback = 'Correct!'
                                    score += 1
                                else:
                                    feedback = f'Incorrect! The correct cause was: {correct_cause}'
                                show_feedback = True
                                feedback_time = pygame.time.get_ticks()
                                break

        # Clear the screen
        screen.fill(WHITE)

        if current_index < len(cause_effect_pairs):
            # Display the current effect
            correct_cause, effect = cause_effect_pairs[current_index]
            effect_surface = FONT.render("Effect: " + effect, True, BLACK)
            screen.blit(effect_surface, (100, 100))

            # Generate options only once per question
            if not options_generated:
                options = generate_options(correct_cause, all_causes)
                option_rects = []
                for idx, option in enumerate(options):
                    rect = pygame.Rect(100, 200 + idx * 60, 600, 50)
                    option_rects.append(rect)
                options_generated = True  # Set the flag to True after generating options

            # Display the options
            for idx, option in enumerate(options):
                rect = option_rects[idx]
                pygame.draw.rect(screen, LIGHT_GRAY, rect)
                option_surface = FONT.render(option, True, BLACK)
                screen.blit(option_surface, (rect.x + 10, rect.y + 10))

            # Display feedback for 2 seconds
            if show_feedback:
                feedback_surface = FONT.render(feedback, True, BLACK)
                screen.blit(feedback_surface, (100, 500))
                if pygame.time.get_ticks() - feedback_time > 2000:
                    show_feedback = False
                    current_index += 1
                    options_generated = False  # Reset the flag for the next question
                    selected_option = None
                    if current_index >= len(cause_effect_pairs):
                        running = False
        else:
            # Display the game over screen
            game_over_surface = FONT.render("Game Over!", True, BLACK)
            score_surface = FONT.render(f"Your score: {score}/{len(cause_effect_pairs)}", True, BLACK)
            screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(30)

    # Exit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
 