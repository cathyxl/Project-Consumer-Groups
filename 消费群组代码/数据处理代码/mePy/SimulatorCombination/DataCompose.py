import os
import csv

PATH = 'E:\\学校文件\\项目\\实验室\\git\\Project-Consumer-Groups\\消费群组代码\\数据处理代码\\mePy\\data\\'
# USRS = [1]    #用户序号
STYPE = ['accele','angular','magne','orien']    #数据种类
# CTIMES = []
# PEOPLES = []
sensortype = STYPE[0]

def get_filenames(dirname):
    P = []
    T = []
    print(os.walk(dirname))
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                time = os.path.splitext(file)[0].split('_')[0]
                pid = os.path.splitext(file)[0].split('_')[1]
                if time not in T:
                    T.append(time)
                if pid not in P:
                    P.append(pid)
    return T, P

def read_actionlist(src):
    srcfile = open(src, 'r')
    reader = csv.reader(srcfile, delimiter=',')
    data = list(reader)[0]
    srcfile.close()
    return data

def read_metadata(src):
    srcfile = open(src, 'r')
    reader = csv.reader(srcfile, delimiter=',')
    data = list(reader)
    datamap = {}

    for row in data:
        ts = int(row[0])
        if ts not in datamap:
            datamap[ts] = [row[1], row[2], row[3], row[4]]

    srcfile.close()
    return datamap

def write_data(tar, datamap, start):
    tarfile = open(tar, 'a')
    tss = list(datamap.keys())
    s = ''
    for ts in tss:
        tmp = ts + start
        if(ts == 0 and int(tmp/2000) != 0):
            tmp = 2000 * int(tmp / 2000)
            start = tmp
        s += str(tmp) + ','
        s += datamap[ts][0] + ','
        s += datamap[ts][1] + ','
        s += datamap[ts][2] + ','
        s += datamap[ts][3] + '\n'
    start += int(tss[-1])

    print(s)
    tarfile.write(s)
    tarfile.close()
    return start

def compose_data(actionlist, time, user):
    cur_start = 0
    for actionid in actionlist:
        meta_srcfile = PATH + "meta_behavior\\" + str(actionid) + ".1" + "_" + sensortype + ".csv"
        tarfile = PATH + "composed_data\\" + str(time) + "." + str(user) + "_" + sensortype + ".csv"
        datamap = read_metadata(meta_srcfile)
        cur_start = write_data(tarfile, datamap, cur_start)
        cur_start += 60



dirname = PATH + "action_data"
CTIMES, USRS = get_filenames(dirname)
for time in CTIMES:
    for user in USRS:
        actionlist_srcfile = PATH + "action_data\\" + str(time) + "_" + str(user) + ".csv"
        actitonlist = read_actionlist(actionlist_srcfile)
        compose_data(actitonlist, time, user)