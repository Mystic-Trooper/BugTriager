import json
from collections import defaultdict
toss_data = open('OutputFiles/toss_data', 'r')
component_file_json_root_key = 'component'
component_file = open('./Dataset/JSON/component.json', encoding="utf8")
component = json.loads(component_file.read())[component_file_json_root_key]


resolution_file_json_root_key= 'resolution'
resolution_file = open('./Dataset/JSON/resolution.json', encoding="utf8")
resolution= json.loads(resolution_file.read())[resolution_file_json_root_key]
def knowledge():
    developer_id= None
    skill_set=set()
    developer_knowledge= defaultdict(set)
    for each in toss_data:
        developer_id= None
        data = each.split(',')
        # check for bugid- data[0] in resolution
        for id in resolution:
            if(id==data[0] and resolution[id][-1]["what"] != ""):
                developer_id= resolution[id][-1]["who"]
        
        # check for components of the resolved id 
        if(developer_id!= None):
            for every in component[data[0]]:
                if(every["who"]== developer_id ):
                    developer_knowledge[developer_id].add(every["what"])
    print(developer_knowledge)       
    
    #print(data[0])
    component_file.close()
    resolution_file.close()

        
knowledge()
