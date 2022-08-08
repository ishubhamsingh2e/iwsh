import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    "C:/Users/shubham/Documents/git/iwsh/machine_learning/data/number/number.csv")

df.drop(["uid"], axis=1,  inplace=True)

for i in range(0, 21):
    df.drop([f"z{i}"], axis=1, inplace=True)

data = df[99:100]
print(data)
for i in range(0, 21):
    plt.scatter(data[f"x{i}"], data[f"y{i}"])

print(data["gesture"])
plt.show()
