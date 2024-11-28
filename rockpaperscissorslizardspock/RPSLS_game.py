import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Lizard Spock Battle")

# FPS setting
FPS = 60
N = 8  # Number of each icon

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

# Define the classes
class Icon:
    def __init__(self, x, y, icon_type):
        self.x = x
        self.y = y
        self.type = icon_type
        self.vx = random.uniform(-2, 2)  # Slower speeds
        self.vy = random.uniform(-2, 2)
    
    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x < 0 or self.x > WIDTH - ICON_WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT - ICON_HEIGHT:
            self.vy *= -1

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

    if distance < ICON_WIDTH:  # Collision detected
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

# Create icons
icons = []
for _ in range(N):
    icons.append(Icon(random.randint(0, WIDTH - ICON_WIDTH), random.randint(0, HEIGHT - ICON_HEIGHT), "rock"))
    icons.append(Icon(random.randint(0, WIDTH - ICON_WIDTH), random.randint(0, HEIGHT - ICON_HEIGHT), "paper"))
    icons.append(Icon(random.randint(0, WIDTH - ICON_WIDTH), random.randint(0, HEIGHT - ICON_HEIGHT), "scissors"))
    icons.append(Icon(random.randint(0, WIDTH - ICON_WIDTH), random.randint(0, HEIGHT - ICON_HEIGHT), "lizard"))
    icons.append(Icon(random.randint(0, WIDTH - ICON_WIDTH), random.randint(0, HEIGHT - ICON_HEIGHT), "spock"))

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
            dx = icons[i].x - icons[j].x
            dy = icons[i].y - icons[j].y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < ICON_WIDTH:  # Collision detected
                handle_collision(icons[i], icons[j])

    # Check if all icons are the same type
    types = {icon.type for icon in icons}
    if len(types) == 1:
        font = pygame.font.Font(None, 74)
        text = font.render(f"{list(types)[0].capitalize()} Wins!", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
