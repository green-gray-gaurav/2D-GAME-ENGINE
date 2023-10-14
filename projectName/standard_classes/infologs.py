import standard_classes.widgets as wid
import os

class infoLogbar():

    def __init__(self ,x , y , textsize , width , showLimit = 5 , switchPos = (10,10)) -> None:
        self.logArray  = []
        self.errorArray = []
        self.x = x
        self.y = y
        self.width = width
        self.textsize = textsize
        self.textCharLimit = 58
        self.gap = 22
        self.showLimit = showLimit
        self.visible = True
        self.colorMode = (50,50,50)
        
        self.switchPos = switchPos
        self.switchToggle = wid.Button("@" , self.switchPos[0] , switchPos[1] , (0,0,0) , (200,0,0) , textsize , self.__triggerToggle)

        self.logButton = wid.Button("LOGS" , x , y , (255,255,255) , (0,0,0) , textsize , self.__triggerLog)
        self.circularNav = wid.Button("NAV <>" , x + self.logButton.TextRect.width, y , (255,255,255) , (200,0,0) , textsize , self.__triggerNav)
        self.clearButton = wid.Button("CLEAR" , x + self.logButton.TextRect.width  + self.circularNav.TextRect.width, y , (255,255,255) , (200,0,0) , textsize , self.__triggerflush)
        self.errorButton = wid.Button("ERRORS" , x +  self.logButton.TextRect.width  + self.circularNav.TextRect.width + self.clearButton.TextRect.width , y , (255,255,255) , (0,0,0) , textsize , self.__triggerError)
        
        #here we have our backgrounf of the console window
        self.textureback = wid.textureRect(self.x , self.y , self.width , self.logButton.TextRect.height  + self.gap * self.showLimit , color = self.colorMode, borders=[5,5,5,5])
        
        #here lets write the text limit
        self.textRegion = [] 
        self.logmessages = [[] , 0]
        self.errormessages = [[] , 0]

        self.recent_selected  = 0

        



        for i in range(self.showLimit):
            text = wid.TextMesh("" , x , y + self.logButton.TextRect.height  + self.gap * (i) , (200,0,0) , (0,0,0) , self.textsize)
            self.textRegion.append(text)

        #initliliaxtion some function to set the inital state
        self.__triggerToggle()


        pass

    def loadWindow(self  , window):
        #load the window of all widgets
        self.logButton.loadWindow(window)
        self.errorButton.loadWindow(window)
        self.switchToggle.loadWindow(window)
        self.circularNav.loadWindow(window)
        self.clearButton.loadWindow(window)
        self.textureback.loadWindow(window)
        for textwig in self.textRegion:
            textwig.loadWindow(window)
        

        pass

    def eventHandler(self , event):
        self.logButton.eventRender(event)
        self.errorButton.eventRender(event)
        self.switchToggle.eventRender(event)
        self.circularNav.eventRender(event)
        self.clearButton.eventRender(event)
        
        pass

    def renderWindow(self):
        #render the widhets
        #backgroubd windows
        self.textureback.renderWidget()

        #forefron t window
        self.logButton.renderWidget()
        self.errorButton.renderWidget()
        self.switchToggle.renderWidget()
        self.circularNav.renderWidget()
        self.clearButton.renderWidget()
        
        for textwig in self.textRegion:
            textwig.renderWidget()
        pass

    def __flushTextMeshArray(self):
        for text in self.textRegion:
            text.text = ""
        pass
        


    def __triggerLog(self):
        #flusing the buffers
        self.__flushTextMeshArray()



        self.recent_selected = 0
        print("___this is log terminal")

        #here we are going to load the fucking messages
        #here is some gaurd code
        #other wise
        msgs , state = self.logmessages
        for i in range(min(len(msgs), self.showLimit)):
            self.textRegion[i].text = msgs[i + state]
            pass
        pass

    def __triggerError(self):
        #flushinf the buffer
        self.__flushTextMeshArray()

        self.recent_selected = 1
        print("___this is error terminal")
        #some gaurd code
        msgs , state = self.errormessages
        for i in range(min(len(msgs), self.showLimit)):
            self.textRegion[i].text = msgs[i + state]
            pass
        

        pass

    def __triggerToggle(self):
        #here we are goint i toggle the visibilty / active  property
        self.errorButton.visible = not  self.errorButton.visible
        self.errorButton.active = not  self.errorButton.active

        self.logButton.visible = not  self.logButton.visible
        self.logButton.active = not  self.logButton.active

        self.circularNav.visible = not  self.circularNav.visible
        self.circularNav.active = not  self.circularNav.active

        self.clearButton.visible = not  self.clearButton.visible
        self.clearButton.active = not  self.clearButton.active

        self.textureback.visible = not  self.textureback.visible


        for  i in self.textRegion: i.visible = not i.visible

        #here is teh thing 
        self.visible = not self.visible

        pass

    def __triggerNav(self):
        if self.recent_selected ==0:

            _ , state = self.logmessages
            if len(_) - (state + 1) >= self.showLimit:
                self.logmessages[1] = (self.logmessages[1] +1) % self.showLimit
            else:
                self.logmessages[1] = 0
            self.__triggerLog()

           
        
        else:
            _ , state = self.errormessages
            if len(_) - (state + 1) >= self.showLimit:
                self.errormessages[1] = (self.errormessages[1] +1) % self.showLimit
            else:
                self.errormessages[1] = 0
            self.__triggerError()
        pass
    
    def __triggerflush(self):
        if self.recent_selected == 1:
            self.errormessages = [[],0]
            self.__triggerError()
        else:
            self.logmessages = [[],0]
            self.__triggerLog()
        pass 

    def Log(self , *text):
        log_string = " ".join(tuple(map(str , text)))
        
        for msgs in self.__limitSlicing(log_string)[::-1]:
            self.logmessages[0].insert(0 , msgs)


        pass
    def Error(self , errorMessage:str):
        for msgs in self.__limitSlicing(errorMessage)[::-1]:
            self.errormessages[0].insert(0 , msgs)
        pass

    def showErrorTab(self):
        self.__triggerError()
        if not self.visible:
            self.__triggerToggle()
        pass

    def showLogTab(self):
        self.__triggerLog()
        if not self.visible:
            self.__triggerToggle()
        pass



    #here is slicing string funito
    def __limitSlicing(self , string):
        sliced = [string]
        while len(sliced[-1]) >= self.textCharLimit:
            strToSlice = sliced.pop()
            sliced.append(strToSlice[0:self.textCharLimit+1])
            sliced.append(strToSlice[self.textCharLimit+1:])
            #here we do slcing
        return sliced 
        pass



        

