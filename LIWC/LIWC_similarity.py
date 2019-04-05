from sklearn.metrics.pairwise import cosine_similarity
import textParser
import numpy as np
from pathlib import Path
import json




def create_idx_dic_for_cosin():
    idx_dic = {}
    f = open('LIWC2007_English100131.dic')
    line = f.readline()
    i = 0
    while '%' not in line:
        line_arr = line.split("\t")
        idx_dic[line_arr[0]] = i
        i = i+1
        line = f.readline()
    f.close()
    return idx_dic


def get_liwc_rate(song_liwc_dic, text_liwc , idx_dic):
    song_vec = fill_vec(song_liwc_dic, idx_dic)
    txt_vec = fill_vec(text_liwc, idx_dic)

    song_vec = song_vec.reshape(1, -1)
    txt_vec = txt_vec.reshape(1, -1)

    return cosine_similarity(song_vec, txt_vec)[0][0]


def fill_vec(some_dic,idx_dic):
    idx_dic_length = len(idx_dic)
    arr = [0]*idx_dic_length
    for key in some_dic:
        arr_idx = idx_dic[str(key)]
        arr[arr_idx] = some_dic[key]
    return np.array(arr)


def get_most_similar_song(text_liwc_dic,played_songs_dict):
    idx_dic = create_idx_dic_for_cosin()
    max_rate = 0
    max_song = ''
    max_artist = ''
    data_folder = Path("C:\songs_after_post_LIWC")
    data_file = 'Songs_Liwc1.txt'
    file_to_open = data_folder / data_file
    # data = []
    with open(file_to_open) as f:
        for line in f:
            json_obj = json.loads(line)
            song_dic = json_obj['liwc_dic']
            song_name = json_obj['name']
            song_artist = json_obj['artist']
            # played_songs_dict form is: <song name,set(artists who played that sing)>
            if song_name in played_songs_dict and song_artist in played_songs_dict[song_name]:
                continue
            rate = get_liwc_rate(song_dic, text_liwc_dic, idx_dic)
            if rate > max_rate:
                max_rate = rate
                max_song = song_name
                max_artist = song_artist


    return max_song, max_artist



