#a projects that solves an daily life problem
#a python game 


#python game is the best i can say 
REQUEST_DELETE_MESH = 1
REQUEST_DETECT_COLL  = 2
REQUEST_ADD_MESH = 3
REQUEST_DETECT_INTERSECT = 4
REQUEST_DETECT_NO_INTERSECT = 5

class gameLoop():
    import pygame
    import sys
   

    def __init__(self , window_width , window_height , fps , window_title = None , window_icon = None):
        

        self.W = window_width
        self.H = window_height
        self.FPS = fps

        self.window_title = window_title
        self.window_icon = window_icon 


        gameLoop.pygame.init()


        self.window = gameLoop.pygame.display.set_mode((self.W , self.H))
        
        if(self.window_title) : 
            gameLoop.pygame.display.set_caption(self.window_title)
        if(self.window_icon):
            gameLoop.pygame.display.set_icon(gameLoop.pygame.image.load(window_icon))

        self.clock  = gameLoop.pygame.time.Clock()

        self.renderable_list = {}
        self.game_object_classes = {}

    def get_window(self) : return self.window
        
    def add_renderable(self , renderable):
        self.renderable_list[renderable.renderable_tag] = renderable
        
    def add_game_object_classes(self , class_dict):
        self.game_object_classes = class_dict

    def __z_index_sync(self):
        self.renderable_list = dict(sorted(self.renderable_list.items() , key =  lambda x : x[1].mesh_obj.z_index))
        
        pass
    def start(self):

        renderable_request_queue = []
        renderable_pending_queue = []
        
        self.__z_index_sync()
        while True:
            happend_event = []

            for event in gameLoop.pygame.event.get():
                if(event.type == gameLoop.pygame.QUIT):
                    gameLoop.pygame.quit()
                    gameLoop.sys.exit(0)
                
                happend_event += [event]
                

            #render the renderable
            for tag , renderable in self.renderable_list.items():
                renderable.draw()
                renderable.update()
                renderable.event(happend_event)
                renderable_request_queue += renderable.get_request_queue()
                renderable_request_queue += renderable_pending_queue
               
                renderable_pending_queue.clear() #flusig the pednign queue
               

            
            #handling queue events
            
            while(len(renderable_request_queue) > 0):
                request =  renderable_request_queue.pop(0)
                pending = self.__request_handler(request)
                if(pending):renderable_pending_queue += pending
                pass
                

            gameLoop.pygame.display.update()
            
            self.window.fill((0,0,0))
            
            self.clock.tick(self.FPS) #30 fps 
            
            pass
    def __request_handler(self , request):
        
        request_type , data = request
        
        if request_type == REQUEST_DELETE_MESH:
            if data[0] in self.renderable_list.keys():
                del self.renderable_list[data[0]]
            print(self.renderable_list.items())
            
            
            
        if request_type == REQUEST_DETECT_COLL:
            #collision detation code in polygon
            if data[0] in self.renderable_list.keys() and data[1] in self.renderable_list.keys():
                #deepest region of the mesh by default acts as collsion mask

                regions  = self.renderable_list[data[0]].mesh_obj.transformed_mesh_regions
                collsion_mask1 = regions[list(regions.keys())[0]][0] 

                regions  = self.renderable_list[data[1]].mesh_obj.transformed_mesh_regions
                collsion_mask2 = regions[list(regions.keys())[0]] [0]

                from shapely.geometry import Polygon
                p1 = Polygon(collsion_mask1)
                p2 = Polygon(collsion_mask2)
                
                if(p1.intersects(p2)):
                    data[2](data[1])
                else:
                    return [request] #re queing the requeset again // in the pedning queue
                    
        
            pass
        if request_type == REQUEST_ADD_MESH:
            #0 - > class tag
            #1 --> renderable tag

            if len(data) > 1 and data[0] in self.game_object_classes.keys():
                render = self.game_object_classes[data[0]](self.window).renderable
                render.renderable_tag = data[1]
                self.add_renderable(render)

                self.__z_index_sync()
               
        if request_type == REQUEST_DETECT_INTERSECT:
            if len(data) > 2:
                #deepest region of the mesh by default acts as collsion mask
                collision_mask1 = data[0]
                collision_mask2 = data[1]

                if(type(data[0]) is str): 
                    if data[0] in self.renderable_list.keys():
                        regions  = self.renderable_list[data[0]].mesh_obj.transformed_mesh_regions
                        collision_mask1 = regions[list(regions.keys())[0]][0]
                
                if(type(data[1]) is str): 
                    if data[1] in self.renderable_list.keys():
                        regions  = self.renderable_list[data[1]].mesh_obj.transformed_mesh_regions
                        collision_mask2 = regions[list(regions.keys())[0]][0] 


                from shapely.geometry import Polygon
                p1 = Polygon(collision_mask1)
                p2 = Polygon(collision_mask2)
                
                if(p1.intersects(p2)):
                    data[2](data[1])
                else:
                    return [request] #re queing the requeset again // in the pedning queue
                    
            pass

        if request_type == REQUEST_DETECT_NO_INTERSECT:
            if len(data) > 2:
                #deepest region of the mesh by default acts as collsion mask
                collision_mask1 = data[0]
                collision_mask2 = data[1]
                
                if(type(data[0]) is str): 
                    if data[0] in self.renderable_list.keys():
                        regions  = self.renderable_list[data[0]].mesh_obj.transformed_mesh_regions
                        collision_mask1 = regions[list(regions.keys())[0]][0]
                
                if(type(data[1]) is str): 
                    if data[1] in self.renderable_list.keys():
                        regions  = self.renderable_list[data[1]].mesh_obj.transformed_mesh_regions
                        collision_mask2 = regions[list(regions.keys())[0]][0] 


                from shapely.geometry import Polygon
                p1 = Polygon(collision_mask1)
                p2 = Polygon(collision_mask2)
                
                if(not p1.intersects(p2)):
                    data[2](data[1])
                else:
                    return [request]#re queing the requeset again // in the pedning queue
                    
            pass
               
        pass