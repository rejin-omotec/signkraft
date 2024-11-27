import pygame
import random
import sys
from pygame.locals import *

def run_game(surface, update_score_callback, level_width, level_height, win_width, win_height):
    """
    Runs the Image Recall Game inside the provided surface.

    :param surface: The Pygame surface where the game level is rendered.
    :param update_score_callback: Callback to update the score in the main menu.
    :param level_width: Width of the game level area (subsurface).
    :param level_height: Height of the game level area (subsurface).
    :param win_width: Width of the entire window.
    :param win_height: Height of the entire window.
    """
    # Set up fonts
    FONT = pygame.font.SysFont(None, 36)

    # Load images
    NUM_IMAGES = 3
    image_list = []
    for i in range(1, NUM_IMAGES + 1):
        image = pygame.image.load(f'asset/Images/img{i}.png')
        image = pygame.transform.scale(image, (200, 200))  # Resize images
        image_list.append(image)

    # Game variables
    sequence_length = 3        # Number of images to show in the sequence
    display_time = 2000        # Time to display each image (in milliseconds)
    sequence = []
    selected_images = []
    score = 0
    max_attempts = 3
    attempts = 0
    clock = pygame.time.Clock()

    def show_message(message):
        """Display a message in the center of the subsurface."""
        surface.fill((0, 0, 0))
        text = FONT.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(level_width // 2, level_height // 2))
        surface.blit(text, rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def show_sequence(sequence):
        """Display the sequence of images."""
        for img in sequence:
            surface.fill((0, 0, 0))
            surface.blit(img, ((level_width - img.get_width()) // 2, (level_height - img.get_height()) // 2))
            pygame.display.update()
            pygame.time.wait(display_time)
        show_message('Now recall the images!')

    def selection_screen(sequence_images):
        """Allow the player to select images they recall from the sequence."""
        nonlocal selected_images
        selected_images = []
        positions = []
        margin = 20
        img_width = (level_width - (len(sequence_images) + 1) * margin) // len(sequence_images)
        img_height = img_width  # Keep images square
        scaled_images = [pygame.transform.scale(img, (img_width, img_height)) for img in sequence_images]

        running = True
        while running:
            surface.fill((0, 0, 0))
            positions = []
            # Draw images at the bottom
            for i, img in enumerate(scaled_images):
                x = margin + i * (img_width + margin)
                y = level_height - img_height - margin
                rect = surface.blit(img, (x, y))
                positions.append(rect)
                if i in selected_images:
                    pygame.draw.rect(surface, (0, 255, 0), rect, 3)

            # Draw 'Done' button
            done_text = FONT.render('Done', True, (255, 255, 255))
            done_rect = done_text.get_rect(center=(level_width - 80, level_height - 30))
            surface.blit(done_text, done_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x_click, y_click = event.pos
                    # Adjust for subsurface coordinates
                    surface_rect = surface.get_abs_offset()
                    x_click -= surface_rect[0]
                    y_click -= surface_rect[1]

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

    running = True

    while running and attempts < max_attempts:
        # Use the entire image list as the sequence
        sequence = image_list.copy()
        random.shuffle(sequence)  # Shuffle the sequence
        show_sequence(sequence)

        # Player selects images they recall
        selection_screen(sequence)

        # Calculate and display the score
        # Map selected indices to images
        score = calculate_score(sequence, selected_images)
        update_score_callback(score)  # Update score
        show_message(f'You identified {score}/{sequence_length} images correctly!')

        attempts += 1

    # Display final message before quitting the level
    show_message(f'Final Score: {score}')
    pygame.time.wait(2000)

    return score, attempts

# This function `run_game()` can now be used similarly to other levels, passing in a subsurface for it to be rendered within.
