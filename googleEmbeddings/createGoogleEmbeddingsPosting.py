import json
import gensim.models.keyedvectors as word2vec
from textParser import parse_txt_to_list
from lyricsmaster import LyricWiki
import os
from os import listdir
from os.path import isfile, join
import textParser


lyric_master_dir_path = "C:\\Users\\yarha\\Desktop\\LyricMaster\\LyricsMaster1\\LyricsMaster"
# path_for_all_songs = "C:\\all_songs\\all_songs.txt"
path_for_google_embd_for_all_songs = "C:\\google_embeddings\\google_embd_vectors.txt"
x = "C:\\LyricsMaster\\LyricsMaster_orig\\A"
provider = LyricWiki()


def create_google_embd_model():
    global model
    model = word2vec.KeyedVectors.load_word2vec_format('../model/GoogleNews-vectors-negative300.bin', binary=True)
    return model



# def create_Google_Embeddings_AVG_Vector_For_All_Songs():
#     f_all_songs = open(path_for_all_songs)
#     for song in f_all_songs:
#         try:
#             song_obj = json.loads(song)
#             song_name = song_obj['songName']
#             song_artist = song_obj['artist']
#             song_lyrics = get_Lyrics_For_A_Song(song_name, song_artist)
#             avg_embeddings_vec = create_Google_Embeddings_AVG_Vector_For_A_Given_Text(song_lyrics)
#             avg_embeddings_vec_obj = {'songName': song_name, 'songArtist': song_artist, 'googleEmbdVector': avg_embeddings_vec}
#             with open(path_for_google_embd_for_all_songs, 'a') as outfile:
#                 json.dump(avg_embeddings_vec_obj, outfile)
#                 outfile.write('\n')
#             print("done")
#         except Exception:
#             pass
#


def create_Google_Embeddings_AVG_Vector_For_A_Given_Text(text,model):
    words_in_model = []
    words_embeddings = []
    sum_vector = []
    for i in range(0, 300):
        sum_vector.append(0);
    text_in_list = parse_txt_to_list(text)
    for word in text_in_list:
        if word in model:
            words_embeddings.append(model[word])
            words_in_model.append(word)
            for i in range(0, 300):
                sum_vector[i] = sum_vector[i] + words_embeddings[0][i]
    for i in range(0, 300):
        sum_vector[i] = sum_vector[i] / len(text_in_list)
    return sum_vector



def get_Lyrics_For_A_Song(song_name, song_artist):
    song_name = song_name.replace(" ", "-")
    song_artist = song_artist.replace(" ", "-")
    artist_path = os.path.join(lyric_master_dir_path, song_artist)
    for albums in os.walk(artist_path):
        for a in range(0, len(albums[1])):
            album_path = os.path.join(artist_path, albums[1][a])
            songs = [f for f in listdir(album_path) if isfile(join(album_path, f))]
            if song_name + ".txt" in songs:
                song_path = os.path.join(album_path, song_name + ".txt") # list.index(song_name + ".txt")))
                return textParser.read_txt(song_path)



#avg_vector = createGoogleEmbeddingAVGVectorForText("hello, I am tired and want to go to food-truck urgentlly")
# create_Google_Embeddings_AVG_Vector_For_All_Songs()
# lyrics = get_Lyrics_For_A_Song("Hard Times", "A")
# print(lyrics)
