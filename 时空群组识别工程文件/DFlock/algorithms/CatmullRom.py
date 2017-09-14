import numpy as np
import math

def CatmullRomSpline(P0, P1, P2, P3, nPoints):
    """
      P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
      nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])
    # Calculate t0 to t4
    alpha = 0.5

    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return (((xj - xi) ** 2 + (yj - yi) ** 2) ** 0.5) ** alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    # Only calculate points between P1 and P2

    t = np.linspace(t1, t2, nPoints+1)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    # print(t.shape)

    t = t.reshape(len(t), 1)
    # print(t.shape)
    # print(t)
    A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
    A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
    A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3
    B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
    B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
    C = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2

    return t,C


def CatmullRomSplineWithT(P0, P1, P2, P3, k):
    """
      P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
      nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])
    # Calculate t0 to t4
    alpha = 0.5

    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return (((xj - xi) ** 2 + (yj - yi) ** 2) ** 0.5) ** alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)
    k = k*(t2-t1)+t1
    # Only calculate points between P1 and P2

    # t = np.linspace(t1, t2, nPoints + 1)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = k.reshape(len(k), 1)
    # print(len(t))
    # print(t)
    A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
    A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
    A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3

    B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
    B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3

    C = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2

    return C
def LineChain(P,Tmap):
    udata = {}
    sz = len(P)
    for i in range(sz-1):
        for ts in Tmap[i]:
            if ts not in udata:
                udata[ts] = []
            dis = math.sqrt(pow(P[i+1][0]-P[i][0],2)+pow(P[i+1][1]-P[i][1],2))

            x = P[i][0]+(P[i+1][0]-P[i][0])*ts/dis
            y = P[i][1]+(P[i+1][1]-P[i][0])*ts/dis

            udata[ts] = [round((x / 1000), 3), round((y / 1000), 3)]
    return udata

def CatmullRomChain(P,Tmap, Kmap, nPoints):
    udata = {}
    """
    Calculate Catmull Rom for a chain of points and return t he combined curve.
    """
    sz = len(P)
    # The curve C will contain an array of (x,y) points.
    if sz > 1:
        for i in range(-1, sz - 2):
            P0 = (0, 0)
            P3 = (0, 0)
            if i == -1:
                x = 2 * P[i + 1][0] - P[i + 2][0]
                y = 2 * P[i + 1][1] - P[i + 2][1]
                P0 = (x, y)
                # c = CatmullRomSpline(P0, P[i+1], P[i+2], P[i+3], nPoints)
            if i == sz - 3:
                x = 2 * P[i + 2][0] - P[i + 1][0]
                y = 2 * P[i + 2][1] - P[i + 1][1]
                P3 = (x, y)
                # c = CatmullRomSpline(P[i], P[i+1], P[i+2], P3, nPoints)
            if -1 < i < sz - 3:
                P0 = P[i]
                P3 = P[i + 3]
            T = Tmap[i + 1]
            k = np.array(Kmap[i + 1])
            # t = np.array(T)
            # print('x'+str(t.shape))
            c = CatmullRomSplineWithT(P0, P[i + 1], P[i + 2], P3, k)
            # c = CatmullRomSpline(P0, P[i + 1], P[i + 2], P3, nPoints)
            for j in range(c.shape[0] - 1):
                ts = T[j]
                if ts not in udata:
                    udata[ts] = []
                x, y = c[j]
                udata[ts] = [round((x / 1000), 3), round((y / 1000), 3)]

        # start = T[i + 1]
        # end = T[i + 2]
        # # step = (end - start) / nPoints
        # step = 0.04
        #
        # ts = start
        #
        # for j in range(c.shape[0]-1):
        #     if ts not in udata:
        #         udata[ts] = []
        #     x, y = c[j]
        #     # file.write(str(ts)+'000,'+id+','+str(x)+','+str(y)+',0.0,+0.0,+0.0+0.0\n')
        #     udata[ts] = [round(x,0), round(y,0)]
        #     if j == c.shape[0]-1:
        #         ts = end
        #     else:
        #         ts = round(ts + step, 3)

    return udata
def calError(x):
    return abs(math.sin(x))+1

if __name__ == '__main__':
    file = open('D:\\python_source\\DFlock\\catmullout.csv','w')
    P0 = (0, 0)
    P1 = (30, 30)
    P2 = (70, 50)
    P3 = (100, 0)

    # P0 = (7258, -1188)
    # P1 = (9283, -3375)
    # P2 = (10704, -5459)
    # P3 = (12686, -7588)
    t, C = CatmullRomSpline(P0, P1, P2, P3, 75)
    for i in range(C.shape[0]):
        print(C[i])
        file.write(str(round(t[i][0],3))+','+str(round(C[i][0],3))+','+str(round(C[i][1],3))+'\n')

    # file.write(str(C))
    # print(C)
    # for i in range(C.shape[0]-1):
    #     file.write(t[i]+','+C[i]+'\n')
    # file.close()





