import cv2
import mediapipe as mp

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Webcam setup
cap = cv2.VideoCapture(0)

def get_gaze_position(landmarks, width, height):
    """Calculate gaze position based on eye landmarks."""
    left_eye = landmarks[474:478]  # Mediapipe indices for left eye landmarks
    gaze_x = int(sum([lm.x for lm in left_eye]) / len(left_eye) * width)
    gaze_y = int(sum([lm.y for lm in left_eye]) / len(left_eye) * height)
    return gaze_x, gaze_y

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for a mirror effect
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert the image to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Get the gaze position based on the left eye
            gaze_x, gaze_y = get_gaze_position(face_landmarks.landmark, width, height)

            # Draw a dot where the user is looking
            cv2.circle(frame, (gaze_x, gaze_y), 10, (0, 255, 0), -1)

    # Display the webcam feed
    cv2.imshow("Gaze Tracking", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
