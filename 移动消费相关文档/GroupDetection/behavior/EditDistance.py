import csv

import numpy as np
import Levenshtein as leven
from utils.config import experiment_users


# datamap = {id:{ts:""}}
def read_sequence_data(data,winsize):
    datamap = {}
    for i in range(len(data)):
        id = int(float(data[i, 0]))
        if id not in datamap:
            datamap[id] = {}
        ts = int(int(float(data[i, 1]))/winsize)
        if ts not in datamap[id]:
            datamap[id][ts] = ''
        val = int(float(data[i, 2]))
        datamap[id][ts] += str(val)
    return datamap

def cal_distance_matrix(datamap, USRS):
    dismatrix = {}
    "numwin表示选取最短长度的窗口"
    numwin = 65535
    for user in USRS:
        numwin = min(numwin, len(datamap[user]))
    "注释区域为选取共有的窗口"
    # winseq = list(datamap[USRS[0]].keys())
    # for id in USRS:
    #     tmplist = list(datamap[id].keys())
    #     print(tmplist)
    #     winseq = list(set(winseq).intersection(set(tmplist)))
    # print('winseq')
    # print(winseq)

    # for ts in winseq:
    for ts in range(numwin):
        print(ts)
        if ts not in dismatrix:
            dismatrix[ts] = {}
        for ui in USRS:
            if ui not in dismatrix[ts]:
                dismatrix[ts][ui] = {}
            for uj in USRS:
                if ui < uj:
                    print(ui,uj)
                    if ts not in datamap[ui] and ts not in datamap[uj]:
                        dismatrix[ts][ui][uj] = 0
                    elif ts not in datamap[ui] and ts in datamap[uj]:
                        dismatrix[ts][ui][uj] = len(datamap[uj][ts])
                    elif ts in datamap[ui] and ts not in datamap[uj]:
                        dismatrix[ts][ui][uj] = len(datamap[ui][ts])
                    else:
                        dismatrix[ts][ui][uj] = leven.distance(datamap[ui][ts], datamap[uj][ts])

    return dismatrix

if __name__ == '__main__':
    WINSIZE = 14
    TIMES = [3]
    PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
    test_classifiers = ['RF']
    for time in TIMES:
        USRS = experiment_users[time]
        groundname = PATH+'groundtruth\\'+str(time)+'.txt'
        for classifier in test_classifiers:
            filename = PATH + 'classified_result\\action_'+classifier+'_'+str(time)+'.csv'
            resultfile = open(PATH + 'classified_result\\disparity_'+classifier+'_'+str(time)+'.txt','w')
            with open(filename) as ftr:
                predict = csv.reader(ftr)
                dataset = list(predict)
                data = np.array(dataset)
                datamap = read_sequence_data(data,WINSIZE)
                for id in datamap:
                    print(datamap[id])
                # print(datamap)
                dismatrix = cal_distance_matrix(datamap,USRS)
                print(dismatrix)
            for ts in dismatrix:
                resultfile.write(str(ts)+'\n')
                for ui in USRS:
                    s = ''
                    for uj in USRS:
                        if uj != USRS[0]:
                            s += ' '
                        if ui == uj:
                            s += '0'
                        elif ui < uj:
                            s += str(dismatrix[ts][ui][uj])
                        else:
                            s += str(dismatrix[ts][uj][ui])
                    resultfile.write(s+'\n')
                resultfile.write('\n')
            resultfile.close()


