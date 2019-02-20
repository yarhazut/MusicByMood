from LIWC import liwcAlgorithm
import textParser
from LIWC import LIWC_similarity

def main_func():
    text = textParser.read_txt('Andy Cohen reveals hes expecting his first child via surrogate.txt')
    text_liwc_lic = textParser.activate_LIWC_algo(text)
    song_name , artist = LIWC_similarity.get_most_similar_song(text_liwc_lic)
    print (song_name)


main_func()