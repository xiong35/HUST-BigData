from numpy.ma.core import dot
import pandas as pd
import numpy as np


df = pd.read_csv("./实验二/数据/sent_receive.csv")

mat = np.zeros((513, 513))

for (sent_id, part_df) in list(df.groupby('sent_id')):
    receivers = []
    for (receiver_id, ppt_df) in list(part_df.groupby('receive_id')):
        receivers.append(int(receiver_id))
    count = len(receivers)
    mat[receivers, int(sent_id)] = 1 / count

r = np.ones((513, 1)) / 513

while 1:
    new_r = np.dot(mat, r)
    diff = (new_r - r)**2

    if np.sum(diff) < 1e-8:
        break
    r = new_r

with open("./result.txt", "w") as fw:
    i = 0
    while 1:
        if i == len(r):
            break

        fw.write(str(i+1) + "\t"+str(float(r[i]))+"\n")
        i += 1
