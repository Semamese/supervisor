import time
from utils import distance,area

import cv2
import  mediapipe as mp
import pandas as pd
from pyautogui import countdown

def countDown(cap,text,countDownTime):
    start = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        elapsed = time.time() - start
        remaining = max(0,countDownTime - elapsed)
        if remaining > 0:
            cv2.putText(frame,f"{text} starting in {remaining}",(0, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        if remaining == 0:
            break
        cv2.imshow("Hand Sampling Process", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



def sampling(is_clicked:int,sampleCount:int,which:str  = "left"):
    dataTmp = pd.DataFrame(columns=['length', 'area', 'left_click_distance', 'is_clicked'])
    counts = 0
    while cap.isOpened():  # 开始循环抽帧
        ret, frame = cap.read()
        if not ret:  # ret是是否成功接触到帧的bool
            continue
        (_, text_height), _ = cv2.getTextSize("a", cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
        cv2.putText(frame,f"{counts} samples are finished",(0, text_height),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        cv2.imshow("Hand Sampling Process", frame)
        # if not window_set_top:
        #     set_window_always_on_top("Hand Tracking Mouse")
        #     window_set_top = True
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_handedness in enumerate(results.multi_handedness):  # 实际上只会进行一次循环
                label = hand_handedness.classification[0].label  # Right Left
                if label == "Right":  # 右手
                    hand_landmarks = results.multi_hand_landmarks[idx]
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    if which == "right":
                        sample = {"length": distance(hand_landmarks.landmark[5], hand_landmarks.landmark[17]),
                                  "area": area(hand_landmarks.landmark[5], hand_landmarks.landmark[17],
                                               hand_landmarks.landmark[0]),
                                  "left_click_distance": distance(hand_landmarks.landmark[8], hand_landmarks.landmark[4]),
                                  "is_clicked": is_clicked}
                        dataTmp = pd.concat([dataTmp, pd.DataFrame([sample])], ignore_index=True)
                        counts += 1
                    if which == "left":
                        sample = {"length": distance(hand_landmarks.landmark[5], hand_landmarks.landmark[17]),
                                  "area": area(hand_landmarks.landmark[5], hand_landmarks.landmark[17],
                                               hand_landmarks.landmark[0]),
                                  "left_click_distance": distance(hand_landmarks.landmark[20],
                                                                  hand_landmarks.landmark[4]),
                                  "is_clicked": is_clicked}
                        dataTmp = pd.concat([dataTmp, pd.DataFrame([sample])], ignore_index=True)
                        counts += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if counts == sampleCount:
            return dataTmp

def main():

    data = pd.DataFrame(columns=['length','area','left_click_distance','is_clicked'])


    # the sampling for unclicked, can be seperated from sampling for some specific movement
    # comment the following 2 lines if we only want to sample the click
    countDown(cap, "sampling for NOT clicked", 5)
    data = pd.concat([sampling(0,1000),data],ignore_index=True)

    data.to_csv("Meng_Unclicked")

    countDown(cap,"sampling for clicked",3)
    data = pd.concat([sampling(1,1000,"right"),data],ignore_index=True)

    data.to_csv("right.csv")


if __name__ == "__main__":
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7, min_tracking_confidence=0.7)
    cap = cv2.VideoCapture(1)
    cv2.namedWindow("Hand Sampling Process", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Sampling Process", 1280, 1280)
    main()






