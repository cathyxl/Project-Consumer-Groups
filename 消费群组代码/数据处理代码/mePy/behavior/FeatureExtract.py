import csv,os,math
import numpy as np
from datetime import datetime
from itertools import chain
STYPE = ['accele','angular','magne','orien']
PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'  #PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
NUMUSER = 11
# time=1
# START='2016/12/18 13:58:59.000'
# END='2016/12/18 14:05:00.000'

# time=2
# START='2016/12/18 14:11:59.000'
# END='2016/12/18 14:17:00.000'

# time=3
# START='2016/12/18 14:37:35.000'
# END='2016/12/18 14:49:00.000'

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


def caltimeinterval(s1, s2):
    interval = int(s2[-3:]) - int(s1[-3:])
    time_a = datetime.strptime(s1[0:-4], '%Y/%m/%d %H:%M:%S')
    time_b = datetime.strptime(s2[0:-4], '%Y/%m/%d %H:%M:%S')
    interval += (time_b - time_a).seconds * 1000
    return interval
def sortcsv(filename):
    data = csv.reader(open(PATH+filename), delimiter=',')
    sortedlist = sorted(data, key=lambda x: (x[0]))
    with open(PATH+'sorted\\' + filename, 'w', newline='') as file:
        filewriter = csv.writer(file, delimiter=',')
        for row in sortedlist:
            if row != sortedlist[-1]:
                filewriter.writerow(row)

def fttfeature(number):
    leftpart=number[1:(int(len(number)/2)+1)]
    avg=np.average(leftpart)
    std=np.std(leftpart)
    return avg,std
def maketrainfeature(u,label,ws,src,tar):
    tmpvalues={}
    fftvalues={}

    for i in range(0,4):
        tmpvalues[i]=[]
        fftvalues[i]=[]
    datamap={}
    featurematrix={}

    data=csv.reader(open(src),delimiter=',')
    tempdata={}
    for row in data:
        t=int(int(row[0])*2/ws)  # ??????????
        if t not in tempdata:
            tempdata[t]={}
            for i in range(0,4):
                tempdata[t][i]=[]
        tempdata[t][0].append(float(row[1]))
        tempdata[t][1].append(float(row[2]))
        tempdata[t][2].append(float(row[3]))
        tempdata[t][3].append(float(row[4]))
    tslist=list(tempdata.keys())
    for k in range(len(tslist)-1):
        #print(k)
        ts=tslist[k]
        tsn=tslist[k+1]
        if ts not in datamap:
            datamap[ts]={}
            featurematrix[ts]=[]
            featurematrix[ts].append(u)
            featurematrix[ts].append(label)
            for i in range(0, 4):
                datamap[ts][i] = []
        for j in range(0, 4):
            datamap[ts][j] = list(chain(tempdata[ts][j],tempdata[tsn][j]))
    #print(datamap)
    for ts in datamap:
        for i in range(0,4):
            fftvalues[i]=np.fft.fft(datamap[ts][i])
        for i in range(0,4):
            tmean=np.mean(datamap[ts][i])
            tstd=np.std(datamap[ts][i])
            tmax=np.max(datamap[ts][i])
            tmin=np.min(datamap[ts][i])
            famp = abs(fftvalues[i])
            fmean,fstd=fttfeature(famp)
            minus = (famp - fmean) / (fstd + 1)
            minn=np.asarray(minus ** 3, dtype=float)
            minnn = minus ** 4 - 3
            fskewness = np.mean(minn)
            fkurtoiss = np.mean(minnn)
            featurematrix[ts].append(tmean)
            featurematrix[ts].append(tstd)
            featurematrix[ts].append(tmax)
            featurematrix[ts].append(tmin)
            featurematrix[ts].append(fmean)
            featurematrix[ts].append(fstd)
            featurematrix[ts].append(fskewness)
            featurematrix[ts].append(fkurtoiss)
            tmplist=[tmean,tstd,tmax,tmin,fmean,fstd,fskewness,fkurtoiss]
    for ts in featurematrix:
        s=''
        for i in range(34):
            if i==33:
                s+=str(featurematrix[ts][i])+'\n'
            else:
                s+=str(featurematrix[ts][i])+','
        tar.write(s)

