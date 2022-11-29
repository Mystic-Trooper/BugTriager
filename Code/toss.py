import operator
toss_data = open('Code/toss_data.txt', 'r')


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
    sorted_d = dict( sorted(mp.items(), key=operator.itemgetter(1),reverse=True))
    sorted_t = dict( sorted(tp.items(), key=operator.itemgetter(1),reverse=True))
    print("no. of tosses")
    for x in sorted_d:
        print(x, " ", sorted_d[x])
    print("total tasks")
    for x in sorted_t:
        print(x, " ", sorted_t[x])
    toss_data.close()
if __name__ == '__main__':
    tosses_more()