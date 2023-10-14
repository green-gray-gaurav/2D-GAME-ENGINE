#here is the utilitycall to the person suing my engine
import pygame 
class TextMeshPro():
    def __init__(self  , text , x , y , bg , fg , size , padding:tuple  = (10,10) , borderRad:list  =[-1,-1,-1,-1],  font = "freesansbold.ttf") -> None:
        self.text = text
        self.x = x 
        self.y = y
        self.paddingx = padding[0]
        self.paddingy = padding[1]
        self.borderRad = borderRad
        self.bg  = bg
        self.fg = fg
        self.size = size
        self.font = font
        self.window  = None
        self.TextRect = None
        self.visible = True
        

        #here we are doing this inital assignment
        font = pygame.font.Font(self.font , self.size)
        text = font.render(self.text , True , self.fg , self.bg  )
        rect = text.get_rect()
        self.TextRect = rect

        #here is the rect
        self.Rect = pygame.Rect(self.x - self.paddingx , self.y - self.paddingy , self.TextRect.width + 2 * self.paddingx , self.TextRect.height + 2 * self.paddingy)

        pass
    def loadWindow(self , window):
        self.window = window
        pass
    def renderWidget(self):
        if self.visible:
            #here is the backgroubd
            self.Rect = pygame.Rect(self.x - self.paddingx , self.y - self.paddingy , self.TextRect.width + 2 * self.paddingx , self.TextRect.height + 2 * self.paddingy)
            pygame.draw.rect(self.window , self.bg , self.Rect , 0 , -1 , *self.borderRad)
            #here is the text
            font = pygame.font.Font(self.font , self.size)
            text = font.render(self.text , True , self.fg , self.bg  )
            rect = text.get_rect()
            self.TextRect = rect
            rect.center = (self.x + rect.width/2 , self.y + rect.height/2)
            self.window.blit(text , rect )
        pass




class Button():
   
    def __init__(self , textObject , clickTrigger) -> None:
        #here is the text ojbjec t
        self.textObject = textObject

        self.mouseevent = "out"
        self.triggerFunctions = [lambda : 0, lambda :0,lambda :0 ,lambda : 0]
        self.triggerFunction = clickTrigger

        self.onenterbg = (255,255,255)
        self.onleavebg = (0,0,0)
        self.onenterfg = (255,0,0)
        self.onleavefg = (255,255,255)
        self.ontriggerbg = (255,255,255)
        self.ontriggerfg = (0,0,0)

        self.active = True

        #retention proopeties // deplicates
        #//
        self.retainBg = self.bg
        self.retainFg = self.fg

    def loadWindow(self, window):
        self.textObject.loadWindow(window)
        

    def renderWidget(self):
        self.textObject.renderWidget()
    
    def eventRender(self , event):
        
        if event == None or not self.active:  
            return
        
       
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.textObject.Rect.collidepoint(event.pos):
                self.triggerFunction()

                self.bg = self.ontriggerbg
                self.fg = self.ontriggerfg
                
                pass

        if event.type == pygame.MOUSEMOTION:
            if self.mouseevent == "out":
                if self.textObject.Rect.collidepoint(event.pos):
                    #on mouse enter

                    self.triggerFunctions[0]()

                    #setitng the buttons proerties
                    self.bg = self.onenterbg
                    self.fg = self.onenterfg

                    self.mouseevent = "in"
                    pass

            if self.mouseevent == "in":
                if not self.textObject.Rect.collidepoint(event.pos):
                    #on mouse leave
                    self.triggerFunctions[1]()

                    self.bg = self.onleavebg
                    self.fg = self.onleavefg

                    self.mouseevent = "out"
                    pass
            
            if self.mouseevent == "in" :

                if self.textObject.Rect.collidepoint(event.pos):

                    self.triggerFunctions[2]()

                    
                    #mouse hover
                    self.mouseevent = "in"
                    pass

            if event.type == pygame.MOUSEMOTION:
                
                if self.mouseevent == "out" :
                    if not self.textObject.Rect.collidepoint(event.pos):
                        #on mouse enter

                    #setitng the buttons proerties
                        self.bg = self.retainBg
                        self.fg = self.retainFg

                        self.mouseevent = "out"
                        pass
        