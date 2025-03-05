import cv2
import  mediapipe as mp
import pyautogui
import utils


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


            zeige = (hand_landmarks.landmark[5].x * screen_width,hand_landmarks.landmark[5].y * screen_height)
            mittel = (hand_landmarks.landmark[9].x * screen_width, hand_landmarks.landmark[9].y * screen_height)
            ring = (hand_landmarks.landmark[13].x * screen_width, hand_landmarks.landmark[13].y * screen_height)

            #palmCentral_x, palmCentral_y = utils.find_circle_center(zeige,mittel,ring)
            # 移动
            pyautogui.moveTo(hand_landmarks.landmark[5].x* screen_width,hand_landmarks.landmark[5].y* screen_height, duration=0.1)

            #大拇指与食指接近
            zeige_tip = hand_landmarks.landmark[4]
            daumen_tip = hand_landmarks.landmark[8]

            left_distance = ((daumen_tip.x - zeige_tip.x) ** 2 + (daumen_tip.y - zeige_tip.y) ** 2) ** 0.5
            if left_distance < 0.005:
                pyautogui.click()

            klein_tip = hand_landmarks.landmark[20]
            right_distance = ((daumen_tip.x - klein_tip.x) ** 2 + (daumen_tip.y - klein_tip.y) ** 2) ** 0.5
            if right_distance < 0.005: pyautogui.rightClick()

            # mittel_tip = hand_landmarks.landmark[12]
            # middle_distance = ((daumen_tip.x - mittel_tip.x)**2 + (daumen_tip.y - mittel_tip.y)**2) ** 0.5
            # if middle_distance < 0.05:
            #     pyautogui.mouseDown()
            # else:
            #     pyautogui.mouseUp()


    cv2.imshow("Hand Tracking Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
