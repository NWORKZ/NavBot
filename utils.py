import re
import json
import csv
import os, sys

def extract_info(base_query,user_query):
	regex = ""
	for query in base_query:
		splitted_base_query = query.split()
		regex += " |".join(splitted_base_query)
		regex += " |"
	
	user_query = re.sub('how to|to go|i ','',user_query)
	user_query = re.sub('to|by|from','-',user_query)
	user_query = re.sub(regex,'',user_query)
	info = user_query.split('-')

	info = [i.lstrip().rstrip() for i in info]	
	info = [i for i in info if i != '']

	return info

def csv_reader(filename):    

    with open(filename, newline='') as csv_file:
        csv_content = csv.reader(csv_file)

        output = [str(o).replace('[','').replace(']','').replace('\'','') for o in csv_content]
    
    return output

def log(data):
	print(data)
	sys.stdout.flush()