def makefeature(u,label,ws,src,tar):
    lastts=0
    tmpvalues={}
    fftvalues={}

    for i in range(0,4):
        tmpvalues[i]=[]
        fftvalues[i]=[]
    datamap={}
    featurematrix={}
    data=csv.reader(open(src),delimiter=',')
    for row in data:
        ts=int(int(row[0])/ws)

        if ts not in datamap:

            featurematrix[ts]=[]
            featurematrix[ts].append(u)
            featurematrix[ts].append(label)
            datamap[ts]={}
            for i in range(0,4):
                datamap[ts][i] = []

        datamap[ts][0].append(float(row[1]))
        datamap[ts][1].append(float(row[2]))
        datamap[ts][2].append(float(row[3]))
        datamap[ts][3].append(float(row[4]))
    for ts in datamap:
        for i in range(0,4):
            fftvalues[i]=np.fft.fft(datamap[ts][i])
        for i in range(0,4):
            tmean = np.mean(datamap[ts][i])
            tstd = np.std(datamap[ts][i])
            tmax = np.max(datamap[ts][i])
            tmin = np.min(datamap[ts][i])
            famp = abs(fftvalues[i])
            fmean, fstd = fttfeature(famp)
            minus = (famp - fmean) / (fstd + 1)
            minn = np.asarray(minus ** 3, dtype=float)
            minnn = minus ** 4 - 3
            fskewness = np.mean(minn)
            fkurtoiss = np.mean(minnn)
            featurematrix[ts].append(tmean)
            featurematrix[ts].append(tstd)
            featurematrix[ts].append(tmax)
            featurematrix[ts].append(tmin)
            featurematrix[ts].append(fmean)
            featurematrix[ts].append(fstd)
            featurematrix[ts].append(fskewness)
            featurematrix[ts].append(fkurtoiss)
            tmplist=[tmean,tstd,tmax,tmin,fmean,fstd,fskewness,fkurtoiss]
            #print(tmplist)
            #print(tmplist)
            #eaturematrix[ts]+=(tmplist)

    for ts in featurematrix:
        s=''
        for i in range(34):
            if i==33:
                s+=str(featurematrix[ts][i])+'\n'
            else:
                s+=str(featurematrix[ts][i])+','
            '''if i==0:
                continue
            if i==1:
                s+=str(featurematrix[ts][i])+' '
            elif i==33:
                s+=str(i-1)+':'+str(featurematrix[ts][i])+'\n'
                #s+=str(featurematrix[ts][i])+'\n'
            else:
                s+=str(i-1)+':'+str(featurematrix[ts][i])+' '
                #s+=str(featurematrix[ts][i])+' '
            '''
        tar.write(s)

'''    for ts in featurematrix:
        s=''
        for i in range(34):
            if i==33:
                s+=str(featurematrix[ts][i])+'\n'
            else: s+=str(featurematrix[ts][i])+','
        tar.write(s)
'''

#对于不连续的窗口数据
def makedecrefeature(u,label,wn,src,tar):
    tmpvalues = {}
    fftvalues = {}
    tempdata = {}
    for i in range(0, 4):
        tmpvalues[i] = []
        fftvalues[i] = []
    datamap = {}
    featurematrix = {}
    data = csv.reader(open(src), delimiter=',')
    num = wn/2
    t = 0
    for row in data:
        if num == 0:
            num = wn/2
            t += 1
        if t not in tempdata:
            tempdata[t] = {}
            for i in range(0, 4):
                tempdata[t][i] = []
        tempdata[t][0].append(float(row[1]))
        tempdata[t][1].append(float(row[2]))
        tempdata[t][2].append(float(row[3]))
        tempdata[t][3].append(float(row[4]))
        num -= 1

    tslist = list(tempdata.keys())
    for k in range(len(tslist)-1):
        ts = tslist[k]
        tsn = tslist[k+1]
        if ts not in datamap:
            datamap[ts] = {}
            featurematrix[ts] = []
            featurematrix[ts].append(u)
            featurematrix[ts].append(label)
            for i in range(0, 4):
                datamap[ts][i] = []
        for j in range(0, 4):
            datamap[ts][j] = list(chain(tempdata[ts][j], (tempdata[tsn][j])))
    for ts in datamap:
        for i in range(0, 4):
            fftvalues[i] = np.fft.fft(datamap[ts][i])
        for i in range(0, 4):
            tmean = np.mean(datamap[ts][i])
            tstd = np.std(datamap[ts][i])
            tmax = np.max(datamap[ts][i])
            tmin = np.min(datamap[ts][i])
            famp = abs(fftvalues[i])
            fmean,fstd=fttfeature(famp)
            minus = (famp - fmean) / (fstd + 1)
            minn = np.asarray(minus ** 3, dtype=float)
            minnn = minus ** 4 - 3
            fskewness = np.mean(minn)
            fkurtoiss = np.mean(minnn)
            featurematrix[ts].append(tmean)
            featurematrix[ts].append(tstd)
            featurematrix[ts].append(tmax)
            featurematrix[ts].append(tmin)
            featurematrix[ts].append(fmean)
            featurematrix[ts].append(fstd)
            featurematrix[ts].append(fskewness)
            featurematrix[ts].append(fkurtoiss)
    for ts in featurematrix:
        s = ''
        for i in range(34):
            if i == 33:
                s += str(featurematrix[ts][i])+'\n'
            else:
                s += str(featurematrix[ts][i])+','
        tar.write(s)

