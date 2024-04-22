import os
from logger import Logger
from text_checker import text_check
from utils import reader
from ignore_files import ignores


def checker(root, path, logger):
    lines = reader(os.path.join(root, path))
    yaml_flag = 0
    for i, line in enumerate(lines):
        # 跳过yaml标记
        if line.startswith('---'):
            yaml_flag += 1
        if yaml_flag < 2:
            continue
        text_check(path, i, line, logger)

if __name__ == '__main__':
    logger = Logger('./text_check.log')
    proj_root = "../aneot/docs/posts/"
    issues = [item for item in os.listdir(proj_root) if item not in ['README.md', '.DS_Store']]
    for issue in issues:
        articles = [i for i in os.listdir(os.path.join(proj_root, issue)) if 'article' in i]
        for article in articles:
            filepath = os.path.join(issue, article)
            if filepath in ignores:
                continue
            checker(proj_root, filepath, logger)
    print(f"检查完毕。")