import re


def reader(filepath):
    with open(filepath) as f:
        text = f.readlines()
    return text

def md_parser(text):
    # 清除文本中的所有花括号内容
    tmp = re.sub(r'\{.*?\}', '', text)
    # 清除html标记
    tmp = re.sub('<.*?>', '', tmp)
    # 清除markdown图片
    tmp = re.sub('\!\[.*?\]\(.*?\)', '', tmp)

    return tmp

def md_extract_image_link(text):
    # 正则表达式匹配Markdown图片链接
    img_pattern = r"!\[.*?\]\((.*?)\)"
    img_links = re.findall(img_pattern, text)
    return img_links