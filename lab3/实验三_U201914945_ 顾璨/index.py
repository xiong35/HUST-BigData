import pandas as pd

"""
读取数据
"""

df = pd.read_csv("../实验三/数据/Groceries.csv")

itemsets = []

for itemset_str in df["items"]:
    itemsets.append(set(itemset_str[1:-1].split(",")))
itemsets_len = itemsets.__len__()

"""
构造频繁一项集
"""

one_deg = {}
for itemset in itemsets:
    for item in itemset:
        one_deg[item] = one_deg.get(item, 0) + 1

count = 0
items = list(one_deg.keys())
with open("support1.txt", "w") as fw:
    for item in items:
        support = one_deg[item] / itemsets_len
        if support > 0.005:
            one_deg[item] = support
            fw.write(str(item)+": "+str(support)+"\n")
            count += 1
        else:
            del one_deg[item]

print("频繁一项集构造完毕，共有"+str(count)+"个，保存在 support1.txt")


"""
构造频繁二项集
"""

two_deg = {}

for i in range(0, len(items)):
    for j in range(i+1, len(items)):
        key = (items[i], items[j])
        for itemset in itemsets:
            if key[0] in itemset and key[1] in itemset:
                two_deg[key] = two_deg.get(key, 0) + 1

pairs = list(two_deg.keys())

count = 0

with open("support2.txt", "w") as fw:
    for pair in pairs:
        support = two_deg[pair] / itemsets_len
        if support > 0.005:
            two_deg[pair] = support
            fw.write(str(pair)+": "+str(support)+"\n")
            count += 1
        else:
            del two_deg[pair]


pairs = list(two_deg.keys())

print("频繁二项集构造完毕，共有"+str(count)+"个，保存在 support2.txt")


"""
构造频繁二项集产生的规则
"""


rules = {}

count = 0
with open("rule2.txt", "w") as fw:
    for pair in pairs:
        rule = (pair[0], pair[1])
        conf = two_deg[pair] / one_deg[rule[0]]
        if conf > 0.5:
            count += 1
            fw.write(str(rule[0])+"->"+str(rule[1])+": "+str(conf)+"\n")

        rule = (pair[1], pair[0])
        conf = two_deg[pair] / one_deg[rule[0]]
        if conf > 0.5:
            count += 1
            fw.write(str(rule[0])+"->"+str(rule[1])+": "+str(conf)+"\n")


print("频繁二项集规则构造完毕，共有"+str(count)+"个，保存在 rule2.txt")


"""
构造频繁三项集
"""

items = set()
for pair in pairs:
    items.add(pair[0])
    items.add(pair[1])
items = list(items)
items.sort()

three_deg = {}

for i in range(0, len(items)):
    for j in range(i+1, len(items)):
        for k in range(j+1,  len(items)):
            item_i = items[i]
            item_j = items[j]
            item_k = items[k]

            for itemset in itemsets:
                if item_i in itemset and item_j in itemset and item_k in itemset:
                    tup = (item_i, item_j, item_k)
                    three_deg[tup] = three_deg.get(tup, 0)+1

count = 0
tups = list(three_deg.keys())

with open("support3.txt", "w") as fw:
    for tup in tups:
        support = three_deg[tup] / itemsets_len
        if support > 0.005:
            three_deg[tup] = support
            fw.write(str(tup)+": "+str(support)+"\n")

            count += 1
        else:
            del three_deg[tup]


tups = list(three_deg.keys())
print("频繁三项集构造完毕，共有"+str(count)+"个，保存在 support3.txt")


"""
构造频繁三项集的关联规则
"""

rules = {}


def enumTup(tup):
    return [
        (tup[0], (tup[1],  tup[2])),
        (tup[1], (tup[0],  tup[2])),
        (tup[2], (tup[0],  tup[1])),
        ((tup[1], tup[2]), tup[0]),
        ((tup[0], tup[2]), tup[1]),
        ((tup[0], tup[1]), tup[2]),
    ]


count = 0
with open("rule3.txt", "w") as fw:
    for tup in tups:
        rules = enumTup(tup)
        for one, two in rules[:3]:
            conf = three_deg[tup] / one_deg[one]
            if conf > 0.5:
                fw.write(str(one)+"->"+str(two)+": "+str(conf)+"\n")
                count += 1
        for two, one in rules[3:]:
            try:
                conf = three_deg[tup] / two_deg[two]
            except:
                continue
            if conf > 0.5:
                fw.write(str(two)+"->"+str(one)+": "+str(conf)+"\n")
                count += 1

print("频繁三项集规则构造完毕，共有"+str(count)+"个，保存在 rule3.txt")
