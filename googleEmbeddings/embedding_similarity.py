from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_google_embedding_rate(song_embed, txt_embed):
    song_vec = np.array(song_embed)
    txt_vec = np.array(txt_embed)

    song_vec = song_vec.reshape(1, -1)
    txt_vec = txt_vec.reshape(1, -1)

    return cosine_similarity(song_vec, txt_vec)[0][0]

