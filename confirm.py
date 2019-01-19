import sys,re

minutes_path = sys.argv[1]
name_path = sys.argv[2]
with open(name_path,'r')as F:
    names = F.read().split(' ')
with open(minutes_path,'r')as f:
    count = 0
    n = []
    pattern = "(.*)　(.*)"  #全角スペースで分ける
    for line in f:
        if line.find('○',0,10) == 0: #○から名前なのでここで取り除く
            sep = re.search(pattern,line)
            n += sep.group(1)
            count += 1

print(len(names),count)
if len(names)-1 == count:
    print("にゃーん")