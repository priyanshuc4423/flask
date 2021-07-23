import requests
from bs4 import BeautifulSoup
import lxml

class Getcontent:
    def __init__(self):
        self.response = requests.get('https://www.imdb.com/chart/top/').content

    def newfunction(self):
        self.soup = BeautifulSoup(self.response,'lxml')
        self.movies = self.soup.select('td a')
        return  self.movies




