from pathlib import Path
import os
import textParser
from Posting.posting_songs_liwc import add_song_to_LIWC_posting
from IBMWatson.IBMWatsonMain import createPostingIBM
source_path = Path("C:\LyricsMaster1\LyricsMaster")
data_folder = Path("C:\songs_artists")
file_to_open = data_folder / "songs_artists_new.txt"
counter=0
countSongs=0
dict=dict()
for a in source_path.glob("**/*"):
    if a.is_dir():
        newPath= a;
        artist = os.path.basename(a)
        for b in newPath.glob("*/*"):
            if b.is_file():
                print(artist)
                counter = counter + 1
                songName =os.path.basename(b)
                base, ext = os.path.splitext(songName)
                songName=base.replace("-" , " ")
                path= b;
                artist=artist.replace("-" , " ")
                if (not(songName in dict and dict[songName]==artist)):
                    #add_song_to_LIWC_posting(path, songName,artist)
                    #with open(file_to_open, 'a', encoding='utf-8') as file:
                      # file.write(songName + '$' + artist + '|')
                    if countSongs == 65 :
                        print('hey')
                    createPostingIBM(songName,artist,textParser.read_txt(path))
                    dict[songName]=artist
                    countSongs=countSongs+1
                    print(countSongs)
print (len(dict))
print(countSongs)