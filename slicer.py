import numpy as np
import math
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
print('start')

#main function
def main():
    #define file to load (update with a user variable later)
    #stlFile = '25mm_cube.stl'
    stlFile = 'files/DwarfBomber.STL' #this is a test file in the code directory
    layerHeight = 1
    #create object representing part to work with
    part1 = part(stlFile,layerHeight)

    #for each facet in part check intercept with z value
    scale = np.concatenate((np.array([0,0,0]),part1.maximums),0)
    lines=[] #list of lines to be used in drawing thi slice
    i=0
    for level in part1.perimeter:
        lines.extend(part1.perimeter[i])
        i=i+1
    print('Done! Drawnig now')
    drawLines(lines,scale)

def drawLines(lines,scale):
    #function takes a list of line objects and draws them on a 3d plot
    
    dlines=[]#empty list to hold the lines in a 2x3 np array
    for item in lines:
        dlines.append(np.vstack((item.start,item.end)))

    #draw the the lines
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Line3DCollection(dlines))
    axes.auto_scale_xyz(scale,scale,scale)
    pyplot.show()

#class to define a part that is to be printed aggregate of facets
class part:
    def __init__(self,filepath,layerHeight=0.5):
        self.model = mesh.Mesh.from_file(filepath)
        self.file = filepath
        self.layerHeight = layerHeight

        #loop through mesh object and create facets
        i = 0 #index for accessing arrays
        self.facets = [] #empty list to contain facets
        for item in self.model.normals:
            self.facets.append(facet(self.model.normals[i],self.model.v0[i],self.model.v1[i],self.model.v2[i]))
            i = i+1

        #determine max values
        maxPoints = np.amax(self.model.points,0)
        self.maximums = np.amax(np.vstack((maxPoints[0:3],maxPoints[3:6],maxPoints[6:9])),0)
        
        #create list of perimeters
        self.generatePerimeters()

    def generatePerimeters(self,newLayerHeight=9999):
        if newLayerHeight!=9999:self.layerHeight=newLayerHeight
        z=0
        #reset permineters
        self.createpIndex()

        for fac in self.facets:
            z=divmod(fac.minZ,self.layerHeight)[0]
            if z <self.layerHeight:z=self.layerHeight
            while z <= fac.maxZ:
                inter = fac.zintersect(z)
                if inter !=0:
                    self.perimeter[self.pIndex.index(z)].append(inter)
                z=z+self.layerHeight

    def createpIndex(self):
        z=0
        self.pIndex=[]
        self.perimeter=[]
        while z<= self.maximums[2]:
            z=z+self.layerHeight
            self.pIndex.append(z)
            self.perimeter.append([])

class point:
    def __init__(self,previous=None,coord=None,following=None):
        return

#class to define a line/edge
class line:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.vector = end - start
        self.norm = np.array([-self.vector[1],self.vector[0],self.vector[2]])
        self.unitNorm = self.norm/math.sqrt(self.norm[0]*self.norm[0]+self.norm[1]*self.norm[1]+self.norm[2]*self.norm[2])

#class to represnt a STL traingular facet
class facet:
    def __init__(self, norm, v0, v1, v2):
        self.norm = norm
        if norm[0]==0 and norm[1]==0:
            self.flatUnitNorm = np.array([0,0,0])
        else:
            self.flatUnitNorm = np.array([norm[0],norm[1],0])/math.sqrt(norm[0]*norm[0]+norm[1]*norm[1])
        self.vertices = [v0,v1,v2]
        self.edges = [line(v0,v1),line(v1,v2),line(v2,v0)]
        self.minZ = min(v0[2],v1[2],v2[2])
        self.maxZ = max(v0[2],v1[2],v2[2])
    def zintersect(self, z):
        points=[]
        crossed = 0 #flag to determine if the facet crossed the z plane
        for edge in self.edges:
            if edge.vector[2]==0:
                t=999
            else:
                t = ((z-edge.start[2])/edge.vector[2])
            if t>0 and t<1:
                crossed = 1
                points.append(edge.start+t*edge.vector)
        if crossed == 1:
            intersect=line(points[0],points[1])
            if (intersect.unitNorm[0]>0 and self.flatUnitNorm[0] <0) or (intersect.unitNorm[0] <0 and self.flatUnitNorm[0] >0):
                intersect=line(points[1],points[0])
            return intersect
        else:
            return 0


if __name__=='__main__':
    main()