"获得"
def makeseqfeature(u,ws,src,tar):
    tmpvalues = {}
    fftvalues = {}

    for i in range(0, 4):
        tmpvalues[i] = []
        fftvalues[i] = []
    datamap = {}
    featurematrix = {}
    data = csv.reader(open(src), delimiter=',')
    tempdata = {}
    for row in data:
        t = int(int(row[0])*2/ws)    #???
        if t not in tempdata:
            tempdata[t] = {}
            for i in range(0, 4):
                tempdata[t][i] = []
        tempdata[t][0].append(float(row[1]))
        tempdata[t][1].append(float(row[2]))
        tempdata[t][2].append(float(row[3]))
        tempdata[t][3].append(float(row[4]))
    tslist = list(tempdata.keys())
    for k in range(len(tslist)-1):
        ts = tslist[k]
        tsn = tslist[k+1]
        if ts not in datamap:
            datamap[ts] = {}
            featurematrix[ts] = []
            featurematrix[ts].append(u)
            featurematrix[ts].append(ts)
            for i in range(0, 4):
                datamap[ts][i] = []
        for j in range(0, 4):
            datamap[ts][j] = list(chain(tempdata[ts][j],(tempdata[tsn][j])))
    for ts in datamap:
        for i in range(0, 4):
            fftvalues[i] = np.fft.fft(datamap[ts][i])
        for i in range(0, 4):
            tmean = np.mean(datamap[ts][i])
            tstd = np.std(datamap[ts][i])
            tmax = np.max(datamap[ts][i])
            tmin = np.min(datamap[ts][i])
            famp = abs(fftvalues[i])
            fmean,fstd = fttfeature(famp)
            minus = (famp - fmean) / (fstd + 1)  #????为什么加1
            minn = np.asarray(minus ** 3, dtype=float)
            minnn = minus ** 4 - 3
            fskewness = np.mean(minn)
            fkurtoiss = np.mean(minnn)
            featurematrix[ts].append(tmean)
            featurematrix[ts].append(tstd)
            featurematrix[ts].append(tmax)
            featurematrix[ts].append(tmin)
            featurematrix[ts].append(fmean)
            featurematrix[ts].append(fstd)
            featurematrix[ts].append(fskewness)
            featurematrix[ts].append(fkurtoiss)
            tmplist=[tmean,tstd,tmax,tmin,fmean,fstd,fskewness,fkurtoiss]
            print(tmplist)
            #print(tmplist)
            #eaturematrix[ts]+=(tmplist)

    for ts in featurematrix:
        s = ''
        for i in range(34):
            if i == 33:
                s += str(featurematrix[ts][i])+'\n'
            else:
                s += str(featurematrix[ts][i])+','
            '''if i==0:
                continue
            if i==1:
                s+=str(featurematrix[ts][i])+' '
            elif i==33:
                s+=str(i-1)+':'+str(featurematrix[ts][i])+'\n'
                #s+=str(featurematrix[ts][i])+'\n'
            else:
                s+=str(i-1)+':'+str(featurematrix[ts][i])+' '
                #s+=str(featurematrix[ts][i])+' '
            '''
        tar.write(s)

sensortype = STYPE[0]
time = 3
#tarfile=open(PATH+'processed_feature\\'+str(time)+'_features.csv','a')
WINSIZE = 2000
WINNUM = 32


for t in [1]:     #[3, 4, 7, 10, 11, 12]:
    tarfile = open(PATH+'processed_feature\\'+str(t)+'_features.csv','a')
    for u in [1]:    #range(1,12):
        srcpath = PATH+'composed_data\\'+str(t)+'.'+str(u)+'_'+sensortype+'.csv'
        print(srcpath)
        makeseqfeature(u, WINSIZE, srcpath, tarfile)
    tarfile.close()


# # tarfile=open(PATH+'train_processed\\train_features.csv','a')
# for t in range(1,):
#     for u in range(1,17):
#         srcpath=PATH+'train_processed\\'+str(t)+'.'+str(u)+'_'+sensortype+'.csv'
#         if os.path.exists(srcpath):
#             srcpath=PATH+'processed\\'+'1.'+str(u)+'_'+sensortype+'.csv'
#             print(srcpath)
#             #maketrainfeature(u,t,WINSIZE,srcpath,tarfile)
#             makedecrefeature(u,t,WINNUM,srcpath,tarfile)
# tarfile.close()

#选取数据




"将文件排序"

# for u in range(1,12):
#     for type in STYPE:
#         filename=str(u)+'_'+sensortype+'.csv'
#         sortcsv(filename)


"处理加速度数据得到四维"
# for u in range(1,12):
#     for sensortype in ['accele','orien']:
#         filename=PATH+'sorted\\'+str(u)+'_'+sensortype+'.csv'
#         filewrite=PATH+'processed\\'+str(time)+'.'+str(u)+'_'+sensortype+'.csv'
#         print(filewrite)
#         rfile=open(filename,'r')
#         wfile=open(filewrite,'w')
#         lines=rfile.readlines()
#         for line in lines:
#             fields=line.split(',')
#             if fields[0] < START or fields[0] > END:
#                 continue
#             ts=caltimeinterval(START,fields[0])
#             x=float(fields[1])
#             y=float(fields[2])
#             z=float(fields[3])
#             value=math.sqrt(x*x+y*y+z*z)
#             wfile.write(str(ts)+','+str(value)+','+fields[1]+','+fields[2]+','+fields[3])
#         rfile.close()
#         wfile.close()
