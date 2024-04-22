import os
from tqdm import tqdm, trange
from utils import md_extract_image_link

proj_dir = '../aneot/docs/posts/'

issues = os.listdir(proj_dir)

# 期刊列表
with open(os.path.join(proj_dir, 'README.md'), 'r') as f:
    issues_list = f.read().split('\n')

line_ptr = 0
yaml_flag = 0
img_title = True
issues_metatext = []
issues_cover = []
for line_ptr in range(len(issues_list)):
    line = issues_list[line_ptr]
    if line.startswith('---'):
        yaml_flag += 1
    if yaml_flag < 2:
        continue
    
    if line.startswith('**'):
        latest_title = line.split('**')[1]
    if line.startswith('|') and line[1] != ':':
        issue_meta = line.split('|')[1:-1]
        match img_title:
            case True:
                issues_cover += md_extract_image_link(line)
                img_title = not img_title
            case False:
                img_title = not img_title

print(issues_cover)
        # issues_meta.append(issue_meta)



