import requests
from bs4 import BeautifulSoup

# get code and build BeautifulSoup object
def runBeautifulSoup(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    return soup