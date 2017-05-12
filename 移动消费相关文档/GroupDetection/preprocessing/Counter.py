import csv
id= 7
NUMFEATURE = 2
START='2016/05/31 21:02:00'
END='2016/05/31 21:04:00'
countmap={}
#countmap -{user: {ts: [[feature_value]]}}
countermap1={}
countermap2={}
fname=''
#PATH='C:\\Users\Lin\Desktop\csv_6_7\\'
PATH='D:\python_source\DBAD\csv_7_29\\'
def sortcsv(filein,fileout):
    data = csv.reader(open(filein), delimiter=',')
    sortedlist = sorted(data, key=lambda x: (x[0]))

    with open(fileout, 'w', newline='') as file:
        filewriter = csv.writer(file, delimiter=',')
        for row in sortedlist:
            if row != sortedlist[-1]:
                filewriter.writerow(row)

'''for i in range(1,11):
    for feature in range(NUMFEATURE):
        if feature==0:
            fname=PATH +str(i)+'_accele.csv'
            sortcsv(fname,PATH +'sorted\\'+str(i)+'_accele.csv')
        else:
            fname=PATH +str(i)+'_orien.csv'
            sortcsv(fname,PATH +'sorted\\'+str(i)+'_orien.csv')'''


for i in range(1,11):
    if i not in countmap:
        countmap[i]={}
    for feature in range(NUMFEATURE):
#        print(feature)
        countmap[i]={}
        if feature==0:
            fname=PATH+str(i)+'_accele.csv'
            sortcsv(fname,PATH +'sorted\\'+str(i)+'_accele.csv')
            fout=PATH+'count\\'+str(i)+'_accele_out.csv'
        else:
            fname=PATH+str(i)+'_orien.csv'
            sortcsv(fname,PATH +'sorted\\'+str(i)+'_orien.csv')
            fout=PATH+'count\\'+str(i)+'_orien_out.csv'
        pfile=open(fname,'r')
        pline=pfile.readlines()
        for line in pline:
            if line==pline[0]:
                continue
            fields=line.split(',')
            ts=fields[0]
            ts=ts[1:20]
#            if ts<START or ts>END:
#                continue
            if ts not in countmap[i]:
                print(ts)
                countmap[i][ts]=[]

                #if feature==0:
                for f in range(NUMFEATURE):
                        countmap[i][ts].append([])
                        countmap[i][ts][f]=0
#                if feature>0 and countmap[i][ts][0]==[]:
#                    continue
            countmap[i][ts][feature]+=1

        pout=open(fout,'w')
        for ts in countmap[i]:
            pout.write(ts+','+str(countmap[i][ts][feature])+'\n')
        pout.close()
        if feature==0:
            sortcsv(fout,PATH+'sorted\count\\'+str(i)+'_accele_out.csv')
        else:
            sortcsv(fout,PATH+'sorted\count\\'+str(i)+'_orien_out.csv')





'''for i in range(1,8):
    fname1=str(i)+'_accele.csv'
    fname2=str(i)+'_orien.csv'
    pfile1=open(fname1,'r')
    pfile2=open(fname2,'r')
    pline1=pfile1.readlines()
    pline2=pfile2.readlines()
    for line in pline1:
        if line == pline1[0]:
            continue
        else:
            fields=line.split(',')
            ts=fields[0]
            ts=ts[1:20]
            if ts not in keys_1:
                keys_1.append(ts)
    for line in pline2:
        if line == pline2[0]:
            continue
        else:
            fields=line.split(',')
            ts=fields[0]
            ts=ts[1:20]
            if ts not in keys_2:
               keys_2.append(ts)


keys_1=sorted(keys_1)
keys_2=sorted(keys_2)
#countermap1[1]=sorted(countermap1[1].items(),key=lambda i:i[0])
#countermap2[1]=sorted(countermap2[1].items(),key=lambda i:i[0])

for i in range(1,8):
    for key in keys_1:
        countermap1[i].append(key)
        countermap1[i][key]=0
    for key in keys_2:
        countermap2[i][key]=0

for i in range(1,2):
    fname1=str(i)+'_accele.csv'
    fname2=str(i)+'_orien.csv'
    fout1=str(i)+'_accele_out.csv'
    fout2=str(i)+'_orien_out.csv'
    pfile1=open(fname1,'r')
    pfile2=open(fname2,'r')
    pout1=open(fout1,'w')
    pout2=open(fout2,'w')
    pline1=pfile1.readlines()
    pline2=pfile2.readlines()

    for line in pline1:
        if line == pline1[0]:
            continue
        else:
            fields=line.split(',')
            ts=fields[0]
            ts=ts[1:20]
            if ts in countermap1[i]:
                countermap1[i][ts] += 1

    print(countermap1[i])

    flag=0
    for ts in countermap1[i]:
        if countermap1[i][ts]!=0:
            flag=1
        if flag!=0:
            pout1.write(ts+','+str(countermap1[i][ts])+'\n')

    for line in pline2:
        if line == pline2[0]:
            continue
        else:
            fields=line.split(',')
            ts=fields[0]
            ts=ts[1:20]
            if ts in countermap2[i]:
                countermap2[i][ts]+=1
    print(countermap2[i])
    flag=0
    for ts in countermap2[i]:
        if countermap2[i][ts]!=0:
            flag=1
        if flag!=0:
            pout2.write(ts+','+str(countermap2[i][ts])+'\n')
'''