import re


def check_continuous_dots(text):
    # 定义正则表达式匹配连续出现的点或句号
    continuous_dots_pattern = r'\.{2,}|\u3002{2,}'  # 匹配两个或更多的点或句号
    
    # 查找所有匹配的连续点或句号
    continuous_dots_matches = re.findall(continuous_dots_pattern, text)
    
    return continuous_dots_matches

def check_chinese_quotes(text):
    stack = []
    quotes = {'“': '”', '‘': '’'}  # 左引号到右引号的映射

    for char in text:
        if char in quotes.keys():
            stack.append(char)
        elif char in quotes.values():
            if not stack or quotes[stack.pop()] != char:
                return False
    return len(stack) == 0