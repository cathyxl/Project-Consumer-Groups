def djcluster(simarray, setPoints, eps, minPoints):
    listClusters = []
    listNoises = []
    for p in setPoints:
        # 计算N(p)，即p点的neighborhood
        np = computeNeighborhood(p, simarray, setPoints, minPoints, eps)
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
                if len(list(set(np).intersection(set(cluster)))) > 0:
                    np = list(set(np).union(set(cluster)))
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
    return [listClusters, listNoises]


"Compute Neighborhood"


def computeNeighborhood(p, simarray, setPoints, minPoints, eps):
    pointOfCluster = []
    for q in setPoints:
        if simarray[p][q] < eps and p != q:
            pointOfCluster.append(q)
    if len(pointOfCluster) < minPoints:
        return None
    else:
        return pointOfCluster
