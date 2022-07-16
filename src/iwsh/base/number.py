import pickle
import numpy as np

from google.protobuf.json_format import MessageToDict

from sklearn.svm import SVC
import site


class Number:
    def __init__(self, landmark: list, hand: list[int]) -> None:
        self.landmark = landmark
        self.hand = hand
        self.data = []

        if self.landmark and self.hand != []:
            for i in range(len(self.hand)):
                _data = [self.hand[i]]
                _landmark = MessageToDict(self.landmark[i])
                for j in _landmark["landmark"]:
                    _data.append(j['x'])
                    _data.append(j['y'])
                    _data.append(j['z'])

                self.data.append(_data)

    def predict(self) -> np.array:
        """predicts the value

        Returns:
            np.array: pridected value
        """

        with open(site.getsitepackages()[-1] + "\\iwsh\\model\\number.pkl", "rb") as model:
            MODEL = pickle.load(model)

        if self.landmark and self.hand != []:
            output = MODEL.predict(np.array(self.data))
            return output.tolist()
