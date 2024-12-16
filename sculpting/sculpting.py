import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize a 3D clay (cube mesh)
grid_size = 20
clay = np.zeros((grid_size, grid_size, grid_size))  # 3D array representing the clay

# Webcam input
cap = cv2.VideoCapture(0)

def detect_gesture(hand_landmarks):
    """Classify gestures based on hand landmarks."""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    palm = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Measure distances
    pinch_distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    palm_distance = ((thumb_tip.x - palm.x)**2 + (thumb_tip.y - palm.y)**2)**0.5

    if pinch_distance < 0.05:  # Adjust threshold as needed
        return "pinch"
    elif palm_distance < 0.2:
        return "grab"
    else:
        return "poke"

def draw_clay():
    """Render the clay as a 3D grid of cubes."""
    glPushMatrix()
    glTranslatef(0, 0, -50)  # Move the clay grid into the view
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                if clay[x, y, z] > 0:  # Only draw active parts
                    glPushMatrix()
                    glTranslatef(x - grid_size // 2, y - grid_size // 2, z - grid_size // 2)
                    glutSolidCube(0.5)  # Adjust size as needed
                    glPopMatrix()
    glPopMatrix()

def sculpt(clay, gesture, hand_position):
    """Modify clay based on detected gesture and hand position."""
    x, y, z = int(hand_position[0]), int(hand_position[1]), int(hand_position[2])
    x, y, z = np.clip([x, y, z], 0, grid_size - 1)  # Ensure indices stay within bounds

    if gesture == "pinch":
        clay[x, y, z] = 0  # Remove material
    elif gesture == "poke":
        clay[x, y, z] += 1  # Add material
    elif gesture == "grab":
        clay[x, y, z] += 2  # Stronger pull outward

def update():
    """Update logic for the game."""
    global clay

    ret, frame = cap.read()
    if not ret:
        return

    # Flip and process the frame for hand tracking
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Detect gesture and map hand position to the grid
            gesture = detect_gesture(hand_landmarks)
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            hand_position = (
                int((index_tip.x - 0.5) * grid_size),
                int((index_tip.y - 0.5) * grid_size),
                grid_size // 2,
            )

            sculpt(clay, gesture, hand_position)

def display():
    """Render function for OpenGL."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_clay()
    glutSwapBuffers()

def idle():
    """Idle function for continuous updates."""
    update()
    glutPostRedisplay()

def main():
    """Main function to initialize OpenGL and run the game."""
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("3D Sculpting")
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
