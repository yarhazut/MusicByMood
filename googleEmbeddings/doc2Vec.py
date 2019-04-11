from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_google_embedding_rate(song_embed, txt_embed):
    song_vec = np.array(song_embed)
    txt_vec = np.array(txt_embed)

    song_vec = song_vec.reshape(1, -1)
    txt_vec = txt_vec.reshape(1, -1)

    return cosine_similarity(song_vec, txt_vec)[0][0]

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
fname = get_tmpfile("my_doc2vec_model")
model.save(fname)
model = Doc2Vec.load(fname)

vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forest', 'fires'])
sim = get_google_embedding_rate(vector, vector);
print(sim);

vector1 = model.infer_vector(['hello', 'I', 'Like', 'beach', 'and', 'surfing'])
vector2 = model.infer_vector(['the', 'sand', 'is', 'soft', 'sun', 'is', 'great', 'weather', 'hot', 'vocation'])
sim1 = get_google_embedding_rate(vector1, vector2);
print(sim1);


print("hello")