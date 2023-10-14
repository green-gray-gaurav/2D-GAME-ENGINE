#here we are going to write a calll to mange projects
import standard_classes.widgets as wid
import os


class projectbar():
    def __init__(self , x , y , tw , switchpos = [0,0]) -> None:
        self.x  =x 
        self.y = y
        self.totalWidth = tw
        self.textsize = 25
        self.switchPos = switchpos
        self.projectName:str = None

        self.mainFilePath:str = None

        self.switchToggle = wid.Button("(P)" , self.switchPos[0] , switchpos[1] , (0,0,0) , (200,0,0) , self.textsize , self.__triggerToggle)
        self.projectRunner = wid.Button("(B / R)" , self.switchPos[0]  - self.switchToggle.TextRect.width, switchpos[1] + self.switchToggle.TextRect.height , (0,0,200) , (0,0,0) , self.textsize , self.__triggerRun)
        

        self.newButton = wid.Button("+" , x , y , (0,0,0) , (255,1,1) , 30 , self.__triggerNewButton )
        self.inputFeild = wid.textInput(x + self.newButton.TextRect.width  ,y , self.totalWidth ,  placeholder= "projectName",  triggger=self.__triggerOnPressTrigger)
        self.loadButton = wid.Button("O" , x + self.totalWidth + self.newButton.TextRect.width ,y , (0,0,0) , (255,1,1) , 30 , self.__triggerLoadButton )
        #here we have our tecture erect 
        self.modeCOLOR = (50,50,50)
        self.textureback = wid.textureRect(x-10 , y -10 , self.totalWidth + self.newButton.TextRect.width + self.loadButton.TextRect.width+20, self.newButton.TextRect.height+20 , self.modeCOLOR,borders=[2,2,2,2])
        
        self.enableLink = False

        self.sceneBar = None
        

        pass

    def loadWindow(self , window):
        self.inputFeild.loadWindow(window)
        self.newButton.loadWindow(window)
        self.loadButton.loadWindow(window)
        self.switchToggle.loadWindow(window)
        self.textureback.loadWindow(window)
        self.projectRunner.loadWindow(window)
        pass

    def renderWindow(self):
        self.textureback.renderWidget()
        self.inputFeild.renderWidget()
        self.newButton.renderWidget()
        self.loadButton.renderWidget()
        self.switchToggle.renderWidget()
        self.projectRunner.renderWidget()
        pass

    def eventHandler(self , event):
        self.newButton.eventRender(event)
        self.loadButton.eventRender(event)
        self.inputFeild.eventHandler(event)
        self.switchToggle.eventRender(event)
        self.projectRunner.eventRender(event)
        pass

    def __triggerNewButton(self):
        print("new project" , self.inputFeild.value )

        #here we are going to create a project
        os.system(f"python bundleGen.py {self.inputFeild.value}")
        
        #here we have predined thing to do

        #here we dealing with class refence file
        file = open(f"{self.inputFeild.value}\\classReferFile.py" , "w")
        file.write(f"import objectFile as SCENE_REF\nPROJ_NAME = '{self.inputFeild.value}'")

        file.close()


        

        


        pass
    def __triggerLoadButton(self):

        print("load project" , self.inputFeild.value  )

        #here we are loadinf the main file path
        self.mainFilePath = f"{self.inputFeild.value}\\main.py"
        self.projectName = self.inputFeild.value

        #here are updain the scence // objectfile in the prohect 
        #here we hvae tol oad the files
        self.enableLink = True
       
        pass
    def __triggerOnPressTrigger(self):
        print("checked")
        self.newButton.bg = (0,0,200)
        self.loadButton.bg = (0,0,200)
        pass

    def __triggerToggle(self):
        self.newButton.visible = not self.newButton.visible
        self.newButton.active = not self.newButton.active

        self.loadButton.visible = not self.loadButton.visible
        self.loadButton.active = not self.loadButton.active

        self.inputFeild.visible = not self.inputFeild.visible
        self.inputFeild.active = not self.inputFeild.active

        self.textureback.visible = not self.textureback.visible



        pass

    def __triggerRun(self):
        #here are goint ot interpet the main file of the current project and run it
        if self.projectName:
            #here we are goint to load the scene file
            if self.sceneBar.sceneContent:
                all_scenes = self.sceneBar.sceneContent
                path = f"{self.projectName}\\scene_initilzer.py"
                data_to_write = f"currentScene = '{self.sceneBar.selectedFile}'\nall_scn = {all_scenes}"
                with open(path , 'w') as file:
                    file.write(data_to_write)


        if self.mainFilePath:
            os.system(f"python {self.mainFilePath}")

        pass


    def linker(self , sceneBar):
        self.sceneBar = sceneBar
        pass
    