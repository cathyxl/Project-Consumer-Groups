import csv
PATH = 'D:\\python_source\\DFlock\\data\\'
"获取特定id的数据"
# IDs = []
# idfile = open(PATH+'groupall.txt','r')
# idlines = idfile.readlines()
# for line in idlines:
#     fields = line.split(' ')
#     pid = fields[0]
#     IDs.append(pid)
# print(IDs)
# idfile.close()
#
# readname = PATH+'person_ATC-1_1200.csv'
# writename = PATH+'group_ATC_1_1200.csv'
# filereader = csv.reader(open(readname,'r'), delimiter=',')
# filewriter = csv.writer(open(writename,'w',newline=''),delimiter=',')
# for row in filereader:
#     if row[1] in IDs:
#         filewriter.writerow(row)



def searchGroup(allgroup,curitems):
    flags=len(curitems)*[-1]
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
            if i == 0:
                s = ''
            else:
                s = ';'
            for k in range(len(cluster)):
                if k != 0:
                    s += ','
                s += cluster[k]
            print(s)
            rt_group.write(s)





"得出每个时刻的分组情况"
groups={}
groupdata=open(PATH+'all_group.txt','r')
grouplines=groupdata.readlines()
gi=0
for line in grouplines:
    fields=line[0:-1].split(' ')
    if len(fields)<=1:
        continue
    tmp=[]
    for f in fields:
        tmp.append(f)
    # print(tmp)
    groups[gi]=[]
    groups[gi]=tmp
    gi+=1

for gi in groups:
    # for group in groups[gi]:
    #     print(group)
    print(groups[gi])
# csv_data = csv.reader(open(PATH+'process_ATC_1_1200_1.csv','r'), delimiter=',')
csv_data = csv.reader(open(PATH+'interpolate_ATC_1_1200.csv','r'), delimiter=',')

# rt_group=open(PATH+'realtime_group.txt','w')
rt_group=open(PATH+'realtime_group_interpo.txt','w')
datamap = {}
lastts='-1'
tmp_items=[]
for row in csv_data:
    ts = row[0]
    if ts != lastts:
        if lastts != '-1':
            rt_group.write(lastts+':')
        searchGroup(groups,tmp_items)
        if lastts != '-1':
            rt_group.write('\n')

        tmp_items=[]
    tmp_items.append(row[1])
    lastts = ts


