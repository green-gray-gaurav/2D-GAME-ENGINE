#here is the code for the editor grid
import pygame
import standard_classes.widgets as wid
import math , cmath 
from functools import reduce

class editorGrid():
    def __init__(self , x , y , color = (200,200,200) , width = 2 ,  screenDim = (100,100) , buttonPos = (0,0)) -> None:
        self.x = x
        self.y = y
        self.window = None
        self.color = color
        self.color2 = (0,0,0)
        self.width = width
        self.screenDim = screenDim
        self.size = 20
        self.visible = False
        self.lock = False
        self.gridVisibility = False

        #here we have grid controls
        self.toggleGrid = wid.Button("GRID" , buttonPos[0] , buttonPos[1] , (200,0,0) , (0 , 0 , 0) , self.size, self.__triggerToggle)
        self.gridLock = wid.Button("LOCK" , buttonPos[0] + self.toggleGrid.TextRect. width , buttonPos[1] , (200,0,0) , (0 ,0 , 0) , self.size , self.__triggerGridLock)
        self.instanceButton = wid.Button("[OBJ]" , buttonPos[0] + self.toggleGrid.TextRect. width + self.toggleGrid.TextRect.width + 10, buttonPos[1] , (200,0,0) , (0 ,0 , 0) ,self.size , self.triggerInstance)
        self.gridDetailButton = wid.Button("#GRID" , buttonPos[0] , buttonPos[1] + self.instanceButton.TextRect.height +5 , (200,0,0) , (0 ,0 , 0) ,self.size , self.__triggerGridDetails)



        self.currentSceneIns  =  {}
        self.nameGenId = 0
        self.sceneBar = None
        self.filesys = None
        self.prop = None

        self.selectedMesh = [None]


    


        pass

    def loadWindow(self , window):

        self.window  = window
        self.toggleGrid.loadWindow(window)
        self.gridLock.loadWindow(window)
        self.instanceButton.loadWindow(window)
        self.gridDetailButton.loadWindow(window)
       
        


    def renderEvent(self , event):

        #here are rending tyhe self event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.lock:
                self.lock = False
                #here when the grid location is updated
                self.updateTheScene()


        #here is the rednering of the srandard buttons
        self.toggleGrid.eventRender(event)
        self.gridLock.eventRender(event)
        self.instanceButton.eventRender(event)
        self.gridDetailButton.eventRender(event)
      

        #here w are rendering the event

        for obj in self.currentSceneIns.values():
            #here we are also passing the trigger
            obj.renderEvent(event , self.updateTheScene , self.mouseclickdetect)
        
       
        pass

    def mouseclickdetect(self, name):
        self.selectedMesh = [name]
        self.updateTheScene()
        self.prop.refreshThePropertBar()
       
        pass


    
    def renderComponent(self):
        self.toggleGrid.renderWidget()
        self.gridLock.renderWidget()
        self.instanceButton.renderWidget()
        self.gridDetailButton.renderWidget()
        
        #mainf the gridlines
        #horizontal line

        if self.visible:
        # horizontal
            pygame.draw.line(self.window , self.color , (self.x - self.screenDim[0] , self.y) , (self.x + self.screenDim[0] , self.y) , self.width)
        #veriacal line
            pygame.draw.line(self.window , self.color , (self.x  , self.y - self.screenDim[1]) , (self.x  , self.y + self.screenDim[1]) , self.width)
            
        #here are scene window resoltion lines
            if self.sceneBar:
                if self.sceneBar.sceneContent and self.sceneBar.selectedFile:
                    #here is the scene resolution of the selected scne
                    rx , ry  = self.sceneBar.sceneContent[self.sceneBar.selectedFile][0][0]
                    color = self.sceneBar.sceneContent[self.sceneBar.selectedFile][0][1]
                    gx , gy = self.sceneBar.sceneContent[self.sceneBar.selectedFile][0][2]


                    pygame.draw.rect( self.window , color , pygame.Rect(self.x +1 , self.y +1, rx , ry ))

                    pygame.draw.line(self.window , self.color2 , (self.x, self.y + ry) , (self.x + rx , self.y + ry) , self.width)
                    #veriacal line
                    pygame.draw.line(self.window , self.color2 , (self.x  + rx , self.y) , (self.x + rx  , self.y + ry) , self.width)

                    #here is the window color
                    

                    if self.gridVisibility:
                        for i in range(rx//gx):
                            pygame.draw.line(self.window , self.color2, (self.x  + i * gx , self.y) , (self.x +  i * gx, self.y + ry) , self.width)
                        for i in range(ry//gy):
                             pygame.draw.line(self.window , self.color2 , (self.x, self.y + i * gy) , (self.x + rx , self.y + i * gy) , self.width)
                    



            

                    pass


        

            if self.lock:
                self.x , self.y  = pygame.mouse.get_pos()

        #here hvae editor print mesh

        for obj in self.currentSceneIns.values():
            obj.render([self , self.sceneBar])


        pass

    def __triggerToggle(self):
        #herewe are goint o toggle the visibility of the grid
        self.visible = not self.visible

        pass

    def __triggerGridLock(self):
        #here letes solve the problem of locking
        self.lock = True
        pass

    def triggerInstance(self):
        if self.sceneBar != None and self.filesys != None:
            if self.sceneBar.selectedFile and self.filesys.selectedFile:
                #here wear egoint t o add print mesh in editor
                #the contect to append
                virtual_scn_obj = [self.filesys.selectedFile  , {'x' : 0, 'y':  0 , 'w' : 20 , 'h' : 20 , 'name' : f'mesh{self.nameGenId}'  ,
                                                                  'color':(200,200,200) , 'angle' : 0 , 'offset':(0,0) , 'pivot' : False
                                                                  , 'type': self.filesys.selectedFile}  ]
                self.sceneBar.sceneContent[self.sceneBar.selectedFile][1].append(virtual_scn_obj)
                self.renderScenePrintRect()
                #here ae arec chaning the genid
                self.nameGenId +=1                                                            


            pass
        pass

    def __triggerGridDetails(self):
        #here goes the cdoe to shoe the grid pivot
        print("-------------------tigger")
        for obj in self.currentSceneIns.values():
            #here we are also passing the trigger
            obj.pivotVisibility = not obj.pivotVisibility
        #here the grid visibility
        self.gridVisibility = not self.gridVisibility

        pass

    def Linker(self , sceneBar , fs , prop):
        self.sceneBar = sceneBar
        self.filesys = fs
        self.prop = prop
        pass


    def renderScenePrintRect(self):
                #here we are actllun updatin gthe rect
        if self.sceneBar != None and self.filesys != None:
            if self.sceneBar.selectedFile and self.filesys.selectedFile: 
                #here the gaurad code 

                self.currentSceneIns = {}
                currentSceneinfo = self.sceneBar.sceneContent[self.sceneBar.selectedFile][1]
                for _ , properties in currentSceneinfo:
                    scenePrintRect = PrintRectIns(self.x , self.y)
                    scenePrintRect.loadWindow(self.window)
                    scenePrintRect.x  = self.x + properties['x']
                    scenePrintRect.y  = self.y + properties['y']
                    scenePrintRect.width = properties['w']
                    scenePrintRect.height = properties['h']
                    scenePrintRect.name = properties['name']
                    scenePrintRect.color = properties['color']
                    scenePrintRect.angle = properties['angle']
                    scenePrintRect.pivotOffset = properties['offset']
                    scenePrintRect.pivotVisibility = properties['pivot']
                    self.currentSceneIns[properties['name']] = scenePrintRect


        pass

    def updateTheScene(self):

        if self.sceneBar != None and self.filesys != None:
            if self.sceneBar.selectedFile and self.filesys.selectedFile:
        #here ar eteh updates scene info about aobjects
                currentSceneinfo = self.sceneBar.sceneContent[self.sceneBar.selectedFile][1]
                for id , (name , properties) in enumerate(currentSceneinfo):
                    obj = self.currentSceneIns[properties['name']] 
                    properties['x'] = obj.x - self.x
                    properties['y'] = obj.y - self.y
                    properties['w'] = obj.width
                    properties['h'] = obj.height
                    properties['name'] = obj.name
                    properties['pivot'] = obj.pivotVisibility
                    self.sceneBar.sceneContent[self.sceneBar.selectedFile][1][id] = [name , properties]
                self.renderScenePrintRect()
    
        pass

    def deleteInstance(self):
        if self.selectedMesh[0]:
            #we deletedt the gui of the mesh
            del self.currentSceneIns[self.selectedMesh[0]] 
            #the deletdfrom the scnene in the scenebar
            if self.sceneBar and self.sceneBar.selectedFile:
                for i , mesh in enumerate(self.sceneBar.sceneContent[self.sceneBar.selectedFile][1]):
                    if mesh[1]['name'] == self.selectedMesh[0]:
                        self.sceneBar.sceneContent[self.sceneBar.selectedFile][1].pop(i)
                        break
            #so the selected mesh is deletd then moting is selected
            self.selectedMesh = [None]

        self.renderScenePrintRect()
        self.updateTheScene()



        pass

    def deleteAll(self):
        self.currentSceneIns = {}
        if self.sceneBar and self.sceneBar.selectedFile:
            self.sceneBar.sceneContent[self.sceneBar.selectedFile][1] = []

        self.selectedMesh = [None]
        self.renderScenePrintRect()
        self.updateTheScene()       
        pass




    def duplicateInstance(self):
        if self.sceneBar != None and self.filesys != None:
            if self.sceneBar.selectedFile and self.filesys.selectedFile:
                
                copied_props = {}
                for mesh in self.sceneBar.sceneContent[self.sceneBar.selectedFile][1]:
                    if mesh[1]['name'] == self.selectedMesh[0]:
                        copied_props = mesh[1].copy()

                if copied_props:
                    print(copied_props)
                    copied_props['name'] = f'mesh{self.nameGenId}'
                    copied_props['x'] = 0
                    copied_props['y'] = 0
                    print(copied_props)

                    virtual_scn_obj = [self.filesys.selectedFile  , copied_props]
                    self.sceneBar.sceneContent[self.sceneBar.selectedFile][1].append(virtual_scn_obj)
                    self.renderScenePrintRect()

                #here ae arec chaning the genid
                    self.nameGenId +=1

                    print(self.sceneBar.sceneContent[self.sceneBar.selectedFile][1])
                    print(self.currentSceneIns)
                    




#here is the utility class no thn moer
class PrintRectIns():
    def __init__(self , x , y) -> None:

        self.name = "mesh"
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.angle = 0
        self.color = (200,200,200)
        self.pivotOffset = [0 , 0]
        self.center = None
        self.window = None
        self.Rect = None
        self.selected = False
        self.pivotVisibility = False


        self.refCoordinates = [(- self.width/2 ,  - self.height/2) ,
                                ( + self.width/2 ,  - self.height/2),
                                ( + self.width/2 ,  + self.height/2),
                                ( - self.width/2 ,  + self.height/2) ]

        pass
    def renderEvent(self , event , trigger , trigger2):
        if self.Rect != None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.Rect.collidepoint(event.pos):
                    self.selected = not self.selected
                    if self.selected == False:
                        #here we gonna updatethe propeties of the selected mesh in scene bar
                        trigger()
                       
            #here dedtecet teh right clik for the selection and then being usied in proerty bar
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.Rect.collidepoint(event.pos):
                    trigger2(self.name)

                    pass

            
        
        pass

    def loadWindow(self , window):
        self.window = window
        pass

    

    def render(self  , objArray):
        #here we have mouse selected option
        if self.selected:
            grid , scn = objArray

            if grid.gridVisibility:
            #here to make the snappin system
                gx , gy = scn.sceneContent[scn.selectedFile][0][2]
                mx , my = pygame.mouse.get_pos()
                
                self.x = grid.x  + ((mx - grid.x)//gx) * gx
                self.y = grid.y + ((my - grid.y)//gy) * gy

                pass
            else:
                self.x ,self.y  = pygame.mouse.get_pos()





        #updating the refecne coordntes
        offsetx , offsety = -self.pivotOffset[0] , -self.pivotOffset[1]

        self.refCoordinates = [(offsetx- self.width/2 , offsety - self.height/2),
                                ( offsetx + self.width/2 , offsety- self.height/2),
                                ( offsetx+ self.width/2 , offsety + self.height/2),
                                (offsetx- self.width/2 ,  offsety+ self.height/2)]
            
        #finif te roated coordinates
        newCoordinates = [None , None , None , None]
        z_mul = complex(math.cos(self.angle*math.pi/180) , - math.sin(self.angle*math.pi/180))
        for i , cord in enumerate(self.refCoordinates):
            direction_vec = complex(*cord) * z_mul
            newCoordinates[i] = (self.x + direction_vec.real ,self.y +  direction_vec.imag)

            #here we gonna make a rect
        self.Rect  =  pygame.draw.polygon(self.window , self.color , newCoordinates) 

        #here we have the centre 

        self.center = reduce( lambda x , y : (x[0]+y[0] , x[1] + y[1]), newCoordinates)
        self.center = (self.center[0]/4 , self.center[1]/4)

         #here we gonna make the pivot for the rect
    
        if self.pivotVisibility:
            pygame.draw.circle(self.window , (255,0,0) , (self.center[0]-self.pivotOffset[0] , self.center[1]-self.pivotOffset[1]) , 2 )
            pygame.draw.circle(self.window , (0,0,255) , (self.center[0]-self.pivotOffset[0] , self.center[1]-self.pivotOffset[1]) , 5 , 1 )

            pass
        

        



        pass

   



