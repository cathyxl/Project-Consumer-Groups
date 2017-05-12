import numpy
import math
from scipy.integrate import quad

EXPID = 3
TYPEFEATURE = 1
GROUNDTRUTH = 4
USERNUMBER = 11
NUMUSER = 10
TSSIZE = 100
LENWINDOW = 15  # 15 for TYPEFEATURE=1, at least 5 for 2
LENFILTER = 5  # 1 for TYPEFEATURE=1, need an optimized value for 2


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


datamap = {}
simmap = {}
simmap1 = {}
# datamap - {user: {ts: [mean, std]}}
fname = 'data' + str(EXPID) + '_' + str(TYPEFEATURE) + '.csv'
pfile = open(fname, 'r')
pline = pfile.readlines()
lastts = 0
tmpvalues = []
for line in pline:
    fields = line.split(',')
    user = int(fields[0])
    ts = int(int(fields[1]) / (TSSIZE * LENWINDOW))
    value = float(fields[2])
    if user not in datamap:
        datamap[user] = {}
        lastts = 0
    if ts not in datamap[user]:
        datamap[user][ts] = []  # [0.0, 0.0]
        datamap[user][ts].append(0.0)
        datamap[user][ts].append(0.0)
        if ts > 0 and len(tmpvalues) > 0:
            if TYPEFEATURE == 1:
                datamap[user][lastts][0] = numpy.mean(tmpvalues)
                datamap[user][lastts][1] = numpy.std(tmpvalues)
            elif TYPEFEATURE == 2:
                vsin = 0.0
                vcos = 0.0
                for j in range(len(tmpvalues)):
                    vsin += math.sin(tmpvalues[j] * math.pi / 180)
                    vcos += math.cos(tmpvalues[j] * math.pi / 180)
                datamap[user][lastts][0] = math.atan2(vsin, vcos)
                datamap[user][lastts][1] = math.sqrt(vsin * vsin + vcos * vcos) / len(tmpvalues)  # compute R
        lastts = ts
        tmpvalues = []
    tmpvalues.append(value)
pfile.close()

numwin = 65535
for user in datamap.keys():
    numwin = min(numwin, len(datamap[user].keys()))

fname = 'outputP.txt'
pfile = open(fname, 'w')
# simmap - {user: {user: {ts: [feature_similarity]}}}
for ui in datamap.keys():
    simmap[ui] = {}
    for uj in datamap.keys():
        if uj <= ui:
            continue

        simmap[ui][uj] = {}
        for ts in range(numwin):
            if ts not in datamap[ui] or ts not in datamap[uj]:
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
    for ui in datamap.keys():
        simmap1[ts][ui] = {}
        for uj in datamap.keys():
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
while threshold < 30.0:
    accuracy = 0.0
    for ts in range(numwin):
        pos = 0
        for ui in datamap.keys():
            for uj in datamap.keys():
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
    print(str(accuracy))
    threshold += 0.2
