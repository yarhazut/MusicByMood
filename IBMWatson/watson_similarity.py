from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pathlib import Path
import json


def dict_to_arr(dict):
    song_vec=[0]*5
    song_vec[0] = dict['sadness']
    song_vec[1] = dict['joy']
    song_vec[2] = dict['fear']
    song_vec[3] = dict['disgust']
    song_vec[4] = dict['anger']
    return song_vec


def get_most_similar_song(text_categories_arr):
    text_categories_arr=dict_to_arr(text_categories_arr)
    max_rate = 0
    max_song = ''
    max_artist = ''
    data_folder = Path("C:\songs_after_post_IBM")
    data_file = 'Songs_Watson.txt'
    file_to_open = data_folder / data_file
    with open(file_to_open) as f:
        for line in f:
            json_obj = json.loads(line)
            json_obj = json.loads(json_obj)
            song_name = json_obj['songName']
            song_artist = json_obj['artist']
            song_categories_arr = dict_to_arr(json_obj)
            rate = get_rate(song_categories_arr, text_categories_arr)
            if rate > max_rate:
                max_rate = rate
                max_song = song_name
                max_artist = song_artist

    return max_song, max_artist


def get_rate(song_categories_arr,text_categories_arr):

    song_vec = np.array(song_categories_arr)
    txt_vec = np.array(text_categories_arr)

    song_vec = song_vec.reshape(1, -1)
    txt_vec = txt_vec.reshape(1, -1)

    return cosine_similarity(song_vec, txt_vec)[0][0]
