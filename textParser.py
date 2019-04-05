from LIWC import liwcAlgorithm
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')


def read_txt(file_name):
    with open(file_name, "r", encoding="utf8") as myfile:
        data = myfile.readlines()
        return ','.join(data)


def parse_txt_to_list(text):
    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for char in '/\{}$!()-.,\n':
        text = text.replace(char, ' ')
    data_str = text.lower()
    data_arr = data_str.split()
    for i in range(len(data_arr)):
        word = data_arr[i]
        # new_word = ps.stem(word)
        lemm_word = lemmatizer.lemmatize(word)
        stem_wors = ps.stem(lemm_word)
        data_arr[i] = stem_wors
    return data_str.split() #word_list

def activate_LIWC_algo(text):
    word_count_dic = {}
    word_list = parse_txt_to_list(text)
    for word in word_list:
        word_count_dic[word] = word_count_dic.get(word, 0) + 1
    return liwcAlgorithm.map_text_to_liwc_cat(word_count_dic,text)


#activate_LIWC_algo(text)


