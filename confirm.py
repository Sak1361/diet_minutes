import sys,re

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
        data_label = ""
        pattern = "(.*)　(.*)"  #全角スペースで分ける
        pattern2 = "(.*)）(.*)"
        for line in f:
            if line.find('○',0,5) == 0: #○から名前なのでここで取り除く
                try:
                    sep = re.search(pattern,line)
                    if len(sep.group(1)) > 2 or len(sep.group(1)) < 20:
                        line = line.replace(sep.group(1),"")
                        data_label += '\n' + '__label__'+name_list[count] + ', '
                        count += 1
                except AttributeError:
                    try:
                        sep = re.search(pattern2,line)
                        if len(sep.group(1)) > 2 or len(sep.group(1)) < 20:
                            line = line.replace(sep.group(1),"")
                            data_label += '\n' + '__label__'+name_list[count] + ', '
                            count += 1
                    except AttributeError:
                        pass
            line = re_half.sub("", line)
            line = re_full.sub("", line)
            line = re_url.sub("", line)
            line = re_tag.sub("",line)
            line = re_n.sub("", line)
            line = re_space.sub("", line)
            line = re_full2.sub(" ", line)
            line = re_comma.sub(" ",line)
            data_label += line
        return data_label

if __name__ == "__main__":
    year = 1990
    mon = ['01','04','05','06','07','08','09','10']
    while year < 2019:
        for m in mon:
            minutes_p = "all-diet/{0}/{1}-{2}.csv".format(year,year,m)
            name_p = "names/{0}-{1}name.csv".format(year,m)
            try:
                label_data = labeling(minutes_p,name_p)
                with open("label_1990to2018.csv",'a')as f:
                    f.write(label_data)
            except FileNotFoundError:
                pass
        year += 1999999
