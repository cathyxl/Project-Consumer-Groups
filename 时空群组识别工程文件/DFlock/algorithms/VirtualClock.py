import math
import random

# 逻辑时钟的消息生成模拟
# 计算设备间时间差算法实现

class Msg:
    def __init__(self,n1,n2,t1,t2,transfertime):
        self.n1 = n1
        self.n2 = n2
        self.t1 = t1
        self.t2 = t2
        self.transfertime = transfertime

    def toString(self):
        return str(self.n1)+' sent msg to '+str(self.n2)+' at '+str(self.t1)+','+str(self.n2)+' received at '+str(self.t2)+' '+str(self.transfertime)

"逻辑时钟生成"
def clockProduce(N,F,OFFRANGE,END):
    # offsets = []
    clocklists = {}
    for i in range(N):
        # offsets[i] = random.uniform(0,OFFRANGE)
        clocklists[i] = []
        tmpoff = round(random.uniform(0, OFFRANGE),3)
        print('offset'+str(i)+'='+str(tmpoff))
        lasttp = tmpoff
        while lasttp < END:
            clocklists[i].append(lasttp)
            lasttp += F
    return clocklists
"传递时间生成"
def transferProduce(mu,sigma):
    import numpy as np
    t = round(abs(float(np.random.normal(mu,sigma,1))),3)
    return t
"生成消息传递"
def msgProduce(mu,sigma,clocklists):
    n1 = random.randint(0,N-1)
    n2 = random.randint(0,N-1)
    while n2 == n1:
        n2 = random.randint(0,N-1)
    t1 = round(random.uniform(clocklists[n1][0],clocklists[n1][-1]),3)
    transfertime = transferProduce(mu,sigma)
    # t1 + transfertime - offset1 = t2 - offset2
    # t1 + transfertime + offset1 = t2 + offset2 ???????
    offset1 = clocklists[n1][0]
    offset2 = clocklists[n2][0]
    t2 = round(t1 + transfertime - offset1 + offset2,3)
    msg = Msg(n1,n2,t1,t2,transfertime)
    print(msg.toString())
    return msg
"合并两个interval"
def calrange(I1,I2):
    interval = I1
    if I1[1] < I2[0] or I1[0] > I2[1]:
        return None
    if I1[0] < I2[0]:
        interval[0] = I2[0]
    if I1[1] > I2[1]:
        interval[1] = I2[1]
    return interval
# def dijkstra1(G,v0):
#     glen = len(G)
#     visited = [0] * glen
#     paths = []
#     pathtree = {}
#     path = [0] * glen
#     dist = [[-math.inf,math.inf]] * glen
#     for i in range(glen):
#         visited.append(0)
#         if i != v0 and G[v0][i][0] > -math.inf or G[v0][i][0] < math.inf:
#             dist[i] = G[v0][i]
#             path[i] = v0
#         else:
#             path[i] = -1
#         path[v0] = v0
#         dist[v0] = [0,0]
#
#     visited[v0] = 1
#     for i in range(1, glen):
#         mindis = []
#         mindis.append(math.inf)
#         # mindis = INF
#         u = 0
#
#         for j in range(glen):
#             res = intervalCompare(dist[j],mindis)
#             if visited[j] == 0 :
#                 if res is None:
#                     mindis.append(math.inf)
#                 elif res is True:
#                     mindis[] = dist[j]
#                 u = j
#         visited[u] = 1
#         # 寻找下一个
#         for k in range(glen):
#             if u != k and visited[k] == 0 and mindis + G[u][k] < dist[k]:
#                 dist[k] = mindis + G[u][k]
#                 path[k] = u
#
#     return dist, path
def dijkstra(G,v0,INF=999):
    glen = len(G)
    visited = [0] * glen
    path = [0] * glen
    dist = [INF] * glen
    for i in range(glen):
        visited.append(0)
        if i != v0 and G[v0][i] > 0:
            dist[i] = G[v0][i]
            path[i] = v0
        else:
            dist[i] = INF
            path[i] = -1
        path[v0] = v0
        dist[v0] = 0

    visited[v0] = 1
    for i in range(1, glen):
        mindis = INF
        u = 0
        for j in range(glen):
            if visited[j] == 0 and dist[j] < mindis:
                mindis = dist[j]
                u = j
        visited[u] = 1
        # 寻找下一个
        for k in range(glen):
            if u != k and visited[k] == 0 and mindis+G[u][k] < dist[k]:
                dist[k] = mindis + G[u][k]
                path[k] = u

    return dist, path
def extractpath(path,v,v0):
    l = []
    while v != v0:
        l.append(v)
        v = path[v]
    l.append(v)
    l = list(reversed(l))
    # print(l)
    return l
