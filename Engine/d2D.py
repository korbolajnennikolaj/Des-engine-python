if __name__== "__main__":
    import d3D
else:
    import Engine.d3D as d3D
import numpy as np
import sys
pygame = d3D.pygame
pygame.init()

MAXFPSu = 120

screen = None
on_processFunctions = []
on_preprocessFunctions = []
on_closeFunctions = []

RenderSurface = None

def d3DInit():
    global RenderSurface
    camera = d3D.d3DSpace.Camera(60, 1920, 1080, 0.1, 1)
    RenderSurface = d3D.Render.RenderSurface(camera)
    return RenderSurface

def CreateDisplay(WidthHeight, pygameFlags=pygame.RESIZABLE, MAXFPS=120):
    global MAXFPSu
    global screen
    screen = pygame.display.set_mode((WidthHeight[0], WidthHeight[1]), pygameFlags)
    MAXFPSu = MAXFPS
    return screen

def StartLoop():
    while True:
        delta_time = pygame.time.Clock().tick(MAXFPSu) / 1000
        for function in on_preprocessFunctions:
            function(delta_time, screen)


        if RenderSurface != None:
            RenderSurface.update(screen)
            sizx, sizy = get_size_screen()
            RenderSurface.MainCamera.width, RenderSurface.MainCamera.height = sizx, sizy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for function in on_closeFunctions:
                    function()
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        screen.fill((0, 0, 0))

        for function in on_processFunctions:
            function(delta_time, screen)

def pre_render(Function):
    on_preprocessFunctions.append(Function)


def on_process(Function):
    on_processFunctions.append(Function)

def on_close(Function):
    on_closeFunctions.append(Function)

def get_size_screen():
    if screen == None:
        raise Exception("Please, create screen")
    else:
        return pygame.display.get_surface().get_size()