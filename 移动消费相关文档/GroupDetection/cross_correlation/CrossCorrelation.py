import numpy
import math
import csv

PATH = 'D:\python_source\DBAD\csv_7_29\sorted\\'
PATH1 = 'D:\python_source\DBAD\csv_7_29\preprocessed\\'
PATH2 = 'D:\python_source\DBAD\csv_7_29\groundtruth\\'
TIMES = '3.'
times=3
datamap = {}

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

    for ui in affi:
        for uj in affi:
            if ui<uj:
                if affi[ui][uj]==ground[ui][uj]:
                    pos+=1
    acc=pos/size
    return acc


def correlation(X, Y,delay):
    mx = 0.0
    my = 0.0
    sx = 0
    sy = 0
    for i in X:
        mx += X[i]
    for j in Y:
        my += Y[j]
    mx /= len(X)
    my /= len(Y)
    for i in X:
        sx += (X[i] - mx) * (X[i] - mx)
    for j in Y:
        sy += (Y[j] - my) * (Y[j] - my)
    denom = math.sqrt(sx * sy)
#    for delay in range(maxdelay, maxdelay + 1):
    sxy = 0
    for i in X:
        j = i + delay
        if j < 0 or j >= len(X) or j >= len(Y):
            continue
        else:
            sxy += (X[i] - mx) * (Y[j] - my)
    r = sxy / denom
    return r

def hcluster(dist_matrix,cluster,cnum):

    while len(dist_matrix)>cnum:
        max=-999
        #print(cluster)
        #print(dist_matrix)
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







T=125
for t in [2,3,4,5,7,8,9,10]:
    if t not in datamap:
        datamap[t] = {}
    filename = PATH1 + TIMES + str(t) + '_orien.csv'
    csv_data = csv.reader(open(filename), delimiter=',')
    n = 0
    for row in csv_data:
        datamap[t][n] = float(row[1])
        n += 1
datamap1={}
n=0



t = 0
ui = 0
us = [2,3,4,5,7,8,9,10]
cnum=3
cluster={}
n=0

filename=PATH2+TIMES+'_correlation.txt'
corr_file=open(filename,'w')
corr_matrix={}
maxdelay=30
for delay in range(-maxdelay,maxdelay+1,2):

    if delay not in corr_matrix:
        corr_matrix[delay]={}
        corr_file.write('delay='+str(delay)+'\n')
    for ui in us:
        if ui not in corr_matrix[delay]:
            corr_matrix[delay][ui]={}
        for uj in us:
            if ui!=uj:
                corr=correlation(datamap[ui], datamap[uj],delay)
                corr_matrix[delay][ui][uj]=corr
                corr_file.write(str(corr)+'  ')
            else:
                corr_matrix[delay][ui][uj]=1.0
                corr_file.write(str(1.0)+' ')
        corr_file.write('\n')
    corr_file.write('\n')
corr_file.close()

#取较大correlation值使对称
for delay in corr_matrix:
    for ui in corr_matrix[delay]:
        for uj in corr_matrix[delay][ui]:
            if(corr_matrix[delay][ui][uj]>=corr_matrix[delay][uj][ui]):
                corr_matrix[delay][uj][ui]=corr_matrix[delay][ui][uj]
            else:
                corr_matrix[delay][ui][uj]=corr_matrix[delay][uj][ui]


filename=PATH2+TIMES+'_1_symmecorr.txt'
corr_file=open(filename,'w')
for delay in corr_matrix:
    for ui in us:
        cluster[ui]=ui
    corr_file.write('delay='+str(delay)+'\n')
    print('delay='+str(delay))
    #for ui in corr_matrix[delay]:
        #for uj in corr_matrix[delay][ui]:
            #corr_file.write(str(round(corr_matrix[delay][ui][uj],4))+'  ')
        #corr_file.write('\n')
    cluster=hcluster(corr_matrix[delay],cluster,cnum)
    cluster=debracket(cluster)
    corr_file.write(str(cluster)+'\n')
    groupaffi=readground(times,us)
    accuracy=calaccuracy(cluster,groupaffi,us)
    corr_file.write('accuracy='+str(accuracy)+'\n')
    print(cluster)
    print(str(accuracy))
    corr_file.write('\n')
corr_file.close()



'''for ui in us:
    if ui not in corr_matrix:
        corr_matrix[ui]={}
    for uj in us:
        if ui!=uj:
            print(str(us[ui]) + " vs " + str(us[uj]))
            corr_file.write(str(us[ui]) + " vs " + str(us[uj])+': ')
            print(correlation(datamap[us[ui]], datamap[us[uj]]))
            corr=correlation(datamap[us[ui]], datamap[us[uj]])
            corr_matrix[ui][uj]=corr
            corr_file.write(str(corr)+'\n')
        else:
            corr_matrix[ui][uj]=1.0
    corr_file.write('\n')
corr_file.close()'''