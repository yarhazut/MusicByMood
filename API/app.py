import json, falcon
from waitress import serve
import requests
import textParser
from Translate.hebrewTranslator import translate_text
from LIWC import LIWC_similarity
from IBMWatson import watson_similarity
from IBMWatson import IBMWatsonMain
from googleEmbeddings.createGoogleEmbeddingsPosting import create_Google_Embeddings_AVG_Vector_For_A_Given_Text,create_google_embd_model
from googleEmbeddings.doc2Vec import create_Doc2Vec_For_A_Given_Text
from All_Algo import weighted_similarity
import urllib.request
import sys
from bs4 import BeautifulSoup
import traceback
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
    for tab_url in tabArray:
        try:
            page = requests.get(tab_url)
            html_bytes = page.content
            soup = BeautifulSoup(html_bytes, 'html.parser')
            result_set = soup.find_all('p')
            result_set_list = list(result_set)
            final_txt = ''
            for tag in result_set_list:
                txt = tag.text
                final_txt += ' ' + txt

            textFinall = translate_text(final_txt)
            print(textFinall)
        except Exception as e:
            if len(tab_url)>1:
                traceback.print_exc()
                print (e)
            pass
    # create text vector/dict for each algorithem
    text_liwc_lic = textParser.activate_LIWC_algo(textFinall)
    ibm_dict = IBMWatsonMain.getIBMVectorFromText(textFinall)
    txt_embd_vec = create_Google_Embeddings_AVG_Vector_For_A_Given_Text(textFinall,google_embd_model)
    txt_doc2vec_vec = create_Doc2Vec_For_A_Given_Text(textFinall)
    song_name, artist = weighted_similarity.get_most_similar_song(text_liwc_lic, ibm_dict, txt_embd_vec)
    print('song: {0}, artist: {1}'.format(song_name, artist))
    return {'Song': song_name, 'artist': artist}


serve(api, host='127.0.0.1', port=5555)