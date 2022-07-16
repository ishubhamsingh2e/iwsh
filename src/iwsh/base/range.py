import math
import numpy as np
class Range:
    def __init__(self,imageh,imagew,res,draw):
        self.image_height = imageh
        self.image_width = imagew
        self.resu= res
        self.draw = draw


    def e_dist(self,pixelthumb,pixelindex):
        if pixelindex != None and pixelthumb != None:
            ecd = math.dist(pixelindex,pixelthumb)
            return ecd



    def continuous_range(self,point_A:int=4,point_B:int=8):
        """ takes two points and converts their landmark to nomalized point

        Args:
            point_A (int, optional): landmark hand point. Defaults to 4.
            point_B (int, optional): landmark hand point. Defaults to 8.

        Returns:
            _type_: _description_
        """
        if self.resu.multi_hand_landmarks != None:
            for handLandmarks in self.resu.multi_hand_landmarks:
                    normalizedLandmark1 = handLandmarks.landmark[point_A]
                    pixelCoordinatesLandmark1 = self.draw._normalized_to_pixel_coordinates(normalizedLandmark1.x, normalizedLandmark1.y, self.image_width,self.image_height)
                    thumb = pixelCoordinatesLandmark1
                    normalizedLandmark2 = handLandmarks.landmark[point_B] #change the value 4 to change the point of finger acc
                    pixelCoordinatesLandmark2 = self.draw._normalized_to_pixel_coordinates(normalizedLandmark2.x, normalizedLandmark2.y,self.image_width,self.image_height)
                    index = pixelCoordinatesLandmark2
                    range_numeric = self.e_dist(thumb,index)
                    real_range = np.interp(range_numeric,[28,280],[0,100])
                    return real_range
        else:
            return 0
