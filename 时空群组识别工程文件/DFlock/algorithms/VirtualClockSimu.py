import math
import random
# 模拟消息生成和传递
# 计算设备间时间差范围
# 选择加入边，包括随机选择，最大最小度选择，以及缩点后随机选择，并模拟结果

N = 10
DFN = [0]*N
LOW = [0]*N
stack = [0]*N
visited = [0]*N
Belong = [0]*N
G = {}
global index
global top
global bcnt


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

def msgProduce1(n1,n2,mu,sigma,clocklists):
    t1 = round(random.uniform(clocklists[n1][0], clocklists[n1][-1]), 3)
    transfertime = transferProduce(mu, sigma)
    offset1 = clocklists[n1][0]
    offset2 = clocklists[n2][0]
    t2 = round(t1 + transfertime - offset1 + offset2, 3)
    msg = Msg(n1, n2, t1, t2, transfertime)
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

def extractpath(path,v,v0):
    l = []
    while v != v0:
        l.append(v)
        v = path[v]
    l.append(v)
    l = list(reversed(l))
    # print(l)
    return l
def intervalCompare(I1,I2):
    if I2[0] == -math.inf and I2[1] == math.inf:
        return False
    if I2[0] >= I1[0] and I2[1] <= I1[1]:
        return True
    elif I2[0] < I1[0] and I2[1] > I1[1]:
        return False
    else:
        return None
def searchAllPath(src,G,path,visited,v,des,length,allPath):
    if visited[v] == 1:
        return
    path[length-1] = v
    if v == des:
        # print(path,length)
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
def calDeviation(G, intervals):
    "以最大出入度的顶点为参考点"
    allPath = {}
    gAdjMatrix = {}
    vetexDegree = [0]*N

    for ni in range(N):
        gAdjMatrix[ni] = {}
        for nj in range(N):
            if nj in G[ni]:
                gAdjMatrix[ni][nj] = 1
                vetexDegree[ni] += 1
                vetexDegree[nj] += 1
            else:
                gAdjMatrix[ni][nj] = 0

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

        print('path ' + str(src) + '->' + str(vj))
        searchAllPath(src, gAdjMatrix, path, visited, src, vj, 1, allPath)
        tmpinter1 = [-math.inf, math.inf]
        for p in allPath[src][vj]:
            tmpinter2 = path2range(p, vj, intervals)
            if calrange(tmpinter1, tmpinter2) is not None:
                tmpinter1 = calrange(tmpinter1, tmpinter2)

        path = [0] * N
        visited = [0] * N
        if vj not in allPath:
            allPath[vj] = {}
        if src not in allPath[vj]:
            allPath[vj][src] = []

        print('path ' + str(vj) + '->' + str(src))
        searchAllPath(vj, gAdjMatrix, path, visited, vj, src, 1, allPath)
        tmpinter2 = [-math.inf, math.inf]
        for p in allPath[vj][src]:
            tmprange = path2range(p, src, intervals)
            if calrange(tmpinter2, tmprange) is not None:
                tmpinter2 = calrange(tmpinter2, tmprange)
        tmpinter2 = [- (tmpinter2[1]), -(tmpinter2[0])]
        tmprange = calrange(tmpinter1, tmpinter2)
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
        avelength = round(avelength, 3)
    else:
        avelength = math.inf
    print(infnum, avelength)
    return infnum,avelength

def msgprocess(msg,intervals):
    small = msg.n1
    large = msg.n2
    value = round(msg.t1 - msg.t2, 3)
    tmpinterval = [value, math.inf]
    if msg.n1 > msg.n2:
        small = msg.n2
        large = msg.n1
        tmpinterval = [- math.inf, - value]
    if calrange(intervals[small][large], tmpinterval) is None:
        print('The offset between ' + str(small) + ' and ' + str(large) + ' is None')
    else:
        intervals[small][large] = calrange(intervals[small][large], tmpinterval)
    return intervals

