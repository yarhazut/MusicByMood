
def read_txt(file_name):
    with open(file_name, "r") as myfile:
        data = myfile.readlines()
        return ','.join(data)

def parse_txt(text):
    for char in '-.,\n':
        data_str = data_str.replace(char, ' ')
    data_str = data_str.lower()
    return data_str.split() #word_list

def get_word_count(file_name):
    word_count_dic = {}
    text= read_txt(file_name)
    word_list = parse_txt(text)
    for word in word_list:
        word_count_dic[word] = word_count_dic.get(word, 0) + 1
    word_freq = []
    for key, value in word_count_dic.items():
        word_freq.append((value, key))
    word_freq.sort(reverse=True)



