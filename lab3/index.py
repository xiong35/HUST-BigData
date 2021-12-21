import pandas as pd

SUPPORT = 0.005
CONF = 0.5


def csv2list():
    df = pd.read_csv("./实验三/数据/Groceries.csv")

    itemsets = []

    for itemset_str in df["items"]:
        itemsets.append(set(itemset_str[1:-1].split(",")))

    return itemsets


itemsets = csv2list()
itemsets_len = itemsets.__len__()


def build1deg(itemsets):
    SAVE_PATH = "./ond_deg_support.txt"

    one_deg = {}
    for itemset in itemsets:
        for item in itemset:
            one_deg[item] = one_deg.get(item, 0) + 1

    one_deg_count = 0
    items = list(one_deg.keys())
    with open(SAVE_PATH, "w") as fw:
        for item in items:
            support = one_deg[item] / itemsets_len
            if support > SUPPORT:
                one_deg[item] = support
                fw.write(f"{item}: {support}\n")
                one_deg_count += 1
            else:
                del one_deg[item]

    print(f"频繁一项集数量: {one_deg_count}", )
    print(f"频繁一项集保存在`{SAVE_PATH}`")

    return one_deg


one_deg = build1deg(itemsets)


def build2deg(one_deg, itemsets):
    SAVE_PATH = "./two_deg_support.txt"

    items = list(one_deg.keys())
    two_deg = {}

    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            key = (items[i], items[j])
            for itemset in itemsets:
                if key[0] in itemset and key[1] in itemset:
                    two_deg[key] = two_deg.get(key, 0) + 1

    pairs = list(two_deg.keys())

    two_deg_count = 0

    with open(SAVE_PATH, "w") as fw:
        for pair in pairs:
            support = two_deg[pair] / itemsets_len
            if support > SUPPORT:
                two_deg[pair] = support
                fw.write(f"{pair}: {support}\n")
                two_deg_count += 1
            else:
                del two_deg[pair]

    print(f"频繁二项集数量: {two_deg_count}", )
    print(f"频繁二项集保存在`{SAVE_PATH}`")

    return two_deg


two_deg = build2deg(one_deg, itemsets)


def gen2deg_rules(one_deg, two_deg):
    SAVE_PATH = "./two_deg_rules.txt"

    pairs = list(two_deg.keys())

    rules = {}

    for pair in pairs:
        rule = (pair[0], pair[1])
        conf = two_deg[pair] / one_deg[rule[0]]
        if conf > CONF:
            rules[rule] = conf

        rule = (pair[1], pair[0])
        conf = two_deg[pair] / one_deg[rule[0]]
        if conf > CONF:
            rules[rule] = conf

    with open(SAVE_PATH, "w") as fw:
        for k, v in rules.items():
            fw.write(f"{k[0]}->{k[1]}: {v}\n")
    print(f"频繁二项集规则数量: {len(rules.keys())}", )
    print(f"频繁二项集规则保存在`{SAVE_PATH}`")


gen2deg_rules(one_deg, two_deg)


def build3deg(two_deg,  itemsets):
    SAVE_PATH = "./three_deg_support.txt"

    pairs = list(two_deg.keys())

    itemset_3 = set()
    for pair in pairs:
        itemset_3.add(pair[0])
        itemset_3.add(pair[1])
    itemset_3 = list(itemset_3)
    itemset_3.sort()

    three_deg = {}

    for i in range(0, len(itemset_3)):
        for j in range(i+1, len(itemset_3)):
            for k in range(j+1,  len(itemset_3)):
                item_i = itemset_3[i]
                item_j = itemset_3[j]
                item_k = itemset_3[k]

                for itemset in itemsets:
                    if item_i in itemset and item_j in itemset and item_k in itemset:
                        tup = (item_i, item_j, item_k)
                        three_deg[tup] = three_deg.get(tup, 0)+1

    three_deg_count = 0
    tups = list(three_deg.keys())

    with open(SAVE_PATH, "w") as fw:
        for tup in tups:
            support = three_deg[tup] / itemsets_len
            if support > SUPPORT:
                three_deg[tup] = support
                fw.write(f"{tup}: {support}\n")
                three_deg_count += 1
            else:
                del three_deg[tup]

    print(f"频繁三项集数量: {three_deg_count}", )
    print(f"频繁三项集保存在`{SAVE_PATH}`")

    return three_deg


three_deg = build3deg(two_deg,  itemsets)


def gen3deg_rules(one_deg, two_deg, three_deg):
    SAVE_PATH = "./three_deg_rules.txt"

    tups = list(three_deg.keys())

    rules = {}

    def enumTup(tup):
        return [
            (tup, tup[0], (tup[1],  tup[2])),
            (tup, tup[1], (tup[0],  tup[2])),
            (tup, tup[2], (tup[0],  tup[1])),
            (tup, (tup[1], tup[2]), tup[0]),
            (tup, (tup[0], tup[2]), tup[1]),
            (tup, (tup[0], tup[1]), tup[2]),
        ]

    three_deg_rule_num = 0
    with open(SAVE_PATH, "w") as fw:
        for tup in tups:
            rules = enumTup(tup)
            for three, one, two in rules[:3]:
                conf = three_deg[three] / one_deg[one]
                if conf > CONF:
                    fw.write(f"{one}->{two}: {conf}\n")
                    three_deg_rule_num += 1
            for three, two, one in rules[3:]:
                try:
                    conf = three_deg[three] / two_deg[two]
                except:
                    try:
                        conf = three_deg[three] / two_deg[(two[1], two[0])]
                    except:
                        print(two, "not found")
                if conf > CONF:
                    fw.write(f"{two}->{one}: {conf}\n")
                    three_deg_rule_num += 1
    print(f"频繁三项集规则数量: {three_deg_rule_num}", )
    print(f"频繁三项集规则保存在`{SAVE_PATH}`")


gen3deg_rules(one_deg, two_deg, three_deg)
