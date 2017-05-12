import math
import csv
import collections
PATH = 'D:\python_source\DBAD\csv_7_29\sorted\\'
PATH1 = 'D:\python_source\DBAD\csv_7_29\preprocessed\\'
PATH2 = 'D:\python_source\DBAD\csv_7_29\groundtruth\\'
TIMES = '2.'
WINSIZE=10000
LENFILTER=2
times=2
DELAY=0
datamap = {}
index={}
cluster={}
cnum=4
us=[2,3,4,5,6,7,8,9]
#us=[2]
for ui in us:
        cluster[ui]=ui

def calmean(list):
    m=0.0
    for i in list:
        m+=i
    m/=len(list)
    return m

def max(x,y):
    if x>y:
        return x
    else:
        return y
def calmeancorr(ui, uj,delay):
    mx = 0.0
    my = 0.0
    sx = 0
    sy = 0
    for i in index[ui]:
        mx += datamap[ui][i]
    for j in index[uj]:
        my += datamap[uj][j]

    mx /= len(index[ui])
    my /= len(index[uj])

    for i in index[ui]:
        sx += (datamap[ui][i] - mx) * (datamap[ui][i] - mx)
    for j in index[uj]:
        sy += (datamap[uj][j] - my) * (datamap[uj][j] - my)
    denom = math.sqrt(sx * sy)
    sxy = 0
    for i in range(len(index[ui])):
        j = i + delay
        if j < 0 or j >= len(index[ui]) or j >= len(index[uj]):
            continue
        else:
            ti=index[ui][i]
            tj=index[uj][j]
            print(ui,uj,ti,tj)
            sxy += (datamap[ui][ti] - mx) * (datamap[uj][tj] - my)
    r = sxy / denom
    return r
def calmeandtw(X,Y):
    distance={}
    output={}
    xlen=len(X)
    ylen=len(Y)
    #获得欧式距离
    for i in range(xlen):
        if i not in distance:
            distance[i]={}
        for j in range(ylen):
            distance[i][j]=(Y[j]-X[i])*(Y[j]-X[i])
    #初始化output
    for i in range(xlen+1):
        if i not in output:
            output[i]={}
        for j in range(ylen+1):
            output[i][j]=0
    #DP过程
    for i in range(1,xlen+1):
        for j in range(1,ylen+1):
            #print(i,j)
            output[i][j]=min(output[i-1][j-1],output[i][j-1],output[i-1][j])+distance[i-1][j-1]
    dtwd=output[xlen][ylen]
    return dtwd

def debracket(cluster):
    for i in cluster:
        cl_str=str(cluster[i])
        if cl_str.startswith('['):
            cl_str=cl_str.replace('[','')
            cl_str=cl_str.replace(']','')
            cluster[i]=list(eval('['+cl_str+']'))
    return cluster

def readground(num,us):

    groupaffi = {}
    fname=PATH2+str(num)+'_1.txt'
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    i=0
    for line in pline:
        userid=us[i]
        groupaffi[userid]={}
        affi = line.split(' ')
        for j in range(len(us)):
        #for j in us:
            groupaffi[userid][us[j]] = int(affi[j])
        i+=1
#    print(groupaffi)
    pfile.close()
    return groupaffi


def calaccuracy(cluster,ground,us):
    i=0
    j=0
    size=(len(us)*len(us)-len(us))/2
    pos=0
    affi={}
    for ui in us:
        affi[ui]={}
        for uj in us:
            if ui==uj:
                affi[ui][uj]=-1
            affi[ui][uj]=0

    for i in cluster:
        if type(cluster[i])==list:
            for ui in cluster[i]:
                for uj in cluster[i]:
                    if ui!=uj:
                        affi[ui][uj]=1
    print(affi)
    for ui in affi:
        for uj in affi:
            if ui<uj:
                if affi[ui][uj]==ground[ui][uj]:
                    pos+=1
    acc=pos/size
    return acc

def hcluster(dist_matrix,cluster,cnum):

    while len(dist_matrix)>cnum:
        max=-999
        for ci in dist_matrix:
            for cj in dist_matrix:
                if ci==cj:
                    continue
                #print(str(ci)+' '+str(cj))
                if max<dist_matrix[ci][cj]:
                    max=dist_matrix[ci][cj]
                    i=ci
                    j=cj

        s=i
        l=j
        if i>j:
            s=j
            l=i
        #print(str(s)+' '+str(l))
        cluster[s]=[cluster[s],(cluster[l])]
        #print(cluster[s])
        del cluster[l]

        for k in dist_matrix:
            if dist_matrix[s][k]>dist_matrix[l][k]:
                dist_matrix[s][k]=dist_matrix[l][k]
        for r in dist_matrix:
            del dist_matrix[r][l]
        del dist_matrix[l]
    #print(cluster)
    return cluster

def hcluster_d(dist_matrix,cluster,cnum):

    while len(dist_matrix)>cnum:
        min=999999
        #print(cluster)
        #print(dist_matrix)
        for ci in dist_matrix:
            for cj in dist_matrix:
                if ci==cj:
                    continue
                #print(str(ci)+' '+str(cj))
                if min>dist_matrix[ci][cj]:
                    min=dist_matrix[ci][cj]
                    i=ci
                    j=cj

        s=i
        l=j
        if i>j:
            s=j
            l=i
        #print(str(s)+' '+str(l))
        cluster[s]=[cluster[s],(cluster[l])]
        #print(cluster[s])
        del cluster[l]

        for k in dist_matrix:
            if dist_matrix[s][k]>dist_matrix[l][k]:
                dist_matrix[s][k]=dist_matrix[l][k]
        for r in dist_matrix:
            del dist_matrix[r][l]
        del dist_matrix[l]
    #print(cluster)
    return cluster


