import mediapipe as mp
import cv2
import sys
import os

mp_hands = mp.solutions.hands

path = sys.argv[1]
_files = os.listdir(path=path)
_files.remove('dump')
_files.remove('data.csv')

for file in _files:
    total_path = path+file
    image = cv2.imread(total_path)
    

    with mp_hands.Hands() as hands:
        print(total_path, end=" ")
        results =  hands.process(image)       
        if results.multi_hand_landmarks:
            print(True)
        else:
            print(False)
            os.system(f"move {total_path} {path}/dump")