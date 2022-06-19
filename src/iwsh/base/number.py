import pickle


class number:
    def __init__(self, window_size: int = 2, digit_width: int = 1) -> None:
        self.MODEL = pickle.load("../model/number.pkl")
        self.WINDOW = window_size
        self.WIDTH = digit_width