'''
#此处注释代码用于处理原始数据
#读取数据
#value=[]
for u in us:
    if u not in datamap:
        #datamap[u] = collections.OrderedDict()
        datamap[u]={}
    if u not in index:
        index[u]=[]
    filename = PATH1 + TIMES + str(u) + '_orien.csv'
    csv_data = csv.reader(open(filename), delimiter=',')
    line=0
    for row in csv_data:
        datamap[u][int(row[0])]=float(row[1])
        index[u].append(int(row[0]))
        #value.append(float(row[1]))
    print(index[u][-1])
#预处理数据

datamap1={}
sortedmap={}
for u in us:
    fname=PATH1+TIMES+str(u)+'_mean_orien.csv'
    mfile=open(fname,'w')
    if u not in datamap1:
        #datamap1[u]=collections.OrderedDict()
        datamap1[u]={}
    for t0 in datamap[u]:
        lv=0.0
        rv=0.0
        num=0
        high=t0
        if t0<5000:
            low=0
        else:
            low=t0-5000
        for t in datamap[u]:
            if low<=t<=high:
                lv+=datamap[u][t]
                num+=1
            else:
                continue
        lv/=num
        #print(t0,num)
        #print(t0,low,high)
        num=0

        low=t0
        if t0+5000>=index[u][-1]:
            high=index[u][-1]
        else:
            high=t0+5000
        for t in datamap[u]:
            if low<=t<=high:
                rv+=datamap[u][t]
                num+=1
            else:
                continue
        rv/=num
        #print(t0,num)
        #print(t0,low,high)
        val=lv-rv
        datamap1[u][t0]=lv-rv
    for t in index[u]:
        mfile.write(str(t)+','+str(datamap1[u][t])+'\n')
    print(fname)
    mfile.close()
'''
for u in us:
    if u not in datamap:
        datamap[u] = {}
    filename = PATH1 + TIMES + str(u) + '_mean_orien.csv'
    csv_data = csv.reader(open(filename), delimiter=',')
    for row in csv_data:
        ts=int(int(row[0])/WINSIZE)
        value=float(row[1])
        #print(ts)
        if ts not in datamap[u]:
            datamap[u][ts]=[]
        datamap[u][ts].append(value)
#读取mean数据
#存在窗口丢失情况，因此需要在计算之前确定所有用户窗口情况，求交集
winseq=datamap[us[0]] #winseq表示所有用户存在窗口的序列
for u in us:
    winseq= [val for val in winseq if val in datamap[u]]

corr_matrix={}
fname=PATH2+TIMES+'_mean_corr.txt'
mfile=open(fname,'w')
for ts in winseq:
    corr_matrix[ts]={}
    mfile.write('window='+str(ts)+'\n')
    for ui in us:
        corr_matrix[ts][ui]={}
        for uj in us:
            if ui<uj:
                dij=calmeandtw(datamap[ui][ts],datamap[uj][ts])
                dji=calmeandtw(datamap[uj][ts],datamap[ui][ts])
                corr=max(dij,dji)
            elif ui>uj:
                corr=corr_matrix[ts][uj][ui]
            else:
                corr=1
            corr_matrix[ts][ui][uj]=corr
finalcorr={}
mfile.write('final matrix:'+'\n')

for ui in us:
    if ui not in finalcorr:
        finalcorr[ui]={}
    for uj in us:
        sum=0.0
        for ts in winseq:
            sum+=corr_matrix[ts][ui][uj]
        finalcorr[ui][uj]=sum/len(winseq)
        mfile.write(str(finalcorr[ui][uj])+' ')
        #print(str(finalcorr[ui][uj])+' ')
    mfile.write('\n')
    #print('\n')
cluster=hcluster_d(finalcorr,cluster,cnum)
cluster=debracket(cluster)
mfile.write('\n'+str(cluster)+'\n')
groupaffi=readground(times,us)
accuracy=calaccuracy(cluster,groupaffi,us)
mfile.write('accuracy='+str(accuracy)+'\n')
print(cluster)
print(str(accuracy))
mfile.close()

#计算correlation的mean
'''datamap1={}
for u in us:
    if u not in datamap:
        datamap[u]={}
        datamap1[u]=[]
    if u not in index:
        index[u]=[]
    fname=PATH1+TIMES+str(u)+'_mean_orien.csv'
    csv_data = csv.reader(open(fname), delimiter=',')
    for row in csv_data:

        datamap[u][int(row[0])]=float(row[1])
        datamap1[u].append(float(row[1]))

        index[u].append(int(row[0]))

#print(index)'''



'''corr_matrix={}
fname=PATH2+TIMES+'_mean_corr.txt'
mfile=open(fname,'w')
for ui in us:
    if ui not in corr_matrix:
        corr_matrix[ui]={}
    for uj in us:
        if ui<uj:
            dij=calmeandtw()
            cij=calmeancorr(ui,uj,DELAY)
            cji=calmeancorr(ui,uj,DELAY)
            corr=max(cij,cji)
        elif ui>uj:
            corr=corr_matrix[uj][ui]
        else:
            corr=1
        corr_matrix[ui][uj]=corr
        mfile.write(str(corr)+' ')
    mfile.write('\n')

cluster=debracket(hcluster(corr_matrix,cluster,cnum))
mfile.write('\n'+str(cluster)+'\n')
groupaffi=readground(times,us)
accuracy=calaccuracy(cluster,groupaffi,us)
mfile.write('accuracy='+str(accuracy)+'\n')
print(cluster)
print(str(accuracy))
mfile.close()'''