def Dijkstra(G, v0, INF=999):
    """ 使用 Dijkstra 算法计算指定点 v0 到图 G 中任意点的最短路径的距离
        INF 为设定的无限远距离值
        此方法不能解决负权值边的图
    """
    book = []
    minv = v0

    # 源顶点到其余各顶点的初始路程
    dis = dict((k, INF) for k in G.keys())
    dis[v0] = 0

    while len(book) < len(G):
        book.append(minv)  # 确定当期顶点的距离
        tmpw = 0
        for w in G[minv]:  # 以当前点的中心向外扩散
            if dis[minv] + G[minv][w] < dis[w]:  # 如果从当前点扩展到某一点的距离小与已知最短距离
                dis[w] = dis[minv] + G[minv][w]  # 对已知距离进行更新

        print(minv,tmpw)

        new = INF  # 从剩下的未确定点中选择最小距离点作为新的扩散点
        for v in dis.keys():
            if v in book:
                continue
            if dis[v] < new:
                new = dis[v]
                minv = v
    return dis, book
def intervalCompare(I1,I2):
    if I2[0] == -math.inf and I2[1] == math.inf:
        return False
    if I2[0] >= I1[0] and I2[1] <= I1[1]:
        return True
    elif I2[0] < I1[0] and I2[1] > I1[1]:
        return False
    else:
        return None

# def floyd(G,intervals):
#     glen = len(G)
#     d = {}
#     path = {}
#     for vi in G:
#         if vi not in path:
#             path[vi] = {}
#             d[vi] = {}
#         for vj in G[vi]:
#             if vj not in path:
#                 path[vi][vj] = {}
#                 path[vi][vj][0] = [vj]
#                 d[vi][vj] = {}
#                 d[vi][vj][0] = intervals[vi][vj]
#     for i in range(glen):
#         for j in range(glen):
#             for k in range(glen):
#                 for ii in range(len(d[i][j])):
#                     i1 = d[i][j][ii]
#                     for i2 in d[i][k]:
#                         for i3 in d[k][j]:
#                             tmpinter = calrange(i2,i3)
#                             cpres = intervalCompare(i1, tmpinter)
#                             if cpres is None:
#                                 path[i][j][len(path[i][j])] = i1
#                             elif cpres is True:
#                                 path[i][j][ii] = i2
#
#                     tmpinter = calrange(d[i][k], d[k][j])
#                     cpres = intervalCompare(i1, tmpinter)
#
#                 tmpinter = calrange(d[i][k][],d[k][j])
#                 cpres = intervalCompare(d[i,j],tmpinter)
#                 if cpres is None:
#                     path[i][j][len(path[i][j])] = path[i][j][]
#                 elif cpres is True:
#                     d[i]


def searchAllPath(src,G,path,visited,v,des,length,allPath):
    if visited[v] == 1:
        return
    path[length-1] = v
    if v == des:
        print(path,length)
        allPath[src][des].append(path.copy())
    else:
        # 如果不是终点则向下一顶点寻找
        visited[v] = 1
        for i in range(len(G)):
            if v != i and G[v][i] != 0 and visited[i] != 1:
                searchAllPath(src,G,path,visited,i,des,length+1,allPath)

        visited[v] = 0


def path2range(path,des,intervals):
    tmpinter = [0]*2
    for vi in range(len(path)-1):
        tmpinter[0] += intervals[path[vi]][path[vi+1]][0]
        tmpinter[1] += intervals[path[vi]][path[vi+1]][1]
        if path[vi+1] == des:
            break
    tmpinter[0] = round(tmpinter[0],3)
    tmpinter[1] = round(tmpinter[1],3)
    return tmpinter

