import pygame
import numpy as np
import multiprocessing
import time
from Engine.Tools import *

CpuThreads = multiprocessing.cpu_count()
UseMultiprocessing = False

class _Vector3(pygame.Vector3):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.Type = "Vector3"

class TheMatrixOperation:
    class Matrix:
        class new:
            def __init__(self, origin=_Vector3(0, 0, 0), x=_Vector3(1, 0, 0),y=_Vector3(0, 1, 0),z=_Vector3(0, 0, 1)):
                self.origin = origin
                self.x = x
                self.y = y
                self.z = z
                self.Type = "Matrix"
            def __str__(self):
                return '[' + str(self.origin)+","+str(self.x)+","+str(self.y)+',' + str(self.z) + "]"
            def __add__(self, other):
                if other.Type == "Vector3":
                    Result = TheMatrixOperation.Matrix.new()
                    Result.origin = self.origin + other
                    Result.x = self.x
                    Result.y = self.y
                    Result.z = self.z
                    return Result
                else:
                    raise Exception("You can add to Matrix only Vector3")
            def __sub__(self, other):
                if other.Type == "Vector3":
                    Result = TheMatrixOperation.Matrix.new()
                    Result.origin = self.origin - other
                    Result.x = self.x
                    Result.y = self.y
                    Result.z = self.z
                    return Result
                else:
                    raise Exception("You can add to Matrix only Vector3")
            def __mul__(self, other):
                if other.Type == "Matrix":
                    Result = TheMatrixOperation.Matrix.new()
                    Result.origin = self.origin + _Vector3((self.x.x*other.origin.x)+(self.x.y*other.origin.y)+(self.x.z*other.origin.z), (self.y.x*other.origin.x)+(self.y.y*other.origin.y)+(self.y.z*other.origin.z), (self.z.x*other.origin.x)+(self.z.y*other.origin.y)+(self.z.z*other.origin.z))
                    xyzMatrix = np.dot([[self.x.x, self.x.y, self.x.z], [self.y.x, self.y.y, self.y.z], [self.z.x, self.z.y, self.z.z]],[[other.x.x, other.x.y, other.x.z], [other.y.x, other.y.y, other.y.z], [other.z.x, other.z.y, other.z.z]])

                    Result.x = _Vector3(xyzMatrix[0][0], xyzMatrix[0][1], xyzMatrix[0][2])
                    Result.y = _Vector3(xyzMatrix[1][0], xyzMatrix[1][1], xyzMatrix[1][2])
                    Result.z = _Vector3(xyzMatrix[2][0], xyzMatrix[2][1], xyzMatrix[2][2])
                    return Result
                else:
                    raise Exception("You can mul Matrix only with Matrix")
            def GetOrientationDegrees(self):
                R = np.array([self.x, self.y, self.z])
                x_angle = np.arctan2(R[1, 2], R[2, 2])
                y_angle = np.arcsin(R[0, 2])
                z_angle = np.arctan2(R[0, 1], R[0, 0])

                x_deg = np.rad2deg(x_angle)
                y_deg = np.rad2deg(y_angle)
                z_deg = np.rad2deg(z_angle)

                result = [x_deg, y_deg, z_deg]
                return _Vector3(-result[0], result[1], -result[2])

            def GetComponents(self):
                return self.origin.x, self.origin.y, self.origin.z, self.x.x, self.x.y, self.x.z, self.y.x, self.y.y, self.y.z, self.z.x, self.z.y, self.z.z
            def GetLocalPosition(self, position):
                MainPoint = np.array([self.origin.x, self.origin.y, self.origin.z])
                OtherPoint = np.array([position.x, position.y, position.z])
                Diff = OtherPoint-MainPoint
                orientation = np.array([[self.x.x, self.x.y, self.x.z],[self.y.x, self.y.y, self.y.z],[self.z.x, self.z.y, self.z.z]])

                LocalVector = np.dot(orientation, Diff)
                result = _Vector3(LocalVector[0], LocalVector[1], LocalVector[2])
                return result

            def SetRotation(self, VectorAnglesDegrees):
                RotationMatrix = TheMatrixOperation.Matrix.new() * TheMatrixOperation.Matrix.Angles(VectorAnglesDegrees)
                self.x = RotationMatrix.x
                self.y = RotationMatrix.y
                self.z = RotationMatrix.z

        def Angles(VectorAnglesDegrees):
            x_rad = np.deg2rad(VectorAnglesDegrees.x)
            y_rad = np.deg2rad(VectorAnglesDegrees.y)
            z_rad = np.deg2rad(VectorAnglesDegrees.z)

            Rx = np.array([[1, 0, 0],
               [0, np.cos(x_rad), -np.sin(x_rad)],
               [0, np.sin(x_rad), np.cos(x_rad)]])

            Ry = np.array([[np.cos(y_rad), 0, np.sin(y_rad)],
                           [0, 1, 0],
                           [-np.sin(y_rad), 0, np.cos(y_rad)]])

            Rz = np.array([[np.cos(z_rad), -np.sin(z_rad), 0],
                           [np.sin(z_rad), np.cos(z_rad), 0],
                           [0, 0, 1]])

            R = np.dot(Rx, np.dot(Ry, Rz))

            return TheMatrixOperation.Matrix.new(_Vector3(0, 0, 0), _Vector3(R[0][0], R[0][1], R[0][2]), _Vector3(R[1][0], R[1][1], R[1][2]), _Vector3(R[2][0], R[2][1], R[2][2]))

    class Vector3:
        def new(x=0, y=0, z=0):
            return _Vector3(x, y, z)
        def NormalFrom3(Vectors):
            v1 = Vectors[1] - Vectors[0]
            v2 = Vectors[2] - Vectors[0]
            cross_product = np.cross(v1, v2)
            result = cross_product / np.linalg.norm(cross_product)

            return _Vector3(result[0], result[1], result[2])

