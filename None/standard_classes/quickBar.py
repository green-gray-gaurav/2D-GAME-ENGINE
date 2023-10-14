from functools import partial
import standard_classes.widgets as wid
import pygame

class quickBar():
    def __init__(self , pos , size , buttons = 5 , buttonLabels = ["(+) new" , "(-) delete" , "(||) duplicate" , "(*) PREFAB" , "CLEAR"]):
        self.pos = pos
        self.size = size
        self.buttons = buttons
        self.window = None
        self.buttonLabels = buttonLabels


        #internal state

        self.buttonArray = []
        self.backgroundRect = None
        self.gap = 20

        self.show = False
        self.keyBuffer = False

        self.editor = None

        #internal state

        self.prefabs = {}

        #command inputs
        self.inputcommand = None
        self.inputButton = None
        self.commandPromptVisibility = False


        pass
    def loadWinow(self , window):
        self.window  = window
        pass
    def renderEvent(self , event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.keyBuffer = True
        

        #other event to rennder
        #left shoif t + mouse right button
        if self.keyBuffer:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.keyBuffer = False
                self.pos = pygame.mouse.get_pos()
                self.makeButtons()
                self.show = True



        if self.show :
            for button in self.buttonArray:
                button.eventRender(event)


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.show  = False

        pass

        if self.commandPromptVisibility:
            if self.inputcommand and self.inputButton:
                self.inputButton.eventRender(event)
                self.inputcommand.eventHandler(event)


    def renderWindow(self):
        if self.show:
            self.backgroundRect.renderWidget()

            for button in self.buttonArray:
                button.renderWidget()


        if self.commandPromptVisibility:
            if self.inputcommand and self.inputButton:
                self.inputButton.renderWidget()
                self.inputcommand.renderWidget()

        
        pass
    def __trigger(self , index):
        #here ar ethe buttin events
        
        if index == 0:
            if self.editor:
                self.editor.triggerInstance()
                
            
        if index == 1:
            if self.editor:
                self.editor.deleteInstance()
            
            pass

        if index == 2:
            if self.editor:
                self.editor.duplicateInstance()
            
            pass

        if index == 3:
            #setitng the buttons and the input feild
            self.inputcommand = wid.textInput(self.pos[0] , self.pos[1] , 100 , 20 )
            self.inputButton = wid.Button("OK" , self.pos[0] + self.inputcommand.width , self.pos[1]  , (200,0,0) , (200,200,200), 15 , trigger=self.setPrefab)
            
            self.inputButton.loadWindow(self.window)
            self.inputcommand.loadWindow(self.window)
            
            self.commandPromptVisibility = True
            
            pass
        if index == 4:
            #clearing the canvas
            if self.editor:
                self.editor.deleteAll()
            pass

        #button pressed common event
        self.show = False
        
        pass

    def setPrefab(self):

        if self.inputcommand.value:
            #hrer we gonan makthe preafab
            if self.editor:
                if self.editor.sceneBar:
                    all_mesh = self.editor.sceneBar.sceneContent[self.editor.sceneBar.selectedFile][1]
                    #here is the key to look back
                    mean_vec = [0 , 0] 
                    size = len(all_mesh)
                    for _ , m in all_mesh:
                        mean_vec[0] += m['x']/size
                        mean_vec[1] += m['y']/size
                    

                    #here is the preafabs
                    self.prefabs[self.inputcommand.value] = [ mean_vec , {props['name']:props for _ ,props in all_mesh}]

                    if self.editor.filesys:
                        file = open(f"{self.editor.filesys.projectName}\\sampleMesh_data.py" , 'w')
                        #here is the weriting part
                        data_to_write  = f"PREFABS  = {self.prefabs}"
                        file.write(data_to_write)
                        file.close()

            pass

        #updaig the sampemesh file
        self.editor.filesys.projectName


        
        self.commandPromptVisibility = False
        
        pass

    def makeButtons(self):
         #craeting all the buttons 
        self.buttonArray = []
        rectwidth = 0 
        rectheight = 0
        for i , buttonlabel in enumerate(self.buttonLabels):
            b = wid.Button(buttonlabel , self.pos[0] ,self.pos[1] +  self.gap * i  , (200,200,200) , (0,0,0) , self.size , partial(self.__trigger , i))
            
            #some calucations
            rectwidth = b.TextRect.width if b.TextRect.width > rectwidth else rectwidth
            rectheight += b.TextRect.height
            
            b.loadWindow(self.window)
            self.buttonArray.append(b)
        #set the background rect
        self.backgroundRect = wid.textureRect(self.pos[0] , self.pos[1] , rectwidth , rectheight)
        self.backgroundRect.loadWindow(self.window)
        pass

    def Linker(self , editor):
        self.editor = editor
        pass