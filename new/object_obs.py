from game_module.game_loop import gameLoop
from game_module.renderable_mesh import Renderable , Mesh , MeshRect  ,SimpleImageMeshRect


class game_object__obs():
    INIT_INSTANCE = True
    CLASS_TAG = "obstacles" #change it
    def __init__(self , window) -> None:

        self.render_name = ["first"] #handling the names

        self.w , self.h  = window.get_size() 
        

        self.renderable = Renderable("first").set_window(window)
        self.mesh = SimpleImageMeshRect([self.w - 70 , self.h-200] , 70 , 400 ,MeshRect.createMeshStyle(100,0,0,1)).create()
        
        

        self.mesh.image_setup("assets/flappy/objs/pipe-green.png" , (0,0) , (70,400))
        self.renderable.set_mesh(self.mesh)
        self.renderable.set_update_callback(self.update)
        self.renderable.set_event_callback(self.event)
        
        self.vec_x = -5

        self.mesh.draw(window)

        self.screen_collision_mask = [[0,0] , [self.w , 0] , [self.w , self.h] , [0 , self.h]]

        
        

        self.renderable.send_request(self.renderable.REQUEST_DETECT_NO_INTERSECT ,
                                      [ "first" , 
                                       self.screen_collision_mask , 
                                       self.collision

                                     ])
        
        
        self.mesh.set_z_index(3)

        


        pass
    def update(self):
        
        self.mesh.translate(self.vec_x,0)
        
        pass
    def event(self , events):
        import pygame
        for event in events:
          
           pass

    def collision(self  , c):
        import random
        r = random.randint(0 , 200)
        self.mesh.translate_to(self.w-70 , self.h-200 + r)
        


        self.renderable.send_request(self.renderable.REQUEST_DETECT_NO_INTERSECT ,
                                      [ "first" , 
                                       self.screen_collision_mask , 
                                       self.collision

                                     ])
    
   
            
