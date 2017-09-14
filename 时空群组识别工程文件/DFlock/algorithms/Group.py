import csv
'''

'''
PATH = 'D:\\python_source\\DFlock\\data\\'

def searchGroup(clusters,allgroup,curitems):
    flags = len(curitems)*[-1]
    for i in range(len(curitems)):
        if flags[i] == 0:
            continue
        else:
            item=curitems[i]
            cluster = []
            cluster.append(item)
            flags[i] = 0

            for gi in allgroup:
                group=allgroup[gi]
                if item in group:
                    for j in range(i,len(curitems)):
                        if flags[j]==0:
                            continue
                        else:
                            other=curitems[j]
                            if other in group:
                                cluster.append(other)
                                flags[j]=0
            if len(cluster)>1:
                clusters.append(cluster)

def getRtGroup(datafile):
    groups = {}
    groupdata = open(PATH + 'all_group.txt', 'r')
    grouplines = groupdata.readlines()
    gi = 0
    for line in grouplines:
        fields = line[0:-1].split(' ')
        if len(fields) <= 1:
            continue
        tmp = []
        for fd in fields:
            tmp.append(fd)
        groups[gi] = []
        groups[gi] = tmp
        gi += 1
    csv_data = csv.reader(open(datafile, 'r'), delimiter=',')


    tmp_items = []
    groupmap={}
    lastts='-1'
    for row in csv_data:
        ts = row[0]
        if ts not in groupmap:
            groupmap[ts]=[]
            if lastts!='-1':
                searchGroup(groupmap[lastts],groups,tmp_items)
            tmp_items=[]
        tmp_items.append(row[1])
        lastts=ts
    searchGroup(groupmap[lastts], groups, tmp_items)
    return groupmap
