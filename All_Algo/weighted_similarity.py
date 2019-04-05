from pathlib import Path
import json
from LIWC.LIWC_similarity import create_idx_dic_for_cosin, get_liwc_rate
from IBMWatson.watson_similarity import get_ibm_watson_rate, dict_to_arr
import textParser
from IBMWatson import IBMWatsonMain


# TO DO: add songs that were already played
def get_most_similar_song(txt_after_liwc_dict, txt_after_watson_dict):
    data_folder = Path("C:\songs_after_post_IBM_LIWC")
    data_file = 'all_songs.txt'
    file_to_open = data_folder / data_file

    idx_dic = create_idx_dic_for_cosin()
    text_categories_ibm_arr  = dict_to_arr(txt_after_watson_dict)

    max_rate = 0
    max_song = ''
    max_artist = ''

    f = open(file_to_open)
    for line in f:
        # ---- read song object from file ----
        song_obj = json.loads(line)
        song_name = song_obj['songName']
        song_artist = song_obj['artist']
        liwc_dict = song_obj['liwc_dic']
        ibm_watson_dict = song_obj['watson_dic']

        ibm_watson_categories_arr = dict_to_arr(ibm_watson_dict)

        # ---- get rate for song from each category ----
        watson_rate = get_ibm_watson_rate(ibm_watson_categories_arr, text_categories_ibm_arr)
        liwc_rate = get_liwc_rate(liwc_dict, txt_after_liwc_dict, idx_dic)

        # ---- get weighted rate ----
        weighted_rate = 0.5*watson_rate + 0.5*liwc_rate

        # ---- get max_rate ----
        if weighted_rate > max_rate:
            max_rate = weighted_rate
            max_song = song_name
            max_artist = song_artist

    return max_song, max_artist


# ----to check get_most_similar_song function ---
# with open('Anywhere-But-Here.txt', 'r') as f:
#     txt = f.read().replace('\n', '')
#
# text_liwc_lic = textParser.activate_LIWC_algo(txt)
# ibm_dict = IBMWatsonMain.getIBMVectorFromText(txt)
# print(ibm_dict)
#
# song_name, artist = get_most_similar_song(text_liwc_lic, ibm_dict)
#
# print('song: {0}, artist: {1}'.format(song_name, artist))






