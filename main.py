import os
from text_checker import text_check
from utils import reader


def checker(path):
    lines = reader(path)
    yaml_flag = 0
    for i, line in enumerate(lines):
        # 跳过yaml标记
        if line[:3] == '---':
            yaml_flag += 1
        if yaml_flag < 2:
            continue
        text_check(path, i, line)

if __name__ == '__main__':
    folder = './test/'
    file = "article6.md"
    path = os.path.join(folder, file)
    checker(path)
    print(f"{path} 检查完毕。")