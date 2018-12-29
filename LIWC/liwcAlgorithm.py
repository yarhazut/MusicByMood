import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

subject_To_Index = dict()
names_toSujectIndex=dict()
# you may also want to remove whitespace characters like `\n` at the end of each line
def open_LIWC_file():
    liwc_content = ''
    with open('LIWC2007_English100131.dic') as f:
        liwc_content = f.readlines()
        content = [x.strip() for x in liwc_content]
    return content

def map_text_to_liwc_cat(word_frec_dic,text):
    text_length=len(text)
    liwc_content=open_LIWC_file()
    liwc_part_1 = 'true'
    for line in liwc_content:
        if (liwc_part_1=='true' and line != '%'):
            lines = line.split("\t")
            subject_To_Index[lines[0]] = lines[1]
        elif(line != '%'):
            lines = re.split('\t|( )',line)
            lines = [x for x in lines if x is not None]
            myarray = np.asarray(lines)
            lines[0] = lines[0].replace('*', '')
            names_toSujectIndex[lines[0]] = myarray[1:len(myarray)]
        if (line == '%'):
            liwc_part_1 = 'false'
    buckets = {}
    for word in word_frec_dic:
        if (word in names_toSujectIndex):
            subjects = names_toSujectIndex[word.lower()]
            for subject in subjects:
                if int(subject) in buckets:
                    buckets[int(subject)] += word_frec_dic[word]
                else:
                    buckets[int(subject)] = word_frec_dic[word]
    for subject in buckets:
        buckets[subject] = format(buckets[subject]/text_length, '.4f')

    return buckets