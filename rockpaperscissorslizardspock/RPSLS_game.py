import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800  # Larger screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Lizard Spock Battle")

# FPS setting
FPS = 60
ICON_SIZE = 25
default_icons = 1  # Default number of icons per group
additional_icons = 0  # User input
game_running = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 74)

# Function to scale images while preserving aspect ratio
def scale_image(image, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    new_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, target_height))

# Load and scale PNG images
ROCK_IMG = scale_image(pygame.image.load("rock.png"), ICON_SIZE)
PAPER_IMG = scale_image(pygame.image.load("paper.png"), ICON_SIZE)
SCISSORS_IMG = scale_image(pygame.image.load("scissors.png"), ICON_SIZE)
LIZARD_IMG = scale_image(pygame.image.load("lizard.png"), ICON_SIZE)
SPOCK_IMG = scale_image(pygame.image.load("spock.png"), ICON_SIZE)

ICON_WIDTH = ROCK_IMG.get_width()
ICON_HEIGHT = ROCK_IMG.get_height()

# Rules for determining outcomes
RPSLS_RULES = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["spock", "paper"],
    "spock": ["scissors", "rock"],
}

# Center of the screen
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Input box class
class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active state
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLACK if self.active else GRAY
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
        return None

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

# Icon class
class Icon:
    def __init__(self, x, y, icon_type):
        self.x = x
        self.y = y
        self.type = icon_type
        angle = math.atan2(CENTER_Y - y, CENTER_X - x)
        speed = random.uniform(1, 2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x < 0 or self.x > WIDTH - ICON_WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT - ICON_HEIGHT:
            self.vy *= -1

    def draw(self):
        img = {"rock": ROCK_IMG, "paper": PAPER_IMG, "scissors": SCISSORS_IMG,
               "lizard": LIZARD_IMG, "spock": SPOCK_IMG}[self.type]
        screen.blit(img, (self.x, self.y))

# Main menu
def main_menu():
    global additional_icons, game_running
    input_box = InputBox(500, 300, 200, 50)
    play_button = Button(500, 400, 200, 50, "Play", start_game)
    icons_button = Button(500, 500, 200, 50, "Set", None)

    while not game_running:
        screen.fill(WHITE)

        # Draw input box and buttons
        input_box.draw()
        play_button.draw()
        icons_button.draw()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if input_box.active:
                result = input_box.handle_event(event)
                if result is not None:
                    additional_icons = int(result)

            if play_button.is_clicked(event):
                play_button.action()

        # Display instructions
        instructions = "Enter number of icons to add and press 'Set', then press 'Play'."
        text_surf = font.render(instructions, True, BLACK)
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 200))

        pygame.display.flip()

# Start the game
def start_game():
    global game_running, icons
    icons = generate_icons(default_icons + additional_icons)
    game_running = True

# Restart the game
def restart_game():
    global game_running
    game_running = False
    main_menu()

# Generate icons
def generate_icons(num_icons):
    start_positions = {
        "rock": (0, 0),  # Top-left
        "paper": (WIDTH - ICON_WIDTH, 0),  # Top-right
        "scissors": (0, HEIGHT - ICON_HEIGHT),  # Bottom-left
        "lizard": (WIDTH - ICON_WIDTH, HEIGHT - ICON_HEIGHT),  # Bottom-right
        "spock": (CENTER_X - ICON_WIDTH // 2, CENTER_Y - ICON_HEIGHT // 2)  # Center
    }
    icons = []
    for icon_type, (start_x, start_y) in start_positions.items():
        icons.append(Icon(start_x, start_y, icon_type))
        for _ in range(num_icons - 1):
            x = random.randint(start_x, start_x + ICON_WIDTH)
            y = random.randint(start_y, start_y + ICON_HEIGHT)
            icons.append(Icon(x, y, icon_type))
    return icons

# Victory screen
def victory_screen(winner):
    restart_button = Button(500, 400, 200, 50, "Restart", restart_game)
    while True:
        screen.fill(WHITE)
        text = f"{winner.capitalize()} Wins!"
        text_surf = big_font.render(text, True, BLACK)
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 200))
        restart_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if restart_button.is_clicked(event):
                restart_button.action()

        pygame.display.flip()

# Game loop
def game_loop():
    global icons
    clock = pygame.time.Clock()

    while game_running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move and draw icons
        for icon in icons:
            icon.move()
            icon.draw()

        # Check for a winner
        types = {icon.type for icon in icons}
        if len(types) == 1:
            victory_screen(list(types)[0])

        pygame.display.flip()
        clock.tick(FPS)

# Run the game
main_menu()
game_loop()
