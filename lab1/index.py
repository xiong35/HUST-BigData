
from concurrent import futures


def read_file(file_id):
    word_dict = {}

    file2read = f"./第一次实验/实验一/source数据文件/source0{file_id}"
    print("reading ", file2read)

    with open(file2read, "r") as fr:
        line = fr.readline()
        while line:
            for word in line.strip().split(", "):
                word_dict[word] = word_dict.get(word, 0) + 1
            line = fr.readline()
    print("finish reading ", file2read)
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

    print("read all files")
    print("begin to reduce")

    split_dicts = [word_dicts[:5], word_dicts[5:]]
    word_dicts = []

    with futures.ProcessPoolExecutor(2) as pool:
        for word_dict in pool.map(reduce, split_dicts):
            word_dicts.append(word_dict)

    print("finish reduce 1")
    return_dict = reduce(word_dicts)
    print("finish reduce 2")

    return return_dict


if __name__ == '__main__':
    return_dict = count_all()
    with open("./result.txt", "w") as fw:
        for k, v in return_dict.items():
            fw.write(f"{k}:\t{v}\n")
