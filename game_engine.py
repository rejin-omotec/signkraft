import importlib

def calculate_time_score(time_taken, max_time):
    """
    Calculates the time score based on time taken and max allotted time.
    """
    time_fraction = time_taken / max_time
    time_score = max(1, 10 - int(time_fraction * 10))  # Scale to a 10-point system
    print("Time Score:", time_score)
    return time_score

def calculate_combined_score(game_score, time_score):
    """
    Combines game and time scores using weights.
    """
    return (game_score * 0.7) + (time_score * 0.3)

def calculate_domain_scores(data, domain_weights, game_weights):
    """
    Calculates the final domain scores based on individual game contributions.
    """
    # Initialize domain scores
    domain_scores = {domain: 0 for domain in domain_weights.keys()}
    domain_contributions = {domain: [] for domain in domain_weights.keys()}  # For debug purposes

    for record in data:
        game_name = record.get("Level Name")
        combined_score = record.get("Combined Score", 0)

        # Distribute game scores into respective domains
        for domain, games in game_weights.items():
            if game_name in games:
                game_weight = games[game_name]
                weighted_score = combined_score * game_weight
                domain_scores[domain] += weighted_score
                domain_contributions[domain].append((game_name, combined_score, game_weight, weighted_score))

    # Apply domain weights
    final_domain_scores = {
        domain: round(score * domain_weights[domain], 2) for domain, score in domain_scores.items()
    }

    # Calculate overall score as the sum of all domain scores
    overall_score = round(sum(final_domain_scores.values()), 2)

    # Debug: Print detailed contributions
    print("\nDomain Contributions:")
    for domain, contributions in domain_contributions.items():
        print(f"{domain}:")
        for game_name, combined_score, game_weight, weighted_score in contributions:
            print(f"  {game_name}: Score={combined_score}, Weight={game_weight}, Weighted Contribution={weighted_score}")

    print("\nOverall Score:", overall_score)

    return final_domain_scores, overall_score


def run(screen, player_name, player_age, initial_score, WIDTH, GAME_HEIGHT):
    """
    Runs the game engine, managing levels and score.
    """
    max_attempts = 3

    levels = [
        {"name": "form", "module": "levels.form", "max_time": 120},
        {"name": "EchoMatch", "module": "levels.EchoMatch", "max_time": 120},
        {"name": "PicChime", "module": "levels.PicChime", "max_time": 120},
        {"name": "StoryWeave", "module": "levels.StoryWeaver", "max_time": 180},     
        {"name": "LogicLink", "module": "levels.LogicLink", "max_time": 60},
        {"name": "QuickAudio", "module": "levels.QuickAudio", "max_time": 60},
        {"name": "BlockMorph", "module": "levels.BlockMorph", "max_time": 60},
        {"name": "QuickTap", "module": "levels.QuickTap", "max_time": 30},            
        {"name": "ChainReaction", "module": "levels.ChainReaction", "max_time": 60},
        {"name": "NumberSort", "module": "levels.NumberSort", "max_time": 60},
        {"name": "SpotTheDifference", "module": "levels.SpotTheDifference", "max_time": 120},
        {"name": "PersonalQuiz", "module": "levels.PersonalQuiz", "max_time": 60},
    ]

    # levels = [
    #     # {"name": "form", "module": "levels.form", "max_time": 120},
    #     {"name": "EchoMatch", "module": "test_levels.EchoMatch", "max_time": 120},
    #     {"name": "PicChime", "module": "test_levels.PicChime", "max_time": 120},
    #     {"name": "StoryWeave", "module": "test_levels.StoryWeaver", "max_time": 180},
    #     {"name": "LogicLink", "module": "test_levels.LogicLink", "max_time": 60},
    #     {"name": "QuickAudio", "module": "test_levels.QuickAudio", "max_time": 60},
    #     {"name": "BlockMorph", "module": "test_levels.BlockMorph", "max_time": 60},
    #     {"name": "QuickTap", "module": "test_levels.QuickTap", "max_time": 30},
    #     {"name": "ChainReaction", "module": "test_levels.ChainReaction", "max_time": 60},
    #     {"name": "NumberSort", "module": "test_levels.NumberSort", "max_time": 60},
    #     {"name": "SpotTheDifference", "module": "test_levels.SpotTheDifference", "max_time": 120},
    #     {"name": "PersonalQuiz", "module": "test_levels.PersonalQuiz", "max_time": 60},
    # ]

    win_width, win_height = screen.get_size()
    current_score = initial_score

    # Data to store level results in memory
    game_results = []

    for level in levels:
        # Dynamically import the level module
        level_module = importlib.import_module(level["module"])

        print(f"Running {level['name']}...")

        # Run the level and get the results
        result_list, time_taken = level_module.run_game(screen, WIDTH, GAME_HEIGHT, win_width, win_height, max_attempts)

        normalized_game_score = sum(result_list)

        # Calculate time efficiency score
        time_score = calculate_time_score(time_taken, level["max_time"])

        # Combine scores
        combined_score = calculate_combined_score(normalized_game_score, time_score)

        current_score += combined_score

        print(f"Combined Score: {combined_score}")

        # Store the result in memory
        game_results.append({
            "Level Name": level["name"],
            "Combined Score": combined_score
        })

    # Domain weights and game weights
    domain_weights = {
        "Memory": 0.4264699478,
        "Attention": 0.1916217044,
        "Language Skills": 0.08756782707,
        "Perception": 0.1370381436,
        "Executive Functions": 0.06795128675,
        "Visuospatial Abilities": 0.04978195458,
        "Reasoning": 0.03956913592,
    }

    game_weights = {
        "Memory": {
            "EchoMatch": 0.1183972954,
            "PicChime": 0.2036272902,
            "StoryWeave": 0.3424397655,
            "QuickAudio": 0.07058380898,
            "SpotTheDifference": 0.06132454972,
            "PersonalQuiz": 0.2036272902,
        },
        "Attention": {
            "EchoMatch": 0.06781119646,
            "PicChime": 0.04668004632,
            "QuickAudio": 0.1612283312,
            "BlockMorph": 0.2689511675,
            "QuickTap": 0.1940127654,
            "NumberSort": 0.1171273612,
            "SpotTheDifference": 0.144189132,
        },
        "Language Skills": {
            "StoryWeave": 0.5,
            "LogicLink": 0.5,
        },
        "Perception": {
            "NumberSort": 0.5,
            "SpotTheDifference": 0.5,
        },
        "Executive Functions": {
            "PicChime": 0.2604471507,
            "BlockMorph": 0.6334107424,
            "NumberSort": 0.1061421069,
        },
        "Visuospatial Abilities": {
            "PicChime": 0.1061421069,
            "BlockMorph": 0.2604471507,
            "NumberSort": 0.6334107424,
        },
        "Reasoning": {
            "EchoMatch": 0.05191915961,
            "StoryWeave": 0.09683812976,
            "LogicLink": 0.3706138976,
            "BlockMorph": 0.255402197,
            "ChainReaction": 0.2252266161,
        },
    }

    # Calculate final domain scores
    final_domain_scores, overall_score = calculate_domain_scores(game_results, domain_weights, game_weights)
    # print("\nFinal Domain Scores:")
    # print(final_domain_scores)

    return final_domain_scores, overall_score
