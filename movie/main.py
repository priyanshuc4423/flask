import requests
from bs4 import BeautifulSoup
import sqlite3

conn =sqlite3.connect('movie.db')
c= conn.cursor()

#c.execute('''CREATE TABLE data(id INTEGER PRIMARY KEY,name TEXT,desc TEXT,image TEXT,video TEXT)''')



def getsrc(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text,'html.parser')
    video = soup.select('#server-9 > div.les-content > a')
    return video[0]['player-data']





for i in range(1,26):
    response =requests.get(f'https://123movies.autos/movie/filter/cinema-movies/all/all/all/all/latest/?page={i}')
    soup = BeautifulSoup(response.text,'html.parser')
    movie_links = soup.select(' div.movies-list.movies-list-full > div > a')
    movie_link = [ f"https://123movies.autos{link['href']}"  for link in movie_links]

    imagelinks = soup.select('div.movies-list.movies-list-full > div > a > img')
    imagelink = [ link['data-original'] for link in imagelinks]

    k =0;



    for link in movie_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text,'html.parser')
        name = soup.select('div.mvi-content > div.mvic-desc > h3')[0].text
        desc = soup.select('div.mvic-desc > div.desc')[0].text
        srclink = soup.select('#mv-info > a')
        image = imagelink[k]
        videolink = getsrc(f'https://123movies.autos{srclink[0]["href"]}?ep=0')
        c.execute('''INSERT INTO data(name,desc,image,video) VALUES(?,?,?,?)''',(name,desc,image,videolink))
        k+=1

conn.commit()
conn.close()