from Engine.d3D import TheMatrixOperation
from Engine.Tools import split_list
import multiprocessing

CpuThreads = multiprocessing.cpu_count()
UseMultiprocessing = False

class Mesh:
    def __init__(self, VertexList, TriangleList):
        self.VertexList = VertexList
        self.TriagleList = TriangleList
    def _buildmesh(self,positions, Matrix, ScaleVector, TriagleList):
        for Triangle in TriagleList:
            for point in Triangle:
                positions.append((Matrix * TheMatrixOperation.Matrix.new(TheMatrixOperation.Vector3.new(self.VertexList[point][0]*ScaleVector.x, self.VertexList[point][1]*ScaleVector.y, self.VertexList[point][2]*ScaleVector.z))).origin)

    def BuildMesh(self, Matrix, ScaleVector=TheMatrixOperation.Vector3.new(1, 1, 1)):
        positions = []
        args = []
        if UseMultiprocessing == False:
            self._buildmesh(positions, Matrix, ScaleVector, self.TriagleList)

        else:
            TriangleList = split_list(self.TriagleList, CpuThreads)
            Threads = []
            for List in TriangleList:
                args.appen((positions, Matrix, ScaleVector, List))

        return positions

def ImportObjFile(FileName):
    Vertex, Triangles = [], []
    with open(FileName) as f:
        for line in f:
            if line.startswith("v "):
                Vertex.append([float(i) for i in line.split()[1:]])
            elif line.startswith("f "):
                faces = line.split()[1:]
                triangle = [int(face.split('/')[0]) - 1 for face in faces]
                if len(faces) > 3:
                    raise Exception("pls, export your obj file with triangle polygons")
                Triangles.append(triangle)

    return Vertex, Triangles

class Figures:
    cubeVertex = [[-0.5,  0.5, -0.5],
                  [ 0.5,  0.5, -0.5],
                  [ 0.5, -0.5, -0.5],
                  [-0.5, -0.5, -0.5],
                  [-0.5,  0.5,  0.5],
                  [ 0.5,  0.5,  0.5],
                  [ 0.5, -0.5,  0.5],
                  [-0.5, -0.5,  0.5]]


    cubeTriangle = [[0, 1, 2],
                    [0, 2, 3],
                    [2, 1, 5],
                    [2, 5, 6],
                    [3, 2, 6],
                    [3, 6, 7],
                    [0, 3, 7],
                    [0, 7, 4],
                    [1, 0, 4],
                    [1, 4, 5],
                    [6, 5, 4],
                    [6, 4, 7]]



    pyramidVertex = [[0, 0, 0],
                     [0.5, 0, 0.5],
                     [0.5, 0, -0.5],
                     [-0.5, 0, -0.5],
                     [-0.5, 0, 0.5],
                     [0, 1, 0]]

    pyramidTriangle = [[0, 1, 2],
                       [0, 2, 3],
                       [0, 3, 4],
                       [0, 4, 1],
                       [1, 5, 2],
                       [2, 5, 3],
                       [3, 5, 4],
                       [4, 5, 1]]