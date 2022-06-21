"""
    use "q" for capturing new gesture
    you can change caps variables
"""

from google.protobuf.json_format import MessageToDict

import pandas as pd

import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import time
import sys

import json

FLAG = int(sys.argv[1])
VIDEO_FEED = 0
WIN_TITLE = ""
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRAKING_CONFIDENCE = 0.3
HAND = sys.argv[2].upper()

index = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(VIDEO_FEED)

data = {
    "uid": [],
    "hand": [],
}

for i in range(0,21):
    data[f"x{i}"] = []
    data[f"y{i}"] = []
    data[f"z{i}"] = []

data["gesture"] = []

print(data)

try:
    os.mkdir('data')
except:
    pass

with mp_hands.Hands(
    min_detection_confidence= MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence= MIN_TRAKING_CONFIDENCE,
    max_num_hands=1
    ) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)
        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imshow(WIN_TITLE, image)

        # try:
        #     os.mkdir("data/"+str(FLAG))
        # except:
        #     pass

        if results.multi_hand_landmarks:
            time.sleep(0.2)
            uid = uuid.uuid1()
            handedness = MessageToDict(results.multi_handedness[0])
            # hand_type = handedness['classification'][0]['label']
            # hand_type_score = handedness['classification'][0]['score']
            landmarks = MessageToDict(results.multi_hand_landmarks[0])

            data["uid"].append(str(uid))
            data["hand"].append(HAND)
            # data["score"].append(hand_type_score)
            data["gesture"].append(FLAG)

            # print(landmarks["landmark"])

            for i in landmarks["landmark"]:

                if index == 21:
                    index = 0

                data[f"x{index}"].append(i['x'])
                data[f"y{index}"].append(i['y'])
                data[f"z{index}"].append(i['z'])

                index += 1

            # cv2.imwrite(os.path.join('data',f"{FLAG}",f"{uid}.jpg"), image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

data = pd.DataFrame.from_dict(data)
data.to_csv(f"data/{uuid.uuid1()}.csv", index=False)
