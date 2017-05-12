import numpy
import math
from scipy.integrate import quad
import algorithms.DBSCAN as DBSCAN
import algorithms.DJcluster as DjCluster
import algorithms.Accuracy as Accuracy
import rpy2.rinterface as r_interface
import rpy2.robjects as r_objs


import utils.util as util

def getM(Im):
    if Im < 0.53:
        res = 2 * Im + Im ** 3 + 5.0 / 6.0 * math.pow(Im, 5)
    elif Im < 0.85:
        res = -0.4 + 1.39 * Im + 0.43 / (1 - Im)
    else:
        tmp = (3 * Im - 4 * Im * Im + Im ** 3)
        if tmp > 0.01:  # 0.000001 :
            res = 1.0 / tmp
        else:
            res = 100.0  # 0.0 #R=1 normal distribution
    return res

def integrand(x, m):
    return math.exp(m * math.cos(x))

# Caculate Jeffery's divergence for von mises distribution
# VM(x|mean,m) = 1/(2*pi*Im)*exp(m*cos(x-mean))
# x: 0~360
def jdVonMises(meani, mi, Imi, meanj, mj, Imj):
    integration = 0.0
    if Imi != 0 and Imj != 0:
        num = 360
        for step in range(num):
            x = step * math.pi / 180
            yi = 1.0 / (2 * math.pi * Imi) * math.exp(mi * math.cos(x - meani))
            yj = 1.0 / (2 * math.pi * Imj) * math.exp(mj * math.cos(x - meanj))
            try:
                integration += (yi - yj) * math.log(yi / yj)
            except:
                pass
        integration *= math.pi / 180
    return integration

# Caculate Jeffery's divergence for Gaussian distribution
# N(x|mean,std) = 1/(sqrt(2*pi)*std)*exp(-0.5*pow((x-mean)/std,2))
# x: 0~10*sqrt(3)
def jdGaussian(meani, stdi, meanj, stdj):
    integration = 0.0
    if stdi != 0 and stdj != 0:
        num = int(math.ceil(100 * math.sqrt(3)))
        for step in range(num):
            x = step / 10.0
            yi = 1.0 / (math.sqrt(2 * math.pi) * stdi) * math.exp(-0.5 * math.pow((x - meani) / stdi, 2))
            yj = 1.0 / (math.sqrt(2 * math.pi) * stdj) * math.exp(-0.5 * math.pow((x - meanj) / stdj, 2))

            try:
                integration += (yi - yj) * math.log(yi / yj)
            except:
                pass
        integration *= 0.1
    return integration

