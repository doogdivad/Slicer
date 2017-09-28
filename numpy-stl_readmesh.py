import numpy
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

#create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

#Load the STL files and add the vectors to the plot
cube = mesh.Mesh.from_file('25mm_cube.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

#Autoscale to the mesh size
scale = cube.points.flatten(-1)
axes.auto_scale_xyz(scale,scale,scale)

#show the plot
pyplot.show()
