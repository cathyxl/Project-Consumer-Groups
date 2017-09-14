import threading
import socket
from model import Position
import display.Display as Display
import numpy as np
import matplotlib.pyplot as plt
import algorithms.flockdetection as FD
import algorithms.Color as color
encoding = 'utf-8'
BUFSIZE = 1024



# a read thread, read data from remote

def decodeMsg(str,left, IDs, pointmap):
    tmpstr = left + str
    tmpIds = []
    # pointmap = {}
    if tmpstr.startswith('%'):
        fields = tmpstr[1:-1].split('%')
        idstr = fields[0]
        tmpstr = fields[1]
        ids = idstr.split(',')
        for uid in ids:
            tmpIds.append(uid)
    fields = tmpstr[1:].split('#')
    left = fields[len(fields)-1]
    for fi in range(len(fields)-1):
        field = fields[fi]
        lines = field.split(';')
        ts = lines[0]
        if ts not in pointmap:
            pointmap[ts] = []
        points = []
        for i in range(1, len(lines)):
            linefields = lines[i].split(',')
            # print(fields)
            uid = linefields[0]
            x = float(linefields[1]) / 1000
            y = float(linefields[2]) / 1000
            p = Position(uid, x, y, 0.0, 0.0, 0.0, 0.0)
            points.append(p)
        pointmap[ts] = points
    if len(tmpIds) == 0:
        tmpIds = IDs
    return tmpIds, pointmap, left


def dePositionMsg(str):
    tmpstr = str[1:-1]
    lines = tmpstr.split(';')
    ts = lines[0]
    points = []
    for i in range(1,len(lines)):
        fields = lines[i].split(',')
        # print(fields)
        uid = fields[0]
        x = float(fields[1])/1000
        y = float(fields[2])/1000
        p = Position(uid, x, y, 0.0, 0.0, 0.0, 0.0)
        # p = Position(fields[0], float(fields[1])/1000, float(fields[2])/1000, float(fields[3])/1000, float(fields[4])/1000,
        #          fields[5], fields[6])
        points.append(p)
    return ts, points
def deIdMsg(str):
    tmpstr = str[1:-1]
    IDs = []
    ids = tmpstr.split(',')
    for id in ids:
        IDs.append(id)
    return IDs

class Reader(threading.Thread):
    def __init__(self, client,eps, minPts, gama, delta, spatialType, frequency,ax):
        threading.Thread.__init__(self)
        self.client = client
        self.eps = eps
        self.minPts = minPts
        self.gama = gama
        self.delta = delta
        self.spatialType = spatialType
        self.frequency = frequency
        self.ax = ax
        # self.pointMap = pointMap
        # self.IDs = IDs

    def run(self):
        "初始值设置"
        IDs = [1,2,3,4,5,6]
        pointMap = {}
        act_flocks = []
        pot_flocks = []
        curid = 0
        colorlist = np.zeros((2, 3))
        for j in range(3):
            colorlist[0][j] = 1
        for j in range(3):
            colorlist[1][j] = 0.9
        onedata = np.zeros((0, 0))
        lasttype = []
        assigned = [0, 0, 0, 0, 0, 0]
        flockmap = {}
        cmap = {}
        maxid = -2
        start = 0
        end = 0
        # XAXISSIZE = 1000
        WIN = 100
        left = ''
        # fig, ax = plt.subplots()
        # plt.axis([0, XAXISSIZE, 0, 10])
        # ax = plt.axis()
        Display.drawFlock(colorlist, onedata, IDs, self.ax, start)
        while True:
            data = self.client.recv(BUFSIZE)
            if data:
                string = bytes.decode(data, encoding)
                # print(string)
                self.client.send("ok".encode(encoding='utf-8'))
                IDs, pointMap,left = decodeMsg(string, left, IDs, pointMap)
                # print(IDs)
                # if string.startswith('#'):
                #     ts, points = dePositionMsg(string)
                #     if ts not in pointMap:
                #         pointMap[ts] = []
                #     pointMap[ts] = points
                # elif string.startswith('%'):
                #     IDs = deIdMsg(string)
                #     print(IDs)

                if len(pointMap) == WIN:
                    pointmap = pointMap
                    pointMap = {}
                    end = start + WIN
                    start = end

                    "画图"
                    draw_array, flockmap, act_flocks, pot_flocks, curid = FD.rtFlockDetect(IDs, self.gama, self.delta,
                                                                                           pointmap, self.eps,
                                                                                           self.minPts,
                                                                                           0, 0.4,
                                                                                           act_flocks,
                                                                                           pot_flocks,
                                                                                           flockmap, curid,
                                                                                           self.spatialType)
                    draw_array1 = np.transpose(draw_array)
                    onedata = Display.combinedata(onedata, draw_array1)
                    "获得色彩数组"
                    colorlist, lasttype, assigned, cmap, maxid = color.chooseColor(colorlist, draw_array, lasttype,
                                                                                   assigned, cmap,
                                                                                   maxid)
                    # print(list(colorlist))
                    "画图"
                    plt.clf()
                    Display.drawFlock(colorlist, onedata, IDs, self.ax, start)
            else:
                print('no data')
                break
        # plt.show()
        print("close:", self.client.getpeername())

    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string) > 2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string


# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port, eps, minPts, gama, delta, spatialType, frequency, ax):
        threading.Thread.__init__(self)
        self.port = port
        self.eps = eps
        self.minPts = minPts
        self.gama = gama
        self.delta = delta
        self.spatialType = spatialType
        self.frequency = frequency
        self.ax = ax
        # self.pointMap = pointMap
        # self.IDs = IDs

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)

    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            client.send("Welcome".encode(encoding="utf-8"))
            Reader(client, self.eps, self.minPts, self.gama, self.delta,
                   self.spatialType, self.frequency,self.ax).start()
            # cltadd = cltadd
            print("accept a connect")


# lst = Listener(9011,1.72, 2, 4, 2, 0, 0.04,pointMap,IDs)  # create a listen thread
# lst.start()  # then start