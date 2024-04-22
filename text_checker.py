import re
from logger import Logger
from punc_checker import check_chinese_quotes, check_continuous_dots
from utils import md_parser


def text_check(path, i, line, logger: Logger):
    # 检测行首/行尾的空格
    if line[0] in [' ', '\t']:
        logger.verbose(path, f"第 {i+1} 行行首有空格，这是否应该有空格？")
    if line[-1] in [' ', '\t']:
        logger.verbose(path, f"第 {i+1} 行行尾有空格,这是否应该有空格?")
    # 跳过空行、标题行和分割线
    text = md_parser(line)
    if (len(text) == 0) or (text[0] == '#') or (text[:3] in ['---', '___', '***']):
        return 0

    # 检测中英标点混用
    pattern = r'[^\x00-\xff]{1,3}[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E][^\x00-\xff]{1,3}'
    find = re.findall(pattern, text)
    if len(find) > 0:
        for item in find:
            logger.verbose(path, f"第 {i+1} 行可能有夹杂在中文中的英文标点 「{item}」.")
    
    # 检测引号闭合问题
    if not check_chinese_quotes(text):
        print(f"{path}: 第 {i+1} 行可能有错误使用的引号.")

    # 检测省略号问题
    dots = check_continuous_dots(text)
    if len(dots) > 0:
        for item in dots:
            logger.verbose(path, f"第 {i+1} 行出现「{item}」，这是否应该是省略号？")

    # pangu
    pattern = re.compile(r'([\u4e00-\u9fff]+[a-zA-Z0-9]+)|([a-zA-Z0-9]+[\u4e00-\u9fff]+)')
    pangu = re.findall(pattern, text)
    for item in pangu:
        for subitem in item:
            if len(subitem) > 0:
                logger.verbose(path, f"第 {i+1} 行出现「{subitem}」，这其中是否缺少了空格？")

    pattern = r'[^\x00-\xff]{1,3}\s[^\x00-\xff]{1,3}'
    result = re.findall(pattern, text)
    if len(result) > 0:
        for item in result:
            logger.verbose(path, f"第 {i+1} 行出现「{item}」，这其中是否有多余的空格？")
