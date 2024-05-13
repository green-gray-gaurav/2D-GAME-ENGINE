from game_module.game_loop import gameLoop
from game_module.renderable_mesh import Renderable , Mesh , MeshRect


class game_object():
    INIT_INSTANCE = True
    CLASS_TAG = "abc" #change it
    def __init__(self , window) -> None:
        self.renderable = Renderable("object1").set_window(window)
        self.mesh = MeshRect([50,50] , 100 , 100 ,MeshRect.createMeshStyle(100,0,0,0)).create()
        

        self.renderable.set_mesh(self.mesh)
        self.renderable.set_update_callback(self.update)
        self.renderable.set_event_callback(self.event)
        
        pass

    def update(self):
        
        
        pass
    def event(self , events):
        import pygame
        for event in events:
           pass
    
   
            
