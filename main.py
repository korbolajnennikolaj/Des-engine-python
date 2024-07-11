from Engine.d2D import *
from Engine.MeshCreater import *

CreateDisplay((500, 500), MAXFPS=120)
surface = d3DInit()
#surface.MainCamera.Matrix.origin = TheMatrixOperation.Vector3.new(5, 10, -2)
object2 = d3D.d3DSpace.Object(surface)
object2.color = [93, 18, 255]
object2.Matrix = surface.MainCamera.Matrix * TheMatrixOperation.Matrix.new(TheMatrixOperation.Vector3.new(0, 0, 3))
object2.Mesh = Mesh(Figures.cubeVertex, Figures.cubeTriangle)
object2.size = TheMatrixOperation.Vector3.new(1, 0.5, 1)

object1 = d3D.d3DSpace.Object(surface)
object1.color = [85,40,12]
object1.Matrix = surface.MainCamera.Matrix * TheMatrixOperation.Matrix.new(TheMatrixOperation.Vector3.new(0, 2, 5))
object1.Mesh = Mesh(Figures.cubeVertex, Figures.cubeTriangle)

pyramid = d3D.d3DSpace.Object(surface)
pyramid.color = [240, 129, 129]
pyramid.Matrix = surface.MainCamera.Matrix * TheMatrixOperation.Matrix.new(TheMatrixOperation.Vector3.new(3, 0, 3))
pyramid.Mesh = Mesh(Figures.pyramidVertex, Figures.pyramidTriangle)
pyramid.size = TheMatrixOperation.Vector3.new(1, 2, 1)

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

countDelta = 0.0
def update(deltatime, screen):
    surface.update(screen)

#
#object1.Matrix = object1.Matrix * TheMatrixOperation.Matrix.Angles(TheMatrixOperation.Vector3.new(0, 0, 90))
def rotate(deltatime, screen):
    object2.Matrix = object2.Matrix * TheMatrixOperation.Matrix.Angles(TheMatrixOperation.Vector3.new(0, deltatime*60, 0))
    object1.Matrix = object1.Matrix * TheMatrixOperation.Matrix.Angles(TheMatrixOperation.Vector3.new(0, deltatime*100, 0))
    pyramid.Matrix = pyramid.Matrix * TheMatrixOperation.Matrix.Angles(TheMatrixOperation.Vector3.new(0, -deltatime*100, 0))
    surface.MainCamera.Matrix *= TheMatrixOperation.Matrix.Angles(TheMatrixOperation.Vector3.new(0, deltatime*25, 0))
    #surface.MainCamera.Matrix *= TheMatrixOperation.Matrix.new(TheMatrixOperation.Vector3.new(0, 0, deltatime))
    text_surface = my_font.render(str(1/deltatime) + " FPS", False, (255, 255, 255))
    screen.blit(text_surface, (0,0))

pre_render(update)
on_process(rotate)
StartLoop()