from numpy.ma.core import dot
import pandas as pd
import numpy as np

PERSON_COUNT = 513

# df = pd.read_csv("./实验二/数据/sent_receive.csv")
df = pd.read_csv(
    "C:\\Users\\xiong35\\Desktop\\projects\\HUST-BigData\\lab2\\实验二\\数据\\sent_receive.csv")

mat = np.zeros((PERSON_COUNT, PERSON_COUNT))

for (sent_id, part_df) in list(df.groupby('sent_id')):
    receivers = []
    for (receiver_id, ppt_df) in list(part_df.groupby('receive_id')):
        receivers.append(int(receiver_id))
    count = len(receivers)
    mat[receivers, int(sent_id)] = 1 / count

# teleport

Beta = 0.9
mat = mat*Beta + np.ones((PERSON_COUNT, PERSON_COUNT))/PERSON_COUNT * (1-Beta)

r = np.ones((PERSON_COUNT, 1)) / PERSON_COUNT

while 1:

    new_r = np.dot(mat, r)
    diff = (new_r - r)**2

    if np.sum(diff) < 1e-10:
        break
    r = new_r

print(np.sum(r))
