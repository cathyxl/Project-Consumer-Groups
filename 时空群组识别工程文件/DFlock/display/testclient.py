def list2str(L,bound):
    res_str = bound
    for k in range(len(L)):
        if k != 0:
            res_str += ','
        res_str += str(L[k])
    res_str += bound
    return res_str


if __name__ == "__main__":
    import socket
    import display.Display as Display

    BUFFSIZE = 1024
    PATH = 'D:\\python_source\\DFlock\\'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9011))
    import time,csv

    pointmatrix = {}
    filepath = 'D:\\python_source\\DFlock\\data\\process_ATC_1_1200_1.csv'
    csv_data = csv.reader(open(filepath, 'r'), delimiter=',')
    for row in csv_data:
        ts = row[0]
        if ts not in pointmatrix:
            pointmatrix[ts] = []
        uid = row[1]
        pointmatrix[ts].append([uid, row[2], row[3], row[4], row[5], row[6], row[7]])

    IDs = []
    groupfile = open(PATH + 'data\\group.txt', 'r')
    lines = groupfile.readlines()
    for line in lines:
        fields = line.split(' ')
        for i in range(len(fields)):
            pi = int(fields[i])
            if pi not in IDs:
                IDs.append(str(pi))
    sock.send(list2str(IDs, '%').encode(encoding="utf-8"))
    print(sock.recv(BUFFSIZE))


    for i in range(len(pointmatrix)):
        position_str = '#'
        ts = list(pointmatrix.keys())[i]
        position_str += ts
        time.sleep(0.04)
        for L in pointmatrix[ts]:
            position_str += ';' + list2str(L,'')
        position_str += '#'
        # print(position_str)
        sock.send(position_str.encode(encoding="utf-8"))
    sock.close()