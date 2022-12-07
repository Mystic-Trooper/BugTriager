import operator
import csv
toss_data = open('Code/toss_data.txt', 'r')

csv_columns = ['name', 'No of tosses']
def tosses_more():
    l = []
    mp = dict()
    tp=dict()
    for each in toss_data:
        data = each.split()
        for d in data:
            if d not in l:
                l.append(d)
                mp[d] = 1
                tp[d]=1
            else:
                if d != data[-1]:
                    mp[d]+=1
                tp[d]+=1
    dictionary_dev = []
    index = 0
    for key, value in mp.items():
        dev = {}
        dev["name"] = key
        dev["No of tosses"] = value
        dictionary_dev.append(dev)
        index += 1
    # print(dictionary_dev)
    csv_file = "tosses.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dictionary_dev:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    # sorted_d = dict( sorted(mp.items(), key=operator.itemgetter(1),reverse=True))
    # sorted_t = dict( sorted(tp.items(), key=operator.itemgetter(1),reverse=True))
    # print("no. of tosses")
    # for x in sorted_d:
    #     print(x, " ", sorted_d[x])
    # print("total tasks")
    # for x in sorted_t:
    #     print(x, " ", sorted_t[x])
    toss_data.close()
if __name__ == '__main__':
    tosses_more()