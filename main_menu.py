import os
import csv
import pygame
import game_engine  # Import the game engine
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GAME_HEIGHT = 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE = (173, 216, 230)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 48)

# Global state
player_name = ""
player_age = ""
# game_state = "MAIN_MENU"  # MAIN_MENU, GAMEPLAY, END_SCREEN
game_state = "GAMEPLAY"  # MAIN_MENU, GAMEPLAY, END_SCREEN
current_score = 0
current_game_name = "Game Hub"

json_file_path = ""
final_domain_scores, overall_score = {}, 0


def setup_player_folder_and_json(name):
    global json_file_path
    """
    Creates a folder and JSON file for the player's name if it doesn't exist.
    """
    normalized_name = name.strip().lower()
    base_dir = "test_data"
    player_folder = os.path.join(base_dir, normalized_name)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    if not os.path.exists(player_folder):
        os.makedirs(player_folder)
        print(f"Folder created: {player_folder}")

    json_file_path = os.path.join(player_folder, f"{normalized_name}.json")

    if not os.path.exists(json_file_path):
        with open(json_file_path, mode="w") as json_file:
            json.dump({"attempts": []}, json_file)  # Initialize with an "attempts" layer
            print(f"JSON file created: {json_file_path}")
    else:
        print(f"JSON file already exists: {json_file_path}")

    return json_file_path


def save_game_result(attempt_data, overall_score, attempt_number, radar_image_path):
    """
    Appends a new game result to the player's JSON file under a specific attempt.
    """
    global json_file_path
    with open(json_file_path, mode="r") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            data = {"attempts": []}  # Initialize if the file is empty

    # Prepare attempt entry
    attempt_entry = {
        "Attempt": attempt_number,
        "Overall Score": overall_score,
        "Radar Image": radar_image_path,
        "Data": attempt_data  # Store the complete JSON data for this attempt
    }

    # Add to attempts list
    data["attempts"].append(attempt_entry)

    # Write back to file
    with open(json_file_path, mode="w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Game result saved to JSON file: {json_file_path}")



def generate_radar_plot(scores, output_path):
    """
    Generates a radar plot for the cognitive scores and saves the plot as an image.
    """
    # Extract categories and values
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Add the first value to close the radar chart
    values += values[:1]
    num_vars = len(categories)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Create radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticks([])

    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Save plot to file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def calculate_cognitive_scores(json_file_path):
    """
    Reads the JSON file, calculates cognitive scores for each category, and returns the scores as a dictionary.
    """
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    def min_max_normalization(value, min_val, max_val):
        return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

    # Categorize games for cognitive dimensions
    categories = {
        "Memory": ["Memory Sequence", "Image Recall"],
        "Attention": ["Story Game", "Whack-a-Mole"],
        "Logical Reasoning": ["Cause and Effect", "Image Analogy"],
        "Spatial Reasoning": ["Shape Orientation"],
        "Abstract Reasoning": ["Image Analogy", "Story Game"],
        "Fluid Reasoning": ["Image Sequence"]
    }

    scores = {key: [] for key in categories.keys()}

    # Debug: Print the loaded JSON data
    print("\nLoaded JSON Data:")
    print(json.dumps(data, indent=2))

    for record in data:
        # Debug: Print each record being processed
        print("\nProcessing Record:")
        print(record)

        game_name = record.get("Game", "")
        weight = record.get("Weight", 1)
        correct = record.get("Correct", 0)
        incorrect = record.get("Incorrect", 0)
        time_taken = record.get("Time Taken", 0)
        total_time = record.get("Max Time", 60)  # Adjusted to "Max Time" based on JSON

        # Debug: Check key extraction
        print(f"Extracted values -> Game: {game_name}, Weight: {weight}, Correct: {correct}, Incorrect: {incorrect}, Time Taken: {time_taken}, Max Time: {total_time}")

        # Validate data and handle missing or zero values
        if not game_name or (correct == 0 and incorrect == 0):
            print("Skipping invalid or incomplete record.")
            continue

        success_rate = correct / (correct + incorrect) if (correct + incorrect) > 0 else 0
        normalized_time = min_max_normalization(time_taken, 0, total_time)
        game_score = weight * success_rate * (1 - normalized_time)

        # Debug: Print calculated game score
        print(f"Calculated Score: {game_score}")

        # Assign scores to appropriate categories
        for category, games in categories.items():
            if game_name in games:
                scores[category].append(game_score)
                print(f"Assigned score {game_score} to category {category}")

    # Calculate average scores for each category
    aggregated_scores = {
        key: round(sum(value) / len(value), 2) if value else 0 for key, value in scores.items()
    }

    # Debug: Print category-wise scores
    print("\nCategory Scores Before Aggregation:")
    print(scores)

    # Calculate overall concentration as the average of all scores
    if aggregated_scores:
        aggregated_scores["Concentration"] = round(sum(aggregated_scores.values()) / len(aggregated_scores), 2)

    # Debug: Print final aggregated scores
    print("\nFinal Aggregated Scores:")
    print(aggregated_scores)

    # Generate and save radar plot
    output_dir = os.path.dirname(json_file_path)
    radar_image_path = os.path.join(output_dir, "radar_plot.png")
    generate_radar_plot(aggregated_scores, radar_image_path)

    return aggregated_scores, radar_image_path


