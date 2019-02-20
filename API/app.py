import json,falcon,requests
from waitress import serve
import requests
import textParser
from LIWC import LIWC_similarity
from IBMWatson import watson_similarity
from IBMWatson import IBMWatsonMain
from bs4 import BeautifulSoup
import urllib.request
import sys
from bs4 import BeautifulSoup
class ObjRequestClass:
    def on_post(self,req,resp):
        body = req.stream.read()
        str = body.decode("utf-8")
        tabArray = str.split('\"')
        songJson = getSongSelected(tabArray)
        id=getID(songJson['Song'],songJson['artist'])
        content={
          'SongName' : songJson['Song'],
          'url' : id
        }
        resp.body=json.dumps(content);
api=falcon.API()
api.add_route('/test',ObjRequestClass())
def getID(Song,artist):
    resp = requests.get("https://www.youtube.com/results?search_query=" + Song + "+" + artist)
    soup = BeautifulSoup(resp.text,features="lxml")
    tags = soup.findAll("div", class_="yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix")
    firstTag='false'
    for tag in tags:
        if (firstTag=='false'):
            firstTag=tag.get('data-context-item-id')
    return firstTag


def getSongSelected(tabArray):
    returnTo={}
    textFinall=''
    for tab in tabArray:
        try:
            html = requests.get(tab)
            soup = BeautifulSoup(html.content)
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            splitted = text.split()
            text=" ".join(splitted[50:440])
            textFinall = text
            print(text)
        except Exception:
            pass
    text_liwc_lic = textParser.activate_LIWC_algo(textFinall)
    dic=IBMWatsonMain.getIBMVectorFromText(textFinall)
    print(dic)
    song_name1, artist1=watson_similarity.get_most_similar_song(IBMWatsonMain.getIBMVectorFromText(textFinall))
    song_name, artist = LIWC_similarity.get_most_similar_song(text_liwc_lic)
    returnTo['Song'] = song_name1
    returnTo['artist'] = artist1
    print(song_name,artist)
   # print(song_name1, artist1)
    return returnTo

serve(api, host='127.0.0.1', port=5555)