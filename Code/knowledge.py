import json
import csv
import pandas as pd
from itertools import chain
from collections import Counter
from collections import defaultdict

toss_data = open('Code/toss_withId.txt', 'r')
component_file_json_root_key = 'component'
component_file = open('./Dataset/JSON/component.json', encoding="utf8")
component = json.loads(component_file.read())[component_file_json_root_key]

csv_columns = ['id', 'skills']
resolution_file_json_root_key= 'resolution'
resolution_file = open('./Dataset/JSON/resolution.json', encoding="utf8")
resolution= json.loads(resolution_file.read())[resolution_file_json_root_key]


dev_id_mapping = open("dev_id.csv", "r", encoding="utf8")

# Generating map of username and its id
datareader = csv.reader(dev_id_mapping)
mapOfNameAndId = dict()
rowNo =-1;
for row in datareader:
    rowNo+=1
    if(rowNo%2!=0):
        continue    
    mapOfNameAndId[row[0]]=row[1]


def knowledge():
    developer_id= None
    skill_set=set()
    dictionary_dev = []
    developer_knowledge= defaultdict(set)
    for each in toss_data:
        developer_id= None
        data = each.split(',')
        dev = {}
        # check for bugid- data[0] in resolution
        for id in resolution:
            if(id==data[0] and resolution[id][-1]["what"] != ""):
                developer_id= resolution[id][-1]["who"]
                dev["id"] = developer_id

        # for id in resolution:
        #     if(id==data[0] and resolution[id][-1]["what"] != ""):
        #         developer_id= resolution[id][-1]["who"]
        #         try:
        #             dev["id"] = mapOfNameAndId[developer_id]
        #         except KeyError as k:
        #             continue

        # check for components of the resolved id
        if(developer_id!= None):
            for every in component[data[0]]:
                if(every["who"]== developer_id ):
                    developer_knowledge[developer_id].add(every["what"])
                    skill_set.add(every["what"])
            dev["skills"]= developer_knowledge[developer_id]
        dictionary_dev.append(dev)
    # print(developer_knowledge)
    
    # print(dictionary_dev)
    csv_file = "Developer_data.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dictionary_dev:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    #print(data[0])
   
    component_file.close()
    resolution_file.close()

knowledge()
