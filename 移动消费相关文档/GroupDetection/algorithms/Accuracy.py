def Fmeasure(USRS,ground,cmatrix):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for ci in USRS:
        for cj in USRS:
            if ci < cj:
                if cmatrix[ci][cj] == 1:
                    if ground[ci][cj] == 1:
                        tp += 1
                    else:
                        fp += 1
                else:
                    if ground[ci][cj] == 0:
                        tn += 1
                    else:
                        fn += 1
    # print(tp,fp,tn,fn)
    if (2*tp+fp+fn) == 0:
        return None
    else:
        return float(2*tp)/float(2*tp+fp+fn)

def Affinity(USRS,ground,cmatrix):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for ci in USRS:
        for cj in USRS:
            if ci < cj:
                if cmatrix[ci][cj] == 1:
                    if ground[ci][cj] == 1:
                        tp += 1
                    else:
                        fp += 1
                else:
                    if ground[ci][cj] == 0:
                        tn += 1
                    else:
                        fn += 1
    # print(tp,fp,tn,fn)
    total = tp+fp+tn+fn
    if total == 0:
        return None
    else:
        return float(tp+tn)/float(total)

def FAA(groudmap,flockmap):
    faa=0.0
    for ts in groudmap:
        cmatrix=flockmap[ts]
        ground=groudmap[ts]
        faa+=Fmeasure(ground,cmatrix)
    faa/=len(flockmap)

    return faa

def NFDA(groudmap,flockmap):
    nfda=0
    for ts in flockmap:
        flen=len(flockmap[ts])
        glen=len(groudmap[ts])
        if flen==glen:
            nfda+=1
    nfda/=len(flockmap)
    return nfda

def loadGround(fname,USRS):
    i=0
    groupaffi = {}
    pfile = open(fname, 'r')
    pline = pfile.readlines()
    for line in pline:
        ui = USRS[i]
        i += 1
        groupaffi[ui] = {}
        affi = line.split(' ')
        for j in range(len(USRS)):
            uj = USRS[j]
            groupaffi[ui][uj] = int(affi[j])
    pfile.close()
    return groupaffi