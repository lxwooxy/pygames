import cv2
import mediapipe as mp
import numpy as np
import pygame
import math

# Initialize Mediapipe and Pygame
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
pygame.init()

# Screen dimensions and 3D settings
WIDTH, HEIGHT = 1200, 800
DOT_SPACING = 10  # Reduced spacing for more dots
GRID_DEPTH = 50  # Maximum depth of the 3D grid
FOV = 500  # Field of view for perspective projection
DOT_RADIUS = 3

# Create a 3D grid of dots
dots = [
    [(x, y, GRID_DEPTH // 2) for y in range(-HEIGHT // 2, HEIGHT // 2, DOT_SPACING)]
    for x in range(-WIDTH // 2, WIDTH // 2, DOT_SPACING)
]

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Pin Toy")

# Webcam setup
cap = cv2.VideoCapture(0)

def perspective_projection(x, y, z):
    """Project 3D coordinates into 2D using a perspective transformation."""
    factor = FOV / (FOV + z)
    screen_x = int(WIDTH // 2 + x * factor)
    screen_y = int(HEIGHT // 2 + y * factor)
    return screen_x, screen_y, factor

def update_dots(hand_landmarks_list):
    """Update dot positions to reflect the shape of the hand more accurately."""
    for i, column in enumerate(dots):
        for j, dot in enumerate(column):
            x, y, z = dot
            influence = 0  # Total influence from all hand landmarks

            for hand_landmarks in hand_landmarks_list:
                for landmark in hand_landmarks.landmark:
                    # Map hand positions to the 3D grid
                    hand_x = int((landmark.x - 0.5) * WIDTH)  # Normalize to grid
                    hand_y = int((landmark.y - 0.5) * HEIGHT)

                    # Calculate distance from dot to landmark
                    distance = math.sqrt((x - hand_x)**2 + (y - hand_y)**2)

                    # Influence decreases with distance (falloff)
                    if distance < 100:  # Only consider close landmarks
                        influence += max(0, 100 - distance)  # Falloff from 100px

            # Push dots outward based on combined influence
            z_new = GRID_DEPTH // 2 + influence / 5  # Scale influence
            dots[i][j] = (x, y, min(GRID_DEPTH, z_new))  # Cap depth
            
def draw_hand_outlines(hand_landmarks_list):
    """Draw hand outlines to visualize the actual hand shape."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Transparent overlay

    for hand_landmarks in hand_landmarks_list:
        hand_points = [
            (int((landmark.x - 0.5) * WIDTH), int((landmark.y - 0.5) * HEIGHT))
            for landmark in hand_landmarks.landmark
        ]

        # Draw lines connecting key points (fingers, palm)
        pygame.draw.lines(overlay, (255, 255, 255, 50), True, hand_points[:5], 2)  # Palm outline
        for i in range(5):  # Fingers
            pygame.draw.lines(
                overlay,
                (255, 255, 255, 50),
                False,
                hand_points[i * 4 : (i + 1) * 4],
                2,
            )

        # Highlight all landmarks
        for point in hand_points:
            pygame.draw.circle(overlay, (255, 255, 255, 100), point, 3)

    # Blit the overlay onto the main screen
    screen.blit(overlay, (0, 0))



def draw_dots():
    """Render the 3D dots on the screen with perspective projection."""
    screen.fill((0, 0, 0))  # Clear the screen
    for column in dots:
        for x, y, z in column:
            screen_x, screen_y, factor = perspective_projection(x, y, z)
            size = max(1, int(DOT_RADIUS * factor))  # Adjust size based on depth
            brightness = max(50, min(255, int(255 * factor)))  # Adjust brightness
            pygame.draw.circle(screen, (brightness, brightness, brightness), (screen_x, screen_y), size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for a mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        update_dots(result.multi_hand_landmarks)
        draw_hand_outlines(result.multi_hand_landmarks)

    # Draw the 3D dot grid
    draw_dots()

    # Update the Pygame display
    pygame.display.flip()

cap.release()
pygame.quit()
