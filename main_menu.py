import pygame
import game_engine  # Import the game engine

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
    global game_state, current_score

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Hub")

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
            current_score = game_engine.run(game_surface, player_name, player_age, current_score, WIDTH, GAME_HEIGHT)
            game_state = "END_SCREEN"
        elif game_state == "END_SCREEN":
            # Display the end screen
            screen.fill(WHITE)
            title_surface = TITLE_FONT.render("Game Over!", True, BLACK)
            screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))
            score_surface = FONT.render(f"Final Score: {current_score}", True, BLACK)
            screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 200))

            # Add Restart or Exit options
            restart_button = pygame.Rect(WIDTH // 2 - 50, 300, 100, 50)
            pygame.draw.rect(screen, BLACK, restart_button)
            restart_text = FONT.render("Restart", True, WHITE)
            screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        game_state = "MAIN_MENU"

            pygame.display.update()

if __name__ == "__main__":
    main()
