import pygame
import random
import time
import queue
from mods.audio_detect import SpeechRecognitionThread  # Replace with your actual module name

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    # Initialize Pygame
    pygame.init()

    # speech detection setup
    speech_queue = queue.Queue(maxsize=10)
    speech_thread = SpeechRecognitionThread(audio_queue=speech_queue, language="english")
    speech_thread.start()


    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (50, 205, 50)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)
    
    # Font
    font = pygame.font.Font(None, 36)

    # Load currency note images and their values
    notes = [
        {"value": 10, "image": pygame.image.load("images/numbersort/10.jpeg")},
        {"value": 50, "image": pygame.image.load("images/numbersort/50.jpeg")},
        {"value": 100, "image": pygame.image.load("images/numbersort/100.jpeg")},
        {"value": 200, "image": pygame.image.load("images/numbersort/200.jpeg")},
        {"value": 500, "image": pygame.image.load("images/numbersort/500.jpeg")},
        {"value": 2000, "image": pygame.image.load("images/numbersort/2000.jpeg")},
    ]

    # Resize images for consistent display
    for note in notes:
        note["image"] = pygame.transform.scale(note["image"], (180, 90))

    # Game variables
    attempts = 0
    max_attempts = max_attempts_arg
    weights = [2, 3, 5] # Weights for different levels of difficulty
    results = [0, 0, 0]

    start_time = time.time()


    while attempts < max_attempts:
        random.shuffle(notes)
        selected_index = 0
        arranged_notes = []
        game_over = False
        start_time = time.time()
        
        def draw_grid():
            for i, note in enumerate(notes):
                row = i // 3
                col = i % 3
                x = GRID_MARGIN_X + col * GRID_CELL_WIDTH
                y = GRID_MARGIN_Y + row * GRID_CELL_HEIGHT
                color = BLUE if i == selected_index else GRAY
                pygame.draw.rect(surface, color, (x, y, GRID_CELL_WIDTH, GRID_CELL_HEIGHT), 2)
                surface.blit(note["image"], (x + 10, y + 10))

        def draw_arranged_notes():
            for i, note in enumerate(arranged_notes):
                x = 10 + i * (GRID_CELL_WIDTH // 2)
                scaled_image = pygame.transform.scale(note["image"], (GRID_CELL_WIDTH // 2, GRID_CELL_HEIGHT // 2))
                surface.blit(scaled_image, (x, arranged_notes_y))

        def is_correct_order():
            return [note["value"] for note in arranged_notes] == sorted([note["value"] for note in arranged_notes])

        GRID_CELL_WIDTH = 180
        GRID_CELL_HEIGHT = 90
        GRID_MARGIN_X = (level_width - (3 * GRID_CELL_WIDTH)) // 2
        GRID_MARGIN_Y = 100
        arranged_notes_y = level_height - 120

        running = True
        while running:
            surface.fill(WHITE)
            draw_grid()
            draw_arranged_notes()

            if len(arranged_notes) == len(notes):
                game_over = True
                end_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(notes)
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(notes)
                    elif event.key == pygame.K_RETURN and not game_over:
                        if notes[selected_index] not in arranged_notes:
                            arranged_notes.append(notes[selected_index])

            # Speech Control
            try:
                if not speech_queue.empty():
                    command = speech_queue.get(block=False)
                    print(f"Recognized command: {command}")
                    if command == "next":
                        selected_index = (selected_index - 1) % len(notes)
                    elif command == "previous":
                        selected_index = (selected_index + 1) % len(notes)
                    elif command == "select":
                        if notes[selected_index] not in arranged_notes:
                            arranged_notes.append(notes[selected_index])
            except queue.Empty:
                pass


            if game_over:
                if is_correct_order():
                    results[attempts] = weights[attempts]
                running = False

            pygame.display.flip()

        attempts += 1

    end_time = time.time()-start_time

    pygame.quit()
    return results, end_time
