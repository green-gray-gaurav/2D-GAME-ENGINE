

class Renderable():
    
    #constanst related toselction of mesh type
    # MESH_TYPE_RECT = 1
    # MESH_TYPE_CUSTOM   = 2

    #reuest types // some of them
    REQUEST_DELETE_MESH = 1
    REQUEST_DETECT_COLL  = 2
    REQUEST_ADD_MESH = 3
    REQUEST_DETECT_INTERSECT = 4
    REQUEST_DETECT_NO_INTERSECT = 5


    def __init__(self , tag) -> None:
        self.mesh_type = None #select the mesh type
        self.mesh_obj = None    #gives the appreance
        self.mesh_type = None
       
        
        self.window  = None

        self.update_callback = None
        self.draw_callback = None
        self.event_callback = None

        self.renderable_tag  = tag #this tag distingusgh differnt renderable objs

        self.request_queue = []


    def set_window(self , window):
        if(window):
            self.window = window    
            return self
        else:
            raise(Exception('cant set window to None `set_window() second argument is None`'))
        pass

    def set_mesh(self  , mesh=None ):
       
        self.mesh_obj = mesh
        self.mesh_type = mesh

        return self
        

        #extension of the normal draw 
    def set_update_callback(self , update_callback:object):

        self.update_callback = update_callback

        pass
    def set_event_callback(self , event_callback : object):

        self.event_callback = event_callback
    def draw(self) : 
        if self.mesh_obj: self.mesh_obj.draw(self.window) #this thing draw in this window
        else :  raise(Exception("Renderable needs a mesh object `use set_mesh()`"))

    def update(self) :
        if(self.update_callback ) : self.update_callback()
        else: raise(Exception('no specified renderable update callback `use set_update()`'))

    def event(self , happend_event):
        if(self.event_callback) : self.event_callback(happend_event)
        else : raise(Exception("no event callback is specified `use set_event_callback()`"))
        pass

    #request avlue
    def send_request(self , request_type : int  , data:list = []):
        self.request_queue.append([request_type , data ])
        pass
    def get_request_queue(self):
        rq = self.request_queue.copy()
        self.request_queue.clear()
        return rq

   

   
        

