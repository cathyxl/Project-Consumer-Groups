# -*- coding:utf-8 -*-
import numpy as np
from sklearn.preprocessing import Imputer
import csv
#from svmutil import *

def knn_classifier(train,labels):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train, labels)
    return model

def random_forest_classifier(train,labels):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=10, max_features=6)
    model.fit(train, labels)
    return model

def svm_classifier(train,labels):
    # y, x = svm_read_problem(svm_file)
    # model = svm_train(y, x)
    from sklearn.svm import SVC
    model = SVC()
    model.fit(train, labels)
    return model

def read_train_data(train_file):
    with open(train_file) as ftr:
        trainreader = csv.reader(ftr)
        trainset = list(trainreader)
        for line in range(len(trainset)):
            trainset[line] = [float(x) for x in trainset[line]]
        train = np.array(trainset)
        train = Imputer().fit_transform(train)
    traindata = train[:, 2:34]
    labels = train[:, 1]
    return traindata, labels


def read_test_data(test_file):
    with open(test_file) as fte:
        testreader = csv.reader(fte)
        testset = list(testreader)
        for line in range(len(testset)):
            testset[line] = [float(x) for x in testset[line]]
        test = np.array(testset)
    datamatrix = test[:, 2:34]   #原式[:, 2:33]，好像有错？？
    #print(datamatrix[])
    idlist = test[:, 0]
    winlist = test[:, 1]
    return datamatrix, idlist, winlist



def transform_svm_data(train_file, svm_file):
    svmfile = open(svm_file,'w')
    with open(train_file) as ftr:
        train_reader = csv.reader(ftr)
        trainset = list(train_reader)
        for line in trainset:
            s = ''
            label = line[1]
            s += label+' '
            for j in range(2,len(line)):
                s += str(j-1)+':'+str(line[j])+' '
            svmfile.write(s+'\n')



if __name__ == '__main__':
    TIMES = [1] #[3, 4, 7, 10, 11]  # 实验序号
    PATH = 'E:\\学校文件\\项目\\实验室\\python代码\\mePy\\data\\'  #PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
    trainfile = PATH + 'train_processed\\train_feature_train_o.csv'  # 训练集数据
    svm_file = PATH + 'train_processed\\svm_feature_train_o.csv' #
    transform_svm_data(trainfile,svm_file)
    test_classifiers = ['KNN', 'RF', 'SVM']
    #test_classifiers = ['KNN', 'RF']
    classifiers = {'KNN': knn_classifier,
                   'RF': random_forest_classifier,
                   'SVM': svm_classifier
                   }
    train, labels = read_train_data(trainfile)
    print(labels)
    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        for time in TIMES:
            testfile = PATH + 'processed_feature\\' + str(time) + '_features.csv'
            writefile = PATH + 'classified_result\\action_'+classifier+'_'+str(time)+'.csv'
            csvwriter = csv.writer(open(writefile, 'w', newline=''), delimiter=',')
            testdata, ids, windows = read_test_data(testfile)
            train_model = classifiers[classifier](train,labels)
            testlabels = train_model.predict(testdata)
            # if classifier == 'SVM':
            #     transform_svm_data(trainfile, svm_file)
            #     train_model = classifiers[classifier](svm_file)
            #
            # else:
            #     train_model = classifiers[classifier](train, labels)
            # if classifier == 'SVM':
            #
            #     testlabels,accuracy, p_val = svm_predict(labels, testdata, train_model)
            #     print(testlabels)
            # else:
            #     testlabels = train_model.predict(testdata)
            for i in range(len(testlabels)):
                label = testlabels[i]
                if label == 10:
                    label = 0
                csvwriter.writerow([str(ids[i]), str(windows[i]), str(int(label))])
            # print(testlabels)
            # for i in range(len(testdata)):
                # label = int(train_model.predict(testdata[i]))
                # if label == 10:
                #     label = 0
                # csvwriter.writerow([str(ids[i]), str(windows[i]), str(label)])
