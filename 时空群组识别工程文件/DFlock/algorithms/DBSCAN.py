from model import Cluster,Position
import time
import csv
# from guppy import hpy
# -*- coding: utf-8 -*-

# A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise
# Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu
# dbscan: density based spatial clustering of applications with noise

import numpy as np
import math

UNCLASSIFIED = -1
NOISE = None


def _eps_neighborhood(p, q, eps):
    return p.distance_eu(q) < eps

def _region_query(setPoints, p, eps):
    seeds = []
    for q in setPoints:
        if _eps_neighborhood(p,q,eps) and p.id != q.id:
            seeds.append(q)
    # print(len(seeds))
    return seeds


def _expand_cluster(setPoints, p, classifications, noises, eps, min_points):
    # start = time.clock()
    points = []
    seeds = _region_query(setPoints, p, eps)
    if len(seeds) < min_points-1:
        noises.append(p)
        classifications[p.id] = -1
        return False
    else:
        points.append(p)
        classifications[p.id] = 1
        for seed in seeds:
            points.append(seed)
            classifications[seed.id] = 1
        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(setPoints, current_point, eps)
            if len(results) >= min_points-1:
                for result_point in results:
                    if classifications[result_point.id] == 0:
                        seeds.append(result_point)
                        classifications[result_point.id] = 1
                        points.append(result_point)
            seeds = seeds[1:]
        # clusters.append(cluster)
        # end = time.clock()
        # print(end - start)
        return points

def dbscan(setPoints, eps, minPoints):
    clusters = []
    noises = []
    IDs = []
    classifications ={}
    for pt in setPoints:
        IDs.append(pt.id)
        classifications[pt.id] = 0

    for pt in setPoints:
        if classifications[pt.id] == 0:
            points = _expand_cluster(setPoints, pt, classifications, noises, eps, minPoints)
            if points:
                clusters.append(Cluster(None, points))
    # s=""
    # for p in noises:
    #     s+=p.toString()+' '
    # print(s)
    # s=""
    # for c in clusters:
    #     s += c.toString()+'\n'
    # print(s)
    return [clusters, noises, IDs]
"测试DBSCAN"
# typeDistance = 0
# minPoints = 4
# eps=1
# PATH = 'D:\\python_source\\DFlock\\'
# filepath=PATH+'a.csv'
#
# # filepath = PATH+'data\\process_ATC_1_1200_1.csv'
# pointmatrix = []
# csv_data = csv.reader(open(filepath,'r'), delimiter=',')
# for row in csv_data:
#     # ts = row[0]
#     # if ts not in pointmatrix:
#     #     pointmatrix[ts] = []
#     # print(row[1],row[2])
#     p = Position(row[0],float(row[1]),float(row[2]),0.0,0.0,0.0,0.0)
#     # p = Position(row[1], float(row[2])/1000, float(row[3])/1000, float(row[4])/1000, float(row[5])/1000, row[6], row[7])
#     pointmatrix.append(p)
# start = time.clock()
#
# dbscan(pointmatrix,eps,minPoints)
#
# end = time.clock()
# print(end-start)
