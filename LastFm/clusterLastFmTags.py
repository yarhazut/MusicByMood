from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
import nltk
import json
import gensim
import gensim.models.keyedvectors as word2vec


def createClusters(num_clusters):
    embeddedTag = []
    embeddedTagInGoogle = []
    path = "C:\\Users\yarha\\Desktop\\fileDict.txt"
    with open(path) as outfile:
        data = json.load(outfile)
    tags = [*data["dict_tag"]]
    model = word2vec.KeyedVectors.load_word2vec_format(
        'C:\\Users\\yarha\\PycharmProjects\\untitled\\MusicByMood\\model\\GoogleNews-vectors-negative300.bin',
        binary=True)

    print("model is done")

    for tag in tags:
        if tag in model:
            embeddedTag.append(model[tag])
            embeddedTagInGoogle.append(tag)
    kclusterer = KMeansClusterer(num_clusters, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(embeddedTag, assign_clusters=True)
    print(assigned_clusters)
    # words = list(model.wv.vocab)

    # for i, word in enumerate(embeddedTagInGoogle):
    #     print(word + ":" + str(assigned_clusters[i]))

    # f = open("numOfclustersIs" + str(num_clusters) + ".txt", "w+")
    # for currCluster in range(0, num_clusters):
    #     f.writelines(":\n")
    #     f.writelines("Clusuter:" + str(currCluster) + ":\n")
    #     for j, word in enumerate(embeddedTagInGoogle):
    #         if (assigned_clusters[j] == currCluster):
    #             f.writelines(word + " | ")
    # f.close();

    for currCluster in range(0, num_clusters):
        print("Clusuter:" + str(currCluster) + ":\n")
        for j, word in enumerate(embeddedTagInGoogle):
            if (assigned_clusters[j] == currCluster):
                print(word + " | ")


createClusters(350)

# x=4;
# f = open("numOfclustersIs" + str(x) + ".txt", "w+")
# f.writelines("Clusuter:")
# f.writelines("1" )
# f.close();






