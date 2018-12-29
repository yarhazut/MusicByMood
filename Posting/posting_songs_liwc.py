from pathlib import Path
import textParser
import json


#input path to main
def addSongLiwc(path,songName):
    data_folder = Path("C:\songs_after_post_LIWC")
    file_to_open = data_folder / "Songs_Liwc.txt"
    with open(file_to_open, 'a', encoding='utf-8') as file:
        file.write(songName + '$' +'ARRAYLIWC')


def add_song_to_LIWC_posting(path_to_song, song_name, song_artist):

    data_folder = Path("C:\songs_after_post_LIWC")
    file_to_open = data_folder / "Songs_Liwc.txt"
    text = textParser.read_txt(path_to_song)
    liwc_song_dic = textParser.activate_LIWC_algo(text)
    json_object = {'name': song_name, 'artist': song_artist, 'liwc_dic': liwc_song_dic}
    with open(file_to_open, 'w') as outfile:
        json.dump(json_object, outfile)
        print('name  song  was insert')

add_song_to_LIWC_posting('Anywhere-But-Here.txt','Anywhere-But-Here','Finch')
