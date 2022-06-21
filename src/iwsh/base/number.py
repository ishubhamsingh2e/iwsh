import pickle
import numpy as np

from google.protobuf.json_format import MessageToDict

from sklearn.svm import SVC


class number:
    def __init__(self, landmark, hand: int) -> None:
        self.__MODEL = pickle.load("../model/number.pkl")
        self.landmark: dict = MessageToDict(landmark)
        self.data = [hand]

        for i in landmarks["landmark"]:
            self.data.append(i['x'])
            self.data.append(i['y'])
            self.data.append(i['z'])

    def predict(self) -> np.array:
        """predicts the value

        Returns:
            np.array: pridected value
        """
        output = self.__MODEL.predict(np.array(data))

        return output
