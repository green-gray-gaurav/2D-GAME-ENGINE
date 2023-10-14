#here is the bundle generator 

import glob 
import os 
import objectFile
import shutil
import sys
import time

if len(sys.argv):
    #hanlde the file name error
    pass

bundle_folder_name = sys.argv[1]

#creating a bundle folder
os.system("mkdir "+ bundle_folder_name)


#here we are making bunlde of the standard class files

for filename in glob.glob("../project_2/*"):
    if filename.endswith(".py"):
        #getting the file name
        only_filename = filename.split("\\")[1]
        #excluding self
        if __file__.split("\\")[-1] == only_filename : continue

        shutil.copy(   filename   , bundle_folder_name + "/" + only_filename )
    

#here we have our object files


#crating the in bundle object folder
BASE_PATH = "\\".join(__file__.split("\\")[:-1])
os.system(f"mkdir {BASE_PATH}\{bundle_folder_name}\obj_files")
 

for filename in glob.glob("..\project_2\obj_files\*"):
    print(filename)
    if filename.endswith(".py"):
        only_filename = filename.split("\\")[-1]
        shutil.copy(   filename   , bundle_folder_name + "/obj_files/" + only_filename )

#here we are creading the in bundle for standard classes

os.system(f"mkdir {BASE_PATH}\{bundle_folder_name}\standard_classes")
 
for filename in glob.glob("..\project_2\standard_classes\*"):
    print(filename)
    if filename.endswith(".py"):
        only_filename = filename.split("\\")[-1]
        shutil.copy(   filename   , bundle_folder_name + "/standard_classes/" + only_filename )


#here are some files// gg-engine exclusive libraries / classes
os.system(f"mkdir {BASE_PATH}\{bundle_folder_name}\ggg_exclusive_lib")
 
for filename in glob.glob("..\project_2\ggg_exclusive_lib\*"):
    print(filename)
    if filename.endswith(".py"):
        only_filename = filename.split("\\")[-1]
        shutil.copy(   filename   , bundle_folder_name + "/ggg_exclusive_lib/" + only_filename )


#here is the asset folder

os.system(f"mkdir {BASE_PATH}\{bundle_folder_name}\\assets")

for file in glob.glob("..\project_2\\template_folder\sample_assets\*"):
    only_filename = file.split("\\")[-1]
    shutil.copy(   file   , bundle_folder_name + "/assets/" + only_filename )

#here is the directiory for the ssaved_data 
os.system(f"mkdir {BASE_PATH}\{bundle_folder_name}\\saved_data")



shutil.copy( "..\project_2\\game_runner.bat" , f"{BASE_PATH}\{bundle_folder_name}\\{bundle_folder_name}_runner.bat" )