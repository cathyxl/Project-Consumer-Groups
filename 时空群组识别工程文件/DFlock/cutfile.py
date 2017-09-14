import csv
PATH = 'D:\\python_source\\DFlock\\'
# F = 5
# for f in range(1,F+1):
#     samplefile = open('D:\\迅雷下载\\ATC-1\\person_ATC-1_1200.csv','r')
#     csvsample = csv.reader(samplefile)
#     datamap = {}
#     for row in csvsample:
#         if row[1] not in datamap:
#             datamap[row[1]] = []
#         datamap[row[1]].append([float(row[0]),round(float(row[2])/1000,3),round(float(row[3])/1000,3)])
#
#         # print(row)
#     for ui in datamap:
#         with open(PATH+'data12\\processfiles\\'+ui+'_process.csv','w') as csvfile:
#             samplewriter = csv.writer(csvfile,delimiter=',',lineterminator='\n')
#             for row in datamap[ui]:
#             # print(row)
#                 samplewriter.writerow(row)
        # csvfile.close()
# samplefile = open('D:\\python_source\\DFlock\\data\\process_ATC_1_1200_1.csv','r')
samplefile = open('D:\\迅雷下载\\ATC-1\\person_ATC-1_1200.csv','r')

csvsample = csv.reader(samplefile)
datamap = {}
EXPUSERS = [12352600,12401100,12424900,12430301,12430900,12431000,12432600,12432900,12433000,12433800,12434701,12441601,
            12441700,12450200,12450701]

for row in csvsample:
    if row[1] not in datamap:
        datamap[row[1]] = []
    datamap[row[1]].append([float(row[0].replace(' ','')),round(float(row[2])/1000,3),round(float(row[3])/1000,3)])

        # print(row)
for ui in EXPUSERS:
    uid = str(ui)
    with open(PATH+'data\\processfiles_1\\'+uid+'_process.csv','w') as csvfile:
        samplewriter = csv.writer(csvfile,delimiter=',',lineterminator='\n')
        for row in datamap[uid]:
            # print(row)
            samplewriter.writerow(row)