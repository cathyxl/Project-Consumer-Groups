import algorithms.CatmullRom as CatmullRom
from model import Position, Flock
import csv,math
import numpy as np
F = 3
PATH = 'D:\\python_source\\DFlock\\'
samplefile = open(PATH+'data\\'+str(F)+'_sample_ATC_1_1200.csv','r')
# interpofile = open(PATH+'data\\interpolate_ATC_1_1200.csv','w')
lines = samplefile.readlines()
nPoints = 25*3
interval = 0.04
samplemap = {}
# interpomap = {}
EXPUSERS = [12352600,12401100,12424900,12430301,12430900,12431000,12432600,12432900,12433000,12433800,12434701,12441601,
            12441700,12450200,12450701]
# EXPUSERS = [12352600,12401100,12431000,12432600,12432900,12433000,12433800,12434701,12441700,12450701]
# EXPUSERS = ['12352600','12401100','12431000','12432600','12432900','12433000','12433800','12434701','12441700','12450701']
# EXPUSERS = ['12352600','12401100','12431000','12432600','12432900','12433000','12433800','12434701']
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

def caltimepoint(t0,T,nPoints,interval):
    T1 = {}
    x = 0
    for ti in range(len(T)-1):
        TS = T[ti]
        TE = T[ti+1]
        if ti not in T1:
            T1[ti] = []
        T1[ti].append(round(TS,3))
        while TS >= t0+x:
            x += interval
        second = t0+x
        T1[ti].append(round(second, 3))
        n = 1
        while second+n*interval < TE:
            T1[ti].append(round(second+n*interval, 3))
            n += 1
        # for ni in range(1, nPoints-1):
        #     T1[ti].append(round(second+ni*interval, 3))
        T1[ti].append(round(TE,3))
    return T1
