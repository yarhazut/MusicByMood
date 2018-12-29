from LIWC import liwcAlgorithm

def read_txt(file_name):
    with open(file_name, "r") as myfile:
        data = myfile.readlines()
        return ','.join(data)

def parse_txt_to_list(text):
    for char in '-.,\n':
        text = text.replace(char, ' ')
    data_str = text.lower()
    return data_str.split() #word_list

def activate_LIWC_algo(text):
    word_count_dic = {}
    word_list = parse_txt_to_list(text)
    for word in word_list:
        word_count_dic[word] = word_count_dic.get(word, 0) + 1
    return liwcAlgorithm.map_text_to_liwc_cat(word_count_dic,text)

#text=read_txt('cnn_articles/helth/Chronic fatigue syndrome may be due to an overactive immune system, study finds.txt')
#activate_LIWC_algo(text)


