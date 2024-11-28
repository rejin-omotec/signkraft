import importlib

def run(screen, player_name, player_age, initial_score, WIDTH, GAME_HEIGHT):
    """
    Runs the game engine, managing levels and score.
    :param screen: Pygame display surface.
    :param player_name: Name of the player.
    :param player_age: Age of the player.
    :param initial_score: Initial score passed from the main menu.
    :return: Final score after all levels.
    """
    max_attempts = 3

    levels = [
        # {"name": "Level 1", "module": "levels.level1"},
        # {"name": "Level 2", "module": "levels.level2"},
        # {"name": "Level 3", "module": "levels.level3"},
        # {"name": "Level 4", "module": "levels.level4"},
        # {"name": "Level 5", "module": "levels.level5"},
        # {"name": "Level 6", "module": "levels.level6"},
        # {"name": "Level 7", "module": "levels.level7"},
        # {"name": "Level 8", "module": "levels.level8"},
        {"name": "Level 9", "module": "levels.level9"},
    ]

    win_width, win_height = screen.get_size()

    current_score = initial_score

    for level in levels:
        # Dynamically import the level module
        level_module = importlib.import_module(level["module"])

        print(f"Running {level['name']}...")
        
        # Define a callback to update the score
        def update_score(points):
            nonlocal current_score
            current_score += points
            print(f"Current Score: {current_score}")

        # Run the level
        result_list = level_module.run_game(screen, update_score, WIDTH, GAME_HEIGHT, win_width, win_height, max_attempts)
        print(result_list)
        # ["Cause and Effect", weights[attempts], correct, incorrect, time_taken, 60]

    return current_score
