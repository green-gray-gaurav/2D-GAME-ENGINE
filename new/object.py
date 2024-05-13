from game_module.game_loop import gameLoop
from game_module.renderable_mesh import Renderable , Mesh , MeshRect  ,SimpleImageMeshRect


class game_object__flappy_bird():
    INIT_INSTANCE = True
    CLASS_TAG = "abc" #change it
    def __init__(self , window) -> None:
        self.renderable = Renderable("object1").set_window(window)
        self.mesh = SimpleImageMeshRect([50,50] , 50 , 50 ,MeshRect.createMeshStyle(0,0,0,1)).create()
        

        self.mesh.image_setup("assets/flappy/objs/yellowbird-midflap.png" , (0,0) , (50,50))
        self.renderable.set_mesh(self.mesh)
        self.renderable.set_update_callback(self.update)
        self.renderable.set_event_callback(self.event)
        
        self.accleration_y = 0.5
        self.vec_y = 0

        self.JUMP = 11
        self.mesh.set_z_index(3)

        self.is_over = False

        self.renderable.send_request(self.renderable.REQUEST_DETECT_COLL , ["object1" , "first" , self.game_over ])
        pass

    def update(self):
        self.vec_y += self.accleration_y
        self.mesh.translate( 0 , self.vec_y)
        if(self.vec_y > 0):
            self.mesh.image_setup("assets/flappy/objs/yellowbird-midflap.png" , (0,0) , (50,50))
        
        pass
    def event(self , events):
        import pygame
        if(self.is_over) : return
        for event in events:
           if(event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.vec_y -= self.JUMP
                self.mesh.image_setup("assets/flappy/objs/yellowbird-downflap.png" , (0,0) , (50,50))
           pass
    def game_over(self , c):
        self.is_over = True
        self.mesh.image_setup("assets/flappy/objs/yellowbird-upflap.png" , (0,0) , (50,50))
        self.renderable.send_request(self.renderable.REQUEST_DELETE_MESH , ["back"])
        
