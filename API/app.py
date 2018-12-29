import json,falcon,requests
from waitress import serve
from bs4 import BeautifulSoup
class ObjRequestClass:
    def on_post(self,req,resp):
        id=getID()
        content={
          'SongName' : 'Nir Is The King',
          'url' : id
        }
        body = req.stream.read()
        resp.body=json.dumps(content);
api=falcon.API()
api.add_route('/test',ObjRequestClass())
def getID():
    Song = 'one day'
    artist = 'assaf avidan'
    resp = requests.get("https://www.youtube.com/results?search_query=" + Song + "+" + artist)
    soup = BeautifulSoup(resp.text)
    tags = soup.findAll("div", class_="yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix")
    firstTag='false'
    for tag in tags:
        if (firstTag=='false'):
            firstTag=tag.get('data-context-item-id')
    return firstTag
serve(api, host='127.0.0.1', port=5555)