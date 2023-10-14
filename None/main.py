# 1 - Import packages
import pygame
from pygame.locals import * #constants
import sys #for quiting the window

#here is out important object file
import objectFile
import scene_initilzer
import classObjRef


# 2 - Define constants
SCREEN_COL = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 60

QUIT_FLAG = False
# 3 - Initialize the world

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()



#scene initlizer data

def game_initiater():
   objectFile.SCENE_NO = scene_initilzer.currentScene
   for sceneName , sceneInfo  in scene_initilzer.all_scn.items():
      objectFile.OBJECT_ARRAY[sceneName] = []

      info , meshinfo = sceneInfo
   #here is the initilizationfo the SCNE INFO
      objectFile.SCENE_INFO[sceneName] = info

   #here is the iniltization of the OBJECT ARRAY
   #flusing the array before 
      objectFile.OBJECT_ARRAY[sceneName].clear()

      for mesh in meshinfo:
         meshtype , meshproperties = mesh
         newmesh = classObjRef.CLASS_ARRAY[meshtype]()

         newmesh.x = meshproperties['x']
         newmesh.y = meshproperties['y']
         newmesh.width = meshproperties['w']
         newmesh.height = meshproperties['h']
         newmesh.name = meshproperties['name']
         newmesh.type = meshproperties['type']
         newmesh.color = meshproperties['color']
         newmesh.angle = meshproperties['angle']
         newmesh.pivotOffset = meshproperties['offset']
         objectFile.OBJECT_ARRAY[sceneName].append(newmesh)
      
#unique id initilatization to each mesh

#setting the mesh
   for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
      object.id = objectFile.idGenerator
      objectFile.idGenerator+=1

#fist we load a window in each mesh
   for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
      object.loadinfo(window)

#here just before the loop we calla the create functin of all obects
   for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
      object.oncreate()




game_initiater()


while not QUIT_FLAG:
    #here we are settin gthe scene
    scne_data = objectFile.SCENE_INFO[objectFile.SCENE_NO] 
    if WINDOW_HEIGHT != scne_data[0][1] and WINDOW_WIDTH != scne_data[0][0]:
       WINDOW_WIDTH , WINDOW_HEIGHT = scne_data[0]
       window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
       
    SCREEN_COL = scne_data[1] #setting the col


    #collectiong the light masked mesh
    objectFile.LIGHT_MASK.clear()
    for i , object in enumerate(objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]):
       objectFile.LIGHT_MASK.append(i)

  

 # 7 - Check for and handle event
    for event in pygame.event.get(): #event loop
 # Clicked the close button? Quit pygame and end the program 
      if event.type == pygame.QUIT: 
         pygame.quit() 
         sys.exit()
      
      #here im hanfling the mose events
      if event.type == pygame.MOUSEBUTTONDOWN:
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]  :object.onMouseDown(event)
      if event.type == pygame.MOUSEBUTTONUP:
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]  :object.onMouseUp(event)

        #here im handling the keyboard events

      if event.type == pygame.KEYDOWN:
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO] :object.onKeyPressed(event.key)
      if event.type == pygame.KEYUP:
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]  :object.onKeyReleased(event.key)
         
    
      keys = pygame.key.get_pressed()
      for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]  :object.onKeyDown(keys)

      #here ar ethe code to rende the evnt of the interal wigets
      
      for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]  :object.eventHandler(event)



   #here we handhe the collsions
    meshs = objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]
    for k,  object in enumerate(meshs):
       for  object2 in meshs[k+1:]:
          if object.Rect and object2.Rect:
            if object.Rect.colliderect(object2.Rect):
               direction1 = [x - y for (x , y) in zip(object.center,object2.center)]
               direction2 = [x - y for (x , y) in zip(object2.center,object.center)]
               object.onCollisionWith(object2 , direction1)
               object2.onCollisionWith(object , direction2)

   

             


   #8 - Do any "per frame" actions
   #fluhint the ligth mask


    for i , object in enumerate(objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]):
        object.update()

           
           

 # 9 - Clear the window
#98   Chapter 5
    window.fill(SCREEN_COL) #equivalent to clear
 
 # 10 - Draw all window elements

    for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
        object.render()

 # 11 - Update the window




    pygame.display.update()
 # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND) 


    #here to handle the break out of the game loop from te inner object
    # 
    for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
        
        if object.restart_flag:
           object.restart_flag = False
           game_initiater()

        if object.quit_flag:
           
           QUIT_FLAG = True
           
    


