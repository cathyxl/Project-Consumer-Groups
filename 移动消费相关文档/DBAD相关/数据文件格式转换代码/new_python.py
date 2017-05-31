"""
    这里new_python.py用来处理新的格式的加速度文件，该文件格式如下：
        time_step_window, acceleration_in_x, acceleration_in_y, acceleration_in_z
    一个文件的文件名形如：“2.1_accele.csv”，其中，2代表实验的序号，1代表人的id。每个文件也就存储着一个实验中的一个人的所有加速度数据。
"""


from rpy2.robjects.packages import importr
from scipy.integrate import quad
import math
import numpy
import os
import re
import rpy2.rinterface as r_interface
import rpy2.robjects as r_objs

EXPID = 6
"""
TYPEFEATURE = 1 means that acceleration data will be processed.
TYPEFEATURE = 2 means that orientation data will be processed.
TYPEFEATURE = 3 means that acceleration data will be processed and Mclust will be used during processing.
"""
TYPEFEATURE = 3  # 3 for using Mclust
GROUNDTRUTH = 4
USERNUMBER = 11
NUMUSER = 10
TSSIZE = 100
LENWINDOW = 15  # 15 for TYPEFEATURE=1, at least 5 for 2
LENFILTER = 5  # 1 for TYPEFEATURE=1, need an optimized value for 2

r = r_objs.r
r_mclust = importr("mclust")


# Caculate parameter m for von mises distribution
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

    '''
    if Imi!=0 and Imj!=0:
        fx = lambda x: (math.exp(mi*math.cos(x-meani))/(2*math.pi*Imi) - math.exp(mj*math.cos(x-meanj))/(2*math.pi*Imj))*math.log(math.exp(mi*math.cos(x-meani))*Imj/Imi/math.exp(mj*math.cos(x-meanj)))
        integration = quad(fx, 0, 2*math.pi)
        return integration[0]
    else:
        return 0.0
    '''


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

    '''
    if stdi!=0 and stdj!=0:
        fx = lambda x: (math.exp(-0.5*math.pow((x-meani)/stdi,2))/(math.sqrt(2*math.pi)*stdi) - math.exp(-0.5*math.pow((x-meanj)/stdj,2))/(math.sqrt(2*math.pi)*stdj))*math.log(math.exp(-0.5*math.pow((x-meani)/stdi,2))*stdj/stdi/math.exp(-0.5*math.pow((x-meanj)/stdj,2)))
        integration = quad(fx, 0, 10*math.sqrt(3))
        return integration[0]
    else:
        return 0.0
    '''


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


# datamap - {user: {ts: [mean, std]}}
datamap = {}
simmap = {}
simmap1 = {}

file_name_list = next(os.walk("."))[2]

for file_name in file_name_list:
    if re.match(str(EXPID) + r"")












fname = 'data' + str(EXPID) + '_' + str(1) + '.csv'
pfile = open(fname, 'r')
pline = pfile.readlines()
lastuser = 0
lastts = 0
tmpvalues = []


def recordInDatamap(user, ts):
    global tmpvalues
    if TYPEFEATURE == 1:
        datamap[user][ts][0] = numpy.mean(tmpvalues)
        datamap[user][ts][1] = numpy.std(tmpvalues)
    elif TYPEFEATURE == 2:
        vsin = 0.0
        vcos = 0.0
        for j in range(len(tmpvalues)):
            vsin += math.sin(tmpvalues[j] * math.pi / 180)
            vcos += math.cos(tmpvalues[j] * math.pi / 180)
        datamap[user][ts][0] = math.atan2(vsin, vcos)
        datamap[user][ts][1] = math.sqrt(vsin * vsin + vcos * vcos) / len(tmpvalues)  # compute R
    elif TYPEFEATURE == 3:  # for Mclust, datamap[user][ts][1] has no meaning, while datamap[user][ts][0] contains a Matrix of the results from Mclust
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
            datamap[user][ts][0] = r.matrix(r.c(mean, std_sigmasq, alpha), ncol=3)
            datamap[user][ts][1] = None
        else:
            del (datamap[user][ts])
    tmpvalues = []


