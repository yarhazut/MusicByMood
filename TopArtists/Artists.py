from bs4 import BeautifulSoup
from requests import get
def getTopArtist():
    artist=set()
    year = 2018
    index = 1
    topArtists='/top-artists'
    while index<5:
        url="https://www.billboard.com/charts/year-end/"+str(year)+topArtists
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        artist_container = html_soup.find_all('article', class_ = 'ye-chart-item')
        for i in range(len(artist_container)):
            text=artist_container[i].text.split("\n")
            text = filter(None, text)
            text = list(filter(None, text))
            if (text[1] not in artist):
                artist.add(text[1])
        index = index+ 1
        year = year - 1
    return artist
