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
import sys
sys.setrecursionlimit(10000)

#path = "C:\\Users\\olsen\\Desktop\\COMP_5360_Project\\"
#os.chdir(path)

session = requests.Session()
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}
first_page = 1
last_page = 7180
for i_ii in range(first_page, last_page + 1):
    clean_review_urls = pickle.load(open("urls/raw_pages" + str(i_ii) + ".p", "rb"))

    raw_review_pages = []
    bad_reviews_urls = []
    for url_i in clean_review_urls:
        time_from_request = time.time()
        try:
            response = session.get(url_i, headers=HEADERS)
            soup_review_page = BeautifulSoup(response.content, 'html.parser')
            structure_reviews = []

            title = soup_review_page.select(".heading-area .article-title")[0].text
            points = soup_review_page.select(".rating #points")[0].text
            description = soup_review_page.select(".description")[0].text
            primary_info_label = soup_review_page.select(".primary-info .row .info-label span")
            primary_info = soup_review_page.select(".primary-info .row .info")
            secondary_info_label = soup_review_page.select(".secondary-info .row .info-label span")
            secondary_info = soup_review_page.select(".secondary-info .row .info")
            taster = soup_review_page.select(".taster .name")[0].text
            structure_reviews.append([url_i, title, points, description, primary_info_label,
                                      primary_info, secondary_info_label,
                                      secondary_info, taster])
            raw_review_pages.append(structure_reviews)
        except:
            bad_reviews_urls.append(url_i)
        if time.time() - time_from_request < 5:
            time.sleep(5.01 - (time.time() - time_from_request))

    pickle.dump(raw_review_pages, open("reviews/raw_pages" + str(i_ii) + ".p", "wb"))
    pickle.dump(bad_reviews_urls, open("bad_urls/url_" + str(i_ii) + ".p", "wb"))