if __name__ == '__main__':
    "模拟时钟和消息传递"
    allPath = {}
    INF = 999
    HALFINF = 499
    N = 5  # 设备个数
    F = 1  # 时间间隔
    OFFRANGE = 120  # 最大时间偏移
    END = 600  #
    mu = 0.1
    sigma = 0.5
    MSGNUM = 8  # 消息传递条数
    clocklists = clockProduce(N,F,OFFRANGE,END)
    msglist = []
    for j in range(MSGNUM):
        msglist.append(msgProduce(mu,sigma,clocklists))

    intervals = {}  # {devi:{devj: [lowbound,upbound]}}, devi < devj
    # 初始化intervals,lowbound=-math.inf,upbound= math.inf
    for ni in range(N):
        intervals[ni] = {}
        for nj in range(N):
            if nj != ni:
                intervals[ni][nj] = [- math.inf, math.inf]

    # 根据所有msglist计算出两两设备之间的offset
    for msg in msglist:
        small = msg.n1
        large = msg.n2
        value = round(msg.t1 - msg.t2,3)
        tmpinterval = [value, math.inf]
        if msg.n1 > msg.n2:
            small = msg.n2
            large = msg.n1
            tmpinterval = [- math.inf, - value]
        if calrange(intervals[small][large], tmpinterval) is None:
            print('The offset between '+str(small)+' and '+str(large)+' is None')
        else:
            intervals[small][large] = calrange(intervals[small][large], tmpinterval)

    for ni in range(N):
        for nj in range(N):
            if ni > nj:
                intervals[ni][nj] = [-intervals[nj][ni][1], -intervals[nj][ni][0]]
            if ni < nj:
                print(ni,nj,intervals[ni][nj])


    "图的邻接矩阵"

    vetexDegree = [0]*N
    gAdjMatrix = {}
    for ni in range(N):
        gAdjMatrix[ni] = {}
        for nj in range(N):
            if ni != nj and intervals[ni][nj][0] != -math.inf:
                gAdjMatrix[ni][nj] = 1
                vetexDegree[ni] += 1
                vetexDegree[nj] += 1
            else:
                gAdjMatrix[ni][nj] = 0
    print(gAdjMatrix)

    # 通过两两之间的offset计算出所有设备与0设备的offset
    # G = {}
    # for ni in range(N):
    #     if ni not in G:
    #         G[ni] = {}
    #     for nj in range(N):
    #         if ni != nj:
    #             G[ni][nj] = round(intervals[ni][nj][1] - intervals[ni][nj][0], 3)
    #             # if intervals[ni][nj][1] == math.inf and intervals[ni][nj][0] == -math.inf:
    #             #     G[ni][nj] = 2*INF
    #             # elif intervals[ni][nj][1] == math.inf:
    #             #     G[ni][nj] = round(INF - intervals[ni][nj][0], 3)
    #             # elif intervals[ni][nj][0] == -math.inf:
    #             #     G[ni][nj] = round(intervals[ni][nj][1] + INF, 3)
    #             # else:
    #             #     G[ni][nj] = round(intervals[ni][nj][1] - intervals[ni][nj][0], 3)
    # print(G)
    print("GAP:")

    # dist, path = dijkstra(G, 0)
    # for ni in range(1,N):
    #     tmppath = extractpath(path,ni,0)
    #     tmpinter = [0,0]
    #     for vi in range(len(tmppath)-1):
    #         tmpinter[0] += intervals[tmppath[vi]][tmppath[vi+1]][0]
    #         tmpinter[1] += intervals[tmppath[vi]][tmppath[vi+1]][1]
    #     tmpinter[0] = round(tmpinter[0],3)
    #     tmpinter[1] = round(tmpinter[1],3)
    #     print(0,ni,tmppath,tmpinter,round(tmpinter[1]-tmpinter[0],3))
    "以最大出入度的顶点为参考点"
    src = vetexDegree.index(max(vetexDegree))
    print(src)
    allPath[src] = {}
    avelength = 0
    avenum = 0
    infnum = 0
    for vj in range(N):
        if vj == src:
            continue
        path = [0] * N
        visited = [0] * N
        if vj not in allPath[src]:
            allPath[src][vj] = []

        print('path '+str(src)+'->'+str(vj))
        searchAllPath(src,gAdjMatrix,path,visited,src,vj,1,allPath)
        tmpinter1 = [-math.inf,math.inf]
        for p in allPath[src][vj]:
            tmprange = path2range(p, vj, intervals)
            if calrange(tmpinter1,tmprange) is not None:
                tmpinter1 = calrange(tmpinter1,tmprange)

        path = [0] * N
        visited = [0] * N
        if vj not in allPath:
            allPath[vj] = {}
        if src not in allPath[vj]:
            allPath[vj][src] = []

        print('path ' + str(vj) + '->' + str(src))
        searchAllPath(vj,gAdjMatrix, path, visited, vj, src, 1,allPath)
        tmpinter2 = [-math.inf, math.inf]
        for p in allPath[vj][src]:
            tmprange = path2range(p, src, intervals)
            if calrange(tmpinter2, tmprange) is not None:
                tmpinter2 = calrange(tmpinter2,tmprange)
        tmpinter2 = [- (tmpinter2[1]), -(tmpinter2[0])]
        tmprange = calrange(tmpinter1,tmpinter2)
        if tmprange[0] == - math.inf:
            infnum += 1
        if tmprange[1] == math.inf:
            infnum += 1
        if tmprange[0] != -math.inf and tmprange[1] != math.inf:
            avelength += tmprange[1] - tmprange[0]
            avenum += 1
        print(src, vj, tmprange)
    if avenum != 0:
        avelength /= avenum
        avelength = round(avelength,3)
    else:
        avelength = math.inf
    print(infnum,avelength)










