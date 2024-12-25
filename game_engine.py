import importlib
import json
import os

import importlib
import json
import os

def run(screen, player_name, player_age, initial_score, json_file_path, WIDTH, GAME_HEIGHT):
    """
    Runs the game engine, managing levels and score.
    :param screen: Pygame display surface.
    :param player_name: Name of the player.
    :param player_age: Age of the player.
    :param initial_score: Initial score passed from the main menu.
    :param json_file_path: Path to the JSON file to record game data.
    :param WIDTH: Width of the game area.
    :param GAME_HEIGHT: Height of the game area.
    :return: Final score after all levels.
    """
    max_attempts = 3

    levels = [
        # {"name": "Form", "module": "levels.form"},
        {"name": "Level 1", "module": "levels.EchoMatch"},
        {"name": "Level 6", "module": "levels.PicChime"},
        {"name": "Level 3", "module": "levels.StoryWeaver"},
        {"name": "Level 9", "module": "levels.LogicLink"},
        {"name": "Level 5", "module": "levels.QuickAudio"},
        {"name": "Level 8", "module": "levels.BlockMorph"},
        {"name": "Level 10", "module": "levels.QuickTap"},
        {"name": "Level 2", "module": "levels.ChainReaction"},
        {"name": "Level 11", "module": "levels.NumberSort"},
        {"name": "Level 12", "module": "levels.SpotTheDifference"},
        # {"name": "Level 13", "module": "levels.test"},
    ]



    win_width, win_height = screen.get_size()

    current_score = initial_score

    # Load existing JSON data or initialize a new list
    if os.path.exists(json_file_path):
        with open(json_file_path, mode="r") as json_file:
            data = json.load(json_file)
    else:
        data = []

    for level in levels:
        # Dynamically import the level module
        level_module = importlib.import_module(level["module"])

        print(f"Running {level['name']}...")

        # Run the level and get the results
        result_list, time = level_module.run_game(screen, WIDTH, GAME_HEIGHT, win_width, win_height, max_attempts)

        # current_score += points
        # print(f"Current Score: {current_score}")


        # # Append each result to the JSON file with additional metadata
        # for attempt in result_list:
        #     attempt_data = {
        #         "Player Name": player_name,
        #         "Player Age": player_age,
        #         "Level Name": level["name"],
        #         **attempt  # Unpack the JSON returned by the game level
        #     }
        #     data.append(attempt_data)
        #     print(f"Logged to JSON: {attempt_data}")

    # Save the updated data back to the JSON file
    with open(json_file_path, mode="w") as json_file:
        json.dump(data, json_file, indent=4)

    return current_score

