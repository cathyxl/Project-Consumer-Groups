import csv


PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'
TIMES = [1]
USRS = [1]
classifiers = ['KNN', 'RF', 'SVM']

def read_actionlist(src):
    srcfile = open(src, 'r')
    reader = csv.reader(srcfile, delimiter=',')
    data = list(reader)[0]
    srcfile.close()
    return data

def read_classifiedlist(src):
    srcfile = open(src, 'r')
    reader = csv.reader(srcfile, delimiter=',')
    data = []
    for index, line in enumerate(reader):
        if index%2 == 0:
            data.append(line[2])
    return data

def write_accuracy(tar, classifier, size, rcount):
    s = ''
    s += classifier + ":\n";
    s += "size:" + str(size) + "\n"
    s += "correct number:" + str(rcount) + "\n"
    s += "accuracy:" + str(rcount/size) + "\n"
    s += "\n"
    tar.write(s)

for time in TIMES:
    for user in USRS:
        tarfile = PATH + "cmp_accuracy\\" + "cmp_accuracy.csv"
        tar = open(tarfile, 'a')
        tar.write("repeatition:new-svm\n")
        for classifier in classifiers:
            actionlist_srcfile = PATH + "action_data\\" + str(time) + "_" + str(user) + ".csv"
            classified_srcfile = PATH + "classified_result\\action_" + classifier + "_" + str(user) + ".csv"
            #tarfile = PATH + "classified_accuracy\\" + classifier + "_" + str(user) + ".csv"

            actionlist = read_actionlist(actionlist_srcfile)
            classifiedlist = read_classifiedlist(classified_srcfile)
            print('原序列:'+str(actionlist))
            print(classifiedlist)

            errcount = 0
            rcount = 0
            size = min(len(actionlist), len(classifiedlist))

            for i in range(size):
                if int(actionlist[i]) == int(classifiedlist[i]):
                    rcount += 1
            write_accuracy(tar, classifier, size, rcount)

        tar.close()
