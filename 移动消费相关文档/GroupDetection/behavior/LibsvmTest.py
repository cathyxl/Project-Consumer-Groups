from svmutil import *
import csv
PATH = 'D:\\Consume Group\\experiment\\csv_12_18\\'
trainfile = PATH + 'train_processed\\train_feature_train_o.csv'
testfile = PATH + 'processed_feature\\3_features.csv'
def read_svm_train_data(train_file):
    labels = []
    train = []
    with open(train_file) as ftr:
        train_reader = csv.reader(ftr)
        for row in train_reader:
            labels.append(int(row[1]))
            dataline = []
            for i in range(2, 34):
                dataline.append(float(row[i]))
            train.append(dataline)
    return train, labels

    # for t in train:
    #     print(t)
    # # print(train)
    # print(labels)

def read_svm_test_data(test_file):
    labels = []
    test = []
    with open(test_file) as ftr:
        train_reader = csv.reader(ftr)
        for row in train_reader:
            labels.append(1)
            dataline = []
            for i in range(1, 34):
                dataline.append(float(row[i]))
            test.append(dataline)
    return test, labels

def svm_classifier(train,labels):
    # y, x = svm_read_problem(svm_file)
    model = svm_train(labels, train)
    # from sklearn.svm import SVC
    # model = SVC(kernel='linear')
    # model.fit(train, labels)
    return model

train, labels = read_svm_train_data(trainfile)
train_model = svm_classifier(train, labels)
test, labels = read_svm_test_data(testfile)
testlablel, p_acc, p_val= svm_predict(labels, test, train_model)
print(testlablel)