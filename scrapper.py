# # import libraries
# import urllib2
# from bs4 import BeautifulSoup
# # specify the url
# hindi_movie_page = 'https://einthusan.tv/movie/results/?find=Year&lang=hindi&page=1&year=2018'
# # query the website and return the html to the variable 'page'
# page = urllib2.urlopen(hindi_movie_page)
# # parse the html using beautiful soup and store in variable 'soup'
# soup = BeautifulSoup(page, 'html.parser')
# # Take out the <div> of name and get its value
# for a in soup.find_all('a', href=True):
#     print "Found the URL:", a['href']



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

base_enthu_url = 'https://einthusan.tv'
title_urls = {} #dictionary
# for x in range(1,6):
url = 'https://einthusan.tv/movie/results/?find=Year&lang=hindi&page=1&year=2018'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
for div in soup.find_all('div', {"class": "block2"}):
    a = div.find('a')
    h3 = a.find('h3')
    title_urls[h3.text] = base_enthu_url+a.attrs['href']
    # urls.append(base_enthu_url+a.attrs['href'])

print(title_urls)


with open('dict.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in title_urls.items():
       writer.writerow([key, value])