import cv2
import mediapipe as mp

class iwsh:
    def __init__(self, VIDEO_FEED, HAND_OBJECT) -> None:
        self.VIDEO_FEED = VIDEO_FEED
        self.HAND_OBJECT = HAND_OBJECT

    def number(self, window_size: int = 2, digit_width: int = 1) -> int:
        while self.VIDEO_FEED.isOpened():
            pass

    def landmarks(self):
        while self.VIDEO_FEED.isOpened():
            ret, frame = self.VIDEO_FEED.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image.flags.writeable = False

            results = self.HAND_OBJECT.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            cv2.imshow("WIN_TITLE", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):        
                self.VIDEO_FEED.release()

            landmark = results.multi_hand_landmarks

        return landmark
