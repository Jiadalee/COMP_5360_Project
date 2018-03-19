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
import glob
import statsmodels.formula.api as sm

import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(10000)





def write_my_file(raw_review_pages):
    file = open("reviews/all"+str(time.time())+".txt","w")
    for x in raw_review_pages:
        x = x[0]
        url_i = x[0]
        title = x[1]
        points = x[2]
        description  = x[3]
        taster = x[8]
        primary_info_label = x[4]
        primary_info = x[5]
        secondary_info_label = x[6]
        secondary_info = x[7]
        file.write(str(url_i).replace('\n','').replace('\t',''))
        file.write("\t")
        file.write(str(title).replace('\n','').replace('\t',''))
        file.write("\t")
        file.write(str(points).replace('\n','').replace('\t',''))
        file.write("\t")
        file.write(str(description).replace('\n','').replace('\t',''))
        file.write("\t")
        file.write(str(taster).replace('\n','').replace('\t',''))
        file.write("\t")
        for y,z in zip(primary_info_label,primary_info):
            file.write(str(y).replace('\n','').replace('\t','').replace('<span>','').replace('</span>',''))
            file.write("||||")
            z =str(z).replace('\n','').replace('\t','')
            z =re.sub(r"<.+?>","", z)
            file.write(z)
            file.write("\t")
        for y,z in zip(secondary_info_label,secondary_info):
            y = str(y).replace('\n','').replace('\t','').replace('<span>','').replace('</span>','')
            if y != "User Avg Rating":
                file.write(str(y).replace('\n','').replace('\t','').replace('<span>','').replace('</span>',''))
                file.write("||||")
                z =str(z).replace('\n','').replace('\t','')
                z =re.sub(r"<.+?>","", z)
                file.write(z)
                file.write("\t")
        file.write("\n")

    file.close()


#path = "C:\\Users\\olsen\\Desktop\\COMP_5360_Project\\"
#os.chdir(path)

session = requests.Session()
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}
first_page =6360
last_page = 6369
for i_ii in range(first_page, last_page + 1):
    my_files = glob.glob("bad_urls/*.p")
    if "bad_urls/url_"+str(i_ii)+".p" not in my_files:
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
        try:
            write_my_file(raw_review_pages)
            pickle.dump(bad_reviews_urls, open("bad_urls/url_" + str(i_ii) + ".p", "wb"))
        except:
            print(url_i)
