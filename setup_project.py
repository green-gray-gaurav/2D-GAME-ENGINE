import os
import sys ,shutil
import pathlib

data = sys.argv
cwd = "".join(pathlib.Path(data[0]).resolve().cwd().as_uri().split("///")[1:])
project_dir = data[1]


project_path = cwd + "/" + project_dir + "/"

os.mkdir(project_dir  + "/game_module")

files = ["__init__.py" , "game_loop.py" , "renderable_mesh.py"]

for file in files:
    open(project_path  + f"game_module/{file}" , 'w+')
    shutil.copyfile(cwd + f"/game_module/{file}"  , project_path  + f"game_module/{file}")

open(project_path  + f"main.py" , 'w+')
open(project_path  + f"object.py" , 'w+')
shutil.copyfile(cwd + f"/game_module/templates/main_template.py"  , project_path  + f"main.py")
shutil.copyfile(cwd + f"/game_module/templates/object_file_template.py"  , project_path  + f"object.py")

with open(project_path + "/runner.bat"  ,  'w+') as f:
    f.write(f"python {project_path}/main.py {project_path}")