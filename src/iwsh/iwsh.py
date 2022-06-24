import time
import cv2
import mediapipe as mp
import threading

from collections import Counter
import scipy.stats as stats

from iwsh.base import Number
from google.protobuf.json_format import MessageToDict

LOCK = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with LOCK:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class iwsh(metaclass=Singleton):
    """main entry point for iwsh module, contains all the
       core methode to calculate and predict values for
       API's and applications
    """

    def __init__(self, VIDEO_FEED, HAND_OBJECT) -> None:
        self.VIDEO_FEED = VIDEO_FEED
        self.HAND_OBJECT = HAND_OBJECT

    def number(self, window_size: int = 2, digit_width: int = 1) -> int:
        """predicts guesture of number in between 0-9 for the landmark

        Args:
            window_size (int, optional): time in sec. for which data should be collected. Defaults to 2.
            digit_width (int, optional): number of digite place. Defaults to 1.

        Returns:
            int: predicted value
        """

        _prediction = []
        start_time = time.time()

        while self.VIDEO_FEED.isOpened():
            landmark, hand = self._landmarks()

            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > window_size:
                _prediction = list(filter(None, _prediction))
                return stats.mode(_prediction).mode
            else:
                _prediction.append(Number.number(landmark, hand).predict())

        return "video feed is not open"

    def _landmarks(self) -> set:
        """return landmark point and hand

        Returns:
            set: contains two objects landmark and int:hand
        """

        hand_out = []

        ret, frame = self.VIDEO_FEED.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False

        results = self.HAND_OBJECT.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        landmark = results.multi_hand_landmarks

        if results.multi_hand_landmarks:
            for i in results.multi_handedness:
                hand = MessageToDict(i)['classification'][0]['label']

                if hand == "Right":
                    hand = 1
                elif hand == "Left":
                    hand = 0
                else:
                    raise ValueError()

                hand_out.append(hand)

        return (landmark, hand_out)
