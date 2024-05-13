from game_module.game_loop import gameLoop
from game_module.renderable_mesh import Renderable , Mesh , MeshRect  ,SimpleImageMeshRect


class game_object_background():
    INIT_INSTANCE = True
    CLASS_TAG = "background" #change it
    def __init__(self , window) -> None:

        self.w , self.h  = window.get_size() 

        self.renderable = Renderable("back").set_window(window)
        self.mesh = SimpleImageMeshRect([self.w/2 , self.h/2] , 0 , 0 ,MeshRect.createMeshStyle(0,0,0,1)).create()
        
        self.mesh.image_setup("assets/flappy/objs/background-day.png" , (0,0) , (self.w,self.h))
        self.renderable.set_mesh(self.mesh)
        self.renderable.set_update_callback(self.update)
        self.renderable.set_event_callback(self.event)
        self.mesh.set_z_index(1)
        pass
    def update(self):pass
    def event(self , events):
           pass



class game_object_background2():
    INIT_INSTANCE = True
    CLASS_TAG = "background2" #change it
    def __init__(self , window) -> None:

        self.w , self.h  = window.get_size() 

        self.renderable = Renderable("back2").set_window(window)
        self.mesh = SimpleImageMeshRect([self.w/2 , self.h/2] , 0 , 0 ,MeshRect.createMeshStyle(0,0,0,1)).create()
        
        self.mesh.image_setup("assets/flappy/UI/gameover.png" , (0,0))
        self.renderable.set_mesh(self.mesh)
        self.renderable.set_update_callback(self.update)
        self.renderable.set_event_callback(self.event)
        self.mesh.set_z_index(0)
        pass
    def update(self):pass
    def event(self , events):
           pass
            
