import math
import time
"轨迹群组识别中的类"

class Position:
    "Represents GPS position"

    def __init__(self, id, pos_x, pos_y,pos_z,velocity,motion_angle,face_angle):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.velocity = velocity
        self.motion_angle = motion_angle
        self.face_angle = face_angle

    # def __init__(self, id, resource, lat, lon, speed, track, date,dismatrix):
    #     self.id = id
    #     self.resource = resource
    #     self.lat = lat
    #     self.lon = lon
    #     self.speed = speed
    #     self.track = track
    #     self.date = date
    #     self.dismatrix=dismatrix

    # def __init__(self,id):
    #     self.id = id

    "String Representation"

    def toString(self):
        return str(self.id)

    "Distance EU simple. Usage: p.distance(q)"

    def distance_eu(self, q):
        return math.sqrt((self.pos_x - q.pos_x) ** 2 + (self.pos_y - q.pos_y) ** 2)

    "Is it in neighboorhoud with radio eps?"

    def is_in_neighborhoodByEUSimple(self, q, eps):
        return self.distance_eu(q) < eps

    "Neighboorhoud EU involving speed module."

    def is_in_neighborhoodByEURelativeSpeed(self, q, eps):
        return self.distance_eu(q) < eps * self.velocity

    #
    # "Neighboorhoud t0-reachable using distance EU and speed module."
    #
    # def is_in_neighborhoodT0Reachable(self, q, t0):
    #     return self.distance_eu(q) < t0 * self.speed


    #
    # "Neighboorhoud EU involving speed and orientation."
    #
    # def is_in_neighborhoodByEURelativeSpeedOrientation(self, q, eps):
    #     # TODO :Obtain orientation from self.orientation
    #     # return distance_eu(self, q) < eps * self.speed
    #     return NotImplemented
    #
    # "Is it in neighboorhood by time?"
    #
    # def is_neighboorhoudByTime(self, q, lapse):
    #     foo = time.mktime(self.date.timetuple())
    #     bar = time.mktime(q.date.timetuple())
    #     return abs(foo - bar) < lapse

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
        if len(self.points)==0:
            return "None"
        pts = self.points
        s = pts[0].toString()
        for i in range(1,len(pts)):
            s += ","+pts[i].toString()
        return "("+s+")"

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
        if len(pts)>0:
            s = pts[0].toString()
            for i in range(1, len(pts)):
                s += "," + pts[i].toString()
            return "["+str(self.id)+" "+str(self.duration)+" "+str(self.lastseen)+" ("+s+")]"
        else:
            return ""
    def idInFlock(self, pid):
        for p in self.points:
            if pid == p.id:
                return True
        return False
    def flock2Cluster(self):
        cluster=[]
        for point in self.points:
            cluster.append(point.id)
        return cluster