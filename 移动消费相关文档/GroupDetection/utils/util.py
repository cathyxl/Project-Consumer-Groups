def cluster2Matrix(clusters):
    clustersMatrix = {}
    ids = []
    # print(clusters)
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
                clustersMatrix[ci][cj] = 1
    return [clustersMatrix, ids]
