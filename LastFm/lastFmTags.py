import requests
import json
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path
settings.configure()
dict_tag = dict()
def lastfm_tagsOfSongs_search(artist_name,track_name):
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    api_key = 'f43f26a4bc4a14141fedd677d6c4d4df'
    url = api_url+'?method=track.gettoptags&artist=' +artist_name + '&track=' +track_name + '&api_key='+api_key +'&format=json'
    data = requests.get(url)
    return HttpResponse(data.content)
def get_tags_Array(tags):
    my_json = tags.content
    data = json.loads(my_json)
    array = data["toptags"]["tag"]
    for tag in array:
        name = tag["name"]
        print(name)
        if name in dict_tag:
            dict_tag[name]["count"]+=tag["count"]
            dict_tag[name]["songs"]+=1
        else:
            dict_tag[name]={}
            dict_tag[name]["count"]=tag["count"]
            dict_tag[name]["songs"]=1
    return array
songToArtist = dict()
def getNamesOfArtistAndSong():
    data_folder = Path("C:\songs_artists")
    file_to_open = data_folder / "songs_artists_withTag_new.txt"
    data="";
    with open('songs_artists_new.txt', encoding="utf8") as myfile:
        data = myfile.read()
        totalIndex=0;
        splited=data.split("|")
        print (len(splited))
        indexSongs = 0
        for music in splited:
            if ((totalIndex /1000) %2 == 0) :
                print('WE Passed Songs'+str(totalIndex))
            splited2=music.split("$")
            try:
                lastFmTags=lastfm_tagsOfSongs_search(splited2[1],splited2[0]);
                arr=get_tags_Array(lastFmTags)
                if (len(arr)>0):
                    indexSongs = indexSongs+1
                    totalIndex = totalIndex+1;
                    print(indexSongs,totalIndex)
                    with open(file_to_open, 'a', encoding='utf-8') as file:
                        file.write(splited2[0] + '$' + splited2[1] + '|')
            except Exception:
                totalIndex = totalIndex +1
                pass
    return data;
#tags=lastfm_tagsOfSongs_search("A Bullet For Pretty Boy","Voices And Vessels")
dat=getNamesOfArtistAndSong();
#get_tags_Array(tags)
print(len(dict_tag))
exDict = {'dict_tag': dict_tag}

with open('fileDictNew.txt', 'w') as file:
     file.write(json.dumps(exDict))