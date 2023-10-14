
import standard_classes.widgets as wid
from functools import partial
import os , glob , shutil


#lets nake the file system

class filesystem():
    def __init__(self , x , y , gap , textWidth , size , navbarLimit = 200):
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
        self.toggleButton = wid.Button("FILES" , x ,y , (0,0,0) , (200,0,0) , 30 , self.__triggerToggle )
        self.InputFeild = wid.textInput(x , y +  self.gap , self.textWidth )
        self.deleteButton = wid.Button("DEL",x  + self.textWidth , y + self.gap,  (200,0,0) , (200,200,200) , self.size , self.__triggerDelete )
        self.createButton = wid.Button("CRT" , x  + self.textWidth + self.deleteButton.TextRect.width  , y + self.gap,  (200,0,0)  , (200,200,200)  ,self.size , self.__triggerCreate )
        self.openButton = wid.Button(">>>" , x  + self.textWidth + self.deleteButton.TextRect.width , y + self.gap + self.createButton.TextRect.height,  (0,0,0)  , (200,200,200)  ,self.size , self.__triggerOpeningTheFile )
        self.y + self.gap + self.createButton.TextRect.height
        self.navBar = wid.Navbar(self.x , self.y + self.gap + self.createButton.TextRect.height , 20 , navbarLimit ,width=200)

        

        self.fileButtonArray:dict = {}
        self.buttongaps  =20
        self.selectedFile = None
        self.modeCOLOR = (50,50,50)

        #herre we have our texture widow
        self.textureBack = wid.textureRect(self.x , self.y , self.textWidth + self.deleteButton.TextRect.width + self.createButton.TextRect.width ,  navbarLimit + 100  , self.modeCOLOR ,  borders=[2,2,2,2] )
        
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
    def __triggerToggle(self):
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



        #seetif the visible of button if any
        for buttons in self.fileButtonArray.values():
            buttons.visible = not buttons.visible
            buttons.active = not buttons.active


        pass
    def __triggerCreate(self):
        #here we are going to create a file // obj files
        if self.InputFeild.value:
            
            #checking the dupliacacy

            for button in self.fileButtonArray.values():
                filename = button.text.split(" ")[1]
                if filename == self.InputFeild.value:
                    #here have consle to handle the error
                    return
                
           
            objfilename = self.InputFeild.value

            #here we adde in file button array to display
            height = self.y + self.gap + self.createButton.TextRect.height  + len(self.fileButtonArray) * self.buttongaps
            button = wid.Button(f"{len(self.fileButtonArray) +1 }. {objfilename} .py" , self.x  , height ,  (0,0,0)  , (200,200,200)  ,self.size , partial(self.__filebuttonselection , objfilename )  )
            #here we have to load windon int o it
            button.loadWindow(self.window)
            self.fileButtonArray[objfilename] = button

            #here we physcall created the file

            


            file = open(f"{self.objectFilePath}\\{objfilename}.py" , "w") 
            #here wear ecopying the required templaye
            shutil.copy("template_folder\\temp1.py" , f"{self.objectFilePath}\\{objfilename}.py")
            file.close()

            #here we are appendind the import file

            file = open(f"{self.projectName}\\objectFileImports.py" , "a") 
            data_to_write = f"import obj_files.{objfilename} as {objfilename}\n" 
            file.write(data_to_write)
            file.close()

        
            #here we are going to refexhs the classsobj rence content
            file = open(f"{self.projectName}\\classObjRef.py" , "w")
            data_to_write = f"from classReferFile import *\nCLASS_ARRAY = " + "{"
            dic_string = [f"'{button.text.split(' ')[1]}': SCENE_REF.{button.text.split(' ')[1]}.mymesh" for button in self.fileButtonArray.values() ]
            final_data_write = data_to_write + ",".join(dic_string) + "}"

            file.write(final_data_write)
            file.close()



            


    def __triggerDelete(self):
        if self.selectedFile == None: return
        #here we aredelting the selected files
        #removing from the directory
        filename = self.fileButtonArray[self.selectedFile].text.split(" ")[1]
        os.remove(f"{self.objectFilePath}\\{filename}.py")

        #corrsspoign gui
        del self.fileButtonArray[self.selectedFile]


        pass

    def linkToProject(self , projectbar):
        
        #here is the link b/w the project manager and the filesystem to 
        #here im upadtin the internal inf0 about pahts


        if projectbar.enableLink:
            print("linked and loaded")
            self.projectName = projectbar.inputFeild.value
            self.objectFilePath = f"{self.projectName}\\obj_files"
            projectbar.enableLink = False

        

        #removie the gui buttons if any
            self.fileButtonArray = {}

        #here loading the files if name as gui
            for filename in glob.glob(f"{self.projectName}\\obj_files\\*"):
    
                #getting the file name
                only_filename = filename.split("\\")[-1]

                only_filename = only_filename.split(".")[0]

                #no button for pychache
                if only_filename.startswith("__") and only_filename.endswith("__"): continue

                height = self.y + self.gap + self.createButton.TextRect.height  + len(self.fileButtonArray) * self.buttongaps
                button = wid.Button(f"{len(self.fileButtonArray) +1 }. {only_filename} .py" , self.x  , height ,  (0,0,0)  , (200,200,200)  ,self.size , partial(self.__filebuttonselection , only_filename ) )
    
                #here we have to load windon int o it
                button.loadWindow(self.window)
                self.fileButtonArray[only_filename] = button
                
            

       

                



        pass
    def __filebuttonselection(self,index):
        self.selectedFile = index
        #playing with the gui stuff
        sfg , sbg = (200,0,0) , (200,200,200)
        #slection coloe
        fg , bg = (200,200,200 ),(0,0,0)
        for buttons in self.fileButtonArray.values(): buttons.retainBg , buttons.retainFg  = bg , fg
        self.fileButtonArray[index].retainFg , self.fileButtonArray[index].retainBg = sfg , sbg
       
        pass

    
    def __triggerOpeningTheFile(self):
        #here the code to open the file
        #let code it
        if self.selectedFile == None: return
        
        filename = self.fileButtonArray[self.selectedFile].text.split(" ")[1]
        os.system(f"start {self.objectFilePath}\\{filename}.py")
        pass

 