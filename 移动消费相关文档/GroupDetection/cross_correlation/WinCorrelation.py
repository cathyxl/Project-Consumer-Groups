import math
import csv
import algorithms.DBSCAN as DBSCAN
import algorithms.DJcluster as DjCluster
import algorithms.Accuracy as Accuracy
import utils.util as util
PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
WINSIZE = 15000
LENFILTER = 1
DELAY = 0
cluster = {}
TYPE = 1


# GROUNDTRUTH = 1
# us=[1,2,3,4,5,6,7,8,9]
# cluster_o={1:[1,2,3,4,5],2:[6,7,8,9]}

# GROUNDTRUTH = 2
# us=[1,2,3,4,5,9,10]
# cluster_o={1:[1,2,3,4,5],2:[9,10]}

# GROUNDTRUTH = 3
# us=[1,2,3,4,5,6,7,8,9]
# cluster_o={1:[1,2,3,4,5],2:[6,7,8,9]}

# GROUNDTRUTH = 4
# us=[1,2,3,4,5,6,7,9]
# cluster_o={1:[1,2,3,4,5],2:[6,7,9]}

# GROUNDTRUTH = 5
# us=[1,2,3,4,5,6,7,8,9]
# cluster_o={1:[1,2,3,4],2:[5,6,7,8],3:[9]}

# GROUNDTRUTH = 6
# us=[1,2,5,8,9,10]
# cluster_o={1:[1,2],2:[5,8],3:[9,10]}

GROUNDTRUTH = 7
us=[1,2,3,4,5,6,7,9,11]
cluster_o={1:[1,2,3,4],2:[5,6,7],3:[9,11]}

# GROUNDTRUTH = 8
# us=[1,2,3,4,5,6,7,9,11]
# cluster_o={1:[1,2],2:[3,4],3:[5,6,7],4:[9,11]}

# GROUNDTRUTH = 9
# us=[1,2,5,9,10,11]
# cluster_o={1:[1,2],2:[5],3:[9,10,11]}

# GROUNDTRUTH = 10
# us=[1,2,3,4,5,6,7,8,9,11]
# cluster_o={1:[1,2],2:[3,4],3:[5,6,7],4:[8,9,11]}

# GROUNDTRUTH = 11
# us=[1,2,3,4,5,6,7,9,11]
# cluster_o={1:[1,2,3,4],2:[5,6,7],3:[9,11]}

# cluster_o={1:[1,2,3,6],2:[8,10,11]}
# cluster_o={1:[1,2,3,6],2:[8,10,11]}
# cluster_o={1:[1,2,3,9],2:[6,8],3:[10,14]}
# cluster_o={1:[1,2,3],2:[6,8,9],3:[10,14]}
# cluster_o={1:[1,2,3],2:[6,8,9],3:[10,14]}
# cluster_o={1:[1,2,3],2:[6,8,9],3:[10,11],4:[14]}
# cluster_o={1:[1,2,3],2:[6],3:[8,9,10,11],4:[13,14]}
# cluster_o={1:[1,16],2:[5,6]}
# us=[1,2,3,6,8,10,11]
# us=[1,2,3,6,8,10,11]
# us=[1,2,3,6,8,9,10,14]
# us=[1,2,3,6,8,9,10,14]
# us=[1,2,3,6,8,9,10,14]
# us=[1,2,3,6,8,9,10,11,14]
# us=[1,2,3,6,8,9,10,11,13,14]
# us=[1,5,6,16]

for ui in us:
        cluster[ui]=[ui]
cnum=len(cluster_o)  # 类的个数

def avejaccard(cluster,cluster_o):
    accuracy=0.0
    for i in cluster:
        match_num=0
        union_num=0
        for j in cluster_o:
            intersec=list(set(cluster_o[j]).intersection(set(cluster[i])))
            union=list(set(cluster_o[j]).union(set(cluster[i])))
            if len(intersec)>match_num:
                match_num=len(intersec)
                union_num=len(union)
            elif len(intersec)==match_num:
                if len(union)<union_num:
                    match_num=len(intersec)
                    union_num=len(union)
        accuracy+=float(match_num/union_num)
    accuracy/=len(cluster)
    return accuracy

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
"计算两个用户在窗口上的cross-correlation"
def calwincorr(X, Y,delay):
    mx = 0.0
    my = 0.0
    sx = 0
    sy = 0
    for i in range(len(X)):
        mx += X[i]
    for j in range(len(Y)):
        my += Y[j]
    mx /= len(X)
    my /= len(Y)
    for i in range(len(X)):
        sx += (X[i] - mx) * (X[i] - mx)
    for j in range(len(Y)):
        sy += (Y[j] - my) * (Y[j] - my)
    denom = math.sqrt(sx * sy)
#    for delay in range(maxdelay, maxdelay + 1):
    sxy = 0
    for i in range(len(X)):
        j = i + delay
        if j < 0 or j >= len(X) or j >= len(Y):
            continue
        else:
            sxy += (X[i] - mx) * (Y[j] - my)
    if equalzero(denom):
        r=0
    else:
        r = sxy / denom
    return r

