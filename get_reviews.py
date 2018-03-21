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

df = pd.read_csv('not_picked.csv')
all_urls = df.x.values.tolist()

box_number = 6


def write_my_file(i, raw_review_pages):
    file = open("reviews/url_" + str(i) + ".txt", "w")
    x = raw_review_pages
    url_i = x[0]
    title = x[1]
    points = x[2]
    description = x[3]
    taster = x[8]
    primary_info_label = x[4]
    primary_info = x[5]
    secondary_info_label = x[6]
    secondary_info = x[7]
    file.write(str(url_i).replace('\n', '').replace('\t', ''))
    file.write("\t")
    file.write(str(title).replace('\n', '').replace('\t', ''))
    file.write("\t")
    file.write(str(points).replace('\n', '').replace('\t', ''))
    file.write("\t")
    file.write(str(description).replace('\n', '').replace('\t', ''))
    file.write("\t")
    file.write(str(taster).replace('\n', '').replace('\t', ''))
    file.write("\t")
    for y, z in zip(primary_info_label, primary_info):
        file.write(str(y).replace('\n', '').replace('\t', '').replace('<span>', '').replace('</span>', ''))
        file.write("||||")
        z = str(z).replace('\n', '').replace('\t', '')
        z = re.sub(r"<.+?>", "", z)
        file.write(z)
        file.write("\t")
    for y, z in zip(secondary_info_label, secondary_info):
        y = str(y).replace('\n', '').replace('\t', '').replace('<span>', '').replace('</span>', '')
        if y != "User Avg Rating":
            file.write(str(y).replace('\n', '').replace('\t', '').replace('<span>', '').replace('</span>', ''))
            file.write("||||")
            z = str(z).replace('\n', '').replace('\t', '')
            z = re.sub(r"<.+?>", "", z)
            file.write(z)
            file.write("\t")
    file.write("\n")
    file.close()  
# path = "C:\\Users\\olsen\\Desktop\\COMP_5360_Project\\"
# os.chdir(path)

session = requests.Session()
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}
first_page = 47600
last_page = 47800
for i_ii in range(first_page, last_page + 1):
    
    time_from_request = time.time()
    my_files = glob.glob("reviews/*.txt")
    if "reviews/url_" + str(i_ii) + ".txt" not in my_files and "reviews\\url_" + str(i_ii) + ".txt" not in my_files :
        url_i = all_urls[i_ii]
        try:
            response = session.get(url_i, headers=HEADERS)
            soup_review_page = BeautifulSoup(response.content, 'html.parser')
            structure_reviews = []
            try:
                title = soup_review_page.select(".heading-area .article-title")[0].text
            except:
                title = None
            try:
                points = soup_review_page.select(".rating #points")[0].text
            except:
                points = None
            try:
                description = soup_review_page.select(".description")[0].text
            except:
                description = None
            try:
                primary_info_label = soup_review_page.select(".primary-info .row .info-label span")
            except:
                primary_info_label = None
            try:
                primary_info = soup_review_page.select(".primary-info .row .info")
            except:
                primary_info = None
            try:
                secondary_info = soup_review_page.select(".secondary-info .row .info")
            except:
                secondary_info = None
            try:
                secondary_info_label = soup_review_page.select(".secondary-info .row .info-label span")
            except:
                secondary_info_label = None
            try:
                taster = soup_review_page.select(".taster .name")[0].text
            except:
                taster = None
            print(i_ii)
            structure_reviews=[url_i, title, points, description, primary_info_label,
                                      primary_info, secondary_info_label,
                                      secondary_info, taster]
            print(i_ii)
            write_my_file(i_ii, structure_reviews)
        except Exception as e:
            print(str(e))
        if time.time() - time_from_request < 5:
            time.sleep(5.01 - (time.time() - time_from_request))