def tarjan(u):
    global index
    global top
    global bcnt
    index += 1
    DFN[u] = LOW[u] = index
    top += 1
    stack[top] = u
    # print(u, index, top, stack)
    visited[u] = 1
    for vj in G[u]:
        if DFN[vj] == 0:
            tarjan(vj)
            LOW[u] = min(LOW[u], LOW[vj])
        elif visited[vj] == 1:
            LOW[u] = min(LOW[u], DFN[vj])
    if LOW[u] == DFN[u]:
        # print('最高节点：'+str(u))
        bcnt += 1
        while True:
            j = stack[top]
            print(str(j)+' ', end='')
            top -= 1
            visited[j] = 0
            Belong[j] = bcnt

            if j == u:
                print('\n', end='')
                break

def selectEdge1(indegree,outdegree,shrmap):
    tmpvs = []
    tmpus = []
    addu = -1
    addv = -1
    for vi in indegree:
        if indegree[vi] == 0:
            tmpvs.append(vi)
    for vi in outdegree:
        if outdegree[vi] == 0:
            tmpus.append(vi)

    if len(tmpvs) == 0:
        addu = tmpus[random.randint(0, len(tmpus) - 1)]
        if len(shrmap[addu]) > 1:
            addu = shrmap[addu][random.randint(0, len(shrmap[addu]) - 1)]
        else:
            addu = shrmap[addu][0]
        while addv == addu:
            addv = random.randint(0, N - 1)
    elif len(tmpus) == 0:
        addv = tmpvs[random.randint(0, len(tmpvs) - 1)]
        if len(shrmap[addv]) > 1:
            addv = shrmap[addv][random.randint(0, len(shrmap[addv]) - 1)]
        else:
            addv = shrmap[addv][0]
        while addu == addv:
            addu = random.randint(0, N - 1)
    else:
        addv = tmpvs[random.randint(0, len(tmpvs)-1)]
        if len(shrmap[addv]) > 1:
            addv = shrmap[addv][random.randint(0, len(shrmap[addv])-1)]
        else:
            addv = shrmap[addv][0]
        addu = tmpus[random.randint(0, len(tmpus)-1)]
        if len(shrmap[addu]) > 1:
            addu = shrmap[addu][random.randint(0, len(shrmap[addu])-1)]
        else:
            addu = shrmap[addu][0]
    return addu, addv

def selectEdge2(indegree,outdegree,shrmap,inde,outde):
    addv = -1
    addu = -1
    if 0 not in indegree:
        maxde = -1
        maxdev = -1
        for vi in outdegree:
            if outdegree[vi] == 0:
                if indegree[vi] > maxde:
                    maxde = indegree[vi]
                    maxdev = vi
        addu = maxdev
        if len(shrmap[addu]) > 1:
            maxsi = -1
            maxsid = -1
            for si in shrmap[addu]:
                if inde[si] > maxsid:
                    maxsid = inde[si]
                    maxsi = si
            addu = maxsi
        else:
            addu = shrmap[addu][0]
        while addv == addu:
            addv = random.randint(0,N-1)
    elif 0 not in outdegree:
        maxde = -1
        maxdev = -1
        for vi in indegree:
            if indegree[vi] == 0:
                if outdegree[vi] > maxde:
                    maxde = outdegree[vi]
                    maxdev = vi
        addv = maxdev
        if len(shrmap[addv]) > 1:
            maxsi = -1
            maxsid = -1
            for si in shrmap[addv]:
                if inde[si] > maxsid:
                    maxsid = inde[si]
                    maxsi = si
            addv = maxsi
        else:
            addv = shrmap[addv][0]
        while addu == addv:
            addu = random.randint(0, N - 1)
    else:
        maxde = -1
        maxdev = -1

        for vi in indegree:
            if indegree[vi] == 0:
                if outdegree[vi] > maxde:
                    maxde = outdegree[vi]
                    maxdev = vi
        addv = maxdev
        if len(shrmap[addv]) > 1:
            maxsi = -1
            maxsid = -1
            for si in shrmap[addv]:
                if outde[si] > maxsid:
                    maxsid = outde[si]
                    maxsi = si
            addv = maxsi
        else:
            addv = shrmap[addv][0]

    maxde = -1
    maxdev = -1
    for vi in outdegree:
        if outdegree[vi] == 0:
            if indegree[vi] > maxde:
                maxde = indegree[vi]
                maxdev = vi
    addu = maxdev
    if len(shrmap[addu]) > 1:
        maxsi = -1
        maxsid = -1
        for si in shrmap[addu]:
            if inde[si] > maxsid:
                maxsid = inde[si]
                maxsi = si
        addu = maxsi
    else:
        addu = shrmap[addu][0]
    return addu, addv
