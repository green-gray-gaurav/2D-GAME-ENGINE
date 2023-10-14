
#here we are going to declare a basic mess calss
import pygame 
import objectFile
import classReferFile

import cmath , math
from functools import reduce
import threading , time
from  vectors import *
import os
import sampleMesh_data


class basicMesh():
    def __init__(self , x = 0  , y = 0 , width  = 10, height = 10 ) -> None:
        #here we go with the flow
        #fist the shape and pos
        #here we have teh unique object id
        self.id = None
        self.name:str
        self.type:str

        #pivot points

        self.pivotOffset = [0,0]
        #cordinates
        self.x = x
        self.y = y
        #here is the rotaion cord
        self.angle = 0

        self.width = width
        self.height = height
        self.center = None
        self.color = (255,255,255)
        self.window = None
        self.windowSize = None
        self.Rect = None
        self.Fullcontrol = True
        self.refCoordinates = [(- self.width/2 ,  - self.height/2) ,
                                ( + self.width/2 , - self.height/2),
                                ( + self.width/2 ,  + self.height/2),
                                (- self.width/2 ,  + self.height/2) ]
        
        self.coordinates = None
        

        #image sprites//
        self.sprite = None
        
        self.wasPlaying = None
        self.animtionPlaying = None
        self.animations = {}

        #light realted
        self.lightmask = True

        #global flags 
        self.restart_flag = False
        self.quit_flag  = False

        #visible 
        self.visible = True



        pass
    def loadinfo(self , window):
        self.window = window
        self.windowSize = (self.window.get_width() , self.window.get_height())
       
        pass
    def oncreate(self):pass
    def update(self ):pass
    def ondelete(self):pass


        #mouse events

    def onMouseDown(self , event):pass
    def onMouseUp(self , event):pass

        #kwyboard events

    def onKeyDown(self , keyInfo):pass
    def onKeyPressed(self , key):pass
    def onKeyReleased(self , key):pass
    

    #here is the collision function

    def onCollisionWith(self , mesh , direction):pass



    #here id the code to sictruc teth sustem
    def eradicate(self):
        self.ondelete()
        for i , obj in enumerate(objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]):
            if obj.id == self.id: objectFile.OBJECT_ARRAY[objectFile.SCENE_NO].pop(i)
        pass


    #here is teh code to acess the other mess using the id
    def accessMeshByName(self , name:str):
        return [ obj for obj in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO] if obj.name == name ]
    

    #here im appending into object array 
    def appendMesh(self , Mesh):

        #id generation
        Mesh.id = objectFile.idGenerator
        objectFile.idGenerator+=1
        #here is the window loader
        Mesh.loadinfo(self.window)
        #here is the oncreate trigger
        Mesh.oncreate()
        objectFile.OBJECT_ARRAY[objectFile.SCENE_NO].append(Mesh)
        pass

    def appendMeshInLayer(self , Mesh , layer):
        #this thing dynmiallic changes the id of the mesh but the name id reminas the same
        layer = max(min(len(objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]) -1, layer) , 0 )

        Mesh.id = objectFile.idGenerator
        objectFile.idGenerator+=1
        #here is the window loader
        Mesh.loadinfo(self.window)
        #here is the oncreate trigger
        Mesh.oncreate()

        objectFile.OBJECT_ARRAY[objectFile.SCENE_NO].insert(layer)
        pass

    #scene realted code
    def changeScne(self ,sceneName):
        #chnage the scene
        objectFile.SCENE_NO = sceneName
        #setting the ids and loading the window
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
            object.id = objectFile.idGenerator
            objectFile.idGenerator+=1
        for object in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
            object.loadinfo(self.window)
            object.create()

    def restartScene(self):
        self.restart_flag = True
        pass
    
    def quitScene(self):
        self.quit_flag = True
        pass


    def appendMeshFromPrefab(self , meshName , prefabName , overrides = {}):

        allMesh = sampleMesh_data.PREFABS[prefabName][1]

        centroid = sampleMesh_data.PREFABS[prefabName][0]

        import classObjRef

        for name , meshprops in allMesh.items():
            newmesh = classObjRef.CLASS_ARRAY[meshprops['type']]()
            #setting the propeties
    
            newmesh.x = centroid[0]
            newmesh.y = centroid[1]
            newmesh.width = meshprops['w']
            newmesh.height = meshprops['h']
            newmesh.name = f"{meshName}___" + meshprops['name']
            newmesh.type =meshprops['type']
            newmesh.color = meshprops['color']
            newmesh.angle = meshprops['angle']
            newmesh.pivotOffset = [   meshprops['x'] - centroid[0], meshprops['y'] - centroid[1] ]
            #here we ,uch change the offset of all to make this rotae around common axis
            self.appendMesh(newmesh)

    def appendMeshFromPrefabOverride(self , meshName, prefabName , overrides = {}):

        allMesh = sampleMesh_data.PREFABS[prefabName][1]
        centroid = sampleMesh_data.PREFABS[prefabName][0]
        import classObjRef

        for name , meshprops in allMesh.items():
            newmesh = classObjRef.CLASS_ARRAY[meshprops['type']]()
            #setting the propeties
            newmesh.x = overrides['x'] if 'x' in overrides.keys() else centroid[0]
            newmesh.y = overrides['y'] if 'y' in overrides.keys() else centroid[1]
            newmesh.width = overrides['w'] if 'w' in overrides.keys() else meshprops['w']
            newmesh.height = overrides['h'] if 'h' in overrides.keys() else meshprops['h']
            newmesh.name = f"{meshName}___" + meshprops['name']
            newmesh.type =overrides['type'] if 'type' in overrides.keys() else meshprops['type']
            newmesh.color = overrides['color'] if 'color' in overrides.keys() else meshprops['color']
            newmesh.angle = overrides['angle'] if 'angle' in overrides.keys() else meshprops['angle']
            newmesh.pivotOffset = [   meshprops['x'] - centroid[0], meshprops['y'] - centroid[1] ]

            #here we ,uch change the offset of all to make this rotae around common axis

            self.appendMesh(newmesh)



    def popPrefabMesh(self , prefabName):
        allmesh = sampleMesh_data.PREFABS[prefabName][1]

        #removing the meah
        for _ , meshprops in allmesh.items():
            for mesh in self.accessMeshByName(meshprops['name']):
                mesh.eradicate()
        pass


    #here is the sprite code
    def setSprite(self , offsetpos = (0,0) , offsetRot = 0 ,imageName = 'mha_logo.png'):

        self.sprite = image(offsetpos,imageName)
        self.sprite.loadWindow(self.window)
        self.sprite.baseObject(self)
        self.sprite.rotateBy(offsetRot)


        pass

    def addAnimation(self , AnimationName , AnimationObj):
        self.animations[AnimationName] = AnimationObj
        
    def playAnimation(self , AnimationName):
        self.wasPlaying = self.animtionPlaying
        self.animtionPlaying = AnimationName

        
        if self.animtionPlaying in self.animations.keys():
            if self.wasPlaying: 
                self.animations[self.wasPlaying].pause()
                self.animations[self.wasPlaying].reset()
                #hrere we strat the new animation thread
            if self.animations[self.animtionPlaying].hasStarted():
                    self.animations[self.animtionPlaying].resume()
            else:
                self.animations[self.animtionPlaying].start()
        pass



    #here is the event code 
    def eventHandler(self ,event):pass
        

    #here is the rendering code

    def render(self):
        #here im writing a render
        if not self.visible : return


        if self.Fullcontrol:
            offsetx , offsety = -self.pivotOffset[0] , -self.pivotOffset[1]

            self.refCoordinates = [(offsetx- self.width/2 , offsety - self.height/2),
                                ( offsetx + self.width/2 , offsety- self.height/2),
                                ( offsetx+ self.width/2 , offsety + self.height/2),
                                (offsetx- self.width/2 ,  offsety+ self.height/2)]
            #here is the full control 
            newCoordinates = [None , None , None , None]
            #cangle conversion
        
            z_mul = complex(math.cos(self.angle*math.pi/180) , - math.sin(self.angle*math.pi/180))
            for i , cord in enumerate(self.refCoordinates):
                new_cord = complex(*cord) * z_mul
                newCoordinates[i] = (self.x + new_cord.real , self.y + new_cord.imag)

            self.coordinates = newCoordinates
            
            #here we gonna make a rect
            self.Rect = pygame.draw.polygon(self.window , self.color , newCoordinates) 

            self.center = reduce( lambda x , y : (x[0]+y[0] , x[1] + y[1]), newCoordinates)
            self.center = (self.center[0]/4 , self.center[1]/4)

            pass


        else:
            self.Rect = pygame.Rect(self.x , self.y , self.width , self.height)
            pygame.draw.rect(self.window , self.color , self.Rect , 0)

        #here we are goint to render the sprite
        if self.sprite:
            self.sprite.render()

        #here imahandling the animation

        if self.animtionPlaying in self.animations.keys():
            self.animations[self.animtionPlaying].renderer(self.window , self)
        
        

        


                






        

    
