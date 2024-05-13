import glob , pathlib
import importlib.util  
import sys

#--------------------------game seup---------------------#


project_path = sys.argv[1] #path to project
prefix_file  = "object"
prefix_class = "game_object"
window_width = 640
window_height = 480
fps = 60

Window_title = "game window"
Window_icon_path = None



#--------------------------game setup---------------------#

from game_module.game_loop import gameLoop



game_object_class_list = []



files = list(filter( lambda x :  x.startswith(prefix_file), 
            map(lambda x : x.split("\\")[-1],  glob.glob(project_path + "*")) ))


#getting the classs from the object files

for file in files:
    spec = importlib.util.spec_from_file_location(file, project_path + "/" + file)    
    foo = importlib.util.module_from_spec(spec)        
    spec.loader.exec_module(foo)
    all_objects = dir(foo) 
    for object_str in all_objects:
        if(object_str.startswith(prefix_class)):
           game_object_class_list.append(getattr(foo , object_str))
        
    
#clearint ga game loop class  ww
game_loop = gameLoop(window_width  ,  window_height , fps , Window_title , Window_icon_path)

#here we are passing the rendrable of the objects to game loop
for game_object_class in game_object_class_list:
    if(game_object_class.INIT_INSTANCE):
        game_loop.add_renderable(game_object_class(game_loop.get_window()).renderable)

game_loop.add_game_object_classes({class_name.CLASS_TAG : class_name  for class_name in game_object_class_list })
game_loop.start()