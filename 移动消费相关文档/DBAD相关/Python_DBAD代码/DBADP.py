import numpy
import math
import string

EXPID = 2
TYPEFEATURE = 2
NUMUSER = 10
TSSIZE = 100
LENWINDOW = 5       #15 for TYPEFEATURE=1
LENFILTER = 30      #1 for TYPEFEATURE=1

# Caculate parameter m for von mises distribution
def getM(Im):
    integration = 0.0
    for theta in range(360):
        integration += math.exp(math.cos(theta))
    em = Im*360/integration
    return math.log(em)

# Caculate Jeffery's divergence for von mises distribution
# VM(x|mean,m) = 1/(2*pi*Im)*exp(m*cos(x-mean))
# x: 0~360
def jdVonMises(meani, mi, Imi, meanj, mj, Imj):
    integration = 0.0
    if Imi!=0 and Imj!=0:
        num = 360
        for step in range(num):
            x = step
            yi = 1.0/(2*math.pi*Imi)*math.exp(mi*math.cos(x-meani))
            yj = 1.0/(2*math.pi*Imj)*math.exp(mj*math.cos(x-meanj))
            try:
                integration += (yi-yj)*math.log(yi/yj)
            except:
                pass
    return integration

# Caculate Jeffery's divergence for Gaussian distribution
# N(x|mean,std) = 1/(sqrt(2*pi)*std)*exp(-0.5*pow((x-mean)/std,2))
# x: 0~10*sqrt(3)
def jdGaussian(meani, stdi, meanj, stdj):
    integration = 0.0
    if stdi!=0 and stdj!=0:
        num = int(math.ceil(100*math.sqrt(3)))
        for step in range(num):
            x = step/10.0
            yi =  1.0/(math.sqrt(2*math.pi)*stdi)*math.exp(-0.5*math.pow((x-meani)/stdi,2))
            yj =  1.0/(math.sqrt(2*math.pi)*stdj)*math.exp(-0.5*math.pow((x-meanj)/stdj,2))
            try:
                integration += (yi-yj)*math.log(yi/yj)
            except:
                pass
        integration *= 0.1
    return integration


datamap = {}
simmap = {}

#datamap - {user: {ts: [mean, std]}}
fname = 'data'+str(EXPID)+'_'+str(TYPEFEATURE)+'.csv'
pfile = open(fname, 'r')
pline = pfile.readlines()
lastts = 0
tmpvalues = []    
for line in pline:
    fields = line.split(',')
    user = string.atoi(fields[0])
    ts = string.atoi(fields[1])/(TSSIZE*LENWINDOW)
    value = string.atof(fields[2])
    if not datamap.has_key(user):
        datamap[user]={}
    if not datamap[user].has_key(ts):
        lastts = ts        
        datamap[user][ts]=[] #[0.0, 0.0]
        datamap[user][ts].append(0.0)
        datamap[user][ts].append(0.0)
        if len(tmpvalues)>0:
            if TYPEFEATURE==1:                
                datamap[user][lastts][0] = numpy.mean(tmpvalues)
                datamap[user][lastts][1] = numpy.std(tmpvalues)
            elif TYPEFEATURE==2:
                vsin = 0.0
                vcos = 0.0
                for j in range(len(tmpvalues)):
                    vsin += math.sin(tmpvalues[j])
                    vcos += math.cos(tmpvalues[j])
                datamap[user][lastts][0] = math.atan2(vsin,vcos)
                datamap[user][lastts][1] = vcos/len(tmpvalues)
        tmpvalues = []
    tmpvalues.append(value)
pfile.close()

numwin = 65535
for user in datamap.keys():
    numwin = min(numwin, len(datamap[user].keys()))

#simmap - {user: {user: {ts: [feature_similarity]}}}    
for ui in datamap.keys():
    simmap[ui] = {}
    for uj in datamap.keys():
        if uj<=ui:
            continue
        
        simmap[ui][uj] = {}
        for ts in range(numwin):
            if not datamap[ui].has_key(ts) or not datamap[uj].has_key(ts):
                simmap[ui][uj][ts] = 0.0
                continue
                
            if TYPEFEATURE==1:
                meani = datamap[ui][ts][0]
                devi = datamap[ui][ts][1]
                meanj = datamap[uj][ts][0]
                devj = datamap[uj][ts][1]
                simmap[ui][uj][ts] = jdGaussian(meani, devi, meanj, devj)
            elif TYPEFEATURE==2:
                meani = datamap[ui][ts][0]
                Imi = datamap[ui][ts][1]
                meanj = datamap[uj][ts][0]
                Imj = datamap[uj][ts][1]
                if Imi>0 and Imj>0:
                    mi = getM(Imi)
                    mj = getM(Imj)
                    simmap[ui][uj][ts] = jdVonMises(meani, mi, Imi, meanj, mj, Imj)
                else:
                    simmap[ui][uj][ts] = 0.0                              
        if LENFILTER>1:
            for ts in range(numwin-LENFILTER):
                index = numwin-1-ts
                jd = simmap[ui][uj][index]
                if index==31:
                    pass
                for history in range(index-LENFILTER, index):
                    jd += simmap[ui][uj][history]
                jd /= LENFILTER
                simmap[ui][uj][index] = jd

        print "user "+str(ui)+" vs user "+str(uj)+" : "
        last = len(simmap[ui][uj].values())-1
        print simmap[ui][uj].values()#[last]
        print "\n"