#some utility classes
class image():
    def __init__(self , pos ,imageName) -> None:
        self.pos = pos
        self.imagePath = f"{classReferFile.PROJ_NAME}\\assets\{imageName}"
        self.image = pygame.image.load(self.imagePath)
        self.baseObj = None
        pass

    def loadWindow(self , window):
        self.window = window

    def baseObject(self , obj):

        self.baseObj = obj
    
    def rotateBy(self , angle):
        #here is the rotaion by angle
        self.image = pygame.transform.rotate(self.image , angle)
        pass


    def render(self):
        #corrdinates
        x , y = self.baseObj.x , self.baseObj.y
        w , h  = self.image.get_rect().size
        pos = [x - w/2 + self.pos[0] , y - h/2 + self.pos[1]]
        self.window.blit(self.image , pos)

        pass





class Timer():
    def __init__(self , timerValue , trigger , onloop = False) -> None:
        self.timerValue = timerValue
        self.timer = 0
        self.trigger = trigger
        self.loop = onloop
        self.thread = threading.Thread(target=self.refreshClock)
        self.initals = None

        self.isPaused = False
        pass

    def start(self):
        self.timer = 0
        self.initals = time.time()
        #initliing the thread
        self.thread.start()
        pass

    def pause(self):
        self.isPaused = True
        
        pass
    def resume(self):
        self.isPaused = False
        pass

    def reset(self):
        self.timer = 0

    def refreshClock(self):
        #gaurd code
        if self.isPaused : return 

        self.timer = time.time() - self.initals

        if self.timer >= self.timerValue:
            #alram!!
            self.trigger()
            #to loop again
            if self.loop:
                self.initals = time.time()
                self.timer = 0
                self.thread = threading.Thread(target=self.refreshClock)
                self.thread.start()
            pass
        else:
            self.thread = threading.Thread(target=self.refreshClock)
            self.thread.start()
        pass
    pass





