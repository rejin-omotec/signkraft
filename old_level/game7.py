import pygame
import sys
import threading
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Description Game with Speech and Scoring")

# Load the image (make sure 'image.jpg' exists or replace with your image file)
try:
    image = pygame.image.load('asset\imagedef\img1.png')
except pygame.error:
    print("Unable to load image. Please ensure 'image.jpg' exists in the script directory.")
    pygame.quit()
    sys.exit()

# Scale the image to fit the screen if necessary
image = pygame.transform.scale(image, (400, 300))
image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

# Define keywords (do not display these to the player)
keywords = ["sunset", "ocean", "reflection", "colors", "horizon"]

# Set up fonts
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 48)

# Variables for speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
speech_text = ''
listening = False
error_message = ''
score = None
matched_keywords = []

# Function to handle speech recognition in a separate thread
def recognize_speech():
    global speech_text, listening, error_message, score, matched_keywords
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            speech_text = recognizer.recognize_google(audio)
            print("You said:", speech_text)
            # Check for keywords in the speech text
            check_keywords()
        except sr.WaitTimeoutError:
            error_message = "Listening timed out. Please try again."
            print(error_message)
        except sr.UnknownValueError:
            error_message = "Could not understand audio. Please try again."
            print(error_message)
        except sr.RequestError as e:
            error_message = f"Could not request results; {e}"
            print(error_message)
        listening = False

# Function to check for keywords in the speech text
def check_keywords():
    global score, matched_keywords
    matched_keywords = []
    words_in_speech = speech_text.lower().split()
    for keyword in keywords:
        if keyword.lower() in words_in_speech:
            matched_keywords.append(keyword)
    score = len(matched_keywords)

# Main loop variables
clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not listening:
                # Start speech recognition
                listening = True
                error_message = ''
                speech_text = ''
                score = None
                matched_keywords = []
                threading.Thread(target=recognize_speech).start()

    # Clear the screen
    screen.fill((30, 30, 30))

    # Draw the image
    screen.blit(image, image_rect)

    # Instructions
    instruction_text = font.render("Press SPACE to start speaking.", True, pygame.Color('yellow'))
    screen.blit(instruction_text, (50, HEIGHT - 100))

    # Display listening status
    if listening:
        listening_text = font.render("Listening...", True, pygame.Color('green'))
        screen.blit(listening_text, (50, HEIGHT - 70))
    elif error_message:
        error_text = font.render(error_message, True, pygame.Color('red'))
        screen.blit(error_text, (50, HEIGHT - 70))
    elif speech_text:
        # Display the player's description
        description_heading = font.render("Your Description:", True, pygame.Color('white'))
        screen.blit(description_heading, (50, HEIGHT - 220))
        description_lines = []
        words = speech_text.split(' ')
        line = ''
        for word in words:
            if font.size(line + word)[0] < WIDTH - 100:
                line += word + ' '
            else:
                description_lines.append(line)
                line = word + ' '
        description_lines.append(line)

        y_text = HEIGHT - 190
        for line in description_lines:
            desc_text = font.render(line, True, pygame.Color('white'))
            screen.blit(desc_text, (60, y_text))
            y_text += 25

        # Display the score
        score_text = big_font.render(f"Score: {score}/{len(keywords)}", True, pygame.Color('cyan'))
        screen.blit(score_text, (50, HEIGHT - 250))

        # Optionally, display which keywords were matched
        matched_text = font.render(f"Keywords used: {', '.join(matched_keywords)}", True, pygame.Color('lightgreen'))
        screen.blit(matched_text, (50, HEIGHT - 160))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
