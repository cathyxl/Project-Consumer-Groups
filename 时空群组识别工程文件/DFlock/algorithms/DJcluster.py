from model import Cluster,Position
import csv
import time

def djcluster(setPoints, typeDistance, eps, minPoints):

    listClusters = []
    listNoises = []
    listPIds = []
    neighborhoods =[]
    for p in setPoints:
        # 计算N(p)，即p点的neighborhood
        listPIds.append(p.id)
        np = computeNeighborhood(p, setPoints, typeDistance, minPoints, eps)

        # DEBUG
        # if np is not None:
        #     print(np.toString())
        # END DEBUG

        # 如果N(p)为空则定义为noise
        if np is None:
            listNoises.append(p)
    #     else:
    #         neighborhoods.append(np)
    #
    # nn = len(neighborhoods)
    # merged = nn*[0]
    # for i in range(nn):
    #     if merged[i] == 1:
    #         continue
    #     merged[i]=1
    #     for j in range(i,nn):
    #         if neighborhoods[i].hasCommon(neighborhoods[j]):
    #             neighborhoods[i].mergeCluster(neighborhoods[j])
    #             merged[j] = 1
    #     listClusters.append(neighborhoods[i])

        else:

            clusters = []
            for i in range(len(listClusters)):
                cluster = listClusters[i]
                if np.hasCommon(cluster):
                    np.mergeCluster(cluster)
                else:
                    clusters.append(cluster)
            listClusters.clear()
            for cluster in clusters:
                listClusters.append(cluster)
            listClusters.append(np)

    # s = ""
    # for p in listNoises:
    #     s += p.toString()+' '
    # print(s)
    # s = ""
    # for c in listClusters:
    #     s += c.toString()+'\n'
    # print(s)
    return [listClusters, listNoises, listPIds]


"Compute Neighborhood"


def computeNeighborhood(p, setPoints, typeDistance, minPoints, eps):
    pointsOfCluster = []
    for q in setPoints:
        if typeDistance == 0:
            if p.is_in_neighborhoodByEUSimple(q, eps):
                pointsOfCluster.append(q)
        elif typeDistance == 1:
            if p.is_in_neighborhoodEURelativeSpeed(q, eps):
                pointsOfCluster.append(q)
    if len(pointsOfCluster) < minPoints:
        return None
    else:
        return Cluster(None,pointsOfCluster)


# typeDistance = 0
# minPoints = 4
# t0=0
# eps= 1
# PATH = 'D:\\python_source\\DFlock\\'
# filepath=PATH+'a.csv'
#
# # filepath = PATH+'data\\process_ATC_1_1200_1.csv'
# pointmatrix = []
# csv_data = csv.reader(open(filepath,'r'), delimiter=',')
# for row in csv_data:
#     # ts = row[0]
#     # if ts not in pointmatrix:
#     #     pointmatrix[ts] = []
#     # print(row[1],row[2])
#     p = Position(row[0],float(row[1]),float(row[2]),0.0,0.0,0.0,0.0)
#     # p = Position(row[1], float(row[2])/1000, float(row[3])/1000, float(row[4])/1000, float(row[5])/1000, row[6], row[7])
#     pointmatrix.append(p)
# start = time.clock()
#
# djcluster(pointmatrix,typeDistance,eps,minPoints)
#
# end = time.clock()
# print(end-start)