class d3DSpace:
    class Object:
        Matrix = TheMatrixOperation.Matrix.new()
        color = [255, 255, 255]
        position = Matrix.origin
        scale = _Vector3(1, 1, 1)
        Mesh = None
        Type="Object"
        def __init__(self, RenderSurface):
            RenderSurface.Objects[self] = True
            self.surface = RenderSurface
        def Destroy(self):
            self.surface.Objects.pop(self)

    class Camera:
        Matrix = TheMatrixOperation.Matrix.new()
        position = Matrix.origin
        Type="Camera"
        def __init__(self, fov_deg, width, height, ZNear, ZFar):
            self.ChangeTheArguments(fov_deg, width, height, ZNear, ZFar)
        def ChangeTheArguments(self, fov_deg, width, height, ZNear, ZFar):
            self.fov = np.rad2deg(fov_deg) / 10000
            self.width = width
            self.height = height
            self.ZNear = -ZNear
            self.ZFar = -ZFar

            projection_matrix = np.array([[self.ZNear / np.tan(self.fov), 0, 0, 0],
                                          [0, self.ZNear / np.tan(self.fov), 0, 0],
                                          [0, 0, -(self.ZFar + self.ZNear) / (self.ZFar - self.ZNear), -2  *  self.ZFar  *  self.ZNear / (self.ZFar - self.ZNear)],
                                          [0, 0, -1, 0]])



            self.projection_matrix = projection_matrix
        def Get2DPointFrom3D(self, LocalPositionOfCamera):
            IsVisible = True
            if LocalPositionOfCamera.z < 0.1:
                LocalPositionOfCamera.z = 0.1
                IsVisible = False

            Point3D = np.array([-LocalPositionOfCamera.x, LocalPositionOfCamera.y, -LocalPositionOfCamera.z, 1])


            projected_point = np.dot(self.projection_matrix, Point3D)

            projected_point /= projected_point[-1]

            x = int(projected_point[0]  *  self.width  + self.width / 2)
            y = int(projected_point[1]  *  self.width  + self.height / 2)

            if x > self.width or x < 0 or y > self.height or y < 0:
                IsVisible = False

            return [x, y, IsVisible]



        def IsPolygonVisible(self, PolygonPoints):
            normalPolygon = TheMatrixOperation.Vector3.NormalFrom3(PolygonPoints)
            scalar = normalPolygon.x * PolygonPoints[0].x + normalPolygon.y * PolygonPoints[0].y + normalPolygon.z * PolygonPoints[0].z
            if scalar < 0.0:
                return True, scalar
            else:
                return False, scalar



class Render:
    class RenderSurface:
        Objects = {}
        BrightnessOfShadows = 35
        MainCamera = None
        def _render(self, pygameSurface, polygons, MaxScalar):
            if MaxScalar > 0:
                MaxScalar *= -1
            for polygon in polygons:
                x1, y1, z1, color = polygon[0], polygon[1], polygon[2], polygon[3] # get positions of triangle
                CheckIsPolygonVisible, scalar = self.MainCamera.IsPolygonVisible([x1, y1, z1]) # is Visible Polygon
                if CheckIsPolygonVisible:

                    d2DPointsFrom3D = [self.MainCamera.Get2DPointFrom3D(x1), self.MainCamera.Get2DPointFrom3D(y1), self.MainCamera.Get2DPointFrom3D(z1)] # convert to 2d

                    NotVisPolygons = 0
                    for o, v in enumerate(d2DPointsFrom3D):

                        if v[2] == False:
                            NotVisPolygons += 1

                        v.pop(2)

                    if NotVisPolygons != 3:
                        try:
                            ScalarPercent = scalar / (MaxScalar / 100) / 100 # COLOR
                            if ScalarPercent > 1:
                                ScalarPercent = 1

                            ScalarMinusPercent = 1 - ScalarPercent
                            ScalarPercent = ScalarPercent + ScalarMinusPercent * (self.BrightnessOfShadows/100)

                            ready = [int(color[0] * ScalarPercent),int(color[1] * ScalarPercent),int(color[2] * ScalarPercent)] # set shadow

                            pygame.draw.polygon(pygameSurface, ready, d2DPointsFrom3D)
                        except:
                            pass

        def update(self, pygameSurface):
            if self.MainCamera != None: # check, is be camera
                polygons = []
                for Object in self.Objects.keys():
                    if Object.Mesh != None: # check mesh
                        matrix = TheMatrixOperation.Matrix.new(self.MainCamera.Matrix.GetLocalPosition(Object.Matrix.origin)) # convert pos point to local camera pos and rotate
                        matrix.SetRotation(self.MainCamera.Matrix.GetOrientationDegrees() + Object.Matrix.GetOrientationDegrees())

                        positions = Object.Mesh.BuildMesh(matrix, Object.scale) # build mesh
                        for i in range(int(len(positions)/3)):
                            polygons.append([positions[i*3], positions[i*3+1], positions[i*3+2], Object.color])

                polygons = SortPolygonsByZ(polygons)

                if UseMultiprocessing == False:
                    self._render(pygameSurface, polygons, -matrix.origin.z)
                else:
                    if LenPolygons > CpuThreads:
                        Threads = []
                        HowMuchPolygonsInOneThread = LenPolygons//CpuThreads
                        _polygons = split_list(polygons, HowMuchPolygonsInOneThread)
                        args = []
                        for _poygon in _polygons:
                            args.append((pygameSurface, _poygon, -matrix.origin.z))



        def __init__(self, MainCamera):
            if MainCamera.Type == "Camera":
                self.MainCamera = MainCamera
            else:
                raise Exception("You can init RednerSurface only with camera")
