import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up display
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Image Recall Game')

# Set up fonts
FONT = pygame.font.SysFont(None, 36)

# Load images
# Ensure you have images named 'image1.png', 'image2.png', and 'image3.png' in a folder named 'images'.
NUM_IMAGES = 3
image_list = []
for i in range(1, NUM_IMAGES + 1):
    image = pygame.image.load(f'asset\Images\img{i}.png')
    image = pygame.transform.scale(image, (200, 200))  # Resize images
    image_list.append(image)

# Game variables
sequence_length = 3        # Number of images to show in the sequence
display_time = 2000        # Time to display each image (in milliseconds)
sequence = []
selected_images = []
score = 0

def show_message(message):
    """Display a message in the center of the screen."""
    SCREEN.fill((0, 0, 0))
    text = FONT.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)

def show_sequence(sequence):
    """Display the sequence of images."""
    for img in sequence:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(img, ((WIDTH - img.get_width()) // 2, (HEIGHT - img.get_height()) // 2))
        pygame.display.update()
        pygame.time.wait(display_time)
    show_message('Now recall the images!')

def selection_screen(sequence_images):
    """Allow the player to select images they recall from the sequence."""
    global selected_images
    selected_images = []
    positions = []
    # Arrange images at the bottom
    margin = 20
    img_width = (WIDTH - (len(sequence_images) + 1) * margin) // len(sequence_images)
    img_height = img_width  # Keep images square
    scaled_images = [pygame.transform.scale(img, (img_width, img_height)) for img in sequence_images]

    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        positions = []
        # Draw images at the bottom
        for i, img in enumerate(scaled_images):
            x = margin + i * (img_width + margin)
            y = HEIGHT - img_height - margin
            rect = SCREEN.blit(img, (x, y))
            positions.append(rect)
            if i in selected_images:
                pygame.draw.rect(SCREEN, (0, 255, 0), rect, 3)

        # Draw 'Done' button
        done_text = FONT.render('Done', True, (255, 255, 255))
        done_rect = done_text.get_rect(center=(WIDTH - 80, HEIGHT - 30))
        SCREEN.blit(done_text, done_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x_click, y_click = event.pos
                # Check if 'Done' button is clicked
                if done_rect.collidepoint(x_click, y_click):
                    running = False
                else:
                    # Check if any image is clicked
                    for idx, rect in enumerate(positions):
                        if rect.collidepoint(x_click, y_click):
                            if idx in selected_images:
                                selected_images.remove(idx)
                            else:
                                selected_images.append(idx)

def calculate_score(sequence, selected_indices):
    """Calculate the player's score based on correct selections."""
    correct_indices = [sequence.index(img) for img in sequence]
    correct_selections = set(correct_indices) & set(selected_indices)
    return len(correct_selections)

def main():
    global score
    while True:
        # Use the entire image list as the sequence
        sequence = image_list.copy()
        random.shuffle(sequence)  # Shuffle the sequence
        show_sequence(sequence)

        # Player selects images they recall
        selection_screen(sequence)

        # Calculate and display the score
        # Map selected indices to images
        selected_imgs = [sequence[i] for i in selected_images]
        score = calculate_score(sequence, selected_images)
        show_message(f'You identified {score}/{sequence_length} images correctly!')

        # Ask if the player wants to play again
        show_message('Play again? (Y/N)')
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_y:
                        waiting = False
                    elif event.key == K_n:
                        pygame.quit()
                        sys.exit()

if __name__ == '__main__':
    main()
