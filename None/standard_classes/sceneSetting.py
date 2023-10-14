#here is out propeties bar class
import  standard_classes.widgets as wid
from functools import partial

class sceneSettingBar():
    def __init__(self , x , y ,  size = 20 , width = 100 , navbarLimit = 200 , togglepos = [0,0]) -> None:
        self.window= None
        self.x = x
        self.y = y
        self.projectName:str
        self.fileArray = []
        self.fileNameArray = []
        self.objectFilePath:str
        self.gap = 20
        self.width = width
        self.size = size
        self.visible = True
        self.active = True
        self.navlimit = navbarLimit
        self.modeCOLOR = (50,50,50)


        self.toggleButton = wid.Button("SETTING" , togglepos[0] ,togglepos[1] , (0,0,0) , (200,0,0) , size , self.triggerToggle )
        self.navBar = wid.Navbar(self.x , self.y , 20 , navbarLimit )
        self.textureBack = wid.textureRect(self.x  , self.y  - navbarLimit - self.toggleButton.TextRect. height, self.width ,  navbarLimit , self.modeCOLOR)
    

        self.InputFeild = wid.textInput(self.x  , self.y  - navbarLimit - self.toggleButton.TextRect. height , self.width-50 )
        self.setButton = wid.Button("SET",  self.x  + self.width-50 , self.y  - navbarLimit - self.toggleButton.TextRect.height ,  (200,0,0) , (200,200,200) , self.size , self.__triggerSet )
        
        self.propetiesButton = []

        self.scenebar = None
        self.editor = None
        self.console = None

        self.selectedMesh = None

        self.sceneProp = ['resolution:' , 'color' , 'gridsize']
        

        #initlally setting 
        self.toggleVisibility()


        pass

    def loadWindow(self , window):
        self.window = window
        self.toggleButton.loadWindow(window)
        self.textureBack.loadWindow(window)
        self.InputFeild.loadWindow(window)
        self.setButton.loadWindow(window)


    def renderEvent(self , event):

        # self.navBar.renderTheWidgetByMotion()
        # self.navBar.setDefaultMotion()
        self.toggleButton.eventRender(event)

        if self.active:
            self.InputFeild.eventHandler(event)
            self.setButton.eventRender(event)
            
            

            #here we are endering the propeties
            for (b , t) in self.propetiesButton:
                b.eventRender(event)


        pass

    def renderWindow(self):
        self.toggleButton.renderWidget()
        if self.visible:
            self.textureBack.renderWidget()

            self.InputFeild.renderWidget()
            self.setButton.renderWidget()
            #here rendering te propperties
            for (b , t) in self.propetiesButton:
                b.renderWidget()
                t.renderWidget() 
        pass

    def Linker(self , sceneBar , editor , console):
        self.editor , self.scenebar = editor , sceneBar
        self.console = console

        pass

    def toggleVisibility(self):
        self.active = not self.active
        self.visible = not self.visible
        pass


    def triggerToggle(self):
        #here the coe o handle the creatin of buttons
        
            #here we set the scenebar inivisble
        if self.scenebar.shareLock[0]==0 and self.scenebar.shareLock[1]==1:
            self.toggleVisibility()
            self.scenebar.shareLock[1] = 0
        elif self.scenebar.shareLock[0]==0 and self.scenebar.shareLock[1]==0:
            self.toggleVisibility()
            self.scenebar.shareLock[1] = 1
        elif self.scenebar.shareLock[0] ==1 and self.scenebar.shareLock[1] == 0:
            self.scenebar.toggleVisibility()
            self.toggleVisibility()
            self.scenebar.shareLock = [0 , 1]

            #here have refesdhign the properties
        if self.visible and self.active:
            self.refreshThePropertBar()
        
    pass

    
   


    def __triggerSet(self):

        #getting the input string
        parse_dic = {'s':str , 'ia':lambda x : tuple(map(int ,x.split(','))) , 'i':int , 'sa':lambda x : tuple(x.split(','))}

        if self.InputFeild.value:
            print("mark1")
            
            try:
                inputdata = self.InputFeild.value.split(':')
                data_value = parse_dic[inputdata[0]](inputdata[1])
            except:
                self.console.Error("invalid input: check data type token or the type of data provided")
                self.console.showErrorTab()

                return 


        #here ew have teh code to set the propertiesof the selecetd mesh
            if self.scenebar != None:
                if self.scenebar.selectedFile and self.scenebar.sceneContent:
        #here ar eteh updates scene info about aobjects

                    for i  , prop in enumerate (self.sceneProp):
                        if prop == self.selectedProperty:
                            if type(self.scenebar.sceneContent[self.scenebar.selectedFile][0][i]) == type(data_value):
                                self.scenebar.sceneContent[self.scenebar.selectedFile][0][i] = data_value
                            else:
                                self.console.Error("ERROR (INCORRECT TYPE): TYPE IS NOT MATCHING")
                            break
                
                #refesrgin the scene
                    self.editor.renderScenePrintRect()
                    self.refreshThePropertBar()
            pass

    def __triggerSelectedProperty(self, property , index):

        self.selectedProperty = property
        sfg , sbg = (200,0,0) , (200,200,200)
        #slection coloe
        fg , bg = (200,200,200 ),(0,0,0)
        for buttons in self.propetiesButton: buttons[0].retainBg , buttons[0].retainFg  =  sbg, sfg
        self.propetiesButton[index][0].retainFg , self.propetiesButton[index][0].retainBg = fg , bg

        pass

    def refreshThePropertBar(self):
        #fluhon the current data
        self.propetiesButton = []
            #some gaurd code
        if self.scenebar :
            if self.scenebar.selectedFile:
                sceneInfo = self.scenebar.sceneContent[self.scenebar.selectedFile][0]
                iter = 0
                for k ,v in zip(self.sceneProp, sceneInfo):

                    button = wid.Button(k ,  self.x ,    self.y  - self.navlimit - self.toggleButton.TextRect.height + (self.setButton.TextRect.height) * (iter + 1 ),  (200,0,0) , (200,200,200) , self.size , partial(self.__triggerSelectedProperty , k , len(self.propetiesButton)) )
                    text = wid.TextMesh(str(v) ,  self.x  + button.TextRect. width + 10 ,     self.y  - self.navlimit - self.toggleButton.TextRect.height + self.setButton.TextRect.height  * (iter + 1 ),  (200,200,200) , (0,0,0)  , self.size )
                    #modying the coordine of the text
                    text.x = self.x + self.width - text.TextRect.width   
                    button.loadWindow(self.window)
                    text.loadWindow(self.window)
                    self.propetiesButton.append([button , text])
                    iter +=1
        
        
        pass