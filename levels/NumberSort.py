import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrange Currency Notes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 36)

# Grid dimensions
GRID_ROWS = 1
GRID_COLS = 7
GRID_CELL_WIDTH = 100
GRID_CELL_HEIGHT = 50
GRID_MARGIN_X = (WIDTH - (GRID_COLS * GRID_CELL_WIDTH)) // 2
GRID_MARGIN_Y = (HEIGHT - (GRID_ROWS * GRID_CELL_HEIGHT)) // 2

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
    note["image"] = pygame.transform.scale(note["image"], (100, 50))

# Shuffle the notes for random display
random.shuffle(notes)

# Grid dimensions (adjust based on the number of notes)
GRID_COLS = len(notes)
GRID_ROWS = 1
GRID_CELL_WIDTH = 100
GRID_CELL_HEIGHT = 50
GRID_MARGIN_X = (WIDTH - (GRID_COLS * GRID_CELL_WIDTH)) // 2
GRID_MARGIN_Y = (HEIGHT - (GRID_ROWS * GRID_CELL_HEIGHT)) // 2

# Note positions (snap to grid)
def get_grid_positions():
    positions = []
    for col in range(GRID_COLS):
        x = GRID_MARGIN_X + col * GRID_CELL_WIDTH
        y = GRID_MARGIN_Y
        positions.append((x, y))
    return positions

grid_positions = get_grid_positions()

# Game variables
selected_note = None
start_time = time.time()
game_over = False
note_offset = (0, 0)
correct_sequence = False

# Helper function to check order correctness
def is_correct_order():
    # Get the current visual order of notes based on grid positions
    visual_order = [
        notes[grid_positions.index(pos)]["value"] for pos in sorted(grid_positions, key=lambda p: p[0])
    ]
    return visual_order == sorted(visual_order)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw the grid
    for col in range(GRID_COLS):
        x = GRID_MARGIN_X + col * GRID_CELL_WIDTH
        y = GRID_MARGIN_Y
        pygame.draw.rect(screen, GRAY, (x, y, GRID_CELL_WIDTH, GRID_CELL_HEIGHT), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            for i, pos in enumerate(grid_positions):
                rect = pygame.Rect(pos[0], pos[1], GRID_CELL_WIDTH, GRID_CELL_HEIGHT)
                if rect.collidepoint(event.pos):
                    selected_note = i
                    note_offset = (event.pos[0] - pos[0], event.pos[1] - pos[1])

        elif event.type == pygame.MOUSEBUTTONUP and not game_over:
            if selected_note is not None:
                for i, pos in enumerate(grid_positions):
                    rect = pygame.Rect(pos[0], pos[1], GRID_CELL_WIDTH, GRID_CELL_HEIGHT)
                    if rect.collidepoint(event.pos):
                        # Swap positions
                        grid_positions[selected_note], grid_positions[i] = grid_positions[i], grid_positions[selected_note]
                        notes[selected_note], notes[i] = notes[i], notes[selected_note]
                        break
                selected_note = None

        elif event.type == pygame.MOUSEMOTION and selected_note is not None:
            # Move the selected note with the mouse
            grid_positions[selected_note] = (event.pos[0] - note_offset[0], event.pos[1] - note_offset[1])

    # Snap notes to grid
    for i, pos in enumerate(grid_positions):
        closest_grid_pos = min(grid_positions, key=lambda gp: abs(gp[0] - pos[0]) + abs(gp[1] - pos[1]))
        grid_positions[i] = closest_grid_pos

    # Draw notes
    for i, note in enumerate(notes):
        screen.blit(note["image"], grid_positions[i])
        text = font.render(str(note["value"]), True, BLACK)
        screen.blit(text, (grid_positions[i][0] + 30, grid_positions[i][1] + 60))

    # Check order
    if not game_over and is_correct_order():
        game_over = True
        correct_sequence = True
        end_time = time.time()
        duration = end_time - start_time

    # Display game over or correct message
    if game_over:
        if correct_sequence:
            text = font.render(f"Correct! Time: {duration:.2f}s", True, GREEN)
        else:
            text = font.render(f"Game Over! Time: {duration:.2f}s", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    pygame.display.flip()

pygame.quit()
