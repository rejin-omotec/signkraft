import os
import csv
import pygame
import game_engine  # Import the game engine
import json

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

# Fonts
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 48)

# Global state
player_name = ""
player_age = ""
game_state = "MAIN_MENU"  # MAIN_MENU, GAMEPLAY, END_SCREEN
current_score = 0
current_game_name = "Game Hub"

json_file_path = ""


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
            json.dump([], json_file)
            print(f"JSON file created: {json_file_path}")
    else:
        print(f"JSON file already exists: {json_file_path}")

    return json_file_path


def save_game_result(game_name, weight, correct, incorrect, time_taken, total_time):
    """
    Appends a new game result to the player's JSON file.
    """
    global json_file_path
    with open(json_file_path, mode="r") as json_file:
        data = json.load(json_file)

    game_result = {
        "Game Name": game_name,
        "Weight": weight,
        "Correct": correct,
        "Incorrect": incorrect,
        "Time Taken": time_taken,
        "Total Time": total_time
    }
    data.append(game_result)

    with open(json_file_path, mode="w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Game result saved to JSON file: {json_file_path}")


def calculate_cognitive_scores():
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

    return aggregated_scores




def draw_end_screen(screen, cognitive_scores):
    """
    Displays the end screen with calculated cognitive scores.
    """
    global current_score

    screen.fill(WHITE)
    title_surface = TITLE_FONT.render("Game Over!", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

    # Display final score
    score_surface = FONT.render(f"Final Score: {current_score}", True, BLACK)
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 200))

    # Display cognitive scores
    y_offset = 300
    for key, value in cognitive_scores.items():
        score_text = FONT.render(f"{key}: {value}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 50

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()




def draw_main_menu(screen):
    """
    Displays the main menu, collects player details, and handles navigation.
    """
    global player_name, player_age, game_state

    name_rect = pygame.Rect(300, 200, 200, 40)
    age_rect = pygame.Rect(300, 300, 200, 40)
    start_button = pygame.Rect(WIDTH // 2 - 50, 400, 100, 50)
    input_active = {"name": False, "age": False}

    while game_state == "MAIN_MENU":
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
                        # Create folder and CSV for the player
                        csv_file_path = setup_player_folder_and_json(player_name)
                        print(f"CSV Writer ready: {csv_file_path}")
                        game_state = "GAMEPLAY"

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
    global game_state, current_score, csv_file_path, current_game_name

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
            current_score = game_engine.run(game_surface, player_name, player_age, current_score, json_file_path, WIDTH, GAME_HEIGHT)
            game_state = "END_SCREEN"
        # elif game_state == "END_SCREEN":
        #     # Display the end screen
        #     screen.fill(WHITE)
        #     title_surface = TITLE_FONT.render("Game Over!", True, BLACK)
        #     screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))
        #     score_surface = FONT.render(f"Final Score: {current_score}", True, BLACK)
        #     screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 200))

        #     # Add Restart or Exit options
        #     restart_button = pygame.Rect(WIDTH // 2 - 50, 300, 100, 50)
        #     pygame.draw.rect(screen, BLACK, restart_button)
        #     restart_text = FONT.render("Restart", True, WHITE)
        #     screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))

        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             exit()
        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             if restart_button.collidepoint(event.pos):
        #                 game_state = "MAIN_MENU"

        #     pygame.display.update()
        elif game_state == "END_SCREEN":
            if not cognitive_bool:
                cognitive_scores = calculate_cognitive_scores()
                cognitive_bool = True
            draw_end_screen(screen, cognitive_scores)


if __name__ == "__main__":
    main()