def getKnotList(Tmap):
    K = {}
    C = 14
    B = 10

    D = 0.1

    T = 4
    averr = 0
    errnum = 0
    for ti in Tmap:
        T = Tmap[ti]
        TS = T[0]
        TE = T[-1]
        if ti not in K:
            K[ti] = []

        for t in T:
            tmpk = round((t-TS)/(TE-TS),3)
            # print(tmpk)
            # averr += 1-tmpk
            # averr += tmpk  # linear
            # averr += math.sin(math.pi*tmpk) # sin
            # averr += -4 * tmpk * (tmpk - 1)  # square

            # averr += - B * math.pow(tmpk, B) + B * math.pow(tmpk, B - 1)
            # averr += - B * math.pow(1-tmpk, B) + B * math.pow(1-tmpk, B - 1)

            # averr += - math.pow(tmpk, C) + tmpk

            # if tmpk < D:
            #     averr += 1/D*tmpk
            # if tmpk > 1-D:
            #     averr += -1/(1-D)*tmpk+1/(1-D)
            # if D <= tmpk <= 1-D:
            #     averr += 1

            # if 0 <= tmpk <= 1/B:
            #     averr += - B * math.pow(1 - tmpk, B) + B * math.pow(1 - tmpk, B - 1)
            # if (B-1)/B <= tmpk <= 1:
            #     averr += - B * math.pow(tmpk, B) + B * math.pow(tmpk, B - 1)
            # if 1/B < tmpk < (B-1)/B:
            #     averr += 0.5

            if tmpk < D:
                averr += 1/D*tmpk
            else:
                averr += -1/(1-D)*tmpk+1/(1-D)

            # averr += -4*math.pow(tmpk,3)+4*tmpk*tmpk
            # if 0.5*math.sin(2*6.28*(tmpk-0.125))+0.5>1:
            #     averr += 1
            # else: averr += 0.5*math.sin(2*6.28*(tmpk-0.125))+0.5
            # averr += 0.5 * math.sin(2 * 6.28 * (tmpk - 0.125)) + 0.5
            # averr += 0.5 * math.sin(4 * 6.28 * (tmpk - 0.0625)) + 0.5
            # if 0.5 * math.sin(5 * 6.28 * (tmpk - 0.048)) + 0.5>1:
            #     averr += 1
            # else: averr += 0.5 * math.sin(5 * 6.28 * (tmpk - 0.048)) + 0.5
            # if tmpk < 1/8:
            #     averr += 8*tmpk
            # if 1/8 <= tmpk < 7/8:
            #     averr += 1
            # if tmpk >= 7/8:
            #     averr += -8*tmpk+8

            # if tmpk < 1/9:
            #     averr += 9*tmpk
            # if 1/9 <= tmpk < 8/9:
            #     averr += 1
            # if tmpk >= 8/9:
            #     averr += -9*tmpk+9

            # if -10*tmpk*(tmpk-1) > 3/4:
            #     if tmpk < 0.5:
            #         averr += 0.6*tmpk+0.7
            #     else:
            #         averr += -0.6*tmpk+1.3
            # else:
            #     averr += -10*tmpk*(tmpk-1)

            # if -10*tmpk*(tmpk-1) > 0.9:
            #     if tmpk < 0.5:
            #         averr += 0.27 * tmpk + 0.87
            #     else:
            #         averr += -0.27 * tmpk + 1.14
            # else:
            #     averr += -10*tmpk*(tmpk-1)


            # if tmpk < 1/2:
            #     averr += 2*tmpk
            # else:
            #     averr += -2*tmpk+2

            # if tmpk < 1/50:
            #     averr += 50*tmpk
            # if 1/50 <= tmpk < 49/50:
            #     averr += 1
            # if tmpk >= 49/50:
            #     averr += -50*tmpk+50

            # if tmpk < 1/45:
            #     averr += 45*tmpk
            # if 1/45 <= tmpk < 44/45:
            #     averr += 1
            # if tmpk >= 44/45:
            #     averr += -45*tmpk+45

            # if tmpk < (2/3):
            #     averr += 1.5*tmpk
            # else:
            #     averr += -3*tmpk+3

            # if tmpk < 1/3:
            #     averr += 3*tmpk
            # else:
            #     averr += -1.5*tmpk+1.5

            # averr += -4*math.pow(tmpk,3)+4*math.pow(tmpk,2) #triple

            # averr += math.exp(-3.14*math.pow(3*(tmpk-0.33)-1/2,2)) # normal

            # averr += -4*tmpk*(tmpk-1) # square

            # averr += abs(math.sin(math.pi*tmpk)) #sin
            errnum += 1
            K[ti].append(tmpk)
    averr /= errnum
    return K, averr

for line in lines:
    fields = line[0:-1].split(',')
    if len(fields) == 0:
        continue
    uid = fields[1]
    ts = float(fields[0])
    if uid not in samplemap:
        samplemap[uid] = {}
    if ts not in samplemap[uid]:
        samplemap[uid][ts] = []
    for i in range(2, 8):
        samplemap[uid][ts].append(float(fields[i]))

