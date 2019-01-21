import os,sys,re, MeCab

def labeling(minutes_path,name_path):
    with open(name_path,'r')as F:
        name_list = F.read().split(' ')
    with open(minutes_path,'r')as f:
        re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
        re_full = re.compile(r'[︰-＠]')  # 全角記号
        re_full2 = re.compile(r'[、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ 
        re_comma = re.compile(r'[。]')  # 全角で取り除けなかったやつ
        re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
        re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
        re_n = re.compile(r'\n')  # 改行文字
        re_space = re.compile(r'[\s+]')  #１以上の空白文字
        count = 0
        name_label = ""
        label_data = ""
        for line in f:
            if line.find('○',0,5) == 0 and not name_label: #○から名前なのでここで取り除く
                line, name_label, count = add_label(line,name_list,count)
            elif line.find('○',0,5) == 0 and name_label:
                label_data = wakati(label_data)
                label_data = name_label + label_data
                yield label_data
                label_data = ""
                line, name_label, count = add_label(line,name_list,count)
            if line:
                line = re_half.sub("", line)
                line = re_full.sub("", line)
                line = re_url.sub("", line)
                line = re_tag.sub("",line)
                line = re_n.sub("", line)
                line = re_space.sub("", line)
                line = re_full2.sub(" ", line)
                line = re_comma.sub(" ",line)
                label_data += line

def wakati(words):
    tagger = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    words = tagger.parse(words).strip()
    return words

def add_label(line,name_list,count):
    pattern = "(.*)　(.*)"  #全角スペースで分ける
    pattern2 = "(.*)）(.*)"
    try:
        sep = re.search(pattern,line)
        if len(sep.group(1)) > 2 or len(sep.group(1)) < 20:
            line = line.replace(sep.group(1),"")
            name_label = '__label__'+name_list[count] + ', '
            count += 1
    except AttributeError:
        try:
            sep = re.search(pattern2,line)
            if len(sep.group(1)) > 2 or len(sep.group(1)) < 20:
                line = line.replace(sep.group(1),"")
                name_label = '__label__'+name_list[count] + ', '
                count += 1
        except AttributeError:
            line = ""
    return line,name_label,count


if __name__ == "__main__":
    labeling_data = ""
    year = 1990
    mon = ['01','04','05','06','07','08','09','10']
    while year < 2019:
        for m in mon:
            minutes_p = "all-diet/{0}/{1}-{2}.csv".format(year,year,m)
            name_p = "names/{0}-{1}name.csv".format(year,m)
            if os.path.exists(minutes_p) and os.path.exists(name_p):
                for data in labeling(minutes_p,name_p):
                    labeling_data += data + '\n'
                print(year,m)
        with open("label_1990to2018.csv",'a')as f:
            f.write(labeling_data)
        year += 1
