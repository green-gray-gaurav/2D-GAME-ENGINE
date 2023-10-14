#here e are goint o copt and pas te the filesystem class and modify some features

import standard_classes.widgets as wid
from functools import partial
import os , glob

#lets nake the file system

class sceneBar():
    def __init__(self , x , y , gap , textWidth , size , navbarLimit = 200 , togglepos =[0,0]):
        #here we have  some properties
        self.window= None
        self.x = x
        self.y = y
        self.projectName:str
        self.fileArray = []
        self.fileNameArray = []
        self.objectFilePath:str
        self.gap = gap
        self.textWidth = textWidth
        self.size = size
        self.visible = True
        self.toggleButton = wid.Button("SCENES" , togglepos[0] ,togglepos[1] , (0,0,0) , (200,0,0) , 20 , self.triggerToggle )
        self.InputFeild = wid.textInput(x , y +  self.gap , self.textWidth )
        self.deleteButton = wid.Button("DEL",x  + self.textWidth , y + self.gap,  (200,0,0) , (200,200,200) , self.size , self.__triggerDeleteScene )
        self.createButton = wid.Button("CRT" , x  + self.textWidth + self.deleteButton.TextRect.width   , y + self.gap,  (200,0,0)  , (200,200,200)  ,self.size , self.__triggerCreateScene )
        self.openButton = wid.Button(".scn" , x  + self.textWidth + self.deleteButton.TextRect.width , y + self.gap + self.createButton.TextRect.height,  (0,0,0)  , (200,200,200)  ,self.size , self.__triggerOpenScene )
        self.y + self.gap + self.createButton.TextRect.height
        self.navBar = wid.Navbar(self.x , self.y + self.gap + self.createButton.TextRect.height , 20 , navbarLimit ,width=200 )

        

        self.fileButtonArray = {}
        self.buttongaps  =20

        #this is the selected scene
        self.selectedFile = None

        self.modeCOLOR = (50,50,50)

        #herre we have our texture widow
        self.textureBack = wid.textureRect(self.x , self.y , self.textWidth + self.deleteButton.TextRect.width + self.createButton.TextRect.width , navbarLimit + 100  , self.modeCOLOR ,borders=[2,2,2,2] )
        
        
        self.sceneContent:dict = {}
        self.gridPOs = (0,0)


        self.editor = None
        self.sceneSetter = None
        self.shareLock = [1,0]

        

        pass
    
    def loadWindow(self , window):

        #retain gthe refecnt o windoe in the onect

        self.window = window

        self.toggleButton.loadWindow(window)
        self.InputFeild.loadWindow(window)
        self.deleteButton.loadWindow(window)
        self.createButton.loadWindow(window)
        self.openButton.loadWindow(window)
        self.textureBack.loadWindow(window)


        #loading the buttonfile if any
        for button in self.fileButtonArray.values():
            button.loadWindow(window)

        pass

    def renderWindow(self):
        self.textureBack.renderWidget()
        self.toggleButton.renderWidget()
        self.InputFeild.renderWidget()
        self.deleteButton.renderWidget()
        self.createButton.renderWidget()
        self.openButton.renderWidget()


        #rendering the buttons if any
        for button in self.fileButtonArray.values():
            # button.renderWidget()
            self.navBar.outboundRenderHandle(button)
            self.navBar.renderTheWidgetByMotion(button)
        
        #here we are stopping the motion of navbar
        self.navBar.setDefaultMotion()
        pass

    def renderEvent(self , event):
        self.toggleButton.eventRender(event)
        self.InputFeild.eventHandler(event)
        self.deleteButton.eventRender(event)
        self.createButton.eventRender(event)
        self.openButton.eventRender(event)
        self.navBar.renderEvent(event)

        #rendering the event for the button if any
        for button in self.fileButtonArray.values():
            button.eventRender(event)

        pass

    def addfile(self):


        pass


    def toggleVisibility(self):
        #here we are going t otoggle the vissibilty and the activity od the wisgets
        self.createButton.visible = not self.createButton.visible
        self.createButton.active = not self.createButton.active

        self.deleteButton.visible = not self.deleteButton.visible
        self.deleteButton.active = not self.deleteButton.active

        self.InputFeild.visible = not self.InputFeild.visible
        self.InputFeild.active = not self.InputFeild.active

        self.openButton.visible = not self.openButton.visible
        self.openButton.active = not self.openButton.active

        self.textureBack.visible = not self.textureBack.visible

        self.visible = not self.visible 

        #seetif the visible of button if any
        for buttons in self.fileButtonArray.values():
            buttons.visible = not buttons.visible
            buttons.active = not buttons.active


        pass
    def triggerToggle(self):

        if self.shareLock[0]==1 and self.shareLock[1]==0:
            self.toggleVisibility()
            self.shareLock[0] = 0

        elif self.shareLock[0]==0 and self.shareLock[1]==0:
            self.toggleVisibility()
            self.shareLock[0] = 1
        
        elif self.shareLock[0] ==0 and self.shareLock[1] == 1:
            self.sceneSetter.toggleVisibility()
            self.toggleVisibility()
            self.shareLock = [1 , 0]



        pass
    def __triggerCreateScene(self):
        #here we are going to create a file // obj files
        if self.InputFeild.value:
            #checking the dupliacacy
            for button in self.fileButtonArray.values():
                filename = button.text.split(" ")[1]
                if filename == self.InputFeild.value:
                    #here have consle to handle the error
                    return
                
           
            #here we physcall created the file
            sceneName = self.InputFeild.value

            #created a new virtual scene

            self.sceneContent[sceneName] = [[(640,480) , (50,50,50) , (32,32)] , []]
            
           
            #here we adde in file button array to display
            height = self.y + self.gap + self.createButton.TextRect.height  + len(self.fileButtonArray) * self.buttongaps
            button = wid.Button(f"{len(self.fileButtonArray) +1 }. {sceneName}" , self.x  , height ,  (0,0,0)  , (200,200,200)  ,self.size , partial(self.__filebuttonselection , sceneName )  )
            
            #here we have to load windon int o it
            button.loadWindow(self.window)
            self.fileButtonArray[sceneName] = button

    def __triggerDeleteScene(self):
        #delete te selected sceene
        del self.sceneContent[self.selectedFile]
        #deetin gthe button
        del self.fileButtonArray[self.selectedFile]
        
        pass
    def __filebuttonselection(self,key):
        self.selectedFile = key
        #playing with the gui stuff
        sfg , sbg = (200,0,0) , (200,200,200)
        #slection coloe
        fg , bg = (200,200,200 ),(0,0,0)
        for buttons in self.fileButtonArray.values(): buttons.retainBg , buttons.retainFg  = bg , fg
        self.fileButtonArray[key].retainFg , self.fileButtonArray[key].retainBg = sfg , sbg

        if self.editor:
            self.editor.renderScenePrintRect()
       
        pass

    def __triggerOpenScene(self):
        if self.editor:
            self.editor.renderScenePrintRect()
        pass

    def SceneToEditorLink(self , editor_grid , sceneSetter):
        self.editor = editor_grid
        self.sceneSetter = sceneSetter


 