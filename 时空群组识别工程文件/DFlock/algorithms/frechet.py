#Frechet Calculations

#Various different Frechet calculations in 1 Program


#Required Import statements
import numpy as np #The usual math library
import matplotlib.pyplot as plt
import matplotlib.animation as animation

################################################################################
#Non-Geodesic Calculation
################################################################################

#Here all variables for calculations are set, so they are global and we can have a 'main'
def setgrid(setn):
    global n
    n = setn #set how many vertices on the graph of alpha
    global s_grid
    s_grid = np.linspace(0,1,n) #this is where we restrict to (0,1)

def getXVals(sgrid, f):
    x_grid = []
    if f[0]=='a':
        for i in range(0,sgrid.size):
            x=AlphaX(sgrid[i])
            x_grid.append(x)
    if f[0]=='b':
        for i in range(0,sgrid.size):
            x=BetaX(sgrid[i])
            x_grid.append(x)
    return x_grid

#Calculate each 'y' value for the curves
def getYVals(xgrid, f):
    y_grid = []
    if f[0]=='a':
        for i in range(0,xgrid.size):
            y=AlphaY(xgrid[i])
            y_grid.append(y)
    if f[0]=='b':
        for i in range(0,xgrid.size):
            y=BetaY(xgrid[i])
            y_grid.append(y)
    return y_grid

#Here we set the two curves so they are like vector functions in the plane

#Currently this is a line passing through a backwards Z
def AlphaX(s):
    f = 2*s-1
    return f
def AlphaY(s):
    f = np.sqrt(1-(2*s-1)**2)
    return f
def BetaX(s):
    f = 2*s-1
    return f
def BetaY(s):
    f = -np.sqrt(1-(2*s-1)**2)
    return f

#Here we define the Euclidean distance
def dEuclid(x1,y1,x2,y2):
    d = np.sqrt((x1-x2)**2+(y1-y2)**2)
    return d


#Here we will take two curves, and produce the freespace plot
def frechetFreeSpace(curveAx,curveAy,curveBx,curveBy,e): #curveA is the y values for alpha and curveB is y values for beta
    blackwhite = np.empty((n,n),int)
    for i in range(0,n):
        for j in range(0,n):
            dist = dEuclid(curveAx[i], curveAy[i], curveBx[j],curveBy[j])
            if dist>=epsilon:
                blackwhite[i,j] = 1
            else:
                blackwhite[i,j] = 0
    img = plt.imshow(blackwhite,cmap='Blues',origin='lower', interpolation='hanning')
    plt.show()

################################################################################
#Main
################################################################################
set_n = 500
setgrid(set_n)
#generate curve stuff
alphaX = getXVals(s_grid, 'a')
betaX = getXVals(s_grid, 'b')
alphaY = getYVals(s_grid,'a')
betaY = getYVals(s_grid,'b')

epsilon = 1.9
frechetFreeSpace(alphaX,alphaY,alphaX,betaY,epsilon) #pass frechetFreeSpace the y values,and epsilon

#epsilon = .50001
#frechetFreeSpace(alphaX,alphaY,alphaX,betaY,epsilon)

#epsilon = .5001
#frechetFreeSpace(alphaX,alphaY,alphaX,betaY,epsilon)




plt.plot(alphaX,alphaY)
plt.plot(betaX,betaY)
plt.show()



#===============================================================================
# This section contains code for certain nice Curves
#===============================================================================

#===============================================================================
# #A flat line beta, and a piecewise backwards Z for alpha
#===============================================================================
#===============================================================================
# def AlphaX(s):
#     if (s<1/3 and s>=0):
#         f = s
#     elif(s>=1/3 and s<2/3):
#         f = 2/3 - s
#     else:
#         f = s - 2/3
#     return f
# def AlphaY(s):
#     if (s<1/3 and s>=0):
#         f = 0
#     elif (s>=1/3 and s<2/3):
#         f = 3*s - 1
#     else:
#         f = 1
#     return f
# def BetaX(s):
#     f = 2*s -1
#     return f
# def BetaY(s):
#     #x = (2*s-1)
#     f = .5
#     return f
#==============================================================================