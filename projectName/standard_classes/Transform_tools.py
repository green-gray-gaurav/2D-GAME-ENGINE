import standard_classes.widgets as wid
from functools import partial
import pygame , math


class transformTool():
    
    def __init__(self , x , y , radius ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.window  = None

        #intercomponets 
        self.buttonTX = None
        self.buttonTY = None
        self.buttonRA = None
        self.buttonRC = None
        self.buttonSX = None
        self.buttonSY = None

        self.dot = None


        self.active = False
        self.prop = None

        self.transformAction = None
        self.ctrlBuffer = False

        pass

    def loadWindow(self ,window):
        self.window = window
        #here to make the bitons once
        self.renderWindow()
        pass

    def renderEvent(self ,event):

        if self.transformAction:
            if self.dot : self.dot.renderEvent(event)

        if not self.active: 
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                self.transformAction = None
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.x ,self.y = pygame.mouse.get_pos()
                self.active = True
            

                #creating the butoons
                self.renderer()
            return
        
        #if any of thebutton is not craeted get ou tofroutine
        if not self.buttonTX : return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #clsog the tools 
            self.active = False
            self.transformAction = None

        self.buttonRA.renderEvent(event)
        self.buttonRC.renderEvent(event)
        self.buttonTX.renderEvent(event)
        self.buttonTY.renderEvent(event)
        self.buttonSX.renderEvent(event)
        self.buttonSY.renderEvent(event)
        


        pass

    def Linker(self , prop):
        self.prop = prop
        pass

    def renderWindow(self):

        #dot for the refence of the change
        if self.transformAction:
                if self.dot : self.dot.renderWindow()
        

    
        if self.prop:

            mx , my = pygame.mouse.get_pos()
            if self.transformAction == "TX":
                self.prop.updateTransfomProperties('x' ,  mx - self.x)
                print(self.x - mx)
                pass
            if self.transformAction == "TY":
                self.prop.updateTransfomProperties('y' , my - self.y)
                pass
            if self.transformAction == "RA":

                if mx - self.x : 

                    angle = math.atan((self.y - my) / (self.x - mx)) * 180 / math.pi

                    #here are some calculatin for angle
                    Y , X = self.y - my , self.x - mx
                    true_angle = angle
                    if Y > 0 and X > 0:pass
                    if Y > 0 and X < 0:true_angle = 180 + angle
                    if Y < 0 and X < 0:true_angle = 180 + angle
                    if Y < 0 and X > 0:true_angle = 360 + angle   


                    self.prop.updateTransfomProperties('angle' , -round(true_angle, 4))


                pass
            if self.transformAction == "RC":
                if mx - self.x : 
                    angle = math.atan((self.y - my) / (self.x - mx)) * 180 / math.pi
                    self.prop.updateTransfomProperties('angle' , round(angle, 4))
                pass
            if self.transformAction == "SX":
                self.prop.updateTransfomProperties('w' , mx - self.x)
                pass
            if self.transformAction == "SY":
                self.prop.updateTransfomProperties('h' , my - self.y)

                pass
        

        if not self.active : return

        self.buttonRA.renderWindow()
        self.buttonRC.renderWindow()
        self.buttonTX.renderWindow()
        self.buttonTY.renderWindow()
        self.buttonSX.renderWindow()
        self.buttonSY.renderWindow()

        
        

        

        pass
    pass

    def renderer(self):
        self.buttonTX = wid.interactiveShape(self.x ,self.y , "poly" , [[0 ,+ self.radius/2]
                                                                                        ,[ + self.radius/2 , + self.radius*3/4]
                                                                                        ,[0  ,+ self.radius]] , partial(self.triggerFunc , "TX"))
        self.buttonTY = wid.interactiveShape(self.x ,self.y , "poly" , [[ -self.radius/2 ,0]
                                                                                      ,[ - self.radius * 3 /4 ,  - self.radius/2]
                                                                                      ,[ - self.radius ,0]] , partial(self.triggerFunc , "TY"))
        self.buttonRA = wid.interactiveShape(self.x  ,self.y ,"poly" , [[-self.radius/2 , 0],
                                                                         [-self.radius/2 , self.radius/2],
                                                                         [0 ,self.radius/2]] ,partial(self.triggerFunc , "RA"))
        self.buttonRC = wid.interactiveShape(self.x ,self.y , "poly" , [[-self.radius , + self.radius/2],
                                                                        [-self.radius/2 ,self.radius/2],
                                                                        [-self.radius/2 , self.radius]] , partial(self.triggerFunc , "RC"))
        self.buttonSY = wid.interactiveShape(self.x - self.radius ,self.y , "rect" , [self.radius/2 ,self.radius/2] , partial(self.triggerFunc , "SY"))
        self.buttonSX = wid.interactiveShape(self.x  -self.radius/2,self.y+ self.radius/2, "rect" , [self.radius/2 ,self.radius/2] , partial(self.triggerFunc , "SX"))


        self.dot = wid.interactiveShape(self.x , self.y , "circle" , [self.radius/5] , lambda :0)


        self.buttonRA.loadWindow(self.window)
        self.buttonRC.loadWindow(self.window)
        self.buttonTX.loadWindow(self.window)
        self.buttonTY.loadWindow(self.window)
        self.buttonSX.loadWindow(self.window)
        self.buttonSY.loadWindow(self.window)
        self.dot.loadWindow(self.window)

        self.buttonRA.setColor('normal' , (200,0,0), (200,0,0))
        self.buttonRC.setColor('normal' , (200,0,0), (200,0,0))
        self.buttonTX.setColor('normal' , (0,0,200), (0,0,200))
        self.buttonTY.setColor('normal' , (0,0,200), (0,0,200))
        self.buttonSX.setColor('normal' , (0,200,0), (0,200,0))
        self.buttonSY.setColor('normal' , (0,200,0), (0,200,0))
        self.dot.setColor('normal' , (200,0,0), (200,0,0))

        


        


        pass


    def triggerFunc(self  , button):

        self.transformAction = button

       

        #make it inactive

        self.active = False


        
        pass
