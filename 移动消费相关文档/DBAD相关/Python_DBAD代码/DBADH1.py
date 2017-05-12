import math
import string

EXPID = 3
NUMFEATURE = 2
GROUNDTRUTH = 4
USERNUMBER = 11
NUMUSER = 10
TSSIZE = 100
LENWINDOW = 5
LENFILTER = 30

datamap = {}
simmap = {}
simmap1 = {}
#datamap - {user: {ts: [[feature_value]]}}
for feature in range(NUMFEATURE):
    fname = 'data'+str(EXPID)+'_'+str(feature+1)+'.csv'
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    
    for line in pline:
        fields = line.split(',')
        user = string.atoi(fields[0])
        ts = string.atoi(fields[1])/(TSSIZE*LENWINDOW)
        value = string.atof(fields[2])
        if not datamap.has_key(user):
            datamap[user]={}
        if not datamap[user].has_key(ts):
            datamap[user][ts]=[]
            for f in range(NUMFEATURE):
                datamap[user][ts].append([])
        if feature>0 and datamap[user][ts][0]==[]:
            continue
        datamap[user][ts][feature].append(value)
        
    pfile.close()

numwin = 65535
for user in datamap.keys():
    numwin = min(numwin, len(datamap[user].keys()))

fname = 'output.txt'
pfile = open(fname, 'w')
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
		'''
        print "user "+str(ui)+" vs user "+str(uj)+" : "
        last = len(simmap[ui][uj].values())-1
        print simmap[ui][uj].values()#[last]
        print "\n"
		'''
		str1 = "user "+str(ui)+" vs user "+str(uj)+" : "
		str2 = str(simmap[ui][uj].values())
		pfile.write(str1)
		last = len(simmap[ui][uj].values())-1
        pfile.write(str2)
        pfile.write("\n")



#sort by timestamp simmap1:{ts: {user:{user:[similarity]}}}
for ts in range(numwin):
    simmap1[ts]={}
    for ui in datamap.keys():
        simmap1[ts][ui] = {}
        for uj in datamap.keys():
            simmap1[ts][ui][uj]=[]
            for feature in range(NUMFEATURE):
                if uj>ui:
                    simmap1[ts][ui][uj].append(simmap[ui][uj][ts][feature])
                elif uj<ui:
                    simmap1[ts][ui][uj].append(simmap[uj][ui][ts][feature])
        pfile.write(str(ts)+" user "+str(ui))
        pfile.write(str(simmap1[ts][ui].values()))#[last]
        pfile.write("\n")
pfile.close()

#load group affiliation ground truth 
userid = 1
groupaffi={}
fname = 'data'+str(EXPID)+'_'+str(GROUNDTRUTH)+'.txt'
pfile = open(fname, 'r')
pline = pfile.readlines()
for line in pline:
    if userid==8:
        userid+=1
    groupaffi[userid]={}
    affi = line.split(' ')
    for i in range(0, USERNUMBER):
        j=i+1
        groupaffi[userid][j]=string.atoi(affi[i])
    userid+=1
pfile.close()
# compute accuracy
acc={}
threshold = 0.0
total=(NUMUSER*NUMUSER-NUMUSER)/2
while threshold< 3.0:
    accuracy=0.0
    for feature in range(NUMFEATURE):
        for ts in range(numwin):
            pos = 0
            for ui in datamap.keys():
                for uj in datamap.keys():
                    if ui < uj:
                        if simmap1[ts][ui][uj][feature]<=threshold:
                            if groupaffi[ui][uj]==1:
                                pos+=1
                        else:
                            if groupaffi[ui][uj]==0:
                                pos+=1
            acc[ts]=float(pos)/total
            accuracy+=acc[ts]
        accuracy/=numwin
       # print str(threshold)+" : "+ str(accuracy)
        if feature==0:
          #print str(threshold)
          print str(accuracy)
    threshold+=0.05