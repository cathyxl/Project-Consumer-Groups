import time,csv
import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import algorithms.flockdetection as FD
import algorithms.Color as color
from model import Position
PATH = 'D:\\python_source\\DFlock\\'

"参数设置"
typeDistance = 0
minPoints = 2
t0 = 0
gama = 4
delta = 2
theta = 0.4
eps = 1.72
def readOriginFile(filepath):
    pointmatrix = {}
    IDs = []
    csv_data = csv.reader(open(filepath, 'r'), delimiter=',')

    for row in csv_data:
        ts = row[0]
        if ts not in pointmatrix:
            pointmatrix[ts] = []
        uid = row[1]
        if uid not in IDs:
            IDs.append(uid)
        p = Position(uid, float(row[2]) / 1000, float(row[3]) / 1000, float(row[4]) / 1000, float(row[5]) / 1000,
                     row[6], row[7])
        pointmatrix[ts].append(p)
    return pointmatrix,IDs


"读取原始数据"

filepath = PATH + 'data\\process_ATC_1_1200_1.csv'

pointmatrix = {}
csv_data = csv.reader(open(filepath,'r'), delimiter=',')
for row in csv_data:
    ts = row[0]
    if ts not in pointmatrix:
        pointmatrix[ts] = []
    p = Position(row[1], float(row[2])/1000, float(row[3])/1000, float(row[4])/1000, float(row[5])/1000, row[6], row[7])
    pointmatrix[ts].append(p)

"获得参与人员"
IDs = []
groupfile = open(PATH+'data\\group.txt','r')
lines = groupfile.readlines()
for line in lines:
    fields = line.split(' ')
    for i in range(len(fields)):
        pi = int(fields[i])
        if pi not in IDs:
            IDs.append(str(pi))

"初始值设置"
act_flocks = []
pot_flocks = []
curid = 0
colorlist = np.zeros((2,3))
for j in range(3):
    colorlist[0][j] = 1
for j in range(3):
    colorlist[1][j] = 0.9

data = np.zeros((0,0))
lasttype = []
assigned = [0,0,0,0,0,0]
flockmap = {}
cmap = {}
maxid = -2

TSNUM = len(pointmatrix)
WIN = 100
tss = []
for ts in pointmatrix:
    tss.append(ts)
start = 0
end = 0
fig, ax = plt.subplots()
XAXISSIZE = 1000
plt.axis([0, XAXISSIZE, 0, len(IDs)])


def drawFlock1(colorlist, data, column_labels, ax, start):

    my_cmap = colors.ListedColormap(colorlist)
    hmap = plt.pcolormesh(data, cmap=my_cmap,alpha=0.8)
    plt.grid()
    if start > XAXISSIZE:
        plt.axis([start-XAXISSIZE, start, 0, 15])
        # plt.axes().set_xticks([start-XAXISSIZE, start, 100])
    ax.set_yticks(np.arange(data.shape[0])+1, minor=False)
    # ax.set_xticks(100, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    # plt.gca().invert_yaxis()
    plt.colorbar(hmap)
    plt.pause(0.5)

def drawFlock(colorlist, data, column_labels, ax, start):

    my_cmap = colors.ListedColormap(colorlist)
    hmap = plt.pcolormesh(data, cmap=my_cmap,alpha=0.8)
    plt.grid()
    if start > XAXISSIZE:
        plt.axis([start-XAXISSIZE, start, 0, 15])
        # plt.axes().set_xticks([start-XAXISSIZE, start, 100])
    plt.axes().set_yticks(np.arange(data.shape[0])+1, minor=False)
    # ax.set_xticks(100, minor=False)
    plt.axes().set_yticklabels(column_labels, minor=False)
    # plt.gca().invert_yaxis()
    plt.colorbar(hmap)
    plt.pause(0.5)

    "画分组实线"
    # y=[2,6,9,10,11,13,15]
    # for h in y:
    #     x = [0, data.shape[1]+100]
    #     plt.plot(x, [h,h], linewidth=2, color='black')

def combinedata(data,draw_array):
    rowlen = draw_array.shape[0]
    columnlen = data.shape[1] + draw_array.shape[1]
    newdata = np.zeros((rowlen, columnlen))
    for di in range(rowlen):
        for dj in range(columnlen):
            if dj < data.shape[1]:
                newdata[di][dj] = data[di][dj]
            else:
                newdata[di][dj] = draw_array[di][dj-data.shape[1]]
    return newdata

if __name__ == '__main__':
    file = open(PATH + 'data\\test.txt', 'w')
    drawFlock1(colorlist, data, IDs, ax, start)
    while start < TSNUM:
        time.sleep(3)
        pointmap = {}
        end = start + WIN
        if end >= TSNUM:
            end = TSNUM
        for tsi in range(start, end):
            ts = tss[tsi]
            if ts not in pointmap:
                pointmap[ts] = pointmatrix[ts]
        start = end
        "下一次传送数据"
        draw_array, flockmap, act_flocks, pot_flocks, curid = FD.rtFlockDetect(IDs, gama, delta, pointmap, eps,
                                                                               minPoints,
                                                                               typeDistance, theta, act_flocks,
                                                                               pot_flocks,
                                                                               flockmap, curid,0)
        draw_array1 = np.transpose(draw_array)
        data = combinedata(data, draw_array1)
        "获得色彩数组"
        colorlist, lasttype, assigned, cmap, maxid = color.chooseColor(colorlist, draw_array, lasttype, assigned, cmap,
                                                                       maxid)
        for i in range(data.shape[0]):
            file.write(str(list(data[i])) + '\n')
        file.write('\n')
        print(list(colorlist))
        "画图"
        plt.clf()
        drawFlock1(colorlist, data, IDs, ax, start)
    plt.show()

# draw_array,flockmap,act_flocks,pot_flocks = FD.rtFlockDetect(IDs, gama, delta, pointmatrix, eps, minPoints, typeDistance, theta, act_flocks, pot_flocks, flockmap)
# # result = FD.rtFlockDetect(IDs, gama, delta, pointmatrix, eps, minPoints, typeDistance, theta, act_flocks, pot_flocks, flockmap)
# # draw_array.shape = (draw_array.shape[1],draw_array.shape[0])
# draw_array1 = np.transpose(draw_array)
# print(draw_array1)
# data = combinedata(data, draw_array1)
#
#
# "获得色彩数组"
# color_result=color.chooseColor(colorlist,draw_array,lasttype,assigned,cmap)
# colorlist=color_result[0]
# lasttype=color_result[1]
# assigned=color_result[2]
# cmap=color_result[3]
# print(colorlist)
# print(data)
#
# "画图"
# drawFlock(colorlist,data,IDs,ax)

