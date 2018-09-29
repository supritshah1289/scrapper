import requests
from bs4 import BeautifulSoup
import csv
import time
import json

#method takes an argument language and year. It calls url and get's html dom, then it parses it to get total number of pages for a given year and language
def getNumberOfPages(lang, year):
    total_pages_url = 'https://einthusan.tv/movie/results/?find=Year&lang=' +str(lang)+'&year='+str(year)
    resp = requests.get(total_pages_url)
    soup = BeautifulSoup(resp.text, 'lxml')
    for div in soup.find_all('div', {"class": "results-info"}):
        p = div.find("p").text
        lenOfPageString = len(p)
        if lenOfPageString == 25:
            num = p[9:11] 
        else:
            num = p[9:12]
        time.sleep(10)
        return num.strip()

#Method iterated over from year to year and decrements 
#goes to each year and creates a url to be used for scraping to get movie title and url
def getLinksOfPagesByYear(lang,fromYear, toYear):
    listOfUrls = []
    for year in range(fromYear,toYear , -1):
        totalPages = getNumberOfPages(lang, year)
        for page in range(1,int(totalPages)+1):
            url_pages = 'https://einthusan.tv/movie/results/?find=Year&lang='+str(lang)+'&page='+str(page)+'&year='+str(year)
            listOfUrls.append(url_pages)
    return listOfUrls



def scrapeUrlsOfMoviesByPages(language,fromYear, toYear):
    urls = getLinksOfPagesByYear(language, fromYear, toYear)
    movies = []
    try:
        for url in urls:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'lxml')
            for div in soup.find_all('div', {"class": "block2"}):
                    movie = {}
                    a = div.find('a')
                    h3 = a.find('h3')
                    movie['url'] = a.attrs['href']
                    movie['title'] = h3.text
                    movie['year'] = url[-4:]
                    movies.append(movie)
                    time.sleep(10)
    except:
        pass
    return movies


movie = scrapeUrlsOfMoviesByPages('hindi',2016, 1988)
with open('outputfile_test_year.json', 'w') as fout:
    json.dump(movie, fout)