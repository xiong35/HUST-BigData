
from concurrent import futures


def read_file(file_id):
    word_dict = {}
    with open(f"./第一次实验/实验一/source数据文件/source0{file_id}", "r") as fr:
        line = fr.readline()
        while line:
            for word in line.strip().split(", "):
                word_dict[word] = word_dict.get(word, 0) + 1
            line = fr.readline()

    return word_dict


def reduce(word_dicts):
    return_dict = {}
    for d in word_dicts:
        for k, v in d.items():
            return_dict[k] = return_dict.get(k, 0) + v
    return return_dict


def count_all():
    # 字典的数组, 每个字典是 词->词频
    word_dicts = []
    with futures.ProcessPoolExecutor(9) as pool:
        for word_dict in pool.map(read_file, range(1, 10)):
            word_dicts.append(word_dict)

    split_dicts = [word_dicts[:5], word_dicts[5:]]
    word_dicts = []

    with futures.ProcessPoolExecutor(2) as pool:
        for word_dict in pool.map(reduce, split_dicts):
            word_dicts.append(word_dict)

    return reduce(word_dicts)


if __name__ == '__main__':
    print(count_all())
