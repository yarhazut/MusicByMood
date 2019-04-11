import json
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from textParser import parse_txt_to_list
from googleEmbeddings.createGoogleEmbeddingsPosting import get_Lyrics_For_A_Song
import numpy as np


def create_doc2vec_model():
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
    model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
    fname = get_tmpfile("my_doc2vec_model")
    model.save(fname)
    return Doc2Vec.load(fname)

model = create_doc2vec_model()
path_for_all_songs = "C:\\all_songs\\all_songs.txt"
path_for_doc_vectors = "C:\\docToVec\\docToVec_vectors.txt"




def create_Doc2Vec_For_All_Songs():
    f_all_songs = open(path_for_all_songs)
    for song in f_all_songs:
        try:
            song_obj = json.loads(song)
            song_name = song_obj['songName']
            song_artist = song_obj['artist']
            song_lyrics = get_Lyrics_For_A_Song(song_name, song_artist)
            song_list = parse_txt_to_list(song_lyrics)
            myarray = np.asarray(song_list)
            song_doc2vec = model.infer_vector(myarray)
            song_doc2vec_array = song_doc2vec.tolist()
            doc2vec_vec_obj = {'songName': song_name, 'songArtist': song_artist, 'doc2vec': song_doc2vec_array}
            with open(path_for_doc_vectors, 'a') as outfile:
                json.dump(doc2vec_vec_obj, outfile)
                outfile.write('\n')
            print("done")
        except Exception:
            pass


def create_Doc2Vec_For_A_Given_Text(text):
    text_list = parse_txt_to_list(text)
    myarray = np.asarray(text_list)
    text_doc2vec = model.infer_vector(myarray)
    song_doc2vec_array = text_doc2vec.tolist()
    return song_doc2vec_array


create_Doc2Vec_For_A_Given_Text("hello I am yarden and i wand to sleep until as much as possible")

create_Doc2Vec_For_All_Songs()