# file = open(PATH + 'data\\process_ATC_1_1200_1.csv', 'r')
# xcsv = csv.reader(file, delimiter=',')
# for row in xcsv:
#     uid = row[1]
#     if uid not in Xmap:
#         Xmap[uid] = []
#     Xmap[uid].append([float(row[2]) / 1000, float(row[3]) / 1000])
# file.close()
# n = 0
# while n < nPoints:
#     t0 = float(lines[0].split(',')[0]) + 0.04*n  # 偏移值
#     n += 1
#     # interpofile = open(PATH + 'data\\interpolate_ATC_1_1200.csv', 'w')
#
#     for uid in samplemap:
#         if uid not in interpomap:
#             interpomap[uid] = {}
#         T = []
#         Tmap = {}
#         P = []
#         for ts in samplemap[uid]:
#             T.append(float(ts))
#             row = samplemap[uid][ts]
#             P.append((float(row[0]), float(row[1])))
#         Tmap = caltimepoint(t0, T, nPoints, interval)
#         udata = CatmullRom.CatmullRomChain(P, Tmap, nPoints)
#         interpomap[uid] = list(udata.values())
#
#         # interpomap[uid] = udata
#
#     # "计算存在的所有的ts"
#     # tslist = []
#     # print(interpomap.keys())
#     # for uid in interpomap:
#     #     tss = list(interpomap[uid].keys())
#     #     tslist = list(set(tslist).union(set(tss)))
#     # tslist = sorted(tslist)
#     #
#     # for ts in tslist:
#     #     for uid in interpomap:
#     #         if ts in interpomap[uid]:
#     #             interpofile.write(str(ts) + '000,' + uid + ',' + str(interpomap[uid][ts][0]) + ',' + str(
#     #                 interpomap[uid][ts][1]) + ',0.0,0.0,0.0,0.0\n')
#     # interpofile.close()
#
#     # file = open(PATH + 'data\\interpolate_ATC_1_1200.csv', 'r')
#     # ycsv = csv.reader(file, delimiter=',')
#     # for row in ycsv:
#     #     uid = row[1]
#     #     if uid not in Ymap:
#     #         Ymap[uid] = []
#     #     Ymap[uid].append([float(row[2]) / 1000, float(row[3]) / 1000])
#     # file.close()
#     # print(interpomap)
#     for u in Xmap:
#         XList = Xmap[u]
#         YList = interpomap[u]
#         print(n, u, caldtw(XList, YList))
#     n += 1
n = 0
errlist = []
while n < 8:
    interpomap = {}
    Xmap = {}
    interpopath = PATH + 'data\\interpofiles_'+str(F)+'\\'+str(n+1)+'_'+'interpolate_ATC_1_1200.csv'
    interpofile = open(interpopath, 'w')
    t0 = float(lines[0].split(',')[0]) + 0.005*n  # 偏移值
    for line in lines:
        fields = line[0:-1].split(',')
        if len(fields) == 0:
            continue
        uid = fields[1]
        ts = float(fields[0])
        if uid not in samplemap:
            samplemap[uid] = {}
        if ts not in samplemap[uid]:
            samplemap[uid][ts] = []
        for i in range(2, 8):
            samplemap[uid][ts].append(float(fields[i]))
    print(n)
    avusrerr = 0

    for uid in EXPUSERS:
    # for uid in ['12450701']:
    #     t0 = list(samplemap[uid].keys())[0]+0.03*n
        uid = str(uid)
        if uid not in interpomap:
            interpomap[uid] = {}
        T = []
        Tmap = {}
        P = []
        # print(uid)
        for ts in samplemap[uid]:
            T.append(float(ts))
            row = samplemap[uid][ts]
            P.append((float(row[0]), float(row[1])))
        Tmap = caltimepoint(t0, T, nPoints, interval)

        # print(Tmap)
        "catmull-rom"
        Kmap,averr = getKnotList(Tmap)
        avusrerr += averr
        udata = CatmullRom.CatmullRomChain(P, Tmap, Kmap, nPoints)

        "线性插值"
        # udata = CatmullRom.LineChain(P, Tmap)

        # print(uid, averr)

        interpomap[uid] = udata

    "catmull-rom"
    avusrerr /= len(EXPUSERS)
    print(avusrerr)
    errlist.append(avusrerr)

    "计算存在的所有的ts"
    tslist = []
    for uid in interpomap:
        tss = list(interpomap[uid].keys())
        tslist = list(set(tslist).union(set(tss)))
    tslist = sorted(tslist)

    for ts in tslist:
        for uid in interpomap:
            if ts in interpomap[uid]:
                interpofile.write(str(ts) + '000,' + uid + ',' + str(interpomap[uid][ts][0]) + ',' + str(
                    interpomap[uid][ts][1]) + ',0.0,0.0,0.0,0.0\n')
    interpofile.close()

    # file = open(PATH+'data\\process_ATC_1_1200_1.csv', 'r')
    file = open(interpopath, 'r')
    xcsv = csv.reader(file, delimiter=',')
    for row in xcsv:
        uid = row[1]
        if uid not in Xmap:
            Xmap[uid] = []
        Xmap[uid].append([row[0], float(row[2]), float(row[3])])
        # Xmap[uid].append([row[0], float(row[2])*1000, float(row[3])*1000])
        # Xmap[uid].append([row[0], float(row[2]) / 1000, float(row[3]) / 1000])
    file.close()
    # for uid in Xmap:
    #     # idfile = open(PATH + 'data\\idfiles\\' + uid + '_process.csv', 'w')
    #     idfile = open(PATH + 'data\\idfiles_'+str(F)+'\\' + str(n+1)+'_'+uid + '_linear.csv', 'w')
    #     for ti in range(len(Xmap[uid])):
    #         idfile.write(Xmap[uid][ti][0] + ',' + str(Xmap[uid][ti][1]) + ',' + str(Xmap[uid][ti][2]) + '\n')
    #     idfile.close()
    n += 1

