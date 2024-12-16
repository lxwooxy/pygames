import cv2
import mediapipe as mp
import pygame
import sys
import math
import time

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Squid Game - Run Away from Gaze")

# Load the Squid Image
squid_img = pygame.image.load("squid.jpg") 
squid_img = pygame.transform.scale(squid_img, (100, 100))
squid_x, squid_y = WIDTH // 2, HEIGHT // 2

# Webcam setup
cap = cv2.VideoCapture(0)

# Calibration variables
corners = {"top_left": None, "top_right": None, "bottom_left": None, "bottom_right": None}
corner_positions = {
    "top_left": (50, 50),
    "top_right": (WIDTH - 50, 50),
    "bottom_left": (50, HEIGHT - 50),
    "bottom_right": (WIDTH - 50, HEIGHT - 50),
}
corner_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
current_corner = 0
pulse_timer = time.time()

def get_gaze_position(landmarks, width, height):
    """Calculate gaze position based on eye landmarks."""
    left_eye = landmarks[474:478]  # Mediapipe indices for left eye landmarks
    gaze_x = int(sum([lm.x for lm in left_eye]) / len(left_eye) * width)
    gaze_y = int(sum([lm.y for lm in left_eye]) / len(left_eye) * height)
    return gaze_x, gaze_y

def draw_pulsing_dot(screen, position, timer):
    """Draw a pulsing green dot at the specified position."""
    pulse_speed = 1.5  # Controls how fast the dot pulses
    max_radius = 20
    min_radius = 10
    elapsed_time = time.time() - timer
    radius = min_radius + abs(math.sin(elapsed_time * pulse_speed)) * (max_radius - min_radius)
    pygame.draw.circle(screen, (0, 255, 0), position, int(radius))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    # Capture frame
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process face landmarks
    result = face_mesh.process(rgb_frame)
    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            gaze_x, gaze_y = get_gaze_position(face_landmarks.landmark, WIDTH, HEIGHT)

            # Calibration step: record corners
            if current_corner < len(corner_names):
                corner_name = corner_names[current_corner]
                instruction = f"Look at the {corner_name.replace('_', ' ')} corner"
                text_surface = pygame.font.Font(None, 36).render(instruction, True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                # Add a pulsing dot in the corner
                draw_pulsing_dot(screen, corner_positions[corner_name], pulse_timer)

                # Display instructions
                screen.fill((0, 0, 0))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()

                # Record gaze position for the corner
                corners[corner_name] = (gaze_x, gaze_y)
                pygame.time.wait(2000)  # Increased delay for instructions
                current_corner += 1
                pulse_timer = time.time()  # Reset pulse timer
                break  # Wait for next frame before continuing calibration

            # Update squid position: Move squid away from gaze
            if all(corners.values()):  # Ensure calibration is complete
                delta_x = squid_x - gaze_x
                delta_y = squid_y - gaze_y
                distance = max(1, (delta_x**2 + delta_y**2)**0.5)
                speed = 10

                squid_x += int(speed * (delta_x / distance))
                squid_y += int(speed * (delta_y / distance))

    # Render Pygame screen
    screen.fill((0, 0, 0))

    # Ensure squid is only visible after calibration
    if all(corners.values()):
        screen.blit(squid_img, (squid_x, squid_y))

    pygame.display.flip()

    # Show webcam frame (optional, for debugging)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
