import numpy
import pylab as plt
# 根据catmull-rom 算法画出某些样点插值后的图

def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
  """
  P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
  nPoints is the number of points to include in this curve segment.
  """
  # Convert the points to numpy so that we can do array multiplication
  P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

  # Calculate t0 to t4
  alpha = 0.5
  def tj(ti, Pi, Pj):
    xi, yi = Pi
    xj, yj = Pj
    return (((xj-xi)**2 + (yj-yi)**2)**0.5)**alpha + ti

  t0 = 0
  t1 = tj(t0, P0, P1)
  t2 = tj(t1, P1, P2)
  t3 = tj(t2, P2, P3)

  # Only calculate points between P1 and P2
  t = numpy.linspace(t1,t2,nPoints)

  # Reshape so that we can multiply by the points P0 to P3
  # and get a point for each value of t.
  t = t.reshape(len(t),1)

  A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
  A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
  A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

  B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
  B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

  C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
  return C

def CatmullRomChain(P):
  """
  Calculate Catmull Rom for a chain of points and return the combined curve.
  """
  sz = len(P)

  # The curve C will contain an array of (x,y) points.
  C = []
  for i in range(sz-3):
    c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
    C.extend(c)

  return C


# 误差函数


# Define a set of points for curve to go through
# Points = [[0,1.5],[2,2],[3,1],[4,0.5],[5,1],[6,2],[7,3]]
# Points = [[0,1],[1,1],[1,0],[2,0]]
# Points = [[0,1],[1,1],[1,0],[1,-1]]
# Points = [[0,1],[1,1],[1,0],[2,-1]]
# Points = [[0,1],[1,1],[1,0],[0,-1]]
# Points = [[0,1],[1,1],[1,0],[2,1]]
# Points = [[0,1],[1,1],[1,0],[0,1]]
# Points = [[0,1],[1,1],[1,0],[1,1]]
# Points = [[0,1],[1,1],[1,0],[0,0]]

# Points = [[0,1],[1,1],[0,0],[1,0]]
# Points = [[0,1],[1,1],[0,0],[0,-1]]
# Points = [[0,1],[1,1],[0,0],[-1,0]]
# Points = [[0,1],[1,1],[0,0],[1,-1]]
# Points = [[0,1],[1,1],[0,0],[-1,-1]]
# Points = [[0,1],[1,1],[0,0],[-1,0]]
# Points = [[0,1],[1,1],[0,0],[-1,1]]
# Points = [[0,1],[1,1],[0,0],[0,1]]

Points = [[0,1],[1,1],[1,0.8],[2,0.8],[0,1],[1,1]]

# Calculate the Catmull-Rom splines through the points
c = CatmullRomChain(Points)
print(list(c))
# Convert the Catmull-Rom curve points into x and y arrays and plot
x,y = zip(*c)
plt.plot(x,y)

# Plot the control points
px, py = zip(*Points)
plt.plot(px,py,'or')

plt.show()