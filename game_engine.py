import importlib
import csv

def run(screen, player_name, player_age, initial_score, csv_file_path, WIDTH, GAME_HEIGHT):
    """
    Runs the game engine, managing levels and score.
    :param screen: Pygame display surface.
    :param player_name: Name of the player.
    :param player_age: Age of the player.
    :param initial_score: Initial score passed from the main menu.
    :param csv_file_path: Path to the CSV file to record game data.
    :param WIDTH: Width of the game area.
    :param GAME_HEIGHT: Height of the game area.
    :return: Final score after all levels.
    """
    max_attempts = 3

    levels = [
        # {"name": "Level 1", "module": "levels.level1"},
        {"name": "Level 2", "module": "levels.level2"},
        # {"name": "Level 3", "module": "levels.level3"},
        # {"name": "Level 4", "module": "levels.level4"},
        # {"name": "Level 5", "module": "levels.level5"},
        # {"name": "Level 6", "module": "levels.level6"},
        # {"name": "Level 7", "module": "levels.level7"},
        # {"name": "Level 8", "module": "levels.level8"},
        # {"name": "Level 9", "module": "levels.level9"},
    ]

    win_width, win_height = screen.get_size()

    current_score = initial_score

    # Open the CSV file for appending
    with open(csv_file_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write headers if CSV is empty
        if csv_file.tell() == 0:  # Check if the file is empty
            writer.writerow(["Player Name", "Player Age", "Level Name", "Attempt Type", "Points", "Correct", "Incorrect", "Time Taken", "Max Time"])

        for level in levels:
            # Dynamically import the level module
            level_module = importlib.import_module(level["module"])

            print(f"Running {level['name']}...")

            # Define a callback to update the score
            def update_score(points):
                nonlocal current_score
                current_score += points
                print(f"Current Score: {current_score}")

            # Run the level and get the results
            result_list = level_module.run_game(screen, update_score, WIDTH, GAME_HEIGHT, win_width, win_height, max_attempts)
            
            # Example result_list format: [["Attempt Type", 10, 2, 1, 45, 60], ["Attempt Type", 8, 1, 2, 50, 60], ...]
            for attempt in result_list:
                # Write each attempt to the CSV
                row = [level["name"]] + attempt
                writer.writerow(row)
                print(f"Logged to CSV: {row}")

    return current_score

