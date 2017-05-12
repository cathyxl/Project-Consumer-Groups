import math
#import string

EXPID = 2
NUMFEATURE = 2
NUMUSER = 10
TSSIZE = 100
LENWINDOW = 5
LENFILTER = 30

datamap = {}
simmap = {}

#datamap - {user: {ts: [[feature_value]]}}
for feature in range(NUMFEATURE):
    fname = 'data'+str(EXPID)+'_'+str(feature+1)+'.csv'
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    
    for line in pline:
        fields = line.split(',')
        #user = string.atoi(fields[0])
        #ts = string.atoi(fields[1])/(TSSIZE*LENWINDOW)
        #value = string.atof(fields[2])
        user=int(fields[0])
        ts=(int(fields[1]))/(TSSIZE*LENWINDOW)
        value=float(fields[2])

        #if not datamap.has_key(user):
        if user not in datamap:
            datamap[user]={}
        if not datamap[user].has_key(ts):
            datamap[user][ts]=[]
            for f in range(NUMFEATURE):
                datamap[user][ts].append([])
        #如果第一个feature的值为空则不存入datamap
        if feature>0 and datamap[user][ts][0] == []:
            continue
        datamap[user][ts][feature].append(value)
        
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
            simmap[ui][uj][ts] = []
            for feature in range(NUMFEATURE):
                if datamap[ui].has_key(ts) and datamap[uj].has_key(ts):
                    numvalue = min(len(datamap[ui][ts][feature]), len(datamap[uj][ts][feature]))
                    jd = 0.0
                    if numvalue>0: 
                        for item in range(numvalue):
                            vi = datamap[ui][ts][feature][item]
                            vj = datamap[uj][ts][feature][item]
                            if vi!=0 and vj!=0:
                                jd += (vi-vj)*math.log(vi/vj)
                        jd /= numvalue
                    simmap[ui][uj][ts].append(jd)
                else:
                    simmap[ui][uj][ts].append(0.0)
                    
        if LENFILTER>1:
            for feature in range(NUMFEATURE):
                for ts in range(numwin-LENFILTER):
                    index = numwin-1-ts
                    jd = simmap[ui][uj][index][feature]
                    for history in range(index-LENFILTER, index):
                        jd += simmap[ui][uj][history][feature]
                    jd /= LENFILTER
                    simmap[ui][uj][index][feature] = jd

        print ("user "+str(ui)+" vs user "+str(uj)+" : ")
        last = len(simmap[ui][uj].values())-1
        print (simmap[ui][uj].values())#[last]
        print ("\n")
