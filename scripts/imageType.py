import cv2
import matplotlib.pyplot as plt
import sys
data_loc = sys.argv[1]

im = cv2.imread(data_loc)

plt.imshow(im)
plt.show() # if the image is not in RGB formate colour diffrence will be their