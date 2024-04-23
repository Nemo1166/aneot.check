import os
import re
import requests
from bs4 import BeautifulSoup

wiki_url = 'https://prts.wiki/'

def write_file(filename: str, content: list):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in content:
            f.write(item + '\n')

def read_file(filename: str):
    with open(filename, encoding='utf-8') as f:
        return [line.strip() for line in f]

# %% org
print('处理组织名')
org = 'w/泰拉大典:组织'
db_orgs = []
response = response = requests.get(wiki_url+org)
soup = BeautifulSoup(response.text, 'html.parser')
body = soup.find('div', class_='mw-parser-output')
results = [li.string for li in body.find_all('li', class_='')]
for result in results:
    if result == None:
        continue
    r = re.sub(r'\（[^)]*\）', '', result)
    if '→' in r:
        db_orgs += r.split('→')
    elif '/' in r:
        db_orgs += r.split('/')
    else:
        db_orgs.append(r)

db_orgs = list(set(db_orgs))
# print(db_orgs)
# write_file('data/std_org.txt', db_orgs)

# %% char
print('处理人物名')
db_char = []
per = 'w/泰拉大典:角色'
response = requests.get(wiki_url+per)
soup = BeautifulSoup(response.text, 'html.parser')
found = soup.find_all('div', style='-moz-column-count:4; -webkit-column-count:4; column-count:4; -moz-column-width:auto; -webkit-column-width:auto; column-width:auto; -moz-column-gap:0; -webkit-column-gap:0; column-gap:0; -moz-column-rule:; -webkit-column-rule:; column-rule:;')
for f in found:
    for i in f.find_all('p'):
        t = i.next
        # print(t)
        # exit()
        if type(t.string) == None:
            db_char.append(t.next.string)
        else:
            db_char.append(t.string)

per2 = 'w/泰拉大典:角色/其他'
response = requests.get(wiki_url+per2)
soup = BeautifulSoup(response.text, 'html.parser')
found = soup.find_all('h3', class_='')
elems = [i.find_all('span', class_='mw-headline') for i in found]
for elem in elems:
    if len(elem) == 0:
        continue
    else:
        db_char += [i.string for i in elem]

per3 = 'w/泰拉大典:Index'
response = requests.get(wiki_url+per3)
soup = BeautifulSoup(response.text, 'html.parser')
found = soup.find_all('tbody', class_='')
for f in found:
    try:
        title = f.find('div', style='font-size:150%').string
        if title == '罗德岛干员名单':
            ops = f.find_all('a')
            break
    except:
        continue
else:
    print('没有找到罗德岛干员名单，程序中断')
    exit()

ops = [i.string for i in ops if '-' not in i.string]
db_char += ops

db_char = list(set(db_char))
# write_file('data/std_char.txt', db_char)

# %% 词典
print('合并词典')
repo = 'w/泰拉词库'
ents = []
response = requests.get(wiki_url+repo)
soup = BeautifulSoup(response.text, 'html.parser')
found = soup.find_all('tbody', class_='')
for table in found:
    if table:
        # 提取表格数据
        data = []
        for row in table.find_all('tr'):
            # 忽略表头行
            if row.find('th'):
                continue
            data.append([cell.text.strip() for cell in row.find_all('td')])
        
        # 合并表头和数据
        ents += [item[0] for item in data]
    else:
        print("未找到表格标签")

ents += db_char+db_orgs+read_file('data/std_prof.txt')
ents = list(set(ents))
write_file('data/std_ent.txt', ents)