class Mesh():
    import pygame as pg
    def __init__(self) -> None:

        self.active = True #realted to visibilty
        self.z_index = 0
        self.transform = None
        self.mesh_regions = {}
        self.transformed_mesh_regions = {}

        pass

    def set_inital_tranform(self, pos = [0,0] , rotation = 0 , sx = 1 , sy = 1):
        import math
        import numpy
        self.transform = numpy.array([
            [sx * math.cos(math.radians(rotation)) , -math.sin(math.radians(rotation))   , pos[0]],
            [math.sin(math.radians(rotation)) ,  sy * math.cos(math.radians(rotation))   , pos[1]],
            [0                                ,         0                           , 1      ]
        ])
        pass
    def set_visibility(self , visible = False):
        self.active = visible

    def set_z_index(self , index) : self.z_index = index

    def create_mesh(self , mesh_tag:str , mesh_region:list , mesh_style:tuple , mesh_z_index:int):
        #createa amesh
        self.mesh_regions[mesh_tag] = [mesh_region , mesh_style , mesh_z_index]

        #sorting the mesh list based on z - index
        self.__z_index_sync()
        
        pass

    # def create_mesh_region(self , poly_points:list):
        
    #     pass
    def createMeshStyle(R :  int ,G  :int , B :int , width : int):
        return [(R,G,B) , width]
      
    def remove_mesh_region(self, mesh_tag : str):
        del self.mesh_regions[mesh_tag]
        pass
    
    #updating the mesh
    def update_mesh_region(self , mesh_tag:str , mesh_region:list):
        self.mesh_regions[mesh_tag][0] = mesh_region #updating the mesh region
    
    def update_mesh_style(self , mesh_tag:str , R :  int ,G  :int , B :int , width : int):
        self.mesh_regions[mesh_tag][1] = ((R,G,B),width) 

    def update_mesh_zindex(self , mesh_tag:str , mesh_z_index : int):
        self.mesh_regions[mesh_tag][2] = mesh_z_index 
        self.__z_index_sync()


    def __z_index_sync(self): #to sync the z index
        sorted_keys = sorted(self.mesh_regions , key=lambda k : self.mesh_regions[k][1] )
        self.mesh_regions = {k: self.mesh_regions[k] for  k  in  sorted_keys}
    #drawing the mesh
        
    def draw(self , window):
        if(window == None) : raise(Exception("window can't be None 'pass the second argument `window`'"))
        
        self.transformed_mesh_regions = {tag : [[self.__perform_transformation(point) for point in region] , style , index] 
                             for tag , [region , style , index] in self.mesh_regions.items() }
            
            #performing a regional tranform
        # print(self.transform , transformed_mesh_regions)
        #this thing dtaw tw polygon in the window using the z indcies
        for mesh_tag , mesh_data in self.transformed_mesh_regions.items():
            mesh_region , mesh_style , mesh_z = mesh_data
            mesh_color , mesh_width = mesh_style
            
            #performing a regional tranform
            Mesh.pg.draw.polygon(window , mesh_color , mesh_region , mesh_width)
        pass



    def __perform_transformation(self , point:list):
        import numpy
        point = numpy.array([point.copy() + [1]]).reshape(-1 , 1)
        T =  numpy.matmul(self.transform , point).reshape(1,-1).tolist()[0][:-1]
        return T
  

    def translate(self , x : int , y : int):
        import math
        import numpy
        
        transform = numpy.array([
            [1 , 0  , x],
            [0 , 1  , y],
            [0 , 0  , 1]
        ])
        
        tr = numpy.matmul(transform , self.transform)
        self.transform = tr
       
        
        pass
    def translate_to(self , x : int , y : int):
        self.transform[0][2] = x
        self.transform[1][2] = y
        pass

    def scale(self , sx : int , sy : int , pivot : list = [0,0]):
        import math
        import numpy
        px , py = pivot
        transform = numpy.array([
            [sx , 0  , px * (1- sx)],
            [0 , sy  , py * (1 -sy)],
            [0 , 0  ,       1      ]
        ])
        self.transform = numpy.matmul(transform , self.transform)
    
    def rotation(self , angle , pivot = [0,0]):
        import math
        import numpy
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        px , py = pivot
        transform = numpy.array([
            [ c , -s  ,  px*(1-c) + py*s   ],
            [ s ,  c  ,  py*(1-c) - px*s   ],
            [0  ,  0 ,          1]
        ])
        self.transform = numpy.matmul(transform , self.transform)


    def get_pos(self):
        return self.transform[0][2]  , self.transform[1][2]
    
    def get_scale(self):
        import numpy
        
        sx = numpy.sqrt(numpy.sum(numpy.square(self.transform[:][0]) , axis=0))
        sy = numpy.sqrt(numpy.sum(numpy.square(self.transform[:][1]) , axis=0))

        return sx ,sy
    def get_collision_mask(self):
        regions  = self.transformed_mesh_regions
        collsion_mask = regions[list(regions.keys())[0]][0]
        return collsion_mask 
        pass



        pass


#standard mesh
class MeshRect(Mesh):
    def __init__(self , pos , width , height  , style) -> None:
        super().__init__()
        self.x  ,self.y = pos
        self.width = width
        self.height = height
        self.style = style
        
    def create(self): # to create a mesh
        self.create_mesh(
            "r1" #region tag internal
            ,[[-1 , 1 ] , [1,1] , [1,-1] , [-1,-1]]
            ,self.style
            , 0 #internal settings
        )
        
        self.set_inital_tranform([self.x , self.y] , 0 , self.width/2 , self.height/2)
        return self
    

class SimpleImageMeshRect(MeshRect):
    import pygame
    def __init__(self   , pos , width , height  , style ) -> None:
        super().__init__(pos, width , height  , style)

        self.image = None
        self.relative_scale = None
        self.relative_offset = None
    pass

    def image_setup(self, path :str , offset , scale = None):
        self.image = SimpleImageMeshRect.pygame.image.load(path)
        self.relative_offset = offset
        self.relative_scale = self.image.get_size() if scale == None else scale
        pass
    def set_image_offset(self , offset) :
        self.relative_offset = offset 
    def set_image_scale(self , scale):
        self.relative_scale = scale

    def get_image_offset(self) : return self.relative_offset
    def get_image_scale(self): return self.relative_scale 


    def draw(self , window):
        #herr we are dreaing the backgroung polygon
        super().draw(window)

        if window == None : raise(Exception("window cant be None"))
        #here we are drawing the foregraound image

        #applying the realtive scaling
        self.image = Mesh.pg.transform.scale(self.image , self.relative_scale)
        
        #applying the scaling
        cx , cy  = self.image.get_rect().center
        x , y  = self.get_pos()
        ox , oy = self.relative_offset
        self.image_pos = [x - cx + ox, y - cy + oy]


        #displaying on the screen
        window.blit(self.image , self.image_pos ) #images cant be rotated
