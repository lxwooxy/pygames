import cv2
import mediapipe as mp
import numpy as np
import pygame

# Initialize Mediapipe and Pygame
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
pygame.init()

# Screen dimensions and dot grid
WIDTH, HEIGHT = 800, 600
DOT_SPACING = 20  # Original spacing
DOT_DEPTH_RANGE = 5  # Reduced range for less glow

# Create a grid of dots
dots = [[(x, y, 0) for y in range(0, HEIGHT, DOT_SPACING)] for x in range(0, WIDTH, DOT_SPACING)]

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2.5D Pin Toy")

# Webcam setup
cap = cv2.VideoCapture(0)

def update_dots(hand_landmarks_list):
    for i, column in enumerate(dots):
        for j, dot in enumerate(column):
            x, y, z = dot

            # Find the minimum distance to any hand landmark
            min_distance = float('inf')
            for hand_landmarks in hand_landmarks_list:
                for landmark in hand_landmarks.landmark:
                    hand_x, hand_y = int(landmark.x * WIDTH), int(landmark.y * HEIGHT)
                    distance = np.sqrt((x - hand_x)**2 + (y - hand_y)**2)
                    min_distance = min(min_distance, distance)

            # Adjust z based on distance (closer = higher depth, subtler glow)
            dots[i][j] = (x, y, max(0, DOT_DEPTH_RANGE - min_distance / 10))  # Increased divisor

def draw_dots():
    screen.fill((0, 0, 0))  # Clear the screen
    for column in dots:
        for x, y, z in column:
            size = int(3 + z)  # Dot size depends on depth
            pygame.draw.circle(screen, (255, 255, 255), (x, y), size)

def draw_hand_outlines(hand_landmarks_list):
    # Create a transparent overlay surface
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for hand_landmarks in hand_landmarks_list:
        # Extract hand points for outline
        hand_points = [
            (int(landmark.x * WIDTH), int(landmark.y * HEIGHT)) 
            for landmark in hand_landmarks.landmark
        ]
        
        # Draw faint outline around the hand
        for point in hand_points:
            pygame.draw.circle(overlay, (255, 255, 255, 50), point, 20)  # Transparent white circles

        # Connect key points for a polygon effect
        pygame.draw.polygon(overlay, (255, 255, 255, 30), hand_points[:5], width=2)  # Connect wrist and fingers

    # Blit the overlay onto the main screen
    screen.blit(overlay, (0, 0))

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
        # Update dots based on hand positions
        update_dots(result.multi_hand_landmarks)

        # Draw hand outlines
        draw_hand_outlines(result.multi_hand_landmarks)

    # Draw the dot grid
    draw_dots()

    # Update the Pygame display
    pygame.display.flip()

cap.release()
pygame.quit()
