import pygame
import random
import time
import sys
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


    # Define constants
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Audio files for notes
    notes = [
        {'name': 'Sa', 'sound': 'sounds/QuickAudio/001.mp3'},
        {'name': 'Re', 'sound': 'sounds/QuickAudio/002.mp3'},
        {'name': 'Ga', 'sound': 'sounds/QuickAudio/003.mp3'},
        {'name': 'Ma', 'sound': 'sounds/QuickAudio/004.mp3'},
        {'name': 'Pa', 'sound': 'sounds/QuickAudio/005.mp3'},
        {'name': 'Dha', 'sound': 'sounds/QuickAudio/006.mp3'},
        {'name': 'Ni', 'sound': 'sounds/QuickAudio/007.mp3'},
        {'name': 'Sa High', 'sound': 'sounds/QuickAudio/008.mp3'}
    ]

    # Load sounds
    for note in notes:
        try:
            note['tone'] = pygame.mixer.Sound(note['sound'])
        except pygame.error as e:
            print(f"Error loading sound {note['sound']}: {e}")
            pygame.quit()
            sys.exit()

    def play_sequence(sequence, speed=0.8):
        """Play a sequence of notes with delay between tones."""
        for index in sequence:
            note = notes[index]
            note['tone'].play()
            time.sleep(speed)
            note['tone'].stop()

    def generate_mcq(correct_sequence, num_choices=3):
        """Generate MCQs with the correct sequence and incorrect ones."""
        options = [correct_sequence]  # Start with the correct sequence
        while len(options) < num_choices:
            random_sequence = random.sample(range(len(notes)), len(correct_sequence))
            if random_sequence != correct_sequence and random_sequence not in options:
                options.append(random_sequence)
        random.shuffle(options)
        return options
    
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

    def render_centered_text(surface, text, font, color, y_offset):
        """Render text centered horizontally."""
        text_surface = font.render(text, True, color)
        x = (level_width - text_surface.get_width()) // 2
        y = (level_height // 2) + y_offset
        surface.blit(text_surface, (x, y))

    def get_player_selection(options, highlighted_index):
        """Display MCQs and return the selected option."""
        font = pygame.font.Font(None, 36)
        selected_index = highlighted_index

        while True:
            surface.fill(BLACK)
            for idx, option in enumerate(options):
                option_text = ', '.join([notes[n]['name'] for n in option])
                color = GREEN if idx == selected_index else WHITE
                render_centered_text(surface, option_text, font, color, y_offset=idx * 50 - 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return selected_index
                    
            # Blink Control
            try:
                blink_message = blink_queue.get_nowait()
                if blink_message == "SINGLE_BLINK":
                    print("Single Blink Detected - Pygame")
                    selected_index = (selected_index + 1) % len(options)
                elif blink_message == "DOUBLE_BLINK":
                    print("Double Blink Detected - Pygame")
                    return selected_index
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
                        return selected_index
            except queue.Empty:
                pass
                    
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
            "1. Wait for a musical tone to play.",
            "2. Quickly tap the object on the screen associated with the tone."
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
            nav_text = text_font.render("Press ENTER or CLICK to proceed.", True, RED)
            surface.blit(nav_text, (screen_width // 2 - nav_text.get_width() // 2, screen_height - 100))

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Proceed to the next screen
                        running = False
                # if any mouse button is pressed, proceed to the next screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

            # Update the screen
            pygame.display.flip()


    # Main game loop
    sequence = []
    max_attempts = max_attempts_arg
    attempts = 0
    running = True
    level = 3  # Start with 3 notes
    weights = [2, 3, 5] # Weights for different levels of difficulty
    results = [0, 0, 0]

    # Display instructions
    instruction_screen(surface, win_width, win_height)
    start_time = time.time()

    while running and attempts < max_attempts:
        surface.fill(BLACK)
        pygame.display.flip()
        pygame.time.wait(1000)

        # Generate sequence
        sequence = random.sample(range(len(notes)), level)

        # Play sequence
        play_sequence(sequence)

        # Generate MCQs
        mcq_options = generate_mcq(sequence)
        correct_index = mcq_options.index(sequence)

        # Get player's answer
        selected_index = get_player_selection(mcq_options, 0)

        # Check correctness
        if selected_index != correct_index:
            if attempts + 1 >= max_attempts:
                break
        else:
            level += 1  # Increase difficulty
            results[attempts] = weights[attempts]
            pygame.time.wait(500)
        
        # Increment attempts after processing the response
        attempts += 1


    end_time = time.time()-start_time

    # Final Stats
    surface.fill(BLACK)
    font = pygame.font.Font(None, 36)
    final_text = f"Final Level Reached: {level - 3}"
    render_centered_text(surface, final_text, font, WHITE, y_offset=0)
    pygame.display.flip()
    pygame.time.wait(2000)

    return results, end_time


# Example invocation for testing (set up Pygame context as needed)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.mixer.init()
    run_game(screen, 800, 600, 800, 600, max_attempts_arg=3)
    pygame.quit()
