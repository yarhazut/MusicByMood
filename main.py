from bs4 import BeautifulSoup
from requests import get
#from PyLyrics import *
from lyricsmaster import LyricWiki, TorController
from pathlib import Path


artists = [];
songs = [];
url_base= 'http://lyrics.wikia.com/wiki/Category:Artists_';
url = 'http://lyrics.wikia.com/wiki/Category:Artists_A';
letterIndx=65;
nextPage="";
discography_folder = 'C:\LyricsMaster';
data_folder = Path("C:\songs_artists")
file_to_open = data_folder / "songs_artists.txt"

#get all artist
while(letterIndx<92):
    while(nextPage is not None):
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        artist_container = html_soup.find_all('a', class_ = 'category-page__member-link')
        nextPage_container= html_soup.find_all('a', class_ = 'category-page__pagination-next wds-button wds-is-secondary')
        if (len(nextPage_container)>0):
            nextPage= nextPage_container[0].attrs['href'];
        else:
            nextPage= None;
        url= nextPage;
        i=0;
        while i < len(artist_container):
            artist= artist_container[i].text;
            if "Category" not in artist:
                artists.append(artist);
                print(artist);
            i=i+1;
    letterIndx = letterIndx + 1;
    letterChr = chr(letterIndx);
    nextPage= url_base+ letterChr;
    url= nextPage;
print(artists)
 # getting album by artist name
provider = LyricWiki();
for artist in artists:
    try:
        discography = provider.get_lyrics(artist)
        discography.save(discography_folder);
        for album in discography:    # album is an Album Object.
            for song in album:
                with open(file_to_open, 'a', encoding='utf-8') as file:
                    file.write(song.title + '$' + artist + '|')
                try:
                # song is a Song Object.
                    x = {
                    'name': song.title,
                    'lyrics': song.lyrics
                    }
                    # songs.append({
                    #      'name': song.title,
                    #     'lyrics': song.lyrics
                    # });
                    #print('Song: ', song.title)
                    #print('Lyrics: ', song.lyrics)
                except Exception as err:
                    pass
            print(len(songs))
        print(len(discography))
    except Exception as err:
        pass

