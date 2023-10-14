# 1 - Import packages
import pygame
from pygame.locals import * #constants
import sys #for quiting the window
import test
import standard_classes.sceneSetting as sceneset
import standard_classes.project_manager as pg
import standard_classes.infologs as logs
import standard_classes.file_system as fs
import standard_classes.widgets as wid
import standard_classes.editor_grid as grid
import standard_classes.sceneBar as scene
import standard_classes.properties_bar as prop
import standard_classes.quickBar as quick
import standard_classes.Transform_tools as trtool
import os


# 2 - Define constants
TOPMARGIN = 500
BLACK = (100, 100, 100)
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 780
FRAMES_PER_SECOND = 60
# 3 - Initialize the world

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("GGG_ENGINE")
image = pygame.image.load("editor_data\\icon_editor.png")
pygame.display.set_icon(image)



#here we have triggered 

#here we have the project manager singlton
projectManager = pg.projectbar(WINDOW_WIDTH/2 - 150 , 20 , 220  , [WINDOW_WIDTH-50 , 10])
projectManager.loadWindow(window)
projectManager.renderWindow()

#here we have the log info singlton

logcat = logs.infoLogbar(WINDOW_WIDTH/2 - 300 , WINDOW_HEIGHT - 200, 20 , 600 , 10 ,switchPos=(WINDOW_WIDTH-30 , WINDOW_HEIGHT-30))
logcat.loadWindow(window)
logcat.renderWindow()


#here we have our file sysytem window
filesystem = fs.filesystem(30 , 30 , 50 , 100 , 20 , WINDOW_HEIGHT/2 - 150)
filesystem.loadWindow(window)
filesystem.renderWindow()


#here we have our editor grid

editorgrid  = grid.editorGrid(WINDOW_WIDTH/2 , WINDOW_HEIGHT/2 , screenDim=(WINDOW_WIDTH , WINDOW_HEIGHT) , buttonPos=(WINDOW_WIDTH - 250 , 10))
editorgrid.loadWindow(window)



scenebar = scene.sceneBar( 30  ,  WINDOW_HEIGHT/2 + 50 , 0 , 100 , 20  , 200 ,  [30 , WINDOW_HEIGHT-30] )
scenebar.loadWindow(window)
scenebar.renderWindow()


propBar = prop.propertiesBar(WINDOW_WIDTH - 200 , WINDOW_HEIGHT -30 , 20 , 170 , 400)
propBar.loadWindow(window)
propBar.renderWindow()


sceneSet = sceneset.sceneSettingBar(30, WINDOW_HEIGHT -30 , 20 , 170 , 300 , [120 , WINDOW_HEIGHT-30])
sceneSet.loadWindow(window)
sceneSet.renderWindow()


quickbar = quick.quickBar((0,0) , 20)
quickbar.loadWinow(window)


transform = trtool.transformTool(0,0,60)
transform.loadWindow(window)



# 4 - Load assets: image(s), sound(s), etc.
# 5 - Initialize variables

while True:
    #here we have the links
    filesystem.linkToProject(projectManager)
    editorgrid.Linker(scenebar , filesystem , propBar)
    propBar.Linker(scenebar , editorgrid , logcat)
    scenebar.SceneToEditorLink(editorgrid , sceneSet)
    projectManager.linker(scenebar)
    sceneSet.Linker(scenebar , editorgrid , logcat)
    quickbar.Linker(editorgrid)
    transform.Linker(propBar)


 # 7 - Check for and handle event
    for event in pygame.event.get(): #event loop
 # Clicked the close button? Quit pygame and end the program 
      if event.type == pygame.QUIT: 
         pygame.quit() 
         sys.exit()


      #here renderin the events
      projectManager.eventHandler(event)
      logcat.eventHandler(event)
      filesystem.renderEvent(event)
      editorgrid.renderEvent(event)

      scenebar.renderEvent(event)
      propBar.renderEvent(event)

      sceneSet.renderEvent(event)

      quickbar.renderEvent(event)

      transform.renderEvent(event)

      
    

 # 8 - Do any "per frame" actions

 
 # 9 - Clear the window
#98   Chapter 5
    window.fill(BLACK) #equivalent to clear
 
 # 10 - Draw all window elements
 #rendering the editor componet
    editorgrid.renderComponent()
    
    projectManager.renderWindow()
    logcat.renderWindow()
    filesystem.renderWindow()

    scenebar.renderWindow()

    propBar.renderWindow()

    sceneSet.renderWindow()

    quickbar.renderWindow()

    transform.renderWindow()
    
 
 # 11 - Update the window




    pygame.display.update()
 # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND) 


