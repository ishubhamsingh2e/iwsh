import json
import sys
import os
import cv2
import numpy


path = sys.argv[1]
_files = os.listdir(path=path)

for i in _files:
    total_path = path + i
    print("converting:", i, "@", total_path[2:])
    img = cv2.imread(total_path[2:])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(total_path[2:], img)

data = {
    "is_RGB": True
}

json_object = json.dumps(data, indent = 4)

with open(path+"formate.json", "w") as md:
    md.write(json_object)