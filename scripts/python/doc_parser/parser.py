#!/usr/bin/python -tt
import csv, re, sys, os, datetime, time

file_list = []
path = "./source_docs/"

for file in [doc for doc in os.listdir(path)
    # Build list of file names in the directory.
    if doc.endswith(".txt")]:
        file_list.append(file)

#setup regular expressions

#dwr: Groundwater Basin Number
p1 = r"Groundwater Basin Number:\s(\d*-\d*(.)\d*)"

#county: County
p2 = r"County:\s(\w*\s\w*\s\w*)"

#surface_area (acres): Surface Area
p3 = r"Surface Area:\s(\b\d[\d,.]*\b)"

#total_storage (acre feet):
p4 = r"total storage capacity.+?(\b\d[\d,.]*\b)|Groundwater Storage Capacity. The total usable storage capacity.+?(\b\d[\d,.]*\b)|Groundwater Storage Capacity. Total storage capacity.+?(\b\d[\d,.]*\b)|Groundwater Storage Capacity. The total storage capacity.+?(\b\d[\d,.]*\b)"

#usable_storage (acre feet):
p5 = r"Groundwater in Storage. The available usable storage.+?(\b\d[\d,.]*\b)|Groundwater in Storage. The usable water in storage.+?(\b\d[\d,.]*\b)"
#total u(s|se)able storage.+?(\n)(\b\d[\d,.]*\b)

# p6 = r"(?i)natural recharge.+?(\b\d[\d,.]*\b)"

data = []

for i in file_list:

    # create placeholder list
    row = ["NULL"] * 5

    print "Processing file: " + path + i

    # Open file
    with open(path + i, "r") as f:

        lines = f.read()

        m1 = re.search(p1,lines,re.S)    
        if m1:
            row.pop(0)
            row.insert(0,m1.group(1))
            
        m2 = re.search(p2,lines,re.S)
        if m2:
            row.pop(1)
            row.insert(1,m2.group(1))

        m3 = re.search(p3,lines,re.S)
        if m3:
            row.pop(2)
            row.insert(2,m3.group(1))

        m4 = re.search(p4,lines,re.S)
        if m4:
            row.pop(3)

            if m4.group(1) != ('' or None):
                row.insert(3,m4.group(1))

            elif m4.group(2) != ('' or None):
                row.insert(3,m4.group(2))

            elif m4.group(3) != ('' or None):
                row.insert(3,m4.group(3))
            
            elif m4.group(4) != ('' or None):
                row.insert(3,m4.group(4))

            # else: row.insert(3,m4.group(3))

        else:
            row.insert(3,"NA")

        m5 = re.search(p5,lines,re.S)
        if m5:
            row.pop(4)
            
            if m5.group(1) != ('' or None):
                row.insert(4,m5.group(1))

            else: row.insert(4,m5.group(2))
    
        else:
            row.insert(4,"NA")

        # m6 = re.search(p6,line,re.S)
        # if m6:
        #     row.pop(5)
        #     row.insert(5,m6.group(1))

    data.append(row)

    with open("./database/b118_extra.csv", "w") as f:
        w = csv.writer(f)
        w.writerow("dwr county surface_area total_storage usable_storage".split())
        w.writerows(data)