# imports and setup
from bs4 import BeautifulSoup
# you can use either of these libraries to get html from a website
import requests
import urllib.request

import pickle
import re
import time

import pandas as pd
import scipy as sc
import numpy as np

import statsmodels.formula.api as sm

import matplotlib.pyplot as plt

session = requests.Session()
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}
first_page = 1
last_page = 7180
results_url = "https://www.winemag.com/?s=&drink_type=wine&price=1.0-15.99,16.0-25.99,100.0-199.99,76.0-99.99,61.0-75.99,41.0-60.99,26.0-40.99,200.0-*&page="
raw_pages = []
for i in range(first_page, last_page + 1 ):
    time_from_request = time.time()
    url = results_url + str(i)
    print(i)
    response = session.get(url, headers=HEADERS)
    my_page = BeautifulSoup(response.content, 'html.parser')
    raw_review_urls = [ review.get("href") for review in my_page.select(".review-item a")]
    clean_review_urls = [ my_url for my_url in raw_review_urls  if   bool(re.search(r'^https://www.winemag.com/buying-guide/', my_url))]
    pickle.dump( clean_review_urls, open( "urls/raw_pages"+str(i)+".p", "wb" ) )
    if time.time() - time_from_request < 5:
        time.sleep(5.01 - (time.time() - time_from_request))

