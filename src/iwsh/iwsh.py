import time
import cv2
import mediapipe as mp

from collections import Counter

from iwsh import base
from google.protobuf.json_format import MessageToDict


class iwsh:
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
        _predictions = []

        t_end = time.time() + window_size
        landmark, hand = self._landmarks()

        while self.VIDEO_FEED.isOpened() and time.time() < t_end:
            _predictions.append(
                base.Number.number(
                    landmark=landmark,
                    hand=hand
                ).predict()
            )

        out = Counter(_predictions).most_common(1)[0][0]
        return out

    def _landmarks(self) -> set:
        """return landmark point and hand

        Returns:
            set: contains two objects landmark and int:hand
        """

        hand_out  = []

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
                hand = MessageToDict(results.multi_handedness[0])['classification'][0]['label']

                if hand == "Right":
                    hand = 1
                elif hand == "Left":
                    hand = 0
                else:
                    raise ValueError()

                hand_out.append(hand)

        return (landmark, hand_out)
