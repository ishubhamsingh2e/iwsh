import pandas as pd
import glob
import sys

PATH = sys.argv[1]
WRITE = sys.argv[2]
FILE = sys.argv[3]

TOTAL_OBSER = 0

files = glob.glob(glob.escape(PATH) + "/*.csv")

data = []
for i in files:
    print(f"read_file: {i}", end="")
    data.append(pd.read_csv(i))
    print( f", shape : {data[-1].shape}")
    TOTAL_OBSER += data[-1].shape[0]

print(f"total observations : {TOTAL_OBSER}")

print("concateating data...")
data = pd.concat(data)

print("preprocessing data...")
data['hand'].replace('RIGHT', 1, inplace=True)
data['hand'].replace('LEFT', 0, inplace=True)

print(f"shape of data writen : {data.shape}")
data.to_csv(f"{WRITE}\\{FILE}", index=False)