import json
import csv
import knowledge


assigned_to_file_json_root_key = 'assigned_to'
assigned_to_file_json_root_key = 'assigned_to'
assigned_to_file = open('../Dataset/JSON/assigned_to.json', encoding="utf8")
# assigned_to_file = open('./Dataset/JSON/assigned_to.json', encoding="utf8")
assigned_to = json.loads(assigned_to_file.read())[
    assigned_to_file_json_root_key]
csv_columns = ['id', 'name']


def devl():
    developer_knowledge = dict()
    for bug_id, assignments in assigned_to.items():
        for data in assignments:
            if data["what"] != None:
                developer_knowledge[data["who"]] = data["what"]

    # print(developer_knowledge)
    dictionary_dev = []
    index = 0
    for key, value in developer_knowledge.items():
        dev = {}
        dev["id"] = key
        dev["name"] = value
        dictionary_dev.append(dev)
        index += 1
    # print(dictionary_dev)
    csv_file = "Names.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dictionary_dev:
                writer.writerow(data)
    except IOError:
        print("I/O error")
devl()
