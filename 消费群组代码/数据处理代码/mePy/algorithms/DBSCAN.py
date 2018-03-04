def _eps_neighborhood(p, q, eps):
    pass

def _region_query(simarray, setPoints, p, eps):
    seeds = []
    for q in setPoints:
        if simarray[p][q] < eps and p != q:
            seeds.append(q)
    # print(len(seeds))
    return seeds


def _expand_cluster(simarray, setPoints, p, classifications, noises, eps, min_points):
    # start = time.clock()
    points = []
    seeds = _region_query(simarray,setPoints, p, eps)
    if len(seeds) < min_points-1:
        noises.append(p)
        classifications[p] = -1
        return False
    else:
        points.append(p)
        classifications[p] = 1
        for seed in seeds:
            points.append(seed)
            classifications[seed] = 1
        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(simarray, setPoints, current_point, eps)
            if len(results) >= min_points-1:
                for result_point in results:
                    if classifications[result_point] == 0:
                        seeds.append(result_point)
                        classifications[result_point] = 1
                        points.append(result_point)
            seeds = seeds[1:]
        # clusters.append(cluster)
        # end = time.clock()
        # print(end - start)
        return points

def dbscan(simarray,setPoints, eps, minPoints):
    clusters = []
    noises = []
    classifications ={}
    for pt in setPoints:
        classifications[pt] = 0
    for pt in setPoints:
        if classifications[pt] == 0:
            points = _expand_cluster(simarray,setPoints, pt, classifications, noises, eps, minPoints)
            if points:
                clusters.append(points)
    # s=""
    # for p in noises:
    #     s+=p.toString()+' '
    # print(s)
    # s=""
    # for c in clusters:
    #     s += c.toString()+'\n'
    # print(s)
    return [clusters, noises]
