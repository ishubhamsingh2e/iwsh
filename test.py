import iwsh

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

VIDEO_FEED = 1

cap = cv2.VideoCapture(VIDEO_FEED)

with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
    obj = iwsh.iwsh(cap, hands)
    print(obj.landmarks())