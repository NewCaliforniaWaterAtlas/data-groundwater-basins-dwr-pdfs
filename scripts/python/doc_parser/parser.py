#!/usr/bin/python
# coding: utf-8
import sys, os, datetime, time, re, codecs

# Create list of files.
file_list = []

# Set path to list of files.
path = "./source_docs/"

# Open file we will write to, replace it with new data.
fout = open("./database/b118_extra.csv", "r+")
fout.seek(0)

# Read each file in the directory.
for file in [doc for doc in os.listdir(path)
	# Build list of file names in the directory.
	if doc.endswith(".txt")]:
	    file_list.append(file)

# Return time file was created.
def modificationDate(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


# Count total records.
totalcount = 0

# Add cleaned up column headers.
header = "DWR_,county,surface_area,total_storage,natural_recharge,filetime"

fout.write(header + '\n')

# Read file list.
for i in file_list:

    print "Processing file: " + path + i

    # Open file
    f = open(path + i, 'r')
    filetime = modificationDate(path + i)

    filecount = 0
    rowcount = 0

    # Read each row, perform cleanup functions.
    for row in f:
        
        # @TODO Properly escape empty files. Deleted no data files from the directory for now.
        if row != '':

        	# Remove whitespace
            # row = row.strip()
    
            # Create placeholder names for columnn header rows.
            if rowcount == 0:
                DWR_ = "DWR_"
                county = "county"
                surface_area = "surface_area"
                total_storage = "total_storage"      
                natural_recharge = "natural_recharge"


            else:

			#ground water basin number: DWR_
			r1 = re.search(r"Groundwater Basin Number:\s(\d*-\d*(.)\d*)", row)

			if r1 == None:
				DWR_ = "null"

			elif r1.group(1) != None:
				DWR_ = r1.group(1)


			#county
			r2 = re.search(r"County:\s(\w*\s\w*\s\w*)", row)

			if r2 == None:
				county = "null"

			elif r2.group(1) != None:
				county = r2.group(1)


			#surface_area
			r3 = re.search(r"Surface Area:\s(\d(,*)\d*)", row)

			if r3 == None:
			  surface_area = "null"

			elif r3.group(1) != None:
				surface_area = r3.group(1)


			#ground water storage capacity: total_storage
			r4 = re.search(r"total storage capacity.+?(\b\d[\d,.]*\b)|total usable groundwater in storage.+?(\b\d[\d,.]*\b)|estimated storage capacity.+?(\b\d[\d,.]*\b)|total usable storage capacity.+?(\b\d[\d,.]*\b)", row)

			if r4 == None:
			  total_storage = "null"

			elif r4.group(1) != None:
				total_storage = r4.group(1)

			elif r4.group(2) != None:
				total_storage = r4.group(2)

			elif r4.group(3) != None:
				total_storage = r4.group(3)

			elif r4.group(4) != None:
				total_storage = r4.group(4)

			elif r4.group(5) != None:
				total_storage = r4.group(5)

			#natural recharge: natural_recharge
			r5 = re.search(r"(?i)natural recharge.+?(\b\d[\d,.]*\b)", row)

			if r5 == None:
				natural_recharge = "null"
			elif r5.group(1) != None:
				natural_recharge = r5.group(1)


            # Build row.
            row = str(DWR_) + "," + county + "," + surface_area + "," + total_storage + "," + natural_recharge + "," + str(filetime)
            
            # Resplit row, clean up columns, add date facets.
            row_nl = row + "\n"

            # Write row to output file.
            if filecount != 0:
                if rowcount != 0:
                    fout.write(row_nl)

            rowcount = rowcount + 1
            totalcount = totalcount + 1
        filecount = filecount + 1

fout.truncate()
fout.close()
print "Done. Processed " + str(totalcount) + " records."

# Then run this
# Convert to geoJSON
# csvjson --lat latitude --lon longitude --k well --crs EPSG:4269 -i 4 ../../database/casgem_timeseries.csv > ../../database/casgem_timeseries.json

sys.exit()