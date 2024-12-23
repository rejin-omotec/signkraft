import pygame

def run_game(surface, level_width, level_height, win_width, win_height, max_attempts_arg):
    """
    Displays a form to collect player inputs and returns the input data.
    """
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 255, 0)

    # Fonts (Reduced sizes)
    TITLE_FONT = pygame.font.Font(None, 36)
    LABEL_FONT = pygame.font.Font(None, 24)
    INPUT_FONT = pygame.font.Font(None, 20)

    # Input fields (organized in two columns)
    input_fields = {
        "player_name": {"label": "Your Name", "value": "", "col": 0, "row": 0},
        "spouse_name": {"label": "Spouse's Name", "value": "", "col": 1, "row": 0},
        "father_name": {"label": "Father's Name", "value": "", "col": 0, "row": 1},
        "mother_name": {"label": "Mother's Name", "value": "", "col": 1, "row": 1},
        "brother_name": {"label": "Brother's Name", "value": "", "col": 0, "row": 2},
        "sister_name": {"label": "Sister's Name", "value": "", "col": 1, "row": 2},
        "birth_city": {"label": "City of Birth", "value": "", "col": 0, "row": 3},
        "favorite_food": {"label": "Favorite Food", "value": "", "col": 1, "row": 3},
        "hobby": {"label": "Hobby", "value": "", "col": 0, "row": 4},
        "favorite_color": {"label": "Favorite Color", "value": "", "col": 1, "row": 4},  # New field
    }

    # Define grid properties
    column_width = level_width // 2
    row_height = 70  # Reduced row height
    padding_x = 110
    padding_y = 10
    input_box_width = 180  # Reduced input box width
    input_box_height = 30  # Reduced input box height

    submit_button = pygame.Rect(level_width // 2 - 100, level_height - 70, 200, 50)

    # Main loop
    running = True
    inputs_collected = False
    collected_data = {}

    while running:
        surface.fill(WHITE)

        # Draw title
        title_surface = TITLE_FONT.render("Basic Details", True, BLACK)
        surface.blit(title_surface, (level_width // 2 - title_surface.get_width() // 2, 20))

        # Draw input fields
        for key, field in input_fields.items():
            col_x = padding_x + field["col"] * column_width
            row_y = 100 + field["row"] * row_height

            # Draw label
            label_surface = LABEL_FONT.render(field["label"], True, BLACK)
            surface.blit(label_surface, (col_x, row_y - 25))

            # Draw input box
            input_rect = pygame.Rect(col_x, row_y, input_box_width, input_box_height)
            pygame.draw.rect(surface, GRAY, input_rect)
            value_surface = INPUT_FONT.render(field["value"], True, BLACK)
            surface.blit(value_surface, (input_rect.x + 5, input_rect.y + 5))

            # Save the rect for interaction
            field["rect"] = input_rect

        # Draw submit button
        pygame.draw.rect(surface, GREEN, submit_button)
        submit_text = LABEL_FONT.render("Submit", True, WHITE)
        surface.blit(submit_text, (submit_button.x + 70, submit_button.y + 18))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit the game loop entirely

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the absolute offset of the game surface
                abs_offset = surface.get_abs_offset()

                # Adjust mouse position to match the game surface
                x, y = event.pos
                x -= abs_offset[0]
                y -= abs_offset[1]

                # First check input boxes
                input_clicked = False
                for key, field in input_fields.items():
                    if field["rect"].collidepoint(x, y):
                        field["active"] = True
                        input_clicked = True
                    else:
                        field["active"] = False

                # Then check the submit button if no input box was clicked
                if not input_clicked and submit_button.collidepoint(x, y):
                    inputs_collected = True

            if event.type == pygame.KEYDOWN:
                for key, field in input_fields.items():
                    if field.get("active", False):
                        if event.key == pygame.K_BACKSPACE:
                            field["value"] = field["value"][:-1]
                        elif event.key == pygame.K_RETURN:
                            field["active"] = False
                        else:
                            field["value"] += event.unicode


        if inputs_collected:
            # Collect data from all fields
            collected_data = {key: field["value"] for key, field in input_fields.items()}
            running = False  # Exit the loop after collecting data

        pygame.display.update()

    # Return the collected data
    return [{"Input Field": key, "Value": value} for key, value in collected_data.items()], 0
