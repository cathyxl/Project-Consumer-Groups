import csv,random
PATH = 'D:\\python_source\\DFlock\\data\\'
F = 3
EXPUSERS = [12352600,12401100,12424900,12430301,12430900,12431000,12432600,12432900,12433000,12433800,12434701,12441601,
            12441700,12450200,12450701]

stfile = open(PATH+'processfiles_1\\idfiles_'+str(F)+'\\start_time.txt','w')
for uid in EXPUSERS:
    filepath = PATH+'processfiles_1\\'+str(uid)+'_process.csv'
    samplefile = open(PATH+'processfiles_1\\idfiles_'+str(F)+'\\'+str(uid)+'_sample.csv','w')
    usrdata = {}
    with open(filepath,'r') as file:
        csvreader = csv.reader(file)
        t0 = float(file.readline().split(',')[0])
        for row in csvreader:
            ts = float(row[0])
            if ts not in usrdata:
                usrdata[ts] = []
            usrdata[ts] = [float(row[1]),float(row[2])]
    if len(usrdata) > 250:
        n = int(F / 0.04)
    else:
        n = 0
    i = random.randint(0, n)
    t0 += i*0.04
    tss = []
    for ts in usrdata:
        if ts < t0:
            tss.append(ts)
    for ts in tss:
        usrdata.pop(ts)
    stfile.write(str(uid)+','+str(t0)+'\n')
    lastts = t0
    for ts in usrdata:
        if ts == t0 or F-0.08 < float(ts - lastts) < F+0.08 or float(ts - lastts) > F+1.08:
            s = str(ts) + ',' + str(usrdata[ts][0])+','+str(usrdata[ts][1])+'\n'
            samplefile.write(s)
            lastts = ts
stfile.close()