def selectEdge0(inde,outde):
    maxind = -1
    maxinu = -1
    maxoutv = -1
    maxoutd = -1
    for vi in inde:
        if inde[vi] > maxind:
            maxind = inde[vi]
            maxinu = vi
    for vj in outde:
        if outde[vj] > maxoutd and vj != maxinu:
            maxoutd = outde[vj]
            maxoutv = vj
    return maxinu, maxoutv

def solve():
    global top
    global bcnt
    global index

    for ui in range(N):
        if DFN[ui] == 0:
            tarjan(ui)
    shrMap = {}
    for i in range(N):
        if Belong[i] not in shrMap:
            shrMap[Belong[i]] = []
        shrMap[Belong[i]].append(i)
        print(str(i)+' belong to '+str(Belong[i]))
    indegree = {}
    outdegree = {}
    isconnected = 0
    if bcnt == 0:
        print("已是强连通图")
        isconnected = 1
    else:

        "使用强连通分量缩点"
        # inde = 0
        # outde = 0
        "计算缩点后的出入度"
        for i in range(bcnt+1):
            indegree[i] = 0
            outdegree[i] = 0
        for vi in G:
            bi = Belong[vi]
            for vj in G[vi]:
                bj = Belong[vj]
                if bi != bj:
                    outdegree[bi] += 1
                    indegree[bj] += 1
        print(indegree, outdegree)
        print(shrMap)


        # "使用缩点后的图计算需要加入的边"
        # for i in range(bcnt+1):
        #     if indegree[i] == 0:
        #         inde += 1
        #     if outdegree[i] == 0:
        #         outde += 1
        # print("还需要"+str(max(inde, outde))+"条边")
    return indegree,outdegree,shrMap,isconnected

