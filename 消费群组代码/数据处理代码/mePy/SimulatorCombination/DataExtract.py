import csv

'此py的功能是从训练集数据文件中部，抽取2秒的数据，并存放于meta_behavior中'

PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'
USRS = [1]    #用户序号
BEHAVIORS = [1,2,3,4,5,6,7,8,9,10]    #1到10为行为动作序号
STYPE = ['accele','angular','magne','orien']    #数据种类

'打开源数据文件，提取中部的2秒数据，写入datamap中'
def extract_data(data, begin, stride):
    '第一次调用'
    if begin == 0:
        begin = int(len(data)/2)

    start = int(data[begin][0])    #起始时间戳
    end = start + stride    #在终止时间戳附近
    subdata = data[begin:]
    datamap = {}

    for row in subdata:
        ts = int(row[0])
        if ts < start or ts > end:
            break
        if ts not in datamap:
            datamap[ts] = [row[1], row[2], row[3], row[4]]

    '当取到有很大误差的数据时重新取数据'
    if len(datamap.keys()) < 32:
        begin += 10
        if (begin + 30) > len(data):
            return datamap
        else:
            datamap.clear()
            return extract_data(data, begin, stride)
    return datamap

'将datamap的数据写入目标文件中'
def write_data(tar, datamap):
    tss = list(datamap.keys())
    start = tss[0]
    s = ''
    for ts in tss:
        s += str(ts-start) + ','
        s += datamap[ts][0] + ','
        s += datamap[ts][1] + ','
        s += datamap[ts][2] + ','
        s += datamap[ts][3] + '\n'

    tar.write(s)

time_stride = 2000
sensortype = STYPE[0]
begin = 0    #数据截取的起始点
datamap = {}

for i in BEHAVIORS:
    for u in USRS:
        srcfile = open(PATH + 'train_processed_o\\' + str(i) + '.' + str(u) + '_' + sensortype + '.csv', 'r')
        tmp = i
        if(i == 10):
            tmp = 0
        tarfile = open(PATH + 'meta_behavior\\' + str(tmp) + '.' + str(u) + '_' + sensortype + '.csv', 'w')
        reader = csv.reader(srcfile, delimiter=',')
        data = list(reader)
        datamap = extract_data(data, begin, time_stride)
        write_data(tarfile, datamap)
        begin = 0
        srcfile.close()
        tarfile.close()

