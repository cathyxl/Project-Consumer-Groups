from position import Position, Cluster, Flock
import algorithms.Accuracy as Accuracy
"用于距离矩阵已经存在的数据"

"Dj-Clustering Algorithm"
PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'

def DjCluster(setPoints, dismatrix,typeDistance, eps, minPoints, t0):
    # Lista clusters
    listClusters = []
    # Puntos ruido
    listNoises = []

    # Para todos los puntos del set
    for p in setPoints:
        # 计算N(p)，即p点的neighborhood
        np = computeNeighborhood(p, setPoints, typeDistance,dismatrix, minPoints, eps, t0)

        # DEBUG
        # if np is not None:
        #     print(np.toString())
        # END DEBUG

        # 如果N(p)为空则定义为noise
        if np is None:
            listNoises.append(p)  # etiquetamos el punto como ruido
        else:
            clusters = []
            for cluster in listClusters:
                if np.hasCommon(cluster):
                    np.mergeCluster(cluster)
                else:
                    clusters.append(cluster)
            listClusters.clear()
            for cluster in clusters:
                listClusters.append(cluster)
            listClusters.append(np)
    # DEBUG
    # print("Clusters:")
    # for cluster in listClusters:
    #     print(cluster.toString())
    # print("Noises:")
    # for p in listNoises:
    #     print(p.toString())
    # END DEBUG
    return listClusters


"Compute Neighborhood"


def computeNeighborhood(p, setPoints, typeDistance, dismatrix, minPoints, eps, t0):
    pointsOfCluster = []
    for q in setPoints:
        if typeDistance == 0:
            if p.is_in_neighborhoodByEUSimple(q, eps):
                pointsOfCluster.append(q)
        elif typeDistance == 1:
            if p.is_in_neighborhoodEURelativeSpeed(q, eps):
                pointsOfCluster.append(q)
        elif typeDistance == 2:
            if p.is_in_neighborhoodT0Reachable(q, t0):
                pointsOfCluster.append(q)
        elif typeDistance == 3:
            if dismatrix[t0][p.id][q.id] < eps:
                pointsOfCluster.append(q)
    if len(pointsOfCluster) < minPoints:
        return None
    else:
        return Cluster(p, pointsOfCluster)

def rmflock(fid,flocklist):
    for flock in flocklist:
        if flock.id == fid:
            flocklist.remove(flock)



def flockDetect(flock_file,list_pos, gama, delta, simmap, eps, minPoints, typeDistance,theta):
    flockmap = {}
    act_flocks = []
    pot_flocks = []
    dis_flocks = []
    curid = 0
    # flock_file = open(PATH+'behavior\\'+str(GROUNDTRUTH)+'_flock_file.txt','w')
    for t in simmap:
        flockmap[t] = []
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

        clusters = DjCluster(list_pos,simmap, typeDistance,eps, minPoints, t)
        act_flockids=set()
        pot_flockids=set()
        print(str(t))
        for cluster in clusters:
            max_value = 0
            max_id = -1
            print(cluster.toString())

            #计算与cluster相似度最大的flock
            for flock in act_flocks:
                tmp = jaccardSimilarity(cluster,flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp

            for flock in pot_flocks:
                tmp = jaccardSimilarity(cluster, flock)
                if tmp > max_value and tmp >= theta:
                    max_id = flock.id
                    max_value = tmp
            # print(max_value,max_id)

            #如果没有匹配的flock则新生成一个potential flock
            if max_id == -1:
                pot_flocks.append(Flock(curid,0,0,cluster.points))
                pot_flockids.add(curid)
                curid += 1
            #反之加入相似度最大的flock
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
        #对于有新加入cluster的flock，duration加1，对于无加入的lastseen加1
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
        flock_file.write(str(t)+' ')

        for flock in act_flocks:
            flockmap[t].append(flock.flock2Cluster())
            flock_file.write(flock.toString())


        for flock in pot_flocks:
            flockmap[t].append(flock.flock2Cluster())
            flock_file.write(flock.toString())
        flock_file.write('\n')

    return flockmap

def jaccardSimilarity(cluster,flock):
    interse=list(set(cluster.points).intersection(set(flock.points)))
    union=list(set(cluster.points).union(set(flock.points)))
    return len(interse)/len(union)

def cluster2matrix(clusters):
    clustersMatrix={}
    ids=[]
    for cluster in clusters:
        for c in cluster:
            ids.append(c)
    for ci in ids:
        if ci not in clustersMatrix:
            clustersMatrix[ci]={}
        for cj in ids:
            clustersMatrix[ci][cj]=0

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



typeDistance=3
minPoints=1
t0=0
gama=4
delta=2
theta=0.4
eps=9

# GROUNDTRUTH = 3
# us=[1,2,3,4,5,6,7,8,9]
# cluster_o={1:[1,2,3,4,5],2:[6,7,8,9]}
#
# GROUNDTRUTH = 7
# us=[1,2,3,4,5,6,7,9,11]
# cluster_o={1:[1,2,3,4],2:[5,6,7],3:[9,11]}

# GROUNDTRUTH = 10
# us=[1,2,3,4,5,6,7,8,9,11]
# cluster_o={1:[1,2],2:[3,4],3:[5,6,7],4:[8,9,11]}

GROUNDTRUTH = 11
us=[1,2,3,4,5,6,7,9,11]
cluster_o={1:[1,2,3,4],2:[5,6,7],3:[9,11]}



USRNUM=len(us)
dismatrix = {}
pfile = open(PATH + 'behavior\\DisparityMatrix-'+str(GROUNDTRUTH)+'.txt','r')
plines = pfile.readlines()
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
        ui = us[i]
        if ui not in dismatrix[ts]:
            dismatrix[ts][ui] = {}
        for j in range(len(fields)):
            uj = us[j]
            dismatrix[ts][ui][uj] = float(fields[j])
        i += 1
pfile.close()


list_pos = []
for u in us:
    list_pos.append(Position(u))

# CLUSTERING
print("CLUSTERING")
flock_file = open(PATH+'behavior\\'+str(GROUNDTRUTH)+'_flock_file.txt','w')

flockmap=flockDetect(flock_file,list_pos, gama, delta, dismatrix, eps, minPoints, typeDistance,theta)
groundfile = PATH+'groundtruth\\'+str(GROUNDTRUTH)+'.txt'
groupaffi = Accuracy.loadGround(groundfile,us)
"处理flock结果"
flockProcessing(flockmap)
groundmap = {}

for ts in flockmap:
    groundmap[ts] = groupaffi
    flockmap[ts] = flock2matrix(us, flockmap[ts])
faa = Accuracy.FAA(us,groundmap,flockmap)
flock_file.write('faa='+str(faa))
flock_file.close()
print('faa='+str(faa))