if __name__ == '__main__':

    N = 10  # 设备个数
    F = 1  # 时间间隔
    OFFRANGE = 120  # 最大时间偏移
    END = 600  #
    mu = 0.1
    sigma = 0.5
    MSGNUM = 20  # 消息传递条数
    clocklists = clockProduce(N, F, OFFRANGE, END)
    msglist = []
    for j in range(MSGNUM):
        msglist.append(msgProduce(mu, sigma, clocklists))

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
        value = round(msg.t1 - msg.t2, 3)
        tmpinterval = [value, math.inf]
        if msg.n1 > msg.n2:
            small = msg.n2
            large = msg.n1
            tmpinterval = [- math.inf, - value]
        if calrange(intervals[small][large], tmpinterval) is None:
            print('The offset between ' + str(small) + ' and ' + str(large) + ' is None')
        else:
            intervals[small][large] = calrange(intervals[small][large], tmpinterval)

    for ni in range(N):
        for nj in range(N):
            if ni > nj:
                intervals[ni][nj] = [-intervals[nj][ni][1], -intervals[nj][ni][0]]
            if ni < nj:
                print(ni, nj, intervals[ni][nj])
    # 图的邻接列表
    G = {}
    for ni in range(N):
        G[ni] = []
        for nj in range(N):
            if ni != nj and intervals[ni][nj][0] != -math.inf:
                G[ni].append(nj)
    # print(G)
    # for v in range(N):
    #     if v not in G:
    #         G[v] = []
    # G[0] = [1, 3]
    # G[1] = []
    # G[2] = [1, 3, 4]
    # G[3] = [4]
    # G[4] = [1, 3]

    # G[0] = [1,2]
    # G[1] = [3]
    # G[2] = [3,4]
    # G[3] = [0,5]
    # G[4] = [5]
    # G[5] = []

    # G[0] = [3]
    # G[1] = [0, 3]
    # G[2] = []
    # G[3] = [2, 4]
    # G[4] = [0, 1, 3]
    # #
    # G[0] = [1, 2, 5, 9]
    # G[1] = [2, 4, 8, 9]
    # G[2] = [1, 4, 6]
    # G[3] = [1, 2, 5, 7, 8, 9]
    # G[4] = [1, 3, 8]
    # G[5] = [0, 1, 2, 3, 4, 6, 7]
    # G[6] = [1, 2, 8]
    # G[7] = [2, 6]
    # G[8] = [0, 1, 6]
    # G[9] = [1, 2, 3, 4, 6, 7, 8]

    global top
    global bcnt
    global index
    index = 0  # 计数，从1开始
    top = -1
    bcnt = -1
    N = len(G)
    gindegree = [0]*N
    goutdegree = [0]*N
    for v in G:
        goutdegree[v] = len(G[v])
        for u in G[v]:
            gindegree[u] += 1

    indegree, outdegree, shrMap, isconnected = solve()

    print('GAP:')
    infnum, avelength = calDeviation(G, intervals)

    print('GAP0:')
    tmpmsg = msgProduce(mu, sigma, clocklists)
    addu = tmpmsg.n1
    addv = tmpmsg.n2
    print(addu, addv)
    intervals0 = msgprocess(tmpmsg, intervals)
    G0 = G.copy()
    G0[addu].append(addv)
    infnum0, avelength0 = calDeviation(G0, intervals0)
    if isconnected == 1:
        print('connected')
        # print('GAP:')
        # infnum, avelength = calDeviation(G, intervals)
        #
        # print('GAP0:')
        # tmpmsg = msgProduce(mu, sigma, clocklists)
        # addu = tmpmsg.n1
        # addv = tmpmsg.n2
        # print(addu, addv)
        # intervals0 = msgprocess(tmpmsg, intervals)
        # G0 = G.copy()
        # G0[addu].append(addv)
        # infnum0, avelength0 = calDeviation(G0, intervals0)
        #
        # print('GAP3:')
        # addu, addv = selectEdge0(gindegree, goutdegree)
        # print(addu, addv)
        # intervals3 = msgprocess(msgProduce1(addu, addv, mu, sigma, clocklists), intervals)
        # G3 = G.copy()
        # G3[addu].append(addv)
        # infnum3, avelength3 = calDeviation(G3, intervals3)
        # print('\n')
        # print(infnum, avelength)
        # print(infnum0, avelength0)
        # print(infnum3, avelength3)
    else:
        print('not connected')
        print('GAP:')
        infnum, avelength = calDeviation(G, intervals)

        print('GAP0:')
        tmpmsg = msgProduce(mu, sigma, clocklists)
        addu = tmpmsg.n1
        addv = tmpmsg.n2
        print(addu, addv)
        intervals0 = msgprocess(tmpmsg, intervals)
        G0 = G.copy()
        G0[addu].append(addv)
        infnum0, avelength0 = calDeviation(G0,intervals0)

        print('GAP1:')
        addu, addv = selectEdge1(indegree, outdegree, shrMap)
        print(addu, addv)
        intervals1 = msgprocess(msgProduce1(addu,addv,mu,sigma,clocklists), intervals)
        G1 = G.copy()
        G1[addu].append(addv)
        infnum1, avelength1 = calDeviation(G1,intervals1)

        print('GAP2:')
        addu, addv = selectEdge2(indegree, outdegree, shrMap, gindegree, goutdegree)
        print(addu, addv)
        intervals2 = msgprocess(msgProduce1(addu, addv, mu, sigma, clocklists), intervals)
        G2 = G.copy()
        G2[addu].append(addv)
        infnum2, avelength2 = calDeviation(G1,intervals2)
        print('\n')
        print(infnum, avelength)
        print(infnum0, avelength0)
        print(infnum1, avelength1)
        print(infnum2, avelength2)



