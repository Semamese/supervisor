import cv2
import  mediapipe as mp
import pyautogui
import numpy as np
import utils
from utils import distance,area
import logging
import time
import joblib
from oneEuroFilter import OneEuroFilter

import win32con
import win32gui


logging.basicConfig(level=logging.INFO)
pyautogui.FAILSAFE = False #限制当鼠标坐标超出屏幕时抛出异常

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7, min_tracking_confidence=0.7) #最多检测一只手

screen_width, screen_height = pyautogui.size()
screenScaleW = 1.8
screenScaleH = 1.8
cap = cv2.VideoCapture(1)

t0 = time.time()
xFilter = OneEuroFilter(t0=t0, x0=screen_width / 2, min_cutoff=2.0, beta=0.0)
yFilter = OneEuroFilter(t0=t0, x0=screen_height / 2, min_cutoff=2.0, beta=0.0)

def set_window_always_on_top(window_name="Hand Tracking Mouse"):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def thresholdCalculation(p1, p2):
    distance = np.linalg.norm(np.array([p1.x,p1.y]) - np.array([p2.x,p2.y]))
    threshold = distance/4.1 # 基于我食指根部和小指根部自然伸展时的长度比较，不断调整得出
    logging.debug(f"current threshold base distance is {distance}")
    logging.debug(f"current threshold is: {threshold}")
    return threshold

def performClick(clicked:bool, lastClickTime: float, firstTip, secondTip,clickForm:str, clickThreshold = 0.5, clickInterval = 0.5):
    distance = np.linalg.norm(np.array([firstTip.x, firstTip.y]) - np.array([secondTip.x, secondTip.y]))
    logging.debug(f"{clickForm}: {distance}")
    if distance < clickThreshold and time.time() - lastClickTime > clickInterval:
        if not clicked:
            if clickForm == "L":
                pyautogui.leftClick()
                logging.info("left clicked")
            if clickForm == "R":
                pyautogui.rightClick()
                logging.info("right clicked")
            lastClickTime = time.time()
            clicked = True
        else:
            clicked = False
    return clicked , lastClickTime

def performClick_Classifier(clicked:bool, lastClickTime: float,leftClickData,clickClassifier,clickForm:str, clickInterval = 0.5):
    rst = clickClassifier.predict(leftClickData)
    logging.debug(f"{clickForm}: {rst}")
    if rst[0] == 1 and time.time() - lastClickTime > clickInterval:
        if not clicked:
            if clickForm == "L":
                pyautogui.leftClick()
                logging.info("left clicked")
            if clickForm == "R":
                pyautogui.rightClick()
                logging.info("right clicked")
            lastClickTime = time.time()
            clicked = True
        else:
            clicked = False
    return clicked , lastClickTime



def drag(isDragging:bool,firstTip, secondTip, center, draggingThreshold):
    distance = np.linalg.norm(np.array([firstTip.x, firstTip.y]) - np.array([secondTip.x, secondTip.y]))
    if not isDragging:
        if distance < draggingThreshold:
            pyautogui.mouseDown()
            isDragging = True
            logging.debug(f"current distance is {distance}")
            logging.info("dragging")
    else:
        mouseMovement(mousePosition(center,screen_height,screen_width,screenScaleW,screenScaleH))
        logging.debug(f"release distance is {distance}")
        if distance > draggingThreshold*1.3:
            pyautogui.mouseUp()
            isDragging = False
            logging.info("dragging stopped")
    return isDragging

def close(firstTip, secondTip, closeThreshold):
    distance = np.linalg.norm(np.array([firstTip.x, firstTip.y]) - np.array([secondTip.x, secondTip.y]))
    if distance < closeThreshold:
        return True
    else :return False

def mousePosition(center,screenH,screenW, scalingW,scalingH):
    return utils.Point(center.x * screenW*scalingW - screenW*(scalingW-1)/2, center.y * screenH*scalingH -screenH*(scalingH-1)/2)

def mouseMovement(mouseCurrentPosition):
    now = time.time()

    smoothed_x = xFilter(now, mouseCurrentPosition.x)
    smoothed_y = yFilter(now, mouseCurrentPosition.y)

    pyautogui.moveTo(smoothed_x, smoothed_y, duration=0.01)

# def positionCal(hand_landmarks):
#     zeige = (hand_landmarks.landmark[5].x * screen_width, hand_landmarks.landmark[5].y * screen_height)
#     mittel = (hand_landmarks.landmark[9].x * screen_width, hand_landmarks.landmark[9].y * screen_height)
#     ring = (hand_landmarks.landmark[13].x * screen_width, hand_landmarks.landmark[13].y * screen_height)
#
#     # palmCentral_x, palmCentral_y = utils.find_circle_center(zeige,mittel,ring)
#     return zeige, mittel, ring


isDragging = False
window_set_top = False
left_last_click_time = 0
right_last_click_time = 0
click_interval = 0.5
leftClicked = False
rightClicked = False
shouldClose = False

leftClickClassifier = joblib.load("left_clicker_prediction.joblib")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: # ret是是否成功接触到帧的bool
        continue
    cv2.imshow("Hand Tracking Mouse", frame)

    # if not window_set_top:
    #     set_window_always_on_top("Hand Tracking Mouse")
    #     window_set_top = True
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_handedness in enumerate(results.multi_handedness): # 实际上只会进行一次循环
            label = hand_handedness.classification[0].label  # Right Left
            if label == "Right": # 右手


                hand_landmarks = results.multi_hand_landmarks[idx]
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                zeige_tip = hand_landmarks.landmark[8]
                daumen_tip = hand_landmarks.landmark[4]
                mittel_tip = hand_landmarks.landmark[12]
                klein_tip = hand_landmarks.landmark[20]

                zeige_wurzel = hand_landmarks.landmark[5]
                klein_wurzel = hand_landmarks.landmark[17]
                palm_wurzel = hand_landmarks.landmark[0]

                threshould = thresholdCalculation(zeige_wurzel,klein_wurzel)
                shouldClose = close(daumen_tip,klein_wurzel,threshould)

                # length= distance(zeige_wurzel,klein_wurzel)
                # palmArea = area(zeige_wurzel,klein_wurzel,palm_wurzel)
                # leftClickDistance = distance(zeige_tip,daumen_tip)
                leftclickData = np.array([distance(zeige_wurzel,klein_wurzel),area(zeige_wurzel,klein_wurzel,palm_wurzel),distance(zeige_tip,daumen_tip)]).reshape(1,-1)

                if shouldClose:
                    cap.release()
                    cv2.destroyAllWindows()
                    exit(1)

                isDragging = drag(isDragging,daumen_tip,mittel_tip,palm_wurzel,draggingThreshold= threshould)
                if not isDragging:
                    # 移动 取食指根部位置
                    mouseMovement(mousePosition(palm_wurzel,screen_height,screen_width,screenScaleW,screenScaleH))
                    #leftClicked, left_last_click_time = performClick(leftClicked,left_last_click_time,daumen_tip,zeige_tip,clickForm="L", clickThreshold = threshould,clickInterval = 0.5)
                    leftClicked, left_last_click_time = performClick_Classifier(leftClicked,left_last_click_time,leftclickData,leftClickClassifier,"L",clickInterval=click_interval)
                    rightClicked, right_last_click_time = performClick(rightClicked,right_last_click_time,daumen_tip,klein_tip,clickForm="R", clickThreshold = threshould,clickInterval = click_interval)

    cv2.imshow("Hand Tracking Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


