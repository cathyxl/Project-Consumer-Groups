from model import Position, Flock
import algorithms.DBSCAN as DBSCAN
import random
import algorithms.DJcluster as DJCluster
import csv
import time
import numpy as np
import algorithms.Group as Group
PATH = 'D:\\python_source\\DFlock\\'

def rmflock(fid, flocklist):
    for flock in flocklist:
        if flock.id == fid:
            flocklist.remove(flock)


def rtFlockDetect(IDs, gama, delta, pointMatrix, eps,minPoints,typeDistance,theta,act_flocks,pot_flocks, flockmap,curid,spatialType):
    dis_flocks = []
    # curid = 0
    tmpcurid = curid

    draw_array = np.zeros((len(pointMatrix), len(IDs)))
    di = 0
    for t in pointMatrix:
        flockmap[t] = []
        rm_actids = []
        rm_potids = []
        for pot_flock in pot_flocks:
            if pot_flock.duration >= gama:
                act_flocks.append(pot_flock)
                rm_potids.append(pot_flock.id)
            if pot_flock.lastseen >= delta:
                rm_potids.append(pot_flock.id)
        for fid in rm_potids:
            rmflock(fid, pot_flocks)

        for act_flock in act_flocks:
            if act_flock.lastseen >= delta:
                rm_actids.append(act_flock.id)
                dis_flocks.append(act_flock)
        for fid in rm_actids:
            rmflock(fid, act_flocks)

        if spatialType == 0:
            result = DBSCAN.dbscan(pointMatrix[t], eps, minPoints)
        elif spatialType == 1:
            result = DJCluster.djcluster(pointMatrix[t], typeDistance, eps, minPoints)

        clusters = result[0]
        listPIds = result[2]
        act_flockids = set()
        pot_flockids = set()
        # print(str(t)
        for cluster in clusters:
            max_value = 0
            max_id = -1
            # print(cluster.toString())

            # 计算与cluster相似度最大的flock
            for flock in act_flocks:
                tmp = jaccardSimilarity(cluster, flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp

            for flock in pot_flocks:
                tmp = jaccardSimilarity(cluster, flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp

            # 如果没有匹配的flock则新生成一个potential flock
            if max_id == -1:
                pot_flocks.append(Flock(curid, 0, 0, cluster.points))
                pot_flockids.add(curid)
                curid += 1
            # 反之加入相似度最大的flock
            else:
                for flock in act_flocks:
                    if flock.id == max_id:
                        act_flockids.add(flock.id)
                        flock.points = cluster.points
                        flock.lastseen = 0
                for flock in pot_flocks:
                    if flock.id == max_id:
                        pot_flockids.add(flock.id)
                        flock.points = cluster.points
                        flock.lastseen = 0

        # 对于有新加入cluster的flock，duration加1，对于无加入的lastseen加1
        for flock in act_flocks:
            if flock.id in act_flockids:
                flock.duration += 1
            else:
                flock.lastseen += 1
        for flock in pot_flocks:
            if flock.id in pot_flockids:
                flock.duration += 1
            else:
                flock.lastseen += 1

        draw_file.write('\'' + str(t) + '\'')

        dj = 0
        for pid in IDs:
            assigned = 0

            for flock in act_flocks:
                if flock.idInFlock(pid):
                    if assigned == 0:
                        draw_array[di][dj] = flock.id
                        dj += 1
                        draw_file.write(',' + str(flock.id))
                        assigned = 1
            for flock in pot_flocks:
                if flock.idInFlock(pid):
                    if assigned == 0:
                        draw_array[di][dj] = flock.id
                        dj += 1
                        draw_file.write(',' + str(flock.id))
                        assigned = 1
            if assigned == 0:
                if pid in listPIds:
                    draw_file.write(',-1')
                    draw_array[di][dj] = -1
                    dj += 1
                else:
                    draw_file.write(',-2')
                    draw_array[di][dj] = -2
                    dj += 1
        di += 1
        draw_file.write('\n')
        for flock in act_flocks:
            flockmap[t].append(flock.flock2Cluster())
        for flock in pot_flocks:
            flockmap[t].append(flock.flock2Cluster())
    if curid > tmpcurid:
        curid -= 1
    return draw_array, flockmap, act_flocks, pot_flocks, curid

def flockDetect(IDs,gama, delta, pointMatrix, eps, minPoints, typeDistance, theta):
    flockmap = {}
    act_flocks = []
    pot_flocks = []
    dis_flocks = []
    curid = 0
    flock_file = open(PATH+'flock_file.txt','w')
    cluster_file = open(PATH+'cluster_file.txt','w')
    draw_array = np.zeros((len(pointMatrix), len(IDs)))
    for t in pointMatrix:
        flockmap[t]=[]
        rm_actids=[]
        rm_potids=[]
        for pot_flock in pot_flocks:
            if pot_flock.duration >= gama:
                act_flocks.append(pot_flock)
                rm_potids.append(pot_flock.id)
            if pot_flock.lastseen >= delta:
                rm_potids.append(pot_flock.id)
        for fid in rm_potids:
            rmflock(fid,pot_flocks)

        for act_flock in act_flocks:
            if act_flock.lastseen >= delta:
                rm_actids.append(act_flock.id)
                dis_flocks.append(act_flock)
        for fid in rm_actids:
            rmflock(fid,act_flocks)

        # result = DJCluster.djcluster(pointMatrix[t], typeDistance,eps, minPoints)
        result = DBSCAN.dbscan(pointMatrix[t],eps,minPoints)
        clusters = result[0]
        listPIds = result[2]
        act_flockids=set()
        pot_flockids=set()
        # print(str(t))
        cluster_file.write(str(t)+'\n')
        for cluster in clusters:
            max_value = 0
            max_id = -1
            cluster_file.write(cluster.toString()+'\n')
            # print(cluster.toString())

            # 计算与cluster相似度最大的flock
            for flock in act_flocks:
                tmp = jaccardSimilarity(cluster, flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp

            for flock in pot_flocks:
                tmp = jaccardSimilarity(cluster, flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp

            # 如果没有匹配的flock则新生成一个potential flock
            if max_id == -1:
                pot_flocks.append(Flock(curid,0,0,cluster.points))
                pot_flockids.add(curid)
                curid += 1
            # 反之加入相似度最大的flock
            else:
                for flock in act_flocks:
                    if flock.id == max_id:
                        act_flockids.add(flock.id)
                        flock.points = cluster.points
                        flock.lastseen = 0
                for flock in pot_flocks:
                    if flock.id == max_id:
                        pot_flockids.add(flock.id)
                        flock.points = cluster.points
                        flock.lastseen = 0

        # 对于有新加入cluster的flock，duration加1，对于无加入的lastseen加1
        for flock in act_flocks:
            if flock.id in act_flockids:
                flock.duration += 1
            else:
                flock.lastseen += 1
        for flock in pot_flocks:
            if flock.id in pot_flockids:
                flock.duration += 1
            else:
                flock.lastseen += 1

        draw_file.write('\''+str(t)+'\'')
        flock_file.write(str(t))
        di=0
        for pid in IDs:
            assigned = 0
            dj=0
            for flock in act_flocks:
                if flock.idInFlock(pid):
                    if assigned == 0:

                        draw_array[di][dj] = flock.id
                        dj += 1
                        draw_file.write(',' + str(flock.id))
                        assigned = 1
            for flock in pot_flocks:
                if flock.idInFlock(pid):
                    if assigned == 0:

                        draw_array[di][dj] = flock.id
                        dj += 1
                        draw_file.write(',' + str(flock.id))
                        assigned = 1
            if assigned == 0:
                if pid in listPIds:
                    draw_file.write(',-1')
                    draw_array[di][dj] = -1
                    dj+=1
                else:
                    draw_file.write(',-2')
                    draw_array[di][dj] = -2
                    dj += 1
        di+=1
        draw_file.write('\n')

        for flock in act_flocks:
            flockmap[t].append(flock.flock2Cluster())
            flock_file.write(','+flock.toString())
        for flock in pot_flocks:
            flockmap[t].append(flock.flock2Cluster())
            flock_file.write(','+flock.toString())
        flock_file.write('\n')

    cluster_file.close()
    flock_file.close()
    return [draw_array,flockmap]

def jaccardSimilarity(cluster,flock):
    flockIds = set()
    clusterIds = set()
    for fp in flock.points:
        flockIds.add(fp.id)
    for cp in cluster.points:
        clusterIds.add(cp.id)
    interse = list(clusterIds.intersection(flockIds))
    union = list(clusterIds.union(flockIds))
    return len(interse) / len(union)

def cluster2matrix(clusters):
    clustersMatrix={}
    ids=[]
    for cluster in clusters:
        for c in cluster:
            ids.append(c)
    for ci in ids:
        if ci not in clustersMatrix:
            clustersMatrix[ci] = {}
        for cj in ids:
            clustersMatrix[ci][cj] = 0

    for cluster in clusters:
        for ci in cluster:
            for cj in cluster:
                clustersMatrix[ci][cj]=1
    return [clustersMatrix,ids]

def flock2matrix(ids,flocks):
    clustersMatrix={}
    for ci in ids:
        if ci not in clustersMatrix:
            clustersMatrix[ci]={}
        for cj in ids:
            clustersMatrix[ci][cj]=0
    for flock in flocks:
        for pointi in flock:
            for pointj in flock:
                if pointi in ids and pointj in ids:
                    clustersMatrix[pointi][pointj]=1
    return clustersMatrix

def Fmeasure(ground, flocks):
    groupresult = cluster2matrix(ground)
    groundMap = groupresult[0]
    ids = groupresult[1]
    flockMap = flock2matrix(ids, flocks)
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for ci in flockMap:
        for cj in flockMap:
            if flockMap[ci][cj] == 1:
                if groundMap[ci][cj] == 1:
                    tp += 1
                else:
                    fp += 1
            else:
                if groundMap[ci][cj] == 0:
                    tn += 1
                else:
                    fn += 1
    # print(tp,fp,tn,fn)
    if (2*tp+fp+fn) == 0:
        return None
    else:
        return float(2*tp/(2*tp+fp+fn))

    pass

def FAA(groudmap,flockmap):
    faa = 0.0
    k = 0
    for t in groudmap:
        flocks = flockmap[t]
        ground = groudmap[t]
        # print(t)
        if Fmeasure(ground, flocks) is None:
            k += 1
        else:
            faa += Fmeasure(ground, flocks)
    faa /= (len(flockmap)-k)

    return faa

def NFDA(groudmap,flockmap):
    nfda = 0
    k = 0
    for t in flockmap:
        flen = len(flockmap[t])
        if flen == 0:
            k += 1
        glen = len(groudmap[t])
        if flen == glen and glen != 0:
            nfda += 1
    nfda /= (len(flockmap.keys())-k)
    return nfda

"处理flocks"
def flockProcessing(flockmap):
    for t in flockmap:
        pointids=[]
        for flock in flockmap[t]:
            rmpoints=[]
            for point in flock:
                if point in pointids:
                    rmpoints.append(point)
                else:
                    pointids.append(point)
            for point in rmpoints:
                flock.remove(point)

def list2str(cluster):
    if len(cluster)==0:
        return ""
    s='('+str(cluster[0])
    for c in range(1,len(cluster)):
        s+=','+str(cluster[c])
    s+=')'
    return s

draw_file = open(PATH+'draw_file.csv','w')

if __name__ == '__main__':
    start = time.clock()
    # parameter
    typeDistance = 0
    minPoints = 2
    t0 = 0
    gama = 4
    delta = 2
    theta = 0.4
    eps = 3.72
    epsfloor = 1
    epsroof = 6
    epsstep = 0.5

    GROUNDTRUTH = 3

    "读数据"
    # filepath = PATH+'data\\process_ATC_1_1200_1.csv'
    # filepath = PATH + 'data\\interpofiles_1\\1_interpolate_ATC_1_1200.csv'
    filepath = PATH + 'data\\5_sample_ATC_1_1200.csv'
    pointmatrix = {}
    csv_data = csv.reader(open(filepath, 'r'), delimiter=',')
    for row in csv_data:
        ts = row[0]
        if ts not in pointmatrix:
            pointmatrix[ts] = []
        p = Position(row[1], float(row[2]) / 1000, float(row[3]) / 1000, float(row[4]) / 1000, float(row[5]) / 1000,
                     row[6], row[7])
        # p = Position(row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]),
        #              row[6], row[7])
        pointmatrix[ts].append(p)

    "读取参与人员"
    draw_file.write('\'00000000\'')
    IDs = []
    groupfile = open(PATH + 'data\\group.txt', 'r')
    lines = groupfile.readlines()
    for line in lines:
        fields = line.split(' ')
        for i in range(len(fields)):
            pi = int(fields[i])
            if pi not in IDs:
                draw_file.write(',\'' + str(pi) + '\'')
                IDs.append(str(pi))
    draw_file.write('\n')

    print(len(IDs))
    print(IDs)
    "获得实时分组"
    groupmap = Group.getRtGroup(filepath)

    eps = epsfloor
    maxfaa = 0.0
    maxeps = 0.0
    file = open(PATH+'data\\test19.txt','w')
    while eps <= epsroof:
        "flock检测"
        result = flockDetect(IDs, gama, delta, pointmatrix, eps, minPoints, typeDistance, theta)
        "处理flock结果"
        flockmap = result[1]
        flockProcessing(flockmap)
        "计算准确度"
        nfda = NFDA(groupmap, flockmap)
        faa = FAA(groupmap, flockmap)
        # print(eps)
        # print('NFDA=' + str(nfda))
        # print('FAA=' + str(faa))
        if maxfaa < faa:
            maxfaa = faa
            maxeps = eps
        file.write(str(eps) + ',' + str(faa) + ',' + str(nfda) + '\n')
        eps += epsstep


    print(maxeps, maxfaa)
    # "flock检测"
    # print("CLUSTERING")
    # testfile = open(PATH + 'test.txt', 'w')
    # result = flockDetect(IDs, gama, delta, pointmatrix, eps, minPoints, typeDistance, theta)
    # draw_file.close()
    #
    # "处理flock结果"
    # flockmap = result[1]
    # flockProcessing(flockmap)
    #
    # "计算准确度"
    # print('NFDA=' + str(NFDA(groupmap, flockmap)))
    # print('FAA=' + str(FAA(groupmap, flockmap)))
    #
    # end = time.clock()
    # print(end - start)


