import math
import time

"用作每个时刻已有距离矩阵的数据的flock detection"
class Position:
    "Represents GPS position"

    def __init__(self,id):
        self.id = id

    "String Representation"

    def toString(self):
        return str(self.id)

    def isInCluster(self, cluster):
        for q in cluster.points:
            if self.id == q.id:
                return True

        return False


class Cluster:
    "Cluster of points, basically set of points with a center"

    def __init__(self, center, points):
        self.center = center
        self.points = points

    "String Representation"

    def toString(self):
        pts = self.points
        s = pts[0].toString()
        for i in range(1,len(pts)):
            s += ","+pts[i].toString()
        return "Cluster centered in: " + self.center.toString()+"   ("+s+")"

    "Cluster is density Joinable with list of clusters? Returns false if not, returns cluster if yes"

    def isDensityJoinable(self, listClusters):
        clusters = []
        for cluster in listClusters:
            for p in self.points:
                if p.isInCluster(cluster):
                    clusters.append(cluster)
                    listClusters.remove(cluster)
        if len(clusters) == 0:
            return None
        else:
            return clusters

    def hasCommon(self,cluster):
        for p in self.points:
            if p.isInCluster(cluster):
                return True
        return False

    "Merge current cluster with another"

    def mergeCluster(self, cluster):
        for p in cluster.points:
            if not p.isInCluster(self):
                self.points.append(p)
        return self

class Flock:
    def __init__(self,id,duration,lastseen,points):
        self.id=id
        self.duration = duration
        self.points = points
        self.lastseen = lastseen

    def toString(self):
        pts = self.points
        s = pts[0].toString()
        for i in range(1, len(pts)):
            s += "," + pts[i].toString()
        return "["+str(self.id)+" "+str(self.duration)+" "+str(self.lastseen)+" ("+s+")]"

    def flock2Cluster(self):
        cluster=[]
        for point in self.points:
            cluster.append(point.id)
        return cluster

    def idInFlock(self, pid):
        for p in self.points:
            if pid == p.id:
                return True
        return False