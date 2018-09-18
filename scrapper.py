# from bs4 import BeautifulSoup
# import urllib2
# import re
# hindi_movie_page = 'https://einthusan.tv/movie/results/?find=Year&lang=hindi&page=1&year=2018'
# html_page = urllib2.urlopen(hindi_movie_page)
# soup = BeautifulSoup(html_page, 'html.parser')
# links = []
 
# for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
#     links.append(link.get('href'))
 
# print(links)

import requests
from bs4 import BeautifulSoup
import csv

#base url
url = 'https://einthusan.tv/movie/results/?find=Year&lang=hindi&page=2&year=2017'

#base url to make a complete enthu url of a movie link 
base_enthu_url = 'https://einthusan.tv'

#dictionary object to hold result of scraping
title_and_urls = {} #dictionary

#method take an argument a url and returns number of page in a given year
def getNumberOfPages(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    for div in soup.find_all('div', {"class": "results-info"}):
        p = div.find("p").text
        lenOfPageString = len(p)
        if lenOfPageString == 25:
            num = p[9:11] 
        else:
            num = p[9:12]
        return num.strip()

totalNumberOfPages = getNumberOfPages(url)


for x in range(1,int(totalNumberOfPages)+1):
    url_pages = 'https://einthusan.tv/movie/results/?find=Year&lang=hindi&page=' +str(x)+'&year=2017'
    resp = requests.get(url_pages, timeout=10)
    soup = BeautifulSoup(resp.text, 'lxml')
    for div in soup.find_all('div', {"class": "block2"}):
        a = div.find('a')
        h3 = a.find('h3')
        print(h3,url_pages)
        title_and_urls[h3.text] = base_enthu_url+a.attrs['href']

print(title_and_urls)


with open('dict.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in title_and_urls.items():
       writer.writerow([key, value])