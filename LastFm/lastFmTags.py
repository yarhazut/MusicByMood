import requests
import json
from django.http import HttpResponse
from django.conf import settings

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
tags=lastfm_tagsOfSongs_search("Rihanna","Love on the Brain")
get_tags_Array(tags)
print(dict_tag)