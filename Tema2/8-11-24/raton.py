import cv2
import pyautogui
import mediapipe as mp
import time

# Set up webcam and mediapipe hand solution
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Variables to manage clicking debounce
click_debounce_time = 0.3  # 300 ms debounce time to avoid multiple clicks
last_click_time = 0

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for a mirror-like view
    frame = cv2.flip(frame, 1)
    
    # Convert frame to RGB for processing
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Check if any hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get specific landmark positions for gesture recognition
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            # Calculate pixel positions of index fingertip
            index_x = int(index_tip.x * frame_width)
            index_y = int(index_tip.y * frame_height)

            # Gesture Detection
            if (index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and 
                index_tip.y < pinky_tip.y and index_tip.y < thumb_tip.y):
                # Pointing gesture - Move mouse to follow fingertip
                screen_x = int(index_tip.x * screen_width)
                screen_y = int(index_tip.y * screen_height)
                pyautogui.moveTo(screen_x, screen_y)
                hand_gesture = "mouse_move"
            elif (index_tip.y > index_mcp.y and middle_tip.y > index_mcp.y and
                  ring_tip.y > index_mcp.y and pinky_tip.y > index_mcp.y):
                # Fist gesture - Trigger click
                current_time = time.time()
                if current_time - last_click_time > click_debounce_time:
                    pyautogui.click()
                    last_click_time = current_time
                hand_gesture = "click"
            else:
                hand_gesture = "other"

            # Print gesture for debugging
            print("Detected Gesture:", hand_gesture)

    # Display the frame
    cv2.imshow('Hand Gesture', frame)

    # Break loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
