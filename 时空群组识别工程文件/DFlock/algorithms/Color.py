import random
import numpy as np

def assginColor(assigned):
    notAssign=[]
    for a in range(len(assigned)):
        if assigned[a] == 0:
            notAssign.append(a)
    x = random.randint(0, len(notAssign)-1)
    assigned[notAssign[x]] = 1
    return notAssign[x]
def combineColor(colorlist, cmap, maxid):
    coArray = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]]
    colornew = np.zeros((maxid + 3, 3))  # 每次都包括数据不存在的-2以及没有分组的-1
    # print(maxid+2)
    for ci in range(maxid + 3):
        if ci < 2 or (ci-2) not in cmap:
            # print(1,ci)
            for cj in range(3):
                colornew[ci][cj] = colorlist[ci][cj]
        else:
            # print(2,ci)
            co = coArray[cmap[ci-2]]
            for cj in range(3):
                colornew[ci][cj] = co[cj]

    return colornew
"在flock组id断开又连上的情况下，此id的颜色会变化一次"
def chooseColor(colorlist, draw_array, lasttype, assigned, cmap,maxid):
    newmaxid = -2
    # 循环计算此次传送的时间段flock，得到最终的色彩list
    for di in range(draw_array.shape[0]):
        newcmap = {}
        type = []        # 当前时刻的flock id集合
        for dj in range(draw_array.shape[1]):
            x = int(draw_array[di][dj])
            if x > newmaxid:
                newmaxid = x  # 获得最大分组
            if x not in type and x >= 0:
                type.append(x)  # 如果当前新出现了flock集合
        for tj in type:
            if tj not in lasttype:
                newcmap[tj] = assginColor(assigned)  # 给当前时刻新增的flock指定颜色
        for ti in lasttype:
            if ti not in type:
                assigned[cmap[ti]] = 0  # 将上一时刻解散的flock颜色变成可用
            else:
                newcmap[ti] = cmap[ti]
        lasttype = type
        cmap = newcmap
        # print(type)
        if maxid < newmaxid:
            maxid = newmaxid
        maxid = int(maxid)
        colorlist = combineColor(colorlist, cmap, maxid)

    # #融合成新的colorlist
    # colornew = np.zeros((maxid+3, 3))  # 每次都包括数据不存在的-2以及没有分组的-1
    # for ci in range(maxid+3):
    #     if ci < 2:
    #         for cj in range(3):
    #             colornew[ci][cj] = colorlist[ci][cj]
    #     else:
    #         co = coArray[newcmap[ci-2]]
    #         for k in range(3):
    #             colornew[ci][k] = co[k]

    # for ci in range(-2, maxid+1):
    #     if ci < colorlist.shape[0]-2:
    #         for cj in range(3):
    #             colornew[ci][cj] = colorlist[ci][cj]
    #     else:
    #         co = coArray[newcmap[ci]]
    #         for k in range(3):
    #             colornew[ci][k] = co[k]

    return colorlist, lasttype, assigned, cmap, maxid