for line in pline:
    if line == "\n" or line == "\r\n":
        continue
    fields = line.split(',')
    user = int(fields[0])
    ts = int(int(fields[1]) / (TSSIZE * LENWINDOW))
    value = float(fields[2])
    if not user in datamap:
        if tmpvalues != []:
            recordInDatamap(lastuser, lastts)
        datamap[user] = {}
        datamap[user][ts] = []  # [0.0, 0.0]
        datamap[user][ts].append(0.0)
        datamap[user][ts].append(0.0)
        lastuser = user
        lastts = ts
    elif not ts in datamap[user]:
        recordInDatamap(lastuser, lastts)
        datamap[user][ts] = []  # [0.0, 0.0]
        datamap[user][ts].append(0.0)
        datamap[user][ts].append(0.0)
        lastts = ts
    tmpvalues.append(value)
recordInDatamap(lastuser, lastts)
pfile.close()

numwin = 65535
for user in datamap:
    numwin = min(numwin, len(datamap[user]))

fname = 'outputP.txt'
pfile = open(fname, 'w')
# simmap - {user: {user: {ts: [feature_similarity]}}}
for ui in datamap:
    simmap[ui] = {}
    for uj in datamap:
        if uj <= ui:
            continue

        simmap[ui][uj] = {}
        for ts in range(numwin):
            if not ts in datamap[ui] or not ts in datamap[uj]:
                simmap[ui][uj][ts] = 0.0
                continue

            if TYPEFEATURE == 1:
                meani = datamap[ui][ts][0]
                devi = datamap[ui][ts][1]
                meanj = datamap[uj][ts][0]
                devj = datamap[uj][ts][1]
                simmap[ui][uj][ts] = jdGaussian(meani, devi, meanj, devj)
            elif TYPEFEATURE == 2:
                meani = datamap[ui][ts][0]
                Imi = datamap[ui][ts][1]
                meanj = datamap[uj][ts][0]
                Imj = datamap[uj][ts][1]
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
                simmap[ui][uj][ts] = jdFuncForMclust(matrixi, matrixj, type = 2)

        if LENFILTER > 1:
            for ts in range(numwin - LENFILTER):
                index = numwin - 1 - ts
                jd = simmap[ui][uj][index]
                for history in range(index - LENFILTER, index):
                    jd += simmap[ui][uj][history]
                jd /= LENFILTER
                simmap[ui][uj][index] = jd

        str1 = "user " + str(ui) + " vs user " + str(uj) + " : "
        last = len(simmap[ui][uj].values()) - 1
        pfile.write(str1)
        pfile.write(str(simmap[ui][uj].values()))
        pfile.write("\n")
    '''
        print str(ts)+" user "+str(ui)
        print simmap1[ts][ui].values()#[last]
        print "\n"
    '''
# sort by timestamp simmap1:{ts: {user:{user:[similarity]}}}
for ts in range(numwin):
    simmap1[ts] = {}
    for ui in datamap:
        simmap1[ts][ui] = {}
        for uj in datamap:
            if uj > ui:
                simmap1[ts][ui][uj] = simmap[ui][uj][ts]
            elif uj < ui:
                simmap1[ts][ui][uj] = simmap[uj][ui][ts]
        pfile.write(str(ts) + " user " + str(ui))
        pfile.write(str(simmap1[ts][ui].values()))  # [last]
        pfile.write("\n")
pfile.close()

# load group affiliation ground truth
userid = 1
groupaffi = {}
fname = 'data' + str(EXPID) + '_' + str(GROUNDTRUTH) + '.txt'
pfile = open(fname, 'r')
pline = pfile.readlines()
for line in pline:
    if userid == 8:
        userid += 1
    groupaffi[userid] = {}
    affi = line.split(' ')
    for i in range(0, USERNUMBER):
        j = i + 1
        groupaffi[userid][j] = int(affi[i])
    userid += 1
pfile.close()
# compute accuracy
acc = {}
threshold = 0.0
total = (NUMUSER * NUMUSER - NUMUSER) / 2
stepsize = 0.02
i = 0
while threshold < 4.0:
    accuracy = 0.0
    for ts in range(numwin):
        pos = 0
        for ui in datamap:
            for uj in datamap:
                if ui < uj:
                    if simmap1[ts][ui][uj] <= threshold:
                        if groupaffi[ui][uj] == 1:
                            pos += 1
                    else:
                        if groupaffi[ui][uj] == 0:
                            pos += 1
        acc[ts] = float(pos) / total
        accuracy += acc[ts]
    accuracy /= numwin
    # print str(threshold)+" : "+ str(accuracy)
    print(str(accuracy) + "   Threshold: " + str(i * stepsize))
    threshold += stepsize
    i += 1
