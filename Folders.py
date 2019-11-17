import os

#method which changes folder.It uses as start folder the folder that belongs the module 
def change_folder(name):
    
    script_dir=os.path.dirname(__file__)
    result_dir=os.path.join(script_dir,name)
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)
    os.chdir(result_dir)

#method which changes inside folder.It used as start folder the current folder of the programm
def change_inside_folder(name):
    result_dir=os.path.join(os.getcwd(),name)
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)
    os.chdir(result_dir)
    

#method which go to the folder of the module
def move_initial_folder():
    script_dir=os.path.dirname(__file__)
    os.chdir(script_dir)