from pathlib import Path
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from googleEmbeddings.embedding_similarity import get_google_embedding_rate
from LIWC.LIWC_similarity import create_idx_dic_for_cosin, get_liwc_rate
from IBMWatson.watson_similarity import get_ibm_watson_rate, dict_to_arr
from googleEmbeddings.embedding_similarity import get_google_embedding_rate
from googleEmbeddings.createGoogleEmbeddingsPosting import create_Google_Embeddings_AVG_Vector_For_A_Given_Text
from LastFm.lastFmTags import lastfm_tagsOfSongs_search,get_tags_Array,getArtistInfo

import textParser
from IBMWatson import IBMWatsonMain

def get_rate(input_txt_vec, input_song_vec):
    song_vec = np.array(input_song_vec)
    txt_vec = np.array(input_txt_vec)

    song_vec = song_vec.reshape(1, -1)
    txt_vec = txt_vec.reshape(1, -1)

    return cosine_similarity(song_vec, txt_vec)[0][0]

# TO DO: add songs that were already played
def get_most_similar_song(txt_after_liwc_dict, txt_after_watson_dict, txt_embd_vec, txt_doc2vec_vec):
    # data_folder = Path("C:\songs_after_post_LIWC_IBM_EMBD")
    # data_file = 'all_songs_final.txt'
    # file_to_open = data_folder / data_file
    file_to_open = '../all_songs_final_with_doc2vec.txt'

    idx_dic = create_idx_dic_for_cosin()
    text_categories_ibm_arr = dict_to_arr(txt_after_watson_dict)


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
        song_embedding_vec = song_obj['embd_vec']
        song_doc2vec_vec = song_obj['word2vec_vec']

        ibm_watson_categories_arr = dict_to_arr(ibm_watson_dict)

        # ---- get rate for song from each category ----
        watson_rate = get_rate(ibm_watson_categories_arr, text_categories_ibm_arr)
        liwc_rate = get_liwc_rate(liwc_dict, txt_after_liwc_dict, idx_dic)
        embd_rate = get_rate(txt_embd_vec, song_embedding_vec)
        doc2vec_rate = get_rate(txt_doc2vec_vec,song_doc2vec_vec)

        # if song_name == 'Hollywood Hoes':
        #     print('watson_rate:{0} ,liwc_rate:{1}, embd_rate:{2}'.format(watson_rate, liwc_rate, embd_rate))

        # ---- get weighted rate ----
        weighted_rate = 0*watson_rate + 0*liwc_rate+1*embd_rate+1*doc2vec_rate

        # ---- get max_rate ----
        if weighted_rate > max_rate:
            try:
             arr = getArtistInfo(song_artist)
             if (len(arr)>0):
                 if "rap" in arr:
                     weighted_rate = weighted_rate -1
                 if weighted_rate > max_rate:
                     max_rate = weighted_rate
                     max_song = song_name
                     max_artist = song_artist
             else:
                 max_rate = weighted_rate
                 max_song = song_name
                 max_artist = song_artist
            except:
                max_rate = weighted_rate
                max_song = song_name
                max_artist = song_artist

    print (max_rate)
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







