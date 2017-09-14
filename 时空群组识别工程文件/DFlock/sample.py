"对于原始数据采样,用作插值的样本数据，采样的周期1-5秒，每个人的轨迹选择开始时间不相同"



PATH = 'D:\\python_source\\DFlock\\'
filepath = PATH+'data\\process_ATC_1_1200_1.csv'
F = 3


file = open(filepath,'r')
lines = file.readlines()
datamap = {}
# t0 = float(lines[0].split(',')[0])
for line in lines:
    fields = line.split(',')
    ts = float(fields[0])
    uid = fields[1]
    if uid not in datamap:
        datamap[uid] = {}
    if ts not in datamap[uid]:
        datamap[uid][ts] = []
    for i in range(2, 8):
        datamap[uid][ts].append(fields[i])
print(datamap.keys())
# print(t0)
samplefile = open(PATH+'data\\'+str(F)+'_sample_ATC_1_1200.csv','w')
k = 0
for uid in datamap:
    # print(list(datamap[uid].keys()))
    print(k)
    t0 = list(datamap[uid].keys())[k]
    print(t0)
    k += 1
    if k == 5:
        k = 0
    # print(t0)
    lastts = t0
    ts = t0
    print(uid)
    for ts in datamap[uid]:
        if ts == t0 or 2.92 < float(ts - lastts) < 3.08 or float(ts - lastts) > 4.08:
            s = datamap[uid][ts][0]
            for j in range(1, len(datamap[uid][ts])):
                s += ',' + datamap[uid][ts][j]
            samplefile.write(str(ts) + ',' + str(uid) + ',' + s)
            lastts = ts


# for uid in datamap:
#     k = 0
#     for ts in datamap[uid]:
#         k %= 25
#         if k == 0:
#             s = datamap[uid][ts][0]
#
#             for j in range(1,len(datamap[uid][ts])):
#                 s += ','+datamap[uid][ts][j]
#             samplefile.write(str(ts)+','+str(uid)+','+s)
#         k += 1

