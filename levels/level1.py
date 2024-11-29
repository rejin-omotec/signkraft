import pygame
import random
import time

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Runs the Memory Recall game inside the given surface.

    :param surface: Pygame surface where the game level will be rendered.
    :param update_score_callback: Callback to update the score in the main menu.
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
    shape_size = 100
    shapes = ['circle', 'square', 'triangle']
    shape_positions = {
        'circle': (level_width // 4, level_height // 2),
        'square': (level_width // 2, level_height // 2),
        'triangle': (3 * level_width // 4, level_height // 2)
    }

    # Define colors for each shape
    shape_colors = {
        'circle': BLUE,
        'square': YELLOW,
        'triangle': RED
    }

    def draw_shape(shape, color):
        """Draw a shape on the surface."""
        if shape == 'circle':
            pygame.draw.circle(surface, color, shape_positions['circle'], shape_size // 2)
        elif shape == 'square':
            pygame.draw.rect(surface, color, pygame.Rect(
                shape_positions['square'][0] - shape_size // 2,
                shape_positions['square'][1] - shape_size // 2,
                shape_size, shape_size
            ))
        elif shape == 'triangle':
            pygame.draw.polygon(surface, color, [
                (shape_positions['triangle'][0], shape_positions['triangle'][1] - shape_size // 2),
                (shape_positions['triangle'][0] - shape_size // 2, shape_positions['triangle'][1] + shape_size // 2),
                (shape_positions['triangle'][0] + shape_size // 2, shape_positions['triangle'][1] + shape_size // 2)
            ])

    def show_sequence(sequence):
        """Show the sequence to the player one shape at a time."""
        for shape in sequence:
            surface.fill(BLACK)
            draw_shape(shape, shape_colors[shape])
            pygame.display.update()
            pygame.time.wait(1000)  # Show each shape for 1 second
            surface.fill(BLACK)
            pygame.display.update()
            pygame.time.wait(500)  # Pause for half a second between shapes

    def get_player_input(sequence_length):
        """Capture player's input sequence."""
        input_sequence = []
        start_time = time.time()

        while len(input_sequence) < sequence_length:
            elapsed_time = time.time() - start_time
            if elapsed_time > 60:  # If more than 60 seconds, time out
                return None, elapsed_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None, elapsed_time

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Translate mouse position to the subsurface coordinates
                    x, y = event.pos

                    # Get the position of the subsurface relative to the main window
                    surface_rect = surface.get_abs_offset()

                    # Adjust the mouse click coordinates relative to the subsurface
                    x -= surface_rect[0]
                    y -= surface_rect[1]

                    # Check click location against shapes
                    for shape in shapes:
                        sx, sy = shape_positions[shape]
                        if shape == 'circle':
                            # Circle collision detection depends on radius (shape_size // 2)
                            distance = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
                            if distance <= shape_size // 2:
                                input_sequence.append('circle')
                                # Show click animation (fade to gray for the clicked shape)
                                surface.fill(BLACK)
                                for s in shapes:
                                    draw_shape(s, GRAY if s == shape else shape_colors[s])
                                pygame.display.update()
                                pygame.time.wait(200)
                        elif shape == 'square':
                            # Rectangular collision detection depends on the size
                            rect = pygame.Rect(sx - shape_size // 2, sy - shape_size // 2, shape_size, shape_size)
                            if rect.collidepoint(x, y):
                                input_sequence.append('square')
                                # Show click animation (fade to gray for the clicked shape)
                                surface.fill(BLACK)
                                for s in shapes:
                                    draw_shape(s, GRAY if s == shape else shape_colors[s])
                                pygame.display.update()
                                pygame.time.wait(200)
                        elif shape == 'triangle':
                            # Use a rectangular bounding box for the triangle
                            rect = pygame.Rect(sx - shape_size // 2, sy - shape_size // 2, shape_size, shape_size)
                            if rect.collidepoint(x, y):
                                input_sequence.append('triangle')
                                # Show click animation (fade to gray for the clicked shape)
                                surface.fill(BLACK)
                                for s in shapes:
                                    draw_shape(s, GRAY if s == shape else shape_colors[s])
                                pygame.display.update()
                                pygame.time.wait(200)

            # Redraw shapes for user feedback
            surface.fill(BLACK)
            for shape in shapes:
                draw_shape(shape, shape_colors[shape])
            pygame.display.update()

        return input_sequence, time.time() - start_time
    
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
    

    # Main instruction screen function
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
            "1. The game will display a series of shapes in a specific order. ",
            "2. Pay attention to the shapes and the order they appear in. ",
            "3. You must select the shapes in the same order when prompted."
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

            # Update the screen
            pygame.display.flip()



    # Game loop variables
    initial_sequence_length = 3
    sequence_length = initial_sequence_length
    sequence = [random.choice(shapes) for _ in range(sequence_length)]
    score = 0
    correct_counter = 0
    incorrect_counter = 0
    running = True
    max_attempts = max_attempts_arg
    attempts = 0
    weights = [1.0, 1.5, 2.0]  # Weights for each attempt, increasing with each attempt as they become harder
    results = []

    instruction_screen(surface, win_width, win_height)

    while running and attempts < max_attempts:
        # Show the sequence
        show_sequence(sequence)

        # Get player's input
        player_input, time_taken = get_player_input(len(sequence))
        if player_input is None:  # User quits or times out
            results.append({
                "Game": "Memory Recall",
                "Attempt Type": "Timeout",
                "Points": 0,
                "Correct": 0,
                "Incorrect": 1,
                "Time Taken": time_taken,
                "Max Time": 60
            })
            attempts += 1
            continue

        # Check if the player's input matches the sequence
        if player_input == sequence:
            score += 1
            correct_counter += 1

            # Record result as correct attempt
            results.append({
                "Game": "Memory Recall",
                "Attempt Type": "Success",
                "Points": weights[attempts],
                "Correct": 1,
                "Incorrect": 0,
                "Time Taken": time_taken,
                "Max Time": 60
            })

            # Generate a new sequence with one additional random shape
            sequence_length += 1
            sequence = [random.choice(shapes) for _ in range(sequence_length)]

            # Display feedback for correct answer
            surface.fill(BLACK)
            font = pygame.font.SysFont(None, 35)
            text = font.render("Correct!", True, GREEN)
            surface.blit(text, (level_width // 2 - text.get_width() // 2, level_height // 2))
            pygame.display.update()
            pygame.time.wait(1000)
        else:
            incorrect_counter += 1
            # Record result as incorrect attempt
            results.append({
                "Game": "Memory Recall",
                "Attempt Type": "Failure",
                "Points": 0,
                "Correct": 0,
                "Incorrect": 1,
                "Time Taken": time_taken,
                "Max Time": 60
            })

            # Display feedback for incorrect answer
            surface.fill(BLACK)
            font = pygame.font.SysFont(None, 35)
            text = font.render("Incorrect!", True, RED)
            surface.blit(text, (level_width // 2 - text.get_width() // 2, level_height // 2))
            pygame.display.update()
            pygame.time.wait(2000)

        attempts += 1

    print("ending")
    return results, score