def debracket(cluster):
    print(cluster)
    for i in cluster:
        cl_str=str(cluster[i])
        if cl_str.startswith('['):
            cl_str=cl_str.replace('[','')
            cl_str=cl_str.replace(']','')
            cluster[i]=list(eval('['+cl_str+']'))
    return cluster

def readground(num,us):
    groupaffi = {}
    fname=PATH+'groundtruth\\'+str(num)+'.txt'
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    i=0
    for line in pline:
        userid=us[i]
        i+=1
        groupaffi[userid]={}
        affi = line.split(' ')
        for j in range(len(us)):
            groupaffi[userid][us[j]] = int(affi[j])
#    print(groupaffi)
    pfile.close()
    return groupaffi

# 近似为0
def equalzero(fnum):
    if fnum - 0.0 < math.pow(10, -7):
        return True
    else:
        return False
"计算关联度"
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

"层次聚类"
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


def densityAccuracy(accfile, USRS, winseq, simmap, eps, minPoints, groupaffi, func):
    accfile.write('\nCC密度聚类各个窗口准确度:')
    faa = 0.0
    acc = 0.0

    for ts in winseq:
        # OUTPUT
        accfile.write('\n' + str(ts))
        # OUTPUT
        if func == 1:
            clusters = DBSCAN.dbscan(simmap[ts], USRS, eps, minPoints)[0]
        else:
            clusters = DjCluster.djcluster(simmap[ts], USRS, eps, minPoints)[0]
        cmatrix = util.cluster2Matrix(clusters)[0]

        # OUTPUT
        for ui in USRS:
            accfile.write('\n')
            for uj in USRS:
                accfile.write(str(cmatrix[ui][uj]) + ' ')
        # OUTPUT

        fscore = Accuracy.Fmeasure(USRS, groupaffi, cmatrix)
        affinity = Accuracy.Affinity(USRS, groupaffi, cmatrix)
        faa += fscore
        acc += affinity
        # OUTPUT
    # print(str(eps)+':'+str(faa/float(len(winseq)))+','+str(acc/float(len(winseq))))
        accfile.write('\n' + str(fscore) + ',' + str(affinity) + '\n')
        #  OUTPUT
    accfile.write('\nfaa='+str(faa/float(len(winseq)))+' acc='+str(acc/float(len(winseq)))+'\n')

def getWinData(PATH,USRS,feature,winlen):
    datamap = {}
    for u in USRS:
        if u not in datamap:
            datamap[u] = {}
        if feature == 1:
            filename = PATH + 'dbad_processed\\' + str(GROUNDTRUTH) + '.' + str(u) + '_accele.csv'
        else:
            filename = PATH + 'dbad_processed\\' + str(GROUNDTRUTH) + '.' + str(u) + '_orien.csv'
        csv_data = csv.reader(open(filename), delimiter=',')
        for row in csv_data:
            ts = int(int(row[0]) / winlen)
            if TYPE == 1:
                value = math.sqrt(math.pow(float(row[1]), 2) + math.pow(float(row[2]), 2) + math.pow(float(row[3]), 2))
            else:
                value = float(row[1])

            if ts not in datamap[u]:
                datamap[u][ts] = []
            datamap[u][ts].append(value)

    "存在窗口丢失情况，因此需要在计算之前确定所有用户窗口情况，求交集"
    winseq = datamap[us[0]]
    for u in us:
        winseq = [val for val in winseq if val in datamap[u]]
    "计算窗口的总数"
    numwin = 65535
    for u in us:
        print(len(datamap[u]))
        numwin = min(numwin, len(datamap[u].keys()))
    return [datamap, winseq, numwin]


def CCSimilarity(USRS,winseq,numwin,datamap,DELAY,LENFILTER):
    # 两两计算cross-correlation得到 usercorr={ui:{uj:{ts:value}}}
    usercorr = {}
    for ui in USRS:
        if ui not in usercorr:
            usercorr[ui] = {}
        for uj in us:
            if uj not in usercorr[ui]:
                usercorr[ui][uj] = {}
            for ts in winseq:
                if ui != uj:
                    corr = calwincorr(datamap[ui][ts], datamap[uj][ts], DELAY)
                    usercorr[ui][uj][ts] = corr
                else:
                    usercorr[ui][uj][ts] = 1
            # 平滑窗口
            if LENFILTER > 0:
                for i in range(len(winseq)):
                    low = 0
                    high = 0
                    corr = 0.0
                    ts = winseq[i]
                    if ts < LENFILTER:
                        low = 0
                        high = i + LENFILTER + 1
                    elif (ts + LENFILTER + 1) > numwin:
                        low = i - LENFILTER
                        high = len(winseq)
                    else:
                        low = i - LENFILTER
                        high = i + LENFILTER + 1
                    # print(low,high)
                    for j in range(low, high):
                        ts = winseq[j]
                        corr += usercorr[ui][uj][ts]
                    corr /= float(high - low)
    return usercorr


def sortByTime(USRS,winseq,usercorr):
    # 以窗口格式 wincorr={ts:{ui:{uj:value}}}
    wincorr = {}
    for ts in winseq:
        corr_file.write('window=' + str(ts) + '\n')
        wincorr[ts] = {}
        for ui in USRS:
            wincorr[ts][ui] = {}
            for uj in USRS:
                # 选择对称的较大的相关系数值，也可只取上三角或者下三角
                wincorr[ts][ui][uj] = max(usercorr[ui][uj][ts], usercorr[uj][ui][ts])
                corr_file.write(str(wincorr[ts][ui][uj]) + ' ')
            corr_file.write('\n')
        corr_file.write('\n')
    return wincorr


result = getWinData(PATH,us,TYPE,WINSIZE)
datamap = result[0]
winseq = result[1]
numwin = result[2]
if TYPE == 1:
    filename = PATH + 'ccorrela\\' + str(GROUNDTRUTH) + '_win_corr_accele.txt'
else:
    filename = PATH+'ccorrela\\'+str(GROUNDTRUTH)+'_win_corr_orien.txt'
corr_file = open(filename,'w')
usercorr = CCSimilarity(us,winseq,numwin,datamap,DELAY,LENFILTER)
wincorr = sortByTime(us,winseq,usercorr)

"计算平均的值"
finalcorr={}
corr_file.write('平均后的矩阵：'+'\n')
for ui in us:
    if ui not in finalcorr:
        finalcorr[ui]={}
    for uj in us:
        sum=0.0
        for ts in winseq:
            sum+=wincorr[ts][ui][uj]
        finalcorr[ui][uj]=sum/numwin
        corr_file.write(str(finalcorr[ui][uj])+' ')
    corr_file.write('\n')

"层次聚类"
cluster=hcluster(finalcorr,cluster,cnum)
cluster=debracket(cluster)
groupaffi=readground(GROUNDTRUTH,us)
accuracy=calaccuracy(cluster,groupaffi,us)
corr_file.write('\n层次聚类结果：'+str(cluster)+'\n')
corr_file.write('new accuracy='+str(accuracy)+'\n')
corr_file.write('Jaccard accuracy='+str(avejaccard(cluster,cluster_o))+'\n')



"分窗口的密度聚类"
eps = 0.05
minPoints = 1
func = 1
densityAccuracy(corr_file,us,winseq,wincorr,eps,minPoints,groupaffi,func)

"阈值方法"
upthresh = 0.5
downthresh = -0.5
stride = 0.01
threshold = downthresh
corr_file.write('\n阈值迭代结果--阈值：ACC，FSCORE \n')
while threshold < upthresh:
    acc = {}
    fsc = {}
    ave_acc = 0.0
    ave_fsc = 0.0
    for ts in winseq:
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for ui in us:
            for uj in us:
                if ui < uj:
                    if wincorr[ts][ui][uj]>threshold:
                        if groupaffi[ui][uj]==1:
                            tp += 1
                        else:
                            fp += 1
                    else:
                        if groupaffi[ui][uj] == 0:
                            tn += 1
                        else:
                            fn += 1
        total = tp + fp + tn + fn
        acc[ts] = float(tp+tn)/total
        fsc[ts] = float(2*tp)/float(2 * tp + fp + fn)
        ave_acc += acc[ts]
        ave_fsc += fsc[ts]
    ave_acc /= len(winseq)
    ave_fsc /= len(winseq)
    corr_file.write(str(threshold) + ':' + str(ave_acc) + ',' + str(ave_fsc) + '\n')
    threshold += stride


"count阈值方法"
threshold = downthresh
count = 0
max_acc = 0.0
max_thresh = 0.0
corr_file.write('\nCOUNT阈值迭代结果：\n')
while threshold < upthresh:
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    fscore = 0.0
    # corr_file.write('threshold='+str(threshold)+'\n')
    for ui in us:
        for uj in us:
            if ui < uj:
                for ts in winseq:
                    if wincorr[ts][ui][uj] > threshold:
                        count += 1
                if count >= (len(winseq)*0.7):
                    if groupaffi[ui][uj] == 1:
                        tp += 1
                    else:
                        fp += 1
                    # corr_file.write(str(1)+'('+str(count)+') ')
                else:
                    if groupaffi[ui][uj] == 0:
                        tn += 1
                    else:
                        fn += 1
                    # corr_file.write(str(0)+'('+str(count)+') ')
            count = 0
        # corr_file.write('\n')
    total = tp + fp + tn + fn
    acc_value = float(tp+tn)/float(total)
    fscore = float(2 * tp) / float(2 * tp + fp + fn)

    if max_acc <= acc_value:
        max_acc = acc_value
        max_thresh = threshold
    corr_file.write(str(threshold)+':'+str(acc_value)+','+str(fscore)+'\n')
    # corr_file.write('\n\n')
    threshold += stride
corr_file.write('Max accuracy is '+str(max_acc)+' at threshold '+str(max_thresh)+'\n')
corr_file.close()