class rigidBody():
    def __init__(self , mesh , classes = None ,  collisionLimit = 0.1) -> None:
        self.mesh = mesh #alls the info about mesh
        self.classes = classes
        self.rendering_depth = 6
        self.minLimit  = collisionLimit
        #shape of the colllider
        self.isCircular = False

        self.mass = 10

        self.speedx = 0
        self.speedy = 0

        self.isCollided = False

        self.normalForces = []
        self.netNormalForce = complex(0,0)

        pass
    #thisi the main thread
    def motion(self , vector):

        for mesh in objectFile.OBJECT_ARRAY[objectFile.SCENE_NO]:
            if self.classes:
                if mesh.type in self.classes:
                    #here render thr motion
                    self.__renderer(self.mesh , mesh , vector)
                    pass
            else:
                #here render collision for themesh
                if self.mesh.type != mesh.type:
                    self.__renderer(self.mesh , mesh , vector)
                pass
        
        #returning the normal object
        if self.isCollided:
            self.isCollided = False
            #flusiong the force
            nf = self.netNormalForce
            self.netNormalForce = complex(0,0)
            return nf



    def __renderer(self , mesh1 , mesh2 , vector):
        #graurd ode 
        if not mesh2.Rect : return 

        x1 , y1 = mesh1.x , mesh1.y
        vx , vy = vector

        rect = pygame.Rect(x1 + vx  - mesh1.width/2, y1 + vy - mesh1.height/2 , mesh1.width , mesh1.height)
        if self.collisionDetect(rect , mesh2.Rect , self.isCircular):
            #collison has happended
            self.isCollided = True

            vec = vector

            while math.dist((0,0) , vec) > 0.5:

                rect = pygame.Rect(x1 + vec[0]  - mesh1.width/2, y1 + vec[1] - mesh1.height/2 , mesh1.width , mesh1.height)
                if self.collisionDetect(rect , mesh2.Rect , self.isCircular):
                    vec  = [vec[0]/2 , vec[1]/2]
                else:
                    #move the mesh
                    mesh1.x += vec[0]
                    mesh1.y += vec[1]
                    x1 , y1 = mesh1.x , mesh1.y

            #here the collisoin has happended so we can experince the normal force
            #here normal forece depends upon the shape of the collider
            normalVec = complex(0,0) #no normal force
            if self.isCircular:
                normalVec = complex(*mesh1.Rect.center) - complex(*mesh2.Rect.center)
            else:
                x1 , y1 = mesh1.Rect.center
                x2 , y2 = mesh2.Rect.center
                if abs(x1-x2) <= mesh1.width/2 + mesh2.width/2:
                    if y1 > y2 :
                        #down
                        normalVec = complex(0,1)
                    else:
                        #up
                        normalVec = complex(0,-1)
                elif abs(y1-y2) <= mesh1.height/2 + mesh2.height/2:
                    if x1 > x2:
                        #right
                        normalVec = complex(1,0)
                    else:
                        #left
                        normalVec = complex(-1,0)
           
            self.netNormalForce = self.netNormalForce + normalVec

        else:
            #if the colision has happende you cnat move the object
            if not self.isCollided:
                mesh1.x += vx
                mesh1.y += vy
            pass

    def collisionDetect(self , rect1 , rect2 , isCircular):
       
        if isCircular:
            if math.dist(rect1.center , rect2.center) <= rect1.width/2 + rect2.width/2:
                return True
            else:
                return False
        else:
            return rect1.colliderect(rect2)

        pass

    #here we gonna work on gravity
    #futher we gonna work on physisc
    def applyForce(self , mag , direction):
        forcevec = self.__vectorNormalizer(complex(*direction)) * mag

        
        #action of the force
        self.speedx += (forcevec.real)/self.mass
        self.speedy += (forcevec.imag)/self.mass

        #spped infukection the motion
        normal = self.motion([self.speedx , self.speedy])
        
        if normal:
        #with the same magnitude but opposite
            normalforce = self.__vectorNormalizer(normal) 

            # self.speedx += (normalforce.real)/self.mass
            # self.speedy += (normalforce.imag)/self.mass
            projection = self.speedx * normalforce.real + self.speedy * normalforce.imag
            speed = complex(self.speedx , self.speedy) - normalforce * projection
            self.speedx , self.speedy = speed.real , speed.imag
            print(self.speedx , self.speedy , forcevec , normalforce , projection)
            pass

            #imapct should rin it yo zero

        

        pass
        #utility fuctions
    def __vectorNormalizer(self , vec)->complex:
        z = vec
        mod = math.sqrt((z * z.conjugate()).real)
        if mod == 0 : return z
        z = z / mod
        return z



