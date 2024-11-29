import pygame
import queue
from mods.blink_detect import BlinkDetectionThread  # Assuming the class above is saved in BlinkDetectionThread.py

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blink Detection with Pygame")
font = pygame.font.Font(None, 74)

# Queue for communication
blink_queue = queue.Queue()

# Start Blink Detection Thread
blink_thread = BlinkDetectionThread(blink_queue)
blink_thread.start()

running = True
message = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for blink messages
    try:
        blink_message = blink_queue.get_nowait()
        if blink_message == "SINGLE_BLINK":
            message = "Single Blink Detected!"
        elif blink_message == "DOUBLE_BLINK":
            message = "Double Blink Detected!"
        else:
            message = ""
    except queue.Empty:
        pass

    # Update screen
    screen.fill((0, 0, 0))  # Clear screen
    text = font.render(message, True, (0, 255, 0))
    screen.blit(text, (100, 250))
    pygame.display.flip()

# Stop blink detection thread
blink_thread.stop()
blink_thread.join()
pygame.quit()
