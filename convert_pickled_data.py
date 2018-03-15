import os
import pickle
import re
import time
import glob
my_files = glob.glob("reviews/*.p")
print(my_files)
file = open("reviews/all"+str(time.time())+".txt","w")
for my_file in my_files:
    raw_review_pages = pickle.load(open(my_file, "rb"))
    os.remove(my_file)
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

