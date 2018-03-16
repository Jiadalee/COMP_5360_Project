import os
import pickle
import re
import time
import glob
import pandas as pd
#path = "C:/Users/Trevor -Workstation/Desktop/git_projects/COMP_5360_Project"
#os.chdir(path)

my_files = glob.glob("reviews/*.txt")
print(my_files)

my_array = []
for my_file in my_files:
    print(my_file)
    file = open(my_file, "r", encoding="utf8")
    i = 0
    for line in file:
        print(i)
        i += 1
        my_array.append(line.split("\t"))
        #print(line)
    file.close()

info_labels = ['Alcohol',
 'Appellation',
 'Bottle Size',
 'Category',
 'Date Published',
 'Designation',
 'Importer',
 'Price',
 'Variety',
 'Winery']

array_of_dic = []
i = 0
for mrow in my_array:
    i += 1
    tel = {'row': i}
    tel['url_i'] = mrow[0]
    tel['title'] = mrow[1]
    tel['points'] = mrow[2]
    tel['description'] = mrow[3]
    tel['taster'] = mrow[4]
    for mcol in mrow:
        if mcol.find("||||")==-1:
            None
        else:
            my_split = mcol.split("||||")
            for info_label in info_labels:
                if my_split[0] == info_label:
                    tel[info_label] = my_split[1]
    array_of_dic.append(tel)


df = pd.DataFrame(array_of_dic)
df.head()

df.to_csv("pandas_data.csv")
