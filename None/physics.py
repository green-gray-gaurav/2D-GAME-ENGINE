import objectFile 
import vectors
import pygame
import math


class Light():
    def __init__(self , pos , color , intense , range , region):

        self.pos = pos
        self.color = color
        self.intense = intense
        self.range = range
        #internal var or state
        region = [vectors.vector2D(*vec) for vec in region]
        self.lightRegion = [region]

        self.sortedMesh = []

        self.renderingPoints = []

        pass

    def rayTracing(self):
        #sorting the mesh by the distance from th lihgt source
        lightSource = vectors.vector2D(*self.pos)

        #getitn the masked mesh only
        maskedMeshList = []
        for index in objectFile.LIGHT_MASK:
            maskedMeshList.append(objectFile.OBJECT_ARRAY[objectFile.SCENE_NO][index])

        #if there notin in the maked mesh list
        if not maskedMeshList:return
        #otherwise

        self.sortedMesh = sorted( maskedMeshList , key = lambda mesh : (vectors.vector2D(*mesh.Rect.center) - lightSource).magnutude())

        for mesh in self.sortedMesh:
            vecCenter = vectors.vector2D(*mesh.Rect.center) - lightSource
            vecs = [vectors.vector2D(*v) - lightSource  for v in mesh.coordinates]


            ex1 = sorted(vecs , key = lambda v : vecs[0].angleWith(v) , reverse=True)[0]
            ex2 = sorted(vecs , key = lambda v : ex1.angleWith(v) , reverse=True)[0]
            mag_com = max(ex1.magnutude() ,ex2.magnutude())
            inters = [v for v in vecs if v.magnutude() < mag_com and v.magnutude()!= ex2.magnutude()]

            #checking for the range 

            if inters:
                if self.range < inters[0].magnutude():
                    return
            else:
                if self.range < min(ex1.magnutude() , ex2.magnutude()):
                    return

        #if inse the ligth range
        #selection the region
            fallRegion = None
            fallInfo = None
            for i , region in enumerate(self.lightRegion):
                fallInfo = [ex1.inBetween(*region) , ex2.inBetween(*region)]
                if fallInfo[0] or fallInfo[1]:
                    fallRegion = self.lightRegion.pop(i)
                    break
            #if its out sideth elight zone
            if not fallRegion : 
                return

            #if in osthe rgion them bistion the fallregion
            orderedExtremes = sorted([ex1 , ex2] , key = lambda p : p.angleWith(fallRegion[0]))
            fallInfo = [ex1.inBetween(*orderedExtremes) , ex2.inBetween(*orderedExtremes)]

            if fallInfo == [True , True]:
                #adding into the rendering oints
                self.renderingPoints.append([vecCenter , ex1 , ex2])
                self.lightRegion.append([fallRegion[0] , orderedExtremes[0]])
                self.lightRegion.append([fallRegion[0] , orderedExtremes[1]])

            if fallInfo == [True , False]:
    
                #here we acan writthe bloacking code
                b1 , b2 = fallRegion
                v1 , v2 = orderedExtremes
                if inters:
                    dir2 = (inters[0] - v2).normalized
                else:
                    dir2 = (v1 - v2).normalized()
                lmda2 = -v2.dot(b2.normalized())/dir2.dot(b2.normalized())
                self.renderingPoints.append([ ex1 , vecCenter ,  v1 + dir2 * lmda2] + inters)

                #divied light region
                self.lightRegion.append([fallRegion[0] , orderedExtremes[0]])

                pass
            if fallInfo == [False , True]:

                #here we acan writthe bloacking code
                b1 , b2 = fallRegion
                v1 , v2 = orderedExtremes
                if inters:
                    dir1 = (inters[0] - v1).normalized
                else:
                    dir1 = (v2 - v1).normalized()
                lmda1 = -v1.dot(b1.normalized())/dir1.dot(b1.normalized())
                
                self.renderingPoints.append([ex2 , vecCenter ,  v1 + dir2 * lmda2] + inters)

                #divied light region
                self.lightRegion.append([fallRegion[0] , orderedExtremes[1]])

                pass
            if fallInfo == [False , False]:
                #here we acan writthe bloacking code
                b1 , b2 = fallRegion
                v1 , v2 = orderedExtremes
                if inters:
                    dir1 = (inters[0] - v1).normalized
                    dir2 = (inters[0] - v2).normalized
                else:
                    dir1 = (v2 - v1).normalized()
                    dir2 = (v1 - v2).normalized()

                lmda1 = -v1.dot(b1.normalized())/dir1.dot(b1.normalized())
                lmda2 = -v2.dot(b2.normalized())/dir2.dot(b2.normalized())
                self.renderingPoints.append([ v1 + dir1 * lmda1 , vecCenter ,  v1 + dir2 * lmda2] + inters)

                pass

        pass

    def render(self , surface):
        #hre is teh rendering part
        #here we rnder teh rendering points and teh leftout light region
        #this hit im goona do today
        for points in self.renderingPoints:
            pointsInArray = [p + self.li for p in points]
            pygame.draw.polygon(surface , self.color , pointsInArray)

        #hrere to render the lef t out region
        #hre the rgion
        for region in self.lightRegion:
            start , end = region[0].angleWithX() , region[1].angleWithX()
            cf = math.pi / 180
            pygame.draw.arc(surface , self.color , pygame.Rect(self.pos[0] - self.range , self.pos[1] - self.range , 2 * self.range , 2 * self.range), cf * start , cf *  end)

            pass


        
        
        





        pass
    
    