"catmull-rom"
# orilist = [0.67,0,0.17,0.179,0.358,1,0.132,0.085]
orilist = [0.67,0,0.17,0.179,0.359,1,0.132,0.085]
# orilist = [0.489,0,0.489,0.496,0.481,1,0,0.015,0.489]
finalerr = 0.0
maxerr = max(errlist)
minerr = min(errlist)
norlist = []
for err in errlist:
    norlist.append((err-minerr)/(maxerr-minerr))
for i in range(8):
    finalerr += abs(norlist[i]-orilist[i])
finalerr /= 8
print('\n')
for ni in norlist:
    print(ni)
# print(norlist)
print(errlist.index(minerr),minerr)
print(finalerr)

# t0 = float(lines[0].split(',')[0])+0.04 * n # 偏移值
# for line in lines:
#     fields = line[0:-1].split(',')
#     if len(fields) == 0:
#         continue
#     uid = fields[1]
#     ts = float(fields[0])
#     if uid not in samplemap:
#         samplemap[uid] = {}
#     if ts not in samplemap[uid]:
#         samplemap[uid][ts] = []
#     for i in range(2, 8):
#         samplemap[uid][ts].append(float(fields[i]))
#
# for uid in samplemap:
#     if uid not in interpomap:
#         interpomap[uid] = {}
#     T = []
#     Tmap = {}
#     P = []
#     for ts in samplemap[uid]:
#         T.append(float(ts))
#         row = samplemap[uid][ts]
#         P.append((float(row[0]), float(row[1])))
#     Tmap = caltimepoint(t0, T, nPoints, interval)
#     udata = CatmullRom.CatmullRomChain(P,Tmap,nPoints)
#     interpomap[uid] = udata
#
# "计算存在的所有的ts"
# tslist = []
# print(interpomap.keys())
# for uid in interpomap:
#     tss = list(interpomap[uid].keys())
#     tslist = list(set(tslist).union(set(tss)))
# tslist =sorted(tslist)
#
# for ts in tslist:
#     for uid in interpomap:
#         if ts in interpomap[uid]:
#             interpofile.write(str(ts)+'000,'+uid+','+str(interpomap[uid][ts][0])+','+str(interpomap[uid][ts][1])+',0.0,0.0,0.0,0.0\n')
# interpofile.close()
#
# # file = open(PATH+'data\\process_ATC_1_1200_1.csv', 'r')
# file = open(PATH+'data\\interpolate_ATC_1_1200.csv', 'r')
# xcsv = csv.reader(file, delimiter=',')
# for row in xcsv:
#     uid = row[1]
#     if uid not in Xmap:
#         Xmap[uid] = []
#     Xmap[uid].append([row[0], float(row[2]), float(row[3])])
#     # Xmap[uid].append([row[0], float(row[2])*1000, float(row[3])*1000])
#     # Xmap[uid].append([row[0], float(row[2]) / 1000, float(row[3]) / 1000])
# file.close()
# for uid in Xmap:
#     # idfile = open(PATH + 'data\\idfiles\\' + uid + '_process.csv', 'w')
#     idfile = open(PATH + 'data\\idfiles\\' + uid + '_interpo.csv', 'w')
#     for ti in range(len(Xmap[uid])):
#         idfile.write(Xmap[uid][ti][0] + ',' + str(Xmap[uid][ti][1]) + ',' + str(Xmap[uid][ti][2]) + '\n')
#     idfile.close()
#
