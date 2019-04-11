import json, falcon
from waitress import serve
import requests
import textParser
from Translate.hebrewTranslator import translate_text
from LIWC import LIWC_similarity
from IBMWatson import watson_similarity
from IBMWatson import IBMWatsonMain
from googleEmbeddings.createGoogleEmbeddingsPosting import create_Google_Embeddings_AVG_Vector_For_A_Given_Text,create_google_embd_model
from All_Algo import weighted_similarity
import urllib.request
import sys
from bs4 import BeautifulSoup

# played_song_dict = {}
class ObjRequestClass:
    def on_post(self,req,resp):
        body = req.stream.read()
        str = body.decode("utf-8")
        newStr = json.loads(str);
        tabArray = newStr['tabs'];
        songJson = getSongSelected(tabArray)
        id = getID(songJson['Song'], songJson['artist'])
        content = {
            'SongName': songJson['Song'],
            'url': id, 'SongArtist': songJson['artist']
        }
        resp.body=json.dumps(content);
api=falcon.API()
api.add_route('/test', ObjRequestClass())
google_embd_model = create_google_embd_model()


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
            textFinall = translate_text(text)
            print(text)
        except Exception as e:
            if len(tab)>1:
                print (e)
            pass
    # create text vector/dict for each algorithem
    text_liwc_lic = textParser.activate_LIWC_algo(textFinall)
    ibm_dict = IBMWatsonMain.getIBMVectorFromText(textFinall)
    txt_embd_vec = create_Google_Embeddings_AVG_Vector_For_A_Given_Text(textFinall,google_embd_model)
    song_name, artist = weighted_similarity.get_most_similar_song(text_liwc_lic, ibm_dict, txt_embd_vec)
    print('song: {0}, artist: {1}'.format(song_name, artist))
    return {'Song': song_name, 'artist': artist}


serve(api, host='127.0.0.1', port=5555)