def jdFuncForMclust(matrixi, matrixj, type = 2):
    """
    Caculate Jeffery's divergence for Gaussian mixture model without log function.
    :param matrixi: Matrix of person i. matrix = r.matrix(r.c(mean, std_sigmasq, alpha), ncol=3)
    :param matrixj: Matrix of person j. matrix = r.matrix(r.c(mean, std_sigmasq, alpha), ncol=3)
    :param type: Value 1 is for using the original integration method whose result is not very good but enough. Value 2
        is for using the improved integration method which learns from the function jdGaussian and it has the best
        result in all of that produced from different Mclust integration method. Value 3 means it uses Monte Carlo
        approach.
    :return: Jeffery's divergence
    """
    if type == 1:
        num_rows1 = r.nrow(matrixi)[0]
        num_rows2 = r.nrow(matrixj)[0]
        num = int(math.ceil(100 * math.sqrt(3)))
        integration = 0.0
        meani_list = []
        stdi_list = []
        alphai_list = []
        meanj_list = []
        stdj_list = []
        alphaj_list = []
        for i in range(1, num_rows1 + 1):
            meani_list.append(matrixi.rx(i, 1)[0])
            stdi_list.append(matrixi.rx(i, 2)[0])
            alphai_list.append(matrixi.rx(i, 3)[0])
        for j in range(1, num_rows2 + 1):
            meanj_list.append(matrixj.rx(j, 1)[0])
            stdj_list.append(matrixj.rx(j, 2)[0])
            alphaj_list.append(matrixj.rx(j, 3)[0])
        for step in range(num):
            x = step / 10.0
            yi = 0.0
            yj = 0.0
            for i in range(num_rows1):
                meani = meani_list[i]
                stdi = stdi_list[i]
                alphai = alphai_list[i]
                yi = yi + alphai / (math.sqrt(2 * math.pi) * stdi) * math.exp(-0.5 * math.pow((x - meani) / stdi, 2))
            for j in range(num_rows2):
                meanj = meanj_list[j]
                stdj = stdj_list[j]
                alphaj = alphaj_list[j]
                yj = yj + alphaj / (math.sqrt(2 * math.pi) * stdj) * math.exp(-0.5 * math.pow((x - meanj) / stdj, 2))
            try:
                integration += (yi - yj) * math.log(yi / yj)
            except:
                pass
        integration *= 0.1
        return integration

    elif type == 2:
        num_rows1 = r.nrow(matrixi)[0]
        num_rows2 = r.nrow(matrixj)[0]
        meani_list = []
        stdi_list = []
        alphai_list = []
        meanj_list = []
        stdj_list = []
        alphaj_list = []
        for i in range(1, num_rows1 + 1):
            meani_list.append(matrixi.rx(i, 1)[0])
            stdi_list.append(matrixi.rx(i, 2)[0])
            alphai_list.append(matrixi.rx(i, 3)[0])
        for j in range(1, num_rows2 + 1):
            meanj_list.append(matrixj.rx(j, 1)[0])
            stdj_list.append(matrixj.rx(j, 2)[0])
            alphaj_list.append(matrixj.rx(j, 3)[0])

        def integrandForMclust(floatSexpVector):
            nonlocal meani_list
            nonlocal stdi_list
            nonlocal alphai_list
            nonlocal meanj_list
            nonlocal stdj_list
            nonlocal alphaj_list
            resultList = []
            for ele in floatSexpVector:
                h1 = 0
                for i in range(num_rows1):
                    meani = meani_list[i]
                    stdi = stdi_list[i]
                    alphai = alphai_list[i]
                    value = 1 / numpy.sqrt(2 * numpy.pi * stdi)
                    exp_content = -numpy.square(ele - meani) / (2 * stdi)
                    h1 = h1 + alphai * value * numpy.exp(exp_content)
                h2 = 0
                for j in range(num_rows2):
                    meanj = meanj_list[j]
                    stdj = stdj_list[j]
                    alphaj = alphaj_list[j]
                    value = 1 / numpy.sqrt(2 * numpy.pi * stdj)
                    exp_content = -numpy.square(ele - meanj) / (2 * stdj)
                    h2 = h2 + alphaj * value * numpy.exp(exp_content)
                resultList.append(numpy.abs(h1 - h2))
            return r_interface.FloatSexpVector(resultList)

        return r.integrate(integrandForMclust, -numpy.inf, numpy.inf)[0][0]

    elif type == 3:
        num_rows1 = r.nrow(matrixi)[0]
        num_rows2 = r.nrow(matrixj)[0]
        matrixi_1_1 = matrixi.rx(1, 1)[0]
        sqrt_matrixi_1_2 = numpy.sqrt(matrixi.rx(1, 2)[0])
        rnorm_result_list = r.rnorm(100000, matrixi_1_1, sqrt_matrixi_1_2)
        dnorm_result_list = r.dnorm(rnorm_result_list, matrixi_1_1, sqrt_matrixi_1_2)
        result_list = []
        meani_list = []
        stdi_list = []
        alphai_list = []
        meanj_list = []
        stdj_list = []
        alphaj_list = []
        for i in range(1, num_rows1 + 1):
            meani_list.append(matrixi.rx(i, 1)[0])
            stdi_list.append(matrixi.rx(i, 2)[0])
            alphai_list.append(matrixi.rx(i, 3)[0])
        for j in range(1, num_rows2 + 1):
            meanj_list.append(matrixj.rx(j, 1)[0])
            stdj_list.append(matrixj.rx(j, 2)[0])
            alphaj_list.append(matrixj.rx(j, 3)[0])
        index = 0
        for ele in rnorm_result_list:
            h1 = 0
            for i in range(num_rows1):
                meani = meani_list[i]
                stdi = stdi_list[i]
                alphai = alphai_list[i]
                value = 1 / numpy.sqrt(2 * numpy.pi * stdi)
                exp_content = -numpy.square(ele - meani) / (2 * stdi)
                h1 = h1 + alphai * value * numpy.exp(exp_content)
            h2 = 0
            for j in range(num_rows2):
                meanj = meanj_list[j]
                stdj = stdj_list[j]
                alphaj = alphaj_list[j]
                value = 1 / numpy.sqrt(2 * numpy.pi * stdj)
                exp_content = -numpy.square(ele - meanj) / (2 * stdj)
                h2 = h2 + alphaj * value * numpy.exp(exp_content)
            result_list.append((h1 - h2) * numpy.log(h1 / h2) / dnorm_result_list[index])
            index += 1
        return numpy.mean(result_list)

"得到窗口化的数据"
def getWinData(PATH, USRS, feature, winlen):
    datamap = {}
    for i in USRS:
        if i not in datamap:
            datamap[i] = {}
        if feature == 1:
            fname = PATH+'dbad_processed\\'+str(GROUNDTRUTH)+'.' + str(i) + '_accele.csv'
        else:
            fname = PATH+'dbad_processed\\'+str(GROUNDTRUTH)+'.' +str(i) + '_orien.csv'

        pfile = open(fname,'r')
        pline = pfile.readlines()
        for line in pline:
            fields = line.split(',')
            ts = int(int(fields[0])/winlen)
            x = float(fields[1])
            value = 0.0
            if feature == 1:
                y = float(fields[2])
                z = float(fields[3])
                value = math.sqrt(math.pow(x,2) + math.pow(y,2) +  math.pow(z,2))
            elif feature == 2:
                value = x
            if ts not in datamap[i]:
                datamap[i][ts] = []
            datamap[i][ts].append(value)
        pfile.close()
    return datamap
"获得需要的参数"
def getParamap(datamap,feature):
    paramap = {}
    if feature == 1:
        medvalue.write('DBAD加速度参数中间值：\n')
    else:
        medvalue.write('DBAD方向参数中间值：\n')
    for i in datamap:
        if i not in paramap:
            paramap[i] = {}
        medvalue.write(str(i)+':')
        for ts in datamap[i]:
            if ts not in paramap[i]:
                paramap[i][ts] = []
                paramap[i][ts].append(0.0)
                paramap[i][ts].append(0.0)
            if feature == 1:
                mean = numpy.mean(datamap[i][ts])
                std = numpy.std(datamap[i][ts])
                paramap[i][ts][0] = mean
                paramap[i][ts][1] = std
                medvalue.write('('+str(mean)+','+str(std)+')')
            elif feature == 2:
                vsin = 0.0
                vcos = 0.0
                tmpvalues = datamap[i][ts]
                # print(tmpvalues)
                for j in range(len(tmpvalues)):
                    vsin += math.sin(tmpvalues[j] * math.pi / 180)
                    vcos += math.cos(tmpvalues[j] * math.pi / 180)
                paramap[i][ts][0] = math.atan2(vsin, vcos)
                paramap[i][ts][1] = math.sqrt(vsin * vsin + vcos * vcos) / len(tmpvalues)
                medvalue.write('(' + str(paramap[i][ts][0]) + ',' + str(paramap[i][ts][1]) + ')')
            elif feature == 3:  # for Mclust, datamap[user][ts][1] has no meaning, while datamap[user][ts][0] contains a Matrix of the results from Mclust
                tmpvalues = datamap[i][ts]
                if len(tmpvalues) > 1:
                    MclustModel = r_mclust.Mclust(r_objs.FloatVector(tmpvalues))
                    # equals to alpha<-MclustModel$parameters$pro in R
                    alpha = MclustModel[11][0]
                    # equals to mean<-MclustModel$parameters$mean in R
                    mean = MclustModel[11][1]
                    # equals to std_sigmasq<-MclustModel$parameters$var$sigmasq in R
                    std_sigmasq = MclustModel[11][2][3]
                    if (r.length(mean)[0] > r.length(std_sigmasq)[0]):
                        std_sigmasq = r.rep(std_sigmasq, r.length(mean))
                    paramap[i][ts][0] = r.matrix(r.c(mean, std_sigmasq, alpha), ncol=3)
                    paramap[i][ts][1] = None
                else:
                    del (paramap[i][ts])

        medvalue.write('\n')
    return paramap
"计算差异矩阵"
def dbadDivergence(paramap,feature):
    numwin=65535
    for user in paramap:
        numwin = min(numwin,len(paramap[user]))

    simmap = {}
    for ui in paramap:
        simmap[ui] = {}
        for uj in paramap:
            if uj <= ui:
                continue
            simmap[ui][uj] = {}
            for ts in range(numwin):
                if ts not in paramap[ui] or ts not in paramap[uj]:
                    simmap[ui][uj][ts] = 0.0
                    continue
                if feature == 1:
                    meani = paramap[ui][ts][0]
                    devi = paramap[ui][ts][1]
                    meanj = paramap[uj][ts][0]
                    devj = paramap[uj][ts][1]
                    simmap[ui][uj][ts] = jdGaussian(meani,devi,meanj, devj)
                elif feature == 2:
                    meani = paramap[ui][ts][0]
                    Imi = paramap[ui][ts][1]
                    meanj = paramap[uj][ts][0]
                    Imj = paramap[uj][ts][1]
                    if Imi > 0 and Imj > 0:
                        mi = getM(Imi)
                        mj = getM(Imj)
                        Imi = quad(integrand, 0, 2 * math.pi, args=(mi))
                        Imj = quad(integrand, 0, 2 * math.pi, args=(mj))
                        simmap[ui][uj][ts] = jdVonMises(meani, mi, Imi[0] / math.pi / 2.0, meanj, mj,
                                                        Imj[0] / math.pi / 2.0)
                    else:
                        simmap[ui][uj][ts] = 0.0
                elif TYPEFEATURE == 3:
                    matrixi = datamap[ui][ts][0]
                    matrixj = datamap[uj][ts][0]
                    simmap[ui][uj][ts] = jdFuncForMclust(matrixi, matrixj, type=2)

            # filter(LENFILTER, numwin, simmap[ui][uj])

    return [simmap,numwin]
"对差异矩阵进行平滑"
def filterSimmap(LENFILTER, numwin, simmap):
    for ui in simmap:
        for uj in simmap:
            if LENFILTER > 1 and ui < uj:
                for ts in range(numwin - LENFILTER):
                    index = numwin - 1 - ts
                    jd = simmap[ui][uj][index]
                    for history in range(index - LENFILTER, index):
                        jd += simmap[ui][uj][history]
                        jd /= LENFILTER
                        simmap[ui][uj][index] = jd

# def filter(LENFILTER, numwin, simsequence):
#     if LENFILTER > 1:
#         for ts in range(numwin - LENFILTER):
#             index = numwin - 1 - ts
#             jd = simsequence[index]
#             for history in range(index - LENFILTER, index):
#                 jd += simsequence[history]
#                 jd /= LENFILTER
#                 simsequence[index] = jd

def outputSimmap(USRS, simmap, numwin):
    for ts in range(numwin):
        medvalue.write(str(ts)+'\n')
        for ui in simmap:
            for uj in simmap:
                if uj != USRS[0]:
                    medvalue.write(' ')
                if ui == uj:
                    medvalue.write('0')
                elif ui < uj:
                    medvalue.write(str(simmap[ui][uj][ts]))
                else:
                    medvalue.write(str(simmap[uj][ui][ts]))
                if uj == USRS[-1]:
                    medvalue.write('\n')

def sortbytimestamp(USRS,simmap,numwin):
    simmap1={}
    for ts in range(numwin):
        simmap1[ts] = {}
        dbadsimmap.write(str(ts)+'\n')
        for ui in simmap:
            simmap1[ts][ui] = {}
            for uj in simmap:
                if uj != USRS[0]:
                    dbadsimmap.write(' ')
                if ui == uj:
                    dbadsimmap.write('0')
                    simmap1[ts][ui][uj] = 0
                elif uj > ui:
                    dbadsimmap.write(str(simmap[ui][uj][ts]))
                    simmap1[ts][ui][uj] = simmap[ui][uj][ts]
                else:
                    dbadsimmap.write(str(simmap[uj][ui][ts]))
                    simmap1[ts][ui][uj] = simmap[uj][ui][ts]
                if uj == USRS[-1]:
                    dbadsimmap.write('\n')
    return simmap1

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

def threshAccuracy(USRS,numwin,upthresh,threshold,thrstride,simmap,groupaffi):
    total = (len(USRS)*len(USRS)-len(USRS)) / 2
    while threshold < upthresh:
        acc = {}
        pre = {}
        rec = {}
        fsc = {}
        precise = 0.0  # 精确率
        recall = 0.0  # 召回率
        fscore = 0.0  # F1 score
        accuracy = 0.0
        for ts in range(numwin):
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
            acc[ts] = float(tp+tn) / float(total)
            if tp + fp != 0:
                pre[ts] = float(tp) / float(tp + fp)
            else:
                pre[ts] = 0
            rec[ts] = float(tp) / float(tp + fn)
            fsc[ts] = 2 * float(tp) / float(2 * tp + fp + fn)
            # accfile.write(str(ts)+':'+str(acc[ts])+','+str(fsc[ts])+'\n')
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

def countAccuracy(USRS,numwin,upthresh,threshold,simmap,groupaffi,thrstride):

    total = (len(USRS) * len(USRS) - len(USRS)) / 2
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
                    for ts in range(numwin):
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
        # print(tp,fp,tn,fn)
        acc_value = float(tp+tn) / float(total)
        if tp + fp != 0:
            precise = float(tp) / float(tp + fp)
        recall = float(tp) / float(tp + fn)
        fscore = float(2 * tp) / float(2 * tp + fp + fn)
        accfile.write(str(threshold) + " : " + str(acc_value) + ' ' + str(fscore)+'\n')
        # print(str(threshold) + " : " + str(acc_value) + ' ' + str(fscore))
        threshold += thrstride

def densityAccuracy(USRS,numwin,simmap,eps,minPoints,groupaffi,func):
    accfile.write('DBAD密度聚类各个窗口准确度：\n')
    faa = 0.0
    acc = 0.0
    for ts in range(numwin):
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
    accfile.write('\nfaa='+str(faa/float(numwin))+' acc='+str(acc/float(numwin)))

if __name__ == '__main__':
    "参数与常量列表"
    from utils.config import experiment_users
    PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
    TYPEFEATURE = 1
    TSSIZE = 1000
    LENWINDOW = 15  # 15 for TYPEFEATURE=1, at least 5 for 2
    LENFILTER = 3  # 1 for TYPEFEATURE=1, need an optimized value for 2
    WINLEN = TSSIZE * LENWINDOW
    GROUNDTRUTH = 7
    USRS = experiment_users[GROUNDTRUTH]
    threshold = 0.0
    upthresh = 0.0
    thrstride = 0.0
    # eps经过迭代选取的比较合适的值
    if TYPEFEATURE == 1:
        eps = 0.2
    else:
        eps = 30
    minPoints = 1
    func = 1  # 1表示DBSCAN，2表示DjCluster
    if TYPEFEATURE == 1:
        upthresh = 6
        thrstride = 0.02
    else:
        upthresh = 100
        thrstride = 1
    "文件列表"
    groundfile = PATH + 'groundtruth\\' + str(GROUNDTRUTH) + '.txt'
    if TYPEFEATURE == 1:
        dbadsimmap = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.1_dbadsimmap.txt', 'w')
        medvalue = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.1_medvalue.txt', 'w')
        accfile = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.1_accfile.txt', 'w')
    else:
        dbadsimmap = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.2_dbadsimmap.txt', 'w')
        medvalue = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.2_medvalue.txt', 'w')
        accfile = open(PATH + 'dbad\\' + str(GROUNDTRUTH) + '.2_accfile.txt', 'w')

    "DBAD过程"

    # 数据分窗口 datamap={ui:{ts:[values]}}
    datamap = getWinData(PATH, USRS, TYPEFEATURE, WINLEN)
    # 参数选取计算 paramap={ui:{ts:[para1,para2]}}
    paramap = getParamap(datamap, TYPEFEATURE)
    # 计算divergence simmap={ui:{uj:{ts:value}}}
    result = dbadDivergence(paramap, TYPEFEATURE)
    simmap = result[0]
    numwin = result[1]
    medvalue.write('过滤前simmap：\n')
    outputSimmap(USRS, simmap, numwin)

    # 过滤divergence matrix
    filterSimmap(LENFILTER, numwin, simmap)
    # 改变simmap的格式 simmap={ts:{ui:{uj:value}}}
    simmap = sortbytimestamp(USRS, simmap, numwin)
    # 加载groundtruth groupaffi={ui:{uj:0/1}}
    groupaffi = loadGround(groundfile, USRS)
    # 计算dbad的准确度
    # 阈值迭代
    threshAccuracy(USRS, numwin, upthresh, threshold, thrstride, simmap, groupaffi)
    # COUNT阈值迭代
    countAccuracy(USRS, numwin, upthresh, threshold, simmap, groupaffi, thrstride)
    # 计算基于密度聚类后的准确度
    densityAccuracy(USRS, numwin, simmap, eps, minPoints, groupaffi, func)

    dbadsimmap.close()
    accfile.close()
    medvalue.close()
