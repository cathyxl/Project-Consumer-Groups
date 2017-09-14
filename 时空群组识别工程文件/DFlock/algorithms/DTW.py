import csv,math
import numpy as np
def caldtw(X,Y):
    distance = {}
    output = {}
    xlen = len(X)
    ylen = len(Y)
    # 获得欧式距离
    for i in range(xlen):
        if i not in distance:
            distance[i] = {}
        for j in range(ylen):
            distance[i][j] = (Y[j][0]-X[i][0])**2+(Y[j][1]-X[i][1])**2
    # 初始化output
    for i in range(xlen + 1):
        if i not in output:
            output[i] = {}
        for j in range(ylen + 1):
            output[i][j] = math.inf
    # DP过程
    output[0][0] = 0
    for i in range(1, xlen + 1):
        for j in range(1, ylen + 1):
            # print(i,j)
            output[i][j] = min(output[i - 1][j - 1], output[i][j - 1], output[i - 1][j]) + distance[i - 1][j - 1]
    dtwd = output[xlen][ylen]
    return dtwd

Xmap = {}
Ymap = {}
F = 3
PATH = 'D:\\python_source\\DFlock\\'
file = open(PATH+'data\\process_ATC_1_1200_1.csv', 'r')
xcsv = csv.reader(file, delimiter=',')
for row in xcsv:
    uid = row[1]
    if uid not in Xmap:
        Xmap[uid] = []
    Xmap[uid].append([float(row[2])/1000, float(row[3])/1000])
file.close()


# file = open(PATH+'data\\interpofiles_3\\1_interpolate_ATC_1_1200.csv', 'r')
# ycsv = csv.reader(file, delimiter=',')
# for row in ycsv:
#     uid = row[1]
#     if uid not in Ymap:
#         Ymap[uid] = []
#     Ymap[uid].append([float(row[2]), float(row[3])])
# file.close()
# # print(Ymap)
# # print(caldtw(Xmap['12434701'], Ymap['12434701']))
# for u in Xmap:
#     XList = Xmap[u]
#     YList = Ymap[u]
#     print(u, caldtw(XList, YList))
us = ['12434701', '12432900', '12430301', '12433800', '12432600', '12433000',
      '12430900', '12431000', '12424900', '12401100', '12352600', '12441700',
      '12441601', '12450200', '12450701']

for i in range(8):
    Ymap = {}
    k = i+1
    file = open(PATH + 'data\\interpofiles_3\\'+str(k) + '_interpolate_ATC_1_1200.csv', 'r')
    ycsv = csv.reader(file, delimiter=',')
    for row in ycsv:
        uid = row[1]
        if uid not in Ymap:
            Ymap[uid] = []
        Ymap[uid].append([float(row[2]), float(row[3])])
    file.close()
    for ui in range(len(us)):
        u = us[ui]
        print(u,caldtw(Xmap[u], Ymap[u]))
    # u = us[10]
    # print(k,caldtw(Xmap[u], Ymap[u]))
    # for u in Xmap:
    #     XList = Xmap[u]
    #     YList = Ymap[u]
    #     print(u, caldtw(XList, YList))