def draw_end_screen(screen, cognitive_scores, radar_image_path):
    """
    Displays the end screen with smaller text on the left and a larger radar plot on the right.
    """
    global current_score

    # Clear the screen
    screen.fill(WHITE)

    # Adjusted fonts for smaller text
    small_font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 50)

    # Title centered at the top
    title_surface = title_font.render("Game Over!", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

    # Display final score on the left
    score_surface = small_font.render(f"Final Score: {current_score}", True, BLACK)
    screen.blit(score_surface, (30, 100))

    # Display cognitive scores on the left side with smaller font
    y_offset = 140
    for key, value in cognitive_scores.items():
        score_text = small_font.render(f"{key}: {value}", True, BLACK)
        screen.blit(score_text, (30, y_offset))
        y_offset += 30

    # Load and display the radar plot image on the right side
    try:
        radar_image = pygame.image.load(radar_image_path)

        # Calculate scale while maintaining proportions for a larger image
        max_width = 500  # Increased maximum width
        max_height = 500  # Increased maximum height
        image_width, image_height = radar_image.get_size()
        scale_factor = min(max_width / image_width, max_height / image_height)

        # Apply scaling
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        radar_image = pygame.transform.scale(radar_image, (new_width, new_height))

        # Position the scaled image
        radar_x = WIDTH - new_width - 30  # Right margin
        radar_y = 80  # Align with the top of the text
        screen.blit(radar_image, (radar_x, radar_y))
    except Exception as e:
        # Display an error message if the image cannot be loaded
        error_surface = small_font.render("Error loading radar image!", True, RED)
        screen.blit(error_surface, (WIDTH - 30 - error_surface.get_width(), 100))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Update the display
    pygame.display.update()




def draw_main_menu(screen):
    """
    Displays the main menu, collects player details, and handles navigation.
    """
    global player_name, player_age, game_state

    name_rect = pygame.Rect(300, 200, 200, 40)
    age_rect = pygame.Rect(300, 300, 200, 40)
    start_button = pygame.Rect(WIDTH // 2 - 50, 400, 100, 50)
    video_button = pygame.Rect(WIDTH // 2 - 125, 480, 250, 50)  # Adjusted button size
    input_active = {"name": False, "age": False}
    showing_video = False

    # Load the instructional video
    video_path = "data/instruction.mp4"
    video_capture = None
    video_original_width = 0
    video_original_height = 0
    if os.path.exists(video_path):
        video_capture = cv2.VideoCapture(video_path)
        video_fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        video_original_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_original_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    else:
        print("Instructional video not found.")

    # Clock for controlling video playback speed
    clock = pygame.time.Clock()

    while game_state == "MAIN_MENU":
        if showing_video:
            if video_capture and video_capture.isOpened():
                # Grab the next frame from the video
                ret, frame = video_capture.read()
                if not ret:
                    # If no frame is returned, video is done or error occurred
                    showing_video = False
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
                    continue

                # Calculate the aspect ratio and scale factor
                video_aspect_ratio = video_original_width / video_original_height
                screen_aspect_ratio = WIDTH / HEIGHT
                if video_aspect_ratio > screen_aspect_ratio:
                    scale_factor = WIDTH / video_original_width
                else:
                    scale_factor = HEIGHT / video_original_height

                # Resize the frame while maintaining aspect ratio
                new_width = int(video_original_width * scale_factor)
                new_height = int(video_original_height * scale_factor)
                frame = cv2.resize(frame, (new_width, new_height))

                # Convert the frame to a Pygame Surface
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert color to RGB
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                # Center the frame on the screen
                frame_x = (WIDTH - new_width) // 2
                frame_y = (HEIGHT - new_height) // 2
                screen.blit(frame_surface, (frame_x, frame_y))

            # Display the skip button
            skip_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)
            pygame.draw.rect(screen, RED, skip_button)
            skip_text = FONT.render("Skip", True, WHITE)
            screen.blit(skip_text, (skip_button.x + 10, skip_button.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if skip_button.collidepoint(event.pos):
                        showing_video = False

            pygame.display.update()
            clock.tick(video_fps)  # Limit to video FPS
            continue

        screen.fill(WHITE)

        # Title
        title_surface = TITLE_FONT.render("Welcome to the Game Hub", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Labels for Name and Age
        name_label = FONT.render("Name:", True, BLACK)
        age_label = FONT.render("Age:", True, BLACK)
        screen.blit(name_label, (200, 210))
        screen.blit(age_label, (200, 310))

        # Player Name Input
        pygame.draw.rect(screen, GRAY, name_rect)
        name_text = FONT.render(player_name, True, BLACK)
        screen.blit(name_text, (name_rect.x + 10, name_rect.y + 10))

        # Player Age Input
        pygame.draw.rect(screen, GRAY, age_rect)
        age_text = FONT.render(player_age, True, BLACK)
        screen.blit(age_text, (age_rect.x + 10, age_rect.y + 10))

        # Start Button
        pygame.draw.rect(screen, BLACK, start_button)
        start_text = FONT.render("Start", True, WHITE)
        screen.blit(start_text, (start_button.x + 10, start_button.y + 10))

        # Instructional Video Button
        pygame.draw.rect(screen, BLUE, video_button)
        video_text = FONT.render("Watch Instructions", True, WHITE)
        text_x = video_button.x + (video_button.width - video_text.get_width()) // 2
        text_y = video_button.y + (video_button.height - video_text.get_height()) // 2
        screen.blit(video_text, (text_x, text_y))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if name_rect.collidepoint(x, y):
                    input_active["name"] = True
                    input_active["age"] = False
                elif age_rect.collidepoint(x, y):
                    input_active["name"] = False
                    input_active["age"] = True
                elif start_button.collidepoint(x, y):
                    if player_name and player_age.isdigit():
                        setup_player_folder_and_json(player_name)
                        game_state = "GAMEPLAY"
                elif video_button.collidepoint(x, y):
                    showing_video = True

            if event.type == pygame.KEYDOWN:
                if input_active["name"]:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                elif input_active["age"]:
                    if event.key == pygame.K_BACKSPACE:
                        player_age = player_age[:-1]
                    elif event.unicode.isdigit():
                        player_age += event.unicode

        pygame.display.update()



def draw_status_bar(screen):
    """
    Draws the status bar at the top of the screen during gameplay.
    """
    # Top Status Bar
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, 50))
    score_text = FONT.render(f"Score: {current_score}", True, BLACK)
    game_name_text = FONT.render(f"Game: {current_game_name}", True, BLACK)
    screen.blit(score_text, (20, 15))
    screen.blit(game_name_text, (WIDTH - game_name_text.get_width() - 20, 15))


def draw_bottom_bar(screen):
    """
    Draws the bottom bar at the bottom of the screen during gameplay.
    """
    # Bottom Bar
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 50, WIDTH, 50))


def main():
    """
    Main function to manage the game loop and states.
    """
    global game_state, current_score, current_game_name, final_domain_scores, overall_score

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Hub")

    cognitive_bool = False

    while True:
        if game_state == "MAIN_MENU":
            draw_main_menu(screen)
        elif game_state == "GAMEPLAY":
            # Fill the background
            screen.fill(WHITE)

            # Draw status bar and bottom bar
            draw_status_bar(screen)
            draw_bottom_bar(screen)

            # Define the game area rectangle (middle 500px of height)
            game_area = pygame.Rect(0, 50, WIDTH, GAME_HEIGHT)
            game_surface = screen.subsurface(game_area)

            # Pass control to the game engine (only the game area is passed)
            final_domain_scores, overall_score = game_engine.run(game_surface, player_name, player_age, current_score, WIDTH, GAME_HEIGHT)
            game_state = "END_SCREEN"
       

        elif game_state == "END_SCREEN":
            if not cognitive_bool:
                # Determine the output directory and attempt-specific radar image path
                output_dir = os.path.dirname(json_file_path)
                try:
                    with open(json_file_path, "r") as json_file:
                        data = json.load(json_file)
                        attempt_number = len(data["attempts"]) + 1  # Calculate the current attempt number
                except (json.JSONDecodeError, KeyError):
                    attempt_number = 1  # Start fresh if file is empty or corrupted

                radar_image_path = os.path.join(output_dir, f"attempt_{attempt_number}_radar.png")

                # Generate and save radar plot for this attempt
                generate_radar_plot(final_domain_scores, radar_image_path)

                # Store the result
                save_game_result(
                    attempt_data=final_domain_scores,
                    overall_score=overall_score,
                    attempt_number=attempt_number,
                    radar_image_path=radar_image_path
                )

                cognitive_bool = True

            # Draw the end screen with the current attempt's radar image
            draw_end_screen(screen, final_domain_scores, radar_image_path)





if __name__ == "__main__":
    main()