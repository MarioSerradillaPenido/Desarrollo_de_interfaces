
import cv2
import pyautogui
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ring_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            pinky_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
            thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            index_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            thumb_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

            if (thumb_tip_y < index_mcp_y and thumb_tip_y < pinky_tip_y and index_tip_y > thumb_tip_y and pinky_tip_y > thumb_tip_y):
                hand_gesture = "thumbs_up"  # 👍 (Thumbs Up)
            elif (thumb_tip_y > index_mcp_y and thumb_tip_y > pinky_tip_y and index_tip_y < thumb_tip_y and pinky_tip_y < thumb_tip_y):
                hand_gesture = "thumbs_down"  # 👎 (Thumbs Down)
            elif (index_tip_y < wrist_y and middle_tip_y < wrist_y and
                ring_tip_y < wrist_y and pinky_tip_y < wrist_y and thumb_tip_y < wrist_y):
                hand_gesture = "palm"  # 🖐️ (Open Palm)
            elif (index_tip_y > index_mcp_y and middle_tip_y > index_mcp_y and ring_tip_y > index_mcp_y and pinky_tip_y > index_mcp_y):
                hand_gesture = "fist"  # ✊ (Fist)
            else:
                hand_gesture = 'other'

            if hand_gesture == 'thumbs_down':
                pyautogui.press('volumedown')
            elif hand_gesture == 'thumbs_up':
                pyautogui.press('volumeup')
            elif hand_gesture == 'palm':
                pyautogui.press('space')
            elif hand_gesture == 'fist':
                pyautogui.press('escape')
            elif hand_gesture == 'peace_sign':
                pyautogui.press('capslock ')

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
