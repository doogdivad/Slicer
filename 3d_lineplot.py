import numpy as np
from mpl_toolkits import mplot3d
from matplotlib import pyplot

#create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

#create lines
line = []
line.append(np.array([(1,2,3),(4,5,8)]))
line.append(np.array([(1,2,8),(4,5,8)]))

#add to axes
axes.add_collection3d(mplot3d.art3d.Line3DCollection(line))

#set scale
scale = np.array([1,2,3,4,5,6,7,8,9,10])
axes.auto_scale_xyz(scale,scale,scale)

#show the plot
pyplot.show()
