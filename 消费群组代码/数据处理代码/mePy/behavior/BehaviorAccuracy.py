import algorithms.DBSCAN as DBSCAN
import algorithms.DJcluster as DjCluster
import algorithms.Accuracy as Accuracy
import utils.util as util
from utils.config import experiment_users
"将每个窗口的距离矩阵分别使用三种方法进行分组，最后计算平均准确度"
def densityAccuracy(accfile, USRS,simmap,eps,minPoints,groupaffi,func):
    accfile.write('行为密度聚类各个窗口准确度：\n')
    faa = 0.0
    acc = 0.0
    numwin = len(simmap)
    for ts in simmap:
        # OUTPUT
        accfile.write('\n'+str(ts))
        # OUTPUT
        if func == 1:
            clusters = DBSCAN.dbscan(simmap[ts],USRS,eps,minPoints)[0]
        else:
            clusters = DjCluster.djcluster(simmap[ts],USRS,eps,minPoints)[0]
        cmatrix = util.cluster2Matrix(clusters)[0]

        # OUTPUT
        for ui in USRS:
            accfile.write('\n')
            for uj in USRS:
                # print(ui,uj)
                accfile.write(str(cmatrix[ui][uj])+' ')
        # OUTPUT

        fscore = Accuracy.Fmeasure(USRS,groupaffi,cmatrix)
        affinity = Accuracy.Affinity(USRS,groupaffi,cmatrix)
        faa += fscore
        acc += affinity
        # OUTPUT

        accfile.write('\n'+str(fscore)+','+str(affinity)+'\n')
        #  OUTPUT
    # print(str(eps)+':'+str(faa/float(numwin))+','+str(acc/float(numwin)))
    # print(numwin)
    accfile.write('\nfaa='+str(faa/float(numwin))+' acc='+str(acc/float(numwin))+'\n\n')
def loadGround(fname,USRS):
    i=0
    groupaffi = {}
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    for line in pline:
        ui = USRS[i]
        i += 1
        groupaffi[ui] = {}
        affi = line.split(' ')
        for j in range(len(USRS)):
            uj = USRS[j]
            groupaffi[ui][uj] = int(affi[j])
    pfile.close()
    return groupaffi
def threshAccuracy(accfile,USRS,simmap,upthresh,threshold,thrstride,groupaffi):
    while threshold < upthresh:
        acc = {}
        pre = {}
        rec = {}
        fsc = {}
        precise = 0.0  # 精确率
        recall = 0.0  # 召回率
        fscore = 0.0  # F1 score
        accuracy = 0.0
        numwin = len(simmap)
        for ts in simmap:
            tp = 0
            fp = 0
            tn = 0
            fn = 0
            for ui in USRS:
                for uj in USRS:
                    if ui < uj:
                        if simmap[ts][ui][uj] <= threshold:  # jd为nan判断为false，jd为inf判断为false
                            if groupaffi[ui][uj] == 1:
                                tp += 1
                            else:
                                fp += 1
                        else:
                            if groupaffi[ui][uj] == 0:
                                tn += 1
                            else:
                                fn += 1
            total = tp + fp + tn + fn
            acc[ts] = float(tp+tn) / float(total)
            if tp + fp != 0:
                pre[ts] = float(tp) / float(tp + fp)
            else:
                pre[ts] = 0
            rec[ts] = float(tp) / float(tp + fn)
            fsc[ts] = 2 * float(tp) / float(2 * tp + fp + fn)
            precise += pre[ts]
            recall += rec[ts]
            fscore += fsc[ts]
            accuracy += acc[ts]
        accuracy /= numwin
        precise /= numwin
        recall /= numwin
        fscore /= numwin
        accfile.write(str(threshold) + " : " + str(accuracy) + ' ' + str(fscore)+'\n')
        # print(str(threshold) + " : " + str(accuracy)+' '+str(fscore))
        threshold += thrstride

def countAccuracy(accfile,USRS,simmap,upthresh,threshold,thrstride,groupaffi):
    numwin = len(simmap)

    while threshold < upthresh:
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        count = 0
        for ui in USRS:
            for uj in USRS:
                # print(ui,uj)
                if ui < uj:
                    for ts in simmap:
                        if simmap[ts][ui][uj] <= threshold:  # jd为nan判断为false，jd为inf判断为false
                            count += 1
                    if count > numwin * 0.7:
                        if groupaffi[ui][uj] == 1:
                            tp += 1
                        else:
                            fp += 1
                    else:
                        if groupaffi[ui][uj] == 0:
                            tn += 1
                        else:
                            fn += 1
                count = 0
        total = tp + fp + tn + fn
        acc_value = float(tp+tn) / float(total)
        if tp + fp != 0:
            precise = float(tp) / float(tp + fp)
        recall = float(tp) / float(tp + fn)
        fscore = float(2 * tp) / float(2 * tp + fp + fn)
        accfile.write(str(threshold) + " : " + str(acc_value) + ' ' + str(fscore)+'\n')
        # print(str(threshold) + " : " + str(acc_value) + ' ' + str(fscore))
        threshold += thrstride


PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'
upthresh = 20
threshold = 0
GROUNDTRUTH = 3
USRS = experiment_users[GROUNDTRUTH]
print(USRS)

pfile = open(PATH + 'classified_result\\disparity_RF_'+str(GROUNDTRUTH)+'.txt','r')   #(PATH + 'behavior\\DisparityMatrix-'+str(GROUNDTRUTH)+'.txt','r')
plines = pfile.readlines()
dismatrix = {}
i = 0
ts = 0
"数据读取"
for line in plines:
    if line[0:-1] == '':
        continue
    fields = line[0:-1].split(' ')
    if len(fields) <= 0:
        continue
    elif len(fields) == 1:
        ts = int(fields[0])
        i = 0
        if ts not in dismatrix:
            dismatrix[ts] = {}
    else:
        ui = USRS[i]
        if ui not in dismatrix[ts]:
            dismatrix[ts][ui] = {}
        for j in range(len(fields)):
            uj = USRS[j]
            dismatrix[ts][ui][uj] = float(fields[j])
        i += 1
pfile.close()

eps = 9
minPoints = 1
func = 1
behavior_acc = open(PATH+'behavior1\\'+str(GROUNDTRUTH)+'_acc_behavior.txt','w')
groundfile = PATH+'groundtruth\\'+str(GROUNDTRUTH)+'.txt'
groupaffi = loadGround(groundfile,USRS)

densityAccuracy(behavior_acc,USRS,dismatrix,eps,minPoints,groupaffi,func)
threshAccuracy(behavior_acc,USRS,dismatrix,upthresh,threshold,1,groupaffi)
countAccuracy(behavior_acc,USRS,dismatrix,upthresh,threshold,1,groupaffi)
behavior_acc.close()

