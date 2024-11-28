import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800  # Larger screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Lizard Spock Battle")

# FPS setting
FPS = 60
N = 20  # Number of each icon per type

# Function to scale images while preserving aspect ratio
def scale_image(image, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    new_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, target_height))

# Load and scale PNG images
TARGET_HEIGHT = 25  # Smaller icons
ROCK_IMG = scale_image(pygame.image.load("rock.png"), TARGET_HEIGHT)
PAPER_IMG = scale_image(pygame.image.load("paper.png"), TARGET_HEIGHT)
SCISSORS_IMG = scale_image(pygame.image.load("scissors.png"), TARGET_HEIGHT)
LIZARD_IMG = scale_image(pygame.image.load("lizard.png"), TARGET_HEIGHT)
SPOCK_IMG = scale_image(pygame.image.load("spock.png"), TARGET_HEIGHT)

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

# Define the classes
class Icon:
    def __init__(self, x, y, icon_type):
        self.x = x
        self.y = y

        # Velocity initialized towards the center with some randomness
        angle = math.atan2(CENTER_Y - y, CENTER_X - x)
        speed = random.uniform(1, 2)  # Adjust initial speed
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.type = icon_type

    def move(self):
        # Small random chance to change direction
        if random.random() < 0.01:  # 1% chance per frame
            random_angle = random.uniform(0, 2 * math.pi)
            random_speed = random.uniform(1, 2)
            self.vx = math.cos(random_angle) * random_speed
            self.vy = math.sin(random_angle) * random_speed

        self.x += self.vx
        self.y += self.vy

        # Bounce off walls and redirect towards center
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x > WIDTH - ICON_WIDTH:
            self.x = WIDTH - ICON_WIDTH
            self.vx = -abs(self.vx)

        if self.y < 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y > HEIGHT - ICON_HEIGHT:
            self.y = HEIGHT - ICON_HEIGHT
            self.vy = -abs(self.vy)

    def draw(self, screen):
        if self.type == "rock":
            screen.blit(ROCK_IMG, (self.x, self.y))
        elif self.type == "paper":
            screen.blit(PAPER_IMG, (self.x, self.y))
        elif self.type == "scissors":
            screen.blit(SCISSORS_IMG, (self.x, self.y))
        elif self.type == "lizard":
            screen.blit(LIZARD_IMG, (self.x, self.y))
        elif self.type == "spock":
            screen.blit(SPOCK_IMG, (self.x, self.y))

def handle_collision(icon1, icon2):
    # Calculate the direction of the collision
    dx = icon1.x - icon2.x
    dy = icon1.y - icon2.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0 or distance >= ICON_WIDTH:  # Prevent division by zero or no collision
        return

    # Resolve overlap by moving icons apart
    overlap = ICON_WIDTH - distance
    move_x = dx / distance * overlap / 2
    move_y = dy / distance * overlap / 2

    icon1.x += move_x
    icon1.y += move_y
    icon2.x -= move_x
    icon2.y -= move_y

    # Swap velocities based on collision angle
    normal_x = dx / distance
    normal_y = dy / distance

    # Dot product of velocity and normal
    dot1 = icon1.vx * normal_x + icon1.vy * normal_y
    dot2 = icon2.vx * normal_x + icon2.vy * normal_y

    # Update velocities
    icon1.vx -= 2 * dot1 * normal_x
    icon1.vy -= 2 * dot1 * normal_y
    icon2.vx -= 2 * dot2 * normal_x
    icon2.vy -= 2 * dot2 * normal_y

    # Determine the winner based on RPSLS rules
    if icon1.type != icon2.type:
        if icon2.type in RPSLS_RULES[icon1.type]:
            icon2.type = icon1.type  # icon1 wins
        elif icon1.type in RPSLS_RULES[icon2.type]:
            icon1.type = icon2.type  # icon2 wins

# Assign starting positions for each group
start_positions = {
    "rock": (0, 0),  # Top-left
    "paper": (WIDTH - ICON_WIDTH, 0),  # Top-right
    "scissors": (0, HEIGHT - ICON_HEIGHT),  # Bottom-left
    "lizard": (WIDTH - ICON_WIDTH, HEIGHT - ICON_HEIGHT),  # Bottom-right
    "spock": (WIDTH // 2 - ICON_WIDTH // 2, HEIGHT // 2 - ICON_HEIGHT // 2),  # Center
}

# Create icons
icons = []
for icon_type, (start_x, start_y) in start_positions.items():
    for _ in range(N):
        x = random.randint(start_x, start_x + ICON_WIDTH)
        y = random.randint(start_y, start_y + ICON_HEIGHT)
        icons.append(Icon(x, y, icon_type))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))  # Clear the screen with white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw icons
    for icon in icons:
        icon.move()
        icon.draw(screen)

    # Check collisions and bounce
    for i in range(len(icons)):
        for j in range(i + 1, len(icons)):
            handle_collision(icons[i], icons[j])

    # Ensure final frame updates before checking for victory
    pygame.display.flip()

    # Check if all icons are the same type
    types = {icon.type for icon in icons}
    if len(types) == 1:
        pygame.time.wait(200)  # Ensure the last conversion is shown
        font = pygame.font.Font(None, 74)
        text = font.render(f"{list(types)[0].capitalize()} Wins!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    clock.tick(FPS)

pygame.quit()
