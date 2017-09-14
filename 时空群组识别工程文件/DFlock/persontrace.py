import csv
"获取每个人的运动轨迹，目的是用来计算原始轨迹和插值轨迹的差异值"
Xmap = {}
Ymap = {}
PATH = 'D:\\python_source\\DFlock\\'
# file = open(PATH+'data\\process_ATC_1_1200_1.csv', 'r')
file = open(PATH+'data\\interpolate_ATC_1_1200.csv', 'r')
xcsv = csv.reader(file, delimiter=',')
for row in xcsv:
    uid = row[1]
    if uid not in Xmap:
        Xmap[uid] = []
    Xmap[uid].append([row[0], float(row[2]), float(row[3])])
    # Xmap[uid].append([row[0], float(row[2])*1000, float(row[3])*1000])
    # Xmap[uid].append([row[0], float(row[2]) / 1000, float(row[3]) / 1000])
file.close()
for uid in Xmap:
    # idfile = open(PATH + 'data\\idfiles\\' + uid + '_process.csv', 'w')
    idfile = open(PATH + 'data\\idfiles\\' + uid + '_interpo.csv', 'w')
    for ti in range(len(Xmap[uid])):
        idfile.write(Xmap[uid][ti][0] + ',' + str(Xmap[uid][ti][1]) + ',' + str(Xmap[uid][ti][2]) + '\n')
    idfile.close()
