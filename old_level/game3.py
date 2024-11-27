import pygame
import sys
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("हिंदी कहानी याद करें खेल")

# Load Hindi Font
FONT_SIZE = 24
hindi_font = pygame.font.Font('Nirmala.ttf', FONT_SIZE)  # Replace with your font file
small_font = pygame.font.Font('Nirmala.ttf', 20)

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sample Hindi story
story = """एक गाँव में एक किसान रहता था। उसके पास एक सुनहरी अंडे देने वाली मुर्गी थी। वह रोज़ एक सुनहरा अंडा पाता और उसे बेचकर अपना गुज़ारा करता। लेकिन वह लालची था और एक दिन उसने सोचा, क्यों न मुर्गी को मारकर सारे अंडे एक साथ ले लूँ। उसने ऐसा ही किया, लेकिन उसे कुछ नहीं मिला। वह पछताने लगा।"""

# Questions related to the story
questions = [
    {
        "question": "किसान के पास कौन सा जानवर था?",
        "options": ["गाय", "मुर्गी", "बकरी", "भेड़"],
        "answer": "मुर्गी"
    },
    {
        "question": "मुर्गी कैसे अंडे देती थी?",
        "options": ["साधारण अंडे", "सुनहरे अंडे", "चाँदी के अंडे", "हीरे के अंडे"],
        "answer": "सुनहरे अंडे"
    },
    {
        "question": "किसान ने मुर्गी के साथ क्या किया?",
        "options": ["उसे बेचा", "उसे मार दिया", "उसे खाना दिया", "उसे छोड़ दिया"],
        "answer": "उसे मार दिया"
    },
    {
        "question": "कहानी से हमें क्या शिक्षा मिलती है?",
        "options": ["लालच बुरी बला है", "मेहनत का फल मीठा होता है", "समय अमूल्य है", "दोस्तों की मदद करें"],
        "answer": "लालच बुरी बला है"
    }
]

# Global variables
score = 0
current_question = 0

# Function to render text
def render_text(text, font, color, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        window.blit(text_surface, (x, y + i * (FONT_SIZE + 5)))

# Function to play story audio
def play_story_audio():
    tts = gTTS(text=story, lang='hi')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)

# Function to display the story
def display_story():
    window.fill(WHITE)
    render_text(story, hindi_font, BLACK, 50, 50)
    play_button = small_font.render("कहानी सुनें (S)", True, BLACK)
    window.blit(play_button, (50, HEIGHT - 100))
    start_button = small_font.render("प्रश्न शुरू करें (Q)", True, BLACK)
    window.blit(start_button, (250, HEIGHT - 100))
    pygame.display.update()

# Function to display a question
def display_question(index, selected_option):
    window.fill(WHITE)
    q = questions[index]
    render_text(q["question"], hindi_font, BLACK, 50, 50)

    for i, option in enumerate(q["options"]):
        color = BLACK
        if selected_option == i:
            color = (0, 128, 0)
        option_text = f"{i + 1}. {option}"
        text_surface = hindi_font.render(option_text, True, color)
        window.blit(text_surface, (70, 150 + i * 40))

    submit_button = small_font.render("जमा करें (Enter)", True, BLACK)
    window.blit(submit_button, (50, HEIGHT - 100))
    pygame.display.update()

# Function to display the final score
def display_score():
    window.fill(WHITE)
    score_text = f"आपका स्कोर है: {score}/{len(questions)}"
    render_text(score_text, hindi_font, BLACK, 50, 50)
    pygame.display.update()

# Main Game Loop
def main():
    global score, current_question
    mode = "story"  # Modes: 'story', 'quiz', 'result'
    selected_option = -1

    running = True
    while running:
        if mode == "story":
            display_story()
        elif mode == "quiz":
            display_question(current_question, selected_option)
        elif mode == "result":
            display_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if mode == "story":
                    if event.key == pygame.K_s:
                        # Play story audio
                        threading.Thread(target=play_story_audio).start()
                    elif event.key == pygame.K_q:
                        mode = "quiz"
                elif mode == "quiz":
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        selected_option = 0
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        selected_option = 1
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        selected_option = 2
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        selected_option = 3
                    elif event.key == pygame.K_RETURN:
                        if selected_option == -1:
                            # No option selected
                            pass
                        else:
                            # Check answer
                            if questions[current_question]["options"][selected_option] == questions[current_question]["answer"]:
                                score += 1
                            current_question += 1
                            selected_option = -1
                            if current_question >= len(questions):
                                mode = "result"
                elif mode == "result":
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()

    pygame.quit()

if __name__ == "__main__":
    main()
