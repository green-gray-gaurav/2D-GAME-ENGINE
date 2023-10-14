#here is out propeties bar class
import  standard_classes.widgets as wid
from functools import partial
class propertiesBar():
    def __init__(self , x , y ,  size = 20 , width = 100 , navbarLimit = 200) -> None:
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


        self.toggleButton = wid.Button("PROPERTIES" , x ,y , (0,0,0) , (200,0,0) , size , self.__triggerToggle )
        self.navBar = wid.Navbar(self.x , self.y , 20 , navbarLimit )
        self.textureBack = wid.textureRect(self.x  , self.y  - navbarLimit - self.toggleButton.TextRect. height, self.width ,  navbarLimit , color=self.modeCOLOR)
    

        self.InputFeild = wid.textInput(self.x  , self.y  - navbarLimit - self.toggleButton.TextRect. height , self.width )
        self.setButton = wid.Button("SET",  self.x  + self.width , self.y  - navbarLimit - self.toggleButton.TextRect.height ,  (200,0,0) , (200,200,200) , self.size , self.__triggerSet )
        self.InputFeild.width -= self.setButton.TextRect.width
        self.setButton.x -= self.setButton.TextRect.width


        self.propetiesButton = []

        self.scenebar = None
        self.editor = None
        self.console = None

        self.selectedMesh = None
        




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


    def __triggerToggle(self):
        self.active = not self.active
        self.visible = not self.visible

        #here the coe to handle the creatin of buttons

        if self.active and self.visible:
            #here have refesdhign the properties
            self.refreshThePropertBar()
        
    pass

   


    def __triggerSet(self):

        #getting the input string
        parse_dic = {'s':str , 'ia':lambda x : tuple(map(int ,x.split(','))) , 'i':int , 'sa':lambda x : x.split(',')}

        if self.InputFeild.value:
            print("mark1")
            inputdata = self.InputFeild.value.split(':')
            try:
                data_value = parse_dic[inputdata[0]](inputdata[1])
            except:
                self.console.Error("invalid input: check data type token or the type of data provided ")
                self.console.showErrorTab()
                return
            
        #here ew have teh code to set the propertiesof the selecetd mesh
            if self.scenebar != None and self.editor != None:
                if self.scenebar.selectedFile and self.scenebar.sceneContent and self.editor.selectedMesh[0]:
        #here ar eteh updates scene info about aobjects
                    print("mark2"  , self.selectedMesh , self.selectedProperty)
                    currentSceneinfo = self.scenebar.sceneContent[self.scenebar.selectedFile][1]
                    for id , (name , properties) in enumerate(currentSceneinfo):
                        if properties['name'] == self.editor.selectedMesh[0] :


                            if type(properties[self.selectedProperty]) ==  type(data_value):
                                properties[self.selectedProperty] = data_value
                                self.scenebar.sceneContent[self.scenebar.selectedFile][1][id] = [name , properties]
                            else:
                                #here is the type error
                                if self.console:
                                    self.console.Error("THE TYPE OF THE PROPERTY IS MATCHING" )
                                    self.console.Error(f" THE PROPERTY TYPE IS {type(properties[self.selectedProperty])}" )
                                    self.console.ShowErrorTab()
                                    #here we e\intreetung the process
                                    return



                            #taling care of the selected mesh itself becaise the mesh is seleced by the name
                            self.editor.selectedMesh[0] = properties['name']
                            break
                
                #refesrgin the scene
                    self.editor.renderScenePrintRect()
                    self.refreshThePropertBar()
                   
                
            
            pass


    def updateTransfomProperties(self   , popName , data_value):
        if self.scenebar != None and self.editor != None:
                if self.scenebar.selectedFile and self.scenebar.sceneContent and self.editor.selectedMesh[0]:

                    currentSceneinfo = self.scenebar.sceneContent[self.scenebar.selectedFile][1]
                    for id , (name , properties) in enumerate(currentSceneinfo):
                        if properties['name'] ==  self.editor.selectedMesh[0]:
                            properties[popName] = data_value
                            self.scenebar.sceneContent[self.scenebar.selectedFile][1][id] = [name , properties]
                    self.editor.renderScenePrintRect()
                    self.refreshThePropertBar()

                    print("worked!!")
                

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
        
        #flushon the current data
        self.propetiesButton = []
            #some gaurd code
        if self.scenebar and self.editor:
            if self.scenebar.selectedFile and self.editor.selectedMesh[0]:

            #here ae arae goint ot create the active scene selectd button
                self.selectedMesh = self.editor.selectedMesh[0]
                selectedProp = None
                if self.selectedMesh:
                    allmesh = self.scenebar.sceneContent[self.scenebar.selectedFile][1]
                    for [_ , prop] in allmesh:
                        print(prop , self.selectedMesh)
                        if prop['name'] == self.selectedMesh:

                            selectedProp = prop
                            break

                    #here goes the ode 

                #here some garuad code
                if not selectedProp: return

                #heer some more code to refesh the 

                iter = 0
                for k ,v in selectedProp.items():

                    button = wid.Button(k ,  self.x ,    self.y  - self.navlimit - self.toggleButton.TextRect.height + (self.setButton.TextRect.height) * (iter + 1 ),  (200,0,0) , (200,200,200) , self.size , partial(self.__triggerSelectedProperty , k , len(self.propetiesButton)) )
                    text = wid.TextMesh(str(v) ,  self.x  + button.TextRect. width + 10 ,     self.y  - self.navlimit - self.toggleButton.TextRect.height + self.setButton.TextRect.height  * (iter + 1 ),  (50,50,50) , (200,200,200)  , self.size )
                    #modying the coordine of the text
                    text.x = self.x + self.width - text.TextRect.width   


                    button.loadWindow(self.window)
                    text.loadWindow(self.window)
                    self.propetiesButton.append([button , text])
                    iter +=1
        
        
        pass