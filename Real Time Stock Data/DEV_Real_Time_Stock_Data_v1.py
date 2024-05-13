import pandas as pd
import datetime
import requests
from requests .exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', ('class': class_path))
    try:
        spdns = web content div(e].flind all('span')
        text = [spdns.get_text() for span in spans]



def real time price(stock code):
    url = 

    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'Ixml')
        texts = web_content_div(web_content, class_path),

