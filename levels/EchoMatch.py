import pygame
import random
import queue
import time
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


    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)

    # Define shapes and their positions based on the level dimensions
    shape_size = 60
    shapes = ['circle', 'square', 'triangle']

    def draw_shape(shape, pos):
        """Draw a white shape at a specified position."""
        if shape == 'circle':
            pygame.draw.circle(surface, WHITE, pos, shape_size // 2)
        elif shape == 'square':
            pygame.draw.rect(surface, WHITE, pygame.Rect(
                pos[0] - shape_size // 2, pos[1] - shape_size // 2, shape_size, shape_size
            ))
        elif shape == 'triangle':
            pygame.draw.polygon(surface, WHITE, [
                (pos[0], pos[1] - shape_size // 2),
                (pos[0] - shape_size // 2, pos[1] + shape_size // 2),
                (pos[0] + shape_size // 2, pos[1] + shape_size // 2)
            ])

    def show_sequence(sequence):
        """Show the sequence to the player one shape at a time."""
        for item in sequence:
            surface.fill(BLACK)
            draw_shape(item, (level_width // 2, level_height // 2))
            pygame.display.update()
            pygame.time.wait(1000)
            surface.fill(BLACK)
            pygame.display.update()
            pygame.time.wait(500)

    def present_mcq(correct_sequence):
        """Present an MCQ with the correct sequence and three random options."""
        options = [correct_sequence]
        while len(options) < 4:
            option = [random.choice(shapes) for _ in range(len(correct_sequence))]
            if option not in options:
                options.append(option)

        random.shuffle(options)

        # Blink-based selection variables
        selected_index = 0
        submit_pressed = False
        show_feedback = False
        feedback = ""
        feedback_time = 0

        # clock = pygame.time.Clock()
        running = True

        while running:
            surface.fill(BLACK)

            for i, option in enumerate(options):
                y_offset = 100 + i * 80
                x_offset = level_width // 2 - 150
                for j, item in enumerate(option):
                    draw_shape(item, (x_offset + j * 100, y_offset))

                # Highlight selected option
                if i == selected_index:
                    pygame.draw.rect(surface, WHITE, pygame.Rect(
                        x_offset - 100, y_offset - shape_size // 2 - 10, len(option) * 113 + 40, shape_size + 20), 2
                    )

            pygame.display.update()

            # Blink Control
            try:
                blink_message = blink_queue.get_nowait()
                if blink_message == "SINGLE_BLINK":
                    print("Single Blink Detected - Pygame")
                    selected_index = (selected_index + 1) % len(options)
                elif blink_message == "DOUBLE_BLINK":
                    print("Double Blink Detected - Pygame")
                    submit_pressed = True  # Ensure double blink sets submit_pressed
            except queue.Empty:
                pass
            
            # Speech Control
            try:
                if not speech_queue.empty():
                    command = speech_queue.get(block=False)
                    print(f"Recognized command: {command}")
                    if command == "down":
                        selected_index = (selected_index + 1) % len(options)
                    elif command == "up":
                        selected_index = (selected_index - 1) % len(options)
                    elif command == "select":
                        submit_pressed = True  # Ensure double blink sets submit_pressed
            except queue.Empty:
                pass


            # Keyboard Control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        submit_pressed = True  # Key-based submit remains unchanged

            if submit_pressed:
                running = False

            # clock.tick(30)

        return options[selected_index]


    def instruction_screen():
        """Displays the instruction screen."""
        font = pygame.font.SysFont(None, 30)
        surface.fill(WHITE)

        instructions = [
            "Welcome to Level 1!",
            "In this game, you will see a sequence of white shapes.",
            "Pay attention to the sequence shown on the screen.",
            "After the sequence, choose the correct option from the MCQ.",
            "Use single blink to navigate and double blink to submit."
        ]

        y_offset = 100
        for line in instructions:
            text = font.render(line, True, BLACK)
            surface.blit(text, (50, y_offset))
            y_offset += 40

        prompt_text = font.render("Press Enter to Start", True, BLACK)
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

    # Game variables
    sequence_length = 3
    attempts = 0
    weights = [2, 3, 5] # Weights for different levels of difficulty
    results = [0, 0, 0]
    max_attempts = max_attempts_arg

    start_time = time.time()

    while attempts < max_attempts:
        # Generate a sequence of shapes
        sequence = [random.choice(shapes) for _ in range(sequence_length)]

        # Show the sequence
        show_sequence(sequence)

        # Present MCQ
        correct_sequence = sequence  # Use the displayed sequence as the correct answer
        player_choice = present_mcq(correct_sequence)

        if player_choice == correct_sequence:
            results[attempts] = weights[attempts]

        sequence_length += 1
        attempts += 1

    end_time = time.time()-start_time

    blink_thread.stop()  # Stop the blink detection thread
    print(results, end_time)
    return results, end_time