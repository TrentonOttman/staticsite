from textnode import *
from htmlnode import *
from splitdelimeter import *
import os
import shutil

def source_to_destination(source, destination, current_path=None): 
    if current_path == None:
        if os.path.exists(source) != True:
            raise Exception("Source does not exist!")
        else:
            shutil.rmtree(destination)
            os.mkdir(destination)
        current_path = source

    # Base case (file)
    if os.path.isfile(current_path):
        fixed_path = current_path.replace(source, destination, 1)
        return shutil.copy(current_path, fixed_path)
    
    # Directory case
    if os.path.isfile(current_path) != True and current_path != source:
        fixed_path = current_path.replace(source, "", 1)
        os.mkdir(f"{destination}/{fixed_path}")

    # Recursive case
    file_list = os.listdir(current_path)
    for file in file_list:
        path = os.path.join(current_path, file)
        source_to_destination(source, destination, path)

def main():
    # source_to_destination("static", "public")
    markdown = "### This should not work"
    print(extract_title(markdown))

if __name__ == "__main__":
    main()