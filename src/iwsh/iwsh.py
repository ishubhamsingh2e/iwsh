import time
import cv2
import mediapipe as mp
import threading

from collections import Counter
import scipy.stats as stats

from iwsh.base import number
from iwsh.base import range

from google.protobuf.json_format import MessageToDict
import numpy as np

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


class video(object):
    print("initializing openCV2...")

    def __init__(self, camera: int = 0) -> None:
        self.camera = camera
        self.FEED = cv2.VideoCapture(camera)

    def show_feed(self, window_title: str = "iwsh") -> None:

        cv2.imshow(
            window_title,
            self.VIDEO_FEED.read()[1]
        )


class hands(object):
    print("initializing mediapipe...")

    def __init__(self, video_object,  static_image_mode: bool, max_num_hands: int, min_detection_confidence: float) -> None:

        self.mp_hands = mp.solutions.hands
        self.video_object = video_object
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence

    def _landmarks(self) -> set:
        """return landmark point and hand

        Returns:
            set: contains two objects landmark and int:hand
        """

        hand_out = []
        ret, frame = self.video_object.FEED.read()

        with self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence
        ) as hands:

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image.flags.writeable = False

            results = hands.process(image)
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


class iwsh(metaclass=Singleton):
    """main entry point for iwsh module, contains all the
       core methode to calculate and predict values for
       API's and applications
    """

    def __init__(self, camera: int = 0, static_image_mode: bool = True, max_num_hands: int = 1, min_detection_confidence: float = 0.5) -> None:

        print("initializing iwsh...")
        self.camera = camera
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence

        self.draw_module = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.VIDEO_FEED = video(camera=self.camera)
        self.HAND_OBJECT = hands(
            video_object=self.VIDEO_FEED,
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence
        )

    def number(self, window_size: int = 2, digit_width: int = 1, show=False) -> np.array:
        """predicts guesture of number in between 0-9 for the landmark

        Args:
            window_size (int, optional): time in sec. for which data should be collected. Defaults to 2.
            digit_width (int, optional): number of digite place. Defaults to 1.

        Returns:
            np.array: predicted value
        """

        _prediction = []
        start_time = time.time()

        while self.VIDEO_FEED.FEED.isOpened():
            landmark, hand = self.HAND_OBJECT._landmarks()

            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > window_size:
                _prediction = list(filter(None, _prediction))
                return stats.mode(_prediction).mode
            else:
                _prediction.append(number.Number(landmark, hand).predict())

        return "video feed is not open"

    def range(self, window_size: int = 2, point_a: int = 4, point_b: int = 8) -> float:
        """
        converts the distance between two points in landmark points,
        into a range between 0 to 1

        Args:
            window_size (int, optional): time in sec for func to run for a specific amount of time. Defaults to 2.
            point_a (int, optional): landmark point of hand. Defaults to 4.
            point_b (int, optional): landmark point of hand. Defaults to 8.

        Returns:
            int: gives a number between 0 to 100 according to the distance between the provided landmark points
        """
        start_time = time.time()
        while self.VIDEO_FEED.FEED.isOpened():
            current_time = time.time()
            elapsed_time = current_time - start_time
            ret, frame = self.VIDEO_FEED.FEED.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image.flags.writeable = False
            res = self.mp_hands.Hands().process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            imageHeight, imageWidth, _ = image.shape
            rangeobj = range.Range(
                imageHeight, imageWidth, res, self.draw_module)
            if elapsed_time > window_size:
                return int(rangeobj.continuous_range(point_A=point_a, point_B=point_b))/100
        return "Video feed is not open"
