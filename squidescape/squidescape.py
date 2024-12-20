import cv2
import mediapipe as mp

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Webcam setup
cap = cv2.VideoCapture(0)

# Calibration variables
calibration_points = {"top_left": None, "top_right": None, "bottom_left": None, "bottom_right": None}
corner_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
current_corner = 0

# Function to calculate gaze position
def get_gaze_position(landmarks, width, height):
    """Calculate gaze position based on eye landmarks."""
    left_eye = landmarks[474:478]  # Mediapipe indices for left eye landmarks
    gaze_x = int(sum([lm.x for lm in left_eye]) / len(left_eye) * width)
    gaze_y = int(sum([lm.y for lm in left_eye]) / len(left_eye) * height)
    return gaze_x, gaze_y

def map_gaze_to_screen(gaze_x, gaze_y, width, height):
    """Map gaze coordinates to full screen using calibration points with bounds."""
    top_left = calibration_points["top_left"]
    top_right = calibration_points["top_right"]
    bottom_left = calibration_points["bottom_left"]
    bottom_right = calibration_points["bottom_right"]

    # Interpolate horizontally
    x_ratio = (gaze_x - top_left[0]) / (top_right[0] - top_left[0])
    # Interpolate vertically
    y_ratio = (gaze_y - top_left[1]) / (bottom_left[1] - top_left[1])

    # Scale to full screen with bounds
    screen_x = int(min(max(x_ratio * width, 0), width - 1))
    screen_y = int(min(max(y_ratio * height, 0), height - 1))
    return screen_x, screen_y

#declare squid.
squid = cv2.imread('squid.jpg')
squid_height, squid_width, _ = squid.shape
#resize squid to 20x20
squid = cv2.resize(squid, (20, 20))

# Main loop
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

    # Draw calibration marker if calibration is not complete
    if current_corner < len(corner_names):
        corner_name = corner_names[current_corner]
        corner_position = {
            "top_left": (50, 50),
            "top_right": (width - 50, 50),
            "bottom_left": (50, height - 50),
            "bottom_right": (width - 50, height - 50),
        }[corner_name]

        # Draw marker for the current corner
        cv2.circle(frame, corner_position, 10, (0, 255, 0), -1)
        cv2.putText(
            frame,
            f"Look at the {corner_name.replace('_', ' ')} corner and press 'd'",
            (50, height - 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    # Process face landmarks if available
    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Get the gaze position
            gaze_x, gaze_y = get_gaze_position(face_landmarks.landmark, width, height)

            # Calibration process
            if current_corner < len(corner_names):
                # Wait for user to press 'd' to save the gaze position
                if cv2.waitKey(1) & 0xFF == ord('d'):
                    calibration_points[corner_names[current_corner]] = (gaze_x, gaze_y)
                    current_corner += 1
            else:
                # Map gaze position to screen coordinates after calibration
                screen_x, screen_y = map_gaze_to_screen(gaze_x, gaze_y, width, height)

                # Draw the gaze dot
                # .circle(image, center_coordinates, radius, color, thickness)
                cv2.circle(frame, (screen_x, screen_y), 10, (255, 0, 0), -1) #color is BGR, which is so cool and not weird at all
                
                # #add the squid.jpg image on top of the gaze dot
                
                
                

    # Display the frame
    cv2.imshow("Gaze Tracking", frame)

    # Exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Check for keypress
    # Check if recalibration is triggered
    if cv2.waitKey(1) & 0xFF == ord('r'):
        # Reset calibration if 'r' is pressed
        calibration_points = {"top_left": None, "top_right": None, "bottom_left": None, "bottom_right": None}
        current_corner = 0
        print("Recalibration started!")

cap.release()
cv2.destroyAllWindows()