class Animation():
    def __init__(self , offset , frameRate = 10 , loop = False) -> None:
        self.offset = offset
        self.frameRate = frameRate
        self.loop = loop

        #here some internal statr
        self.frames = []
        self.currentFrame = -1
        self.isPlaying = True
        self.mainFrameAvail = True
        self.isOver = False
        self.animHandle = Timer(1/self.frameRate , trigger=self.trigger , onloop = self.loop)

        self.isStarted = False
        pass

    def start(self ):
        self.animHandle.start()
        self.isStarted = True
        
        pass

    def hasStarted(self):
        return self.isStarted

    def reset(self):
        self.resetFrame()
        self.animHandle.reset()

        pass
    def resume(self):
        self.isPlaying = True
        self.animHandle.resume()
        pass
    def pause(self):
        self.isPlaying = False
        self.animHandle.pause()
        pass
    def trigger(self):
        self.mainFrameAvail = True

    def resetFrame(self):
        self.currentFrame =-1

    def addFrame(self , imagepath):
        self.frames.append(image(self.offset , imagepath))

    def addFrames(self , imageDir , imageNameArray):
        for imageName in imageNameArray:
            self.addFrame(f"{imageDir}\\{imageName}")
        pass


    def renderer(self, surface , baseObj):
        self.frames[self.currentFrame].loadWindow(surface)
        self.frames[self.currentFrame].baseObject(baseObj)
        self.frames[self.currentFrame].render()

        if self.isPlaying:
            if self.mainFrameAvail:
                self.currentFrame = (self.currentFrame+1)%len(self.frames)
                if self.currentFrame == len(self.frames) -1 : self.isOver = True
                self.mainFrameAvail = False

        if self.isOver:
            if self.loop:
                self.isOver = False
            else:
                self.isPlaying = False

        pass



class dataBase():
    def __init__(self) -> None:

        self.selectedCollection = None
        self.collectionData = {}
        self.collectionPath = None


        self.parser = {'str' : lambda s : str(s) 
                       ,'int' : lambda i : int(i)
                       ,'listi' : lambda l : map(lambda i : int(i.strip()) , l[1:-1].split(','))
                       ,'lists' : lambda l : map(lambda i : i.strip() , l[1:-1].split(','))}
        pass

    def createCollection(self , name):
        file = open(f"{classReferFile.PROJ_NAME}\\saved_data\{name}.txt" , 'w')
        file.close()
        pass

    def selectCollection(self , name):
        #nulling the ditinary
        self.collectionData = {}

        self.collectionPath = f"{classReferFile.PROJ_NAME}\\saved_data\{name}.txt"
        #retriving the data of collection side the file 
        file = open(self.collectionPath, 'r')
        for line in file.readlines():
            key , value , type = line.split(':')
            self.collectionData[key] = [self.parser[type](value) , type]
        pass

    def getData(self , key ):
        if key in self.collectionData.keys():
            return self.collectionData[key][0]
        pass

    def addData(self ,key , value , type):
        if key not in self.collectionData.keys():
            self.collectionData[key] = [value , type]
        pass
    def deleteCollection(self, name):
        #delectio nofcollections
        os.remove(self.collectionPath)
        self.collectionData = {}

        pass
    def updateData(self , key , value , type):
        if key in self.collectionData.keys():
            self.collectionData[key] = [value , type]
        pass

    def updateCollection(self):
        #wrting the colletio file
        
        file = open(self.collectionPath , 'w')
        for key , value in self.collectionData.items():
            file.write(f"{key}:{value[0]}:{value[1]}")
        file.close()

        pass


    