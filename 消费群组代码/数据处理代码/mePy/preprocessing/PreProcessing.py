import csv
import math
from datetime import datetime
import json

NUMFEATURE = 2
datamap = {}

# time=1
# START='2016/12/18 13:58:59.000'
# END='2016/12/18 14:05:00.000'

# time=2
# START='2016/12/18 14:11:59.000'
# END='2016/12/18 14:17:00.000'

time=3
START='2016/12/18 14:37:35.000'
END='2016/12/18 14:49:00.000'

# time=4
# START='2016/12/18 15:04:00.000'
# END='2016/12/18 15:14:14.000'

# time=5
# START='2016/12/18 15:20:59.000'
# END='2016/12/18 15:26:00.000'

# time=6
# START='2016/12/18 15:32:59.000'
# END='2016/12/18 15:38:00.000'

# time=7
# START='2016/12/18 15:46:48.000'
# END='2016/12/18 15:56:37.000'

# time=8
# START='2016/12/18 16:02:59.000'
# END='2016/12/18 16:08:00.000'

# time=9
# START='2016/12/18 16:12:59.000'
# END='2016/12/18 16:18:00.000'

# time=10
# START='2016/12/18 16:27:00.000'
# END='2016/12/18 16:35:29.000'

# time=11
# START='2016/12/18 16:39:27.000'
# END='2016/12/18 16:46:50.000'

# time=12
# START='2016/12/18 17:01:20.000'
# END='2016/12/18 17:16:08.000'

usrs=[1,2,3,4,5,6,7,8,9,10,11]
STYPE = ['accele','angular','magne','orien']
PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'    #'D:\\Consume Group\\experiment\\csv_12_18\\'
down = 1
small = []
big = []
avg = []


def degravity(value):
    alpha=0.8
    gravity=9.81
    gravity=alpha*gravity+(1-alpha)*value
    l_value=value-gravity
    return l_value


def sortcsv(filename):
    data = csv.reader(open(filename), delimiter=',')
    sortedlist = sorted(data, key=lambda x: (x[0]))

    with open(PATH + filename, 'w', newline='') as file:
        filewriter = csv.writer(file, delimiter=',')
        for row in sortedlist:
            if row != sortedlist[-1]:
                filewriter.writerow(row)
    f.close()

def debracket(cluster):
    for i in cluster:
        cl_str=str(cluster[i])
        if cl_str.startswith('['):
            cl_str=cl_str.replace('[','')
            cl_str=cl_str.replace(']','')
            cluster[i]=list(eval('['+cl_str+']'))
    print(cluster)


# 如果日期间隔过大，可能存在溢出的情况
def caltimeinterval(s1, s2):
    interval = int(s2[-3:]) - int(s1[-3:])
    time_a = datetime.strptime(s1[0:-4], '%Y/%m/%d %H:%M:%S')
    time_b = datetime.strptime(s2[0:-4], '%Y/%m/%d %H:%M:%S')
    interval += (time_b - time_a).seconds * 1000
    return interval


# 近似为0
def equalzero(fnum):
    if fnum - 0.0 < math.pow(10, -7):
        return True
    else:
        return False


for fea in range(NUMFEATURE):
    # if fea not in small:
    #     small.append([fea, ''])
    #     big.append([fea, ''])
    for i in range(5):
        if fea == 0:
            avg.append([i, [fea, []]])


# read and transform original data

for i in usrs:
    if i not in datamap:
        datamap[i] = {}
    for feature in range(NUMFEATURE):
        if feature == 0:
            fname = PATH+'sorted\\' + str(i) + '_accele.csv'
        else:
            fname = PATH+'sorted\\' + str(i) + '_orien.csv'
        pfile = open(fname, 'r')
        pline = pfile.readlines()
        j = 0
        for line in pline:
            fields = line.split(',')
            ts = fields[0]
            if ts < START or ts > END:
                continue
            x = float(fields[1])
            y = float(fields[2])
            z = float(fields[3])
            value = []
            if feature == 0:
                value.append(x)
                value.append(y)
                value.append(z)
            else:
                value = x
            # if feature == 0:
            #     if equalzero(x) and equalzero(y) and equalzero(z):
            #         tmp1 = tmp2 = tmp3 = 0.0
            #         for k in range(5):
            #             tmp1 += avg[k][feature][0]
            #             tmp2 += avg[k][feature][1]
            #             tmp3 += avg[k][feature][2]
            #         value = [tmp1 / 5, tmp2 / 5, tmp3 / 5]
            #     else:
            #         value.append(x)
            #         value.append(y)
            #         value.append(z)
            #     j = int(math.fmod(j, 5))
            #     avg[j][feature] = value
            #     j += 1
            # else:
            #     if equalzero(x) and equalzero(y) and equalzero(z):
            #         tmp1 = 0.0
            #         for k in range(5):
            #             tmp1 += avg[k][feature]
            #         value = tmp1 / 5
            #     else:
            #         value = x
            #     j = int(math.fmod(j, 5))
            #     avg[j][feature] = value
            #     j += 1
            if ts not in datamap[i]:
                datamap[i][ts] = []
            for f in range(NUMFEATURE):
                datamap[i][ts].append([])
            datamap[i][ts][feature] = value
'''
        tss = sorted(datamap[i].keys())
        if i == down:
            small[feature] = tss[0]
            big[feature] = tss[-1]
        else:
            print(tss[0])
            print(small[feature])
            if small[feature] < tss[0]:
                small[feature] = tss[0]
            if big[feature] > tss[-1]:
                big[feature] = tss[-1]
    #print(small)
    #print(big)
print(small)
print(big)
'''

#print(datamap)

# write the processed data into files

# tempmap = datamap
# jsonDumpsIndentStr = json.dumps(tempmap, indent=1)
# print("jsonDumpsIndentStr=", jsonDumpsIndentStr)
def calMultiAccele(tempmap):
    res = math.sqrt(tempmap[0] ** 2 +
                    tempmap[1] ** 2 +
                    tempmap[2] ** 2)
    return res

for i in usrs:
    for f1 in range(NUMFEATURE):
        if f1 == 0:
            fout = PATH+'dbad_processed\\' + str(time) + '.' + str(i) + '_accele.csv'
        else:
            fout = PATH+'dbad_processed\\'+ str(time) + '.' + str(i) + '_orien.csv'
        print(fout)
        pout = open(fout, 'w')
        tss = sorted(datamap[i].keys())
        print(len(tss))
        for ts in tss:
            if ts >= START and ts <= END and datamap[i][ts][f1] != []:
                if f1 == 0:
                    pout.write(str(caltimeinterval(START, ts)) + ',' +
                               str(calMultiAccele(datamap[i][ts][f1])) + ',' +
                               str(datamap[i][ts][f1][0]) + ',' +
                               str(datamap[i][ts][f1][1]) + ',' +
                               str(datamap[i][ts][f1][2]) + '\n')
                else:
                    pout.write(str(caltimeinterval(START, ts)) + ',' + str(datamap[i][ts][f1]) + '\n')


'''
        for ts in tss:
            if ts >= small[f1] and ts <= big[f1] and datamap[i][ts][f1] != []:
                if f1 == 0:
                    pout.write(str(caltimeinterval(small[f1], ts)) + ',' + str(datamap[i][ts][f1][0]) + ','+
                               str(datamap[i][ts][f1][1]) + ',' + str(datamap[i][ts][f1][2]) + '\n')
                else:
                    pout.write(str(caltimeinterval(small[f1], ts)) + ',' + str(datamap[i][ts][f1]) + '\n')
'''