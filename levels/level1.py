import pygame
import random
import time

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs Level 1 with random game modes (Shapes, Colors, Colored Shapes).
    
    :param surface: Pygame surface where the game level will be rendered.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (169, 169, 169)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Define shapes and their positions based on the level dimensions
    shape_size = 60
    shapes = ['circle', 'square', 'triangle']
    shape_positions = {
        'circle': (level_width // 4, level_height // 2),
        'square': (level_width // 2, level_height // 2),
        'triangle': (3 * level_width // 4, level_height // 2),
        'rectangle': (level_width // 2, level_height // 3)
    }

    # Define colors for each shape
    shape_colors = {
        'circle': BLUE,
        'square': YELLOW,
        'triangle': RED,
        'rectangle': GREEN
    }

    def draw_shape(shape, color, pos):
        """Draw a shape at a specified position."""
        if shape == 'circle':
            pygame.draw.circle(surface, color, pos, shape_size // 2)
        elif shape == 'square':
            pygame.draw.rect(surface, color, pygame.Rect(
                pos[0] - shape_size // 2, pos[1] - shape_size // 2, shape_size, shape_size
            ))
        elif shape == 'triangle':
            pygame.draw.polygon(surface, color, [
                (pos[0], pos[1] - shape_size // 2),
                (pos[0] - shape_size // 2, pos[1] + shape_size // 2),
                (pos[0] + shape_size // 2, pos[1] + shape_size // 2)
            ])
        

    def show_sequence(sequence, mode):
        """Show the sequence to the player one shape at a time."""
        for item in sequence:
            surface.fill(BLACK)
            if mode == 'shapes':
                draw_shape(item, WHITE, (level_width // 2, level_height // 2))
            elif mode == 'colors':
                pygame.draw.rect(surface, item, pygame.Rect(
                    level_width // 2 - shape_size, level_height // 2 - shape_size, shape_size * 2, shape_size * 2))
            elif mode == 'colored_shapes':
                shape, color = item
                draw_shape(shape, color, (level_width // 2, level_height // 2))
            pygame.display.update()
            pygame.time.wait(1000)
            surface.fill(BLACK)
            pygame.display.update()
            pygame.time.wait(500)

    def present_mcq(correct_sequence, mode):
        """Present an MCQ with the correct sequence and three random options."""
        options = [correct_sequence]
        while len(options) < 4:
            if mode == 'shapes':
                option = [random.choice(shapes) for _ in range(len(correct_sequence))]
            elif mode == 'colors':
                option = [random.choice(list(shape_colors.values())) for _ in range(len(correct_sequence))]
            elif mode == 'colored_shapes':
                option = [(random.choice(shapes), random.choice(list(shape_colors.values()))) for _ in range(len(correct_sequence))]

            if option not in options:
                options.append(option)

        random.shuffle(options)

        # Display options as shapes
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 30)
        selected_index = 0

        # Add a "Submit" button rectangle
        submit_button = pygame.Rect(level_width // 2 - 50, level_height - 60, 100, 40)

        def render_options():
            surface.fill(BLACK)
            for i, option in enumerate(options):
                y_offset = 100 + i * 80
                x_offset = level_width // 2 - 150
                for j, item in enumerate(option):
                    if mode == 'shapes':
                        draw_shape(item, shape_colors.get(item, WHITE), (x_offset + j * 100, y_offset))
                    elif mode == 'colors':
                        pygame.draw.rect(surface, item, pygame.Rect(
                            x_offset + j * 100 - shape_size // 2, y_offset - shape_size // 2, shape_size, shape_size
                        ))
                    elif mode == 'colored_shapes':
                        shape, color = item
                        draw_shape(shape, color, (x_offset + j * 100, y_offset))

                # Highlight selected option
                if i == selected_index:
                    pygame.draw.rect(surface, GRAY, pygame.Rect(
                        x_offset - 50, y_offset - shape_size // 2 - 10, len(option) * 85 + 50, shape_size + 20), 2
                    )

            # Draw the submit button
            pygame.draw.rect(surface, GRAY, submit_button)
            submit_text = font.render("Submit", True, BLACK)
            surface.blit(submit_text, (submit_button.x + 10, submit_button.y + 10))

            pygame.display.update()

        render_options()

        # Capture user input for the MCQ
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected_index]
                    render_options()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    surface_rect = surface.get_abs_offset()
                    x -= surface_rect[0]
                    y -= surface_rect[1]
                    if submit_button.collidepoint(x, y):
                        return options[selected_index]

    def instruction_screen():
            """Displays the instruction screen."""
            font = pygame.font.SysFont(None, 30)
            surface.fill(WHITE)

            instructions = [
                "Welcome to Level 1!",
                "In this game, you will see a sequence of shapes or colors.",
                "Pay attention to the sequence shown on the screen.",
                "After the sequence, choose the correct option from the MCQ.",
                "Use arrow keys to navigate and Enter to submit, or use touch."
            ]

            y_offset = 100
            for line in instructions:
                text = font.render(line, True, BLACK)
                surface.blit(text, (50, y_offset))
                y_offset += 40

            prompt_text = font.render("Press Enter to Start", True, RED)
            surface.blit(prompt_text, (level_width // 2 - prompt_text.get_width() // 2, level_height - 100))

            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        return

    # Show instructions
    instruction_screen()

    # Select a random mode
    game_modes = ['shapes', 'colors', 'colored_shapes']
    

    # Game variables
    sequence_length = 3
    sequence = []
    score = 0
    attempts = 0
    results = []
    max_attempts = max_attempts_arg

    while attempts < max_attempts:
        mode = game_modes[attempts % len(game_modes)]  # Cycle through modes for each attempt
        if mode == 'shapes':
            sequence = [random.choice(shapes) for _ in range(sequence_length)]
        elif mode == 'colors':
            sequence = [random.choice(list(shape_colors.values())) for _ in range(sequence_length)]
        elif mode == 'colored_shapes':
            sequence = [(random.choice(shapes), random.choice(list(shape_colors.values()))) for _ in range(sequence_length)]

        show_sequence(sequence, mode)

        correct_sequence = sequence  # Use the displayed sequence as the correct answer
        player_choice = present_mcq(correct_sequence, mode)

        if player_choice == correct_sequence:
            score += 10
            sequence_length += 1
            results.append({
                "Game": "Level 1",
                "Attempt Type": "Success",
                "Points": 10,
                "Correct": 1,
                "Incorrect": 0
            })
        else:
            results.append({
                "Game": "Level 1",
                "Attempt Type": "Failure",
                "Points": 0,
                "Correct": 0,
                "Incorrect": 1
            })

        attempts += 1

    return results, score
