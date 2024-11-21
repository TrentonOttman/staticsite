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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    source_data = f.read()
    f.close()
    f = open(template_path)
    template_data = f.read()
    f.close()
    html_node = markdown_to_html_node(source_data)
    html = html_node.to_html()
    title = extract_title(source_data)
    template_data = template_data.replace("{{ Title }}", title, 1)
    template_data = template_data.replace("{{ Content }}", html, 1)
    f = open(dest_path, "w")
    f.write(template_data)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    current_path = dir_path_content
    if os.path.isfile(current_path) == True and current_path[-3:] != ".md":
        raise Exception("File not markdown or directory")

    if current_path[-3:] == ".md":
        fixed_path = dest_dir_path.replace(".md", ".html", 1)
        generate_page(current_path, template_path, fixed_path)
        return

    if os.path.isfile(current_path) != True and current_path.find("/") != -1:
        slash_index = current_path.find("/")
        destination = dest_dir_path + current_path[slash_index:]
        os.mkdir(dest_dir_path)

    file_list = os.listdir(dir_path_content)
    for file in file_list:
        path = os.path.join(current_path, file)
        slash_index = path.rfind("/")
        destination = dest_dir_path + path[slash_index:]
        generate_pages_recursive(path, template_path, destination)

def main():
    # Source directory to copy from. Include CSS, images, etc here
    SOURCE_PATH = "static"
    # Destination directory to copy to.
    DESTINATION_PATH = "public"
    # Content directory containing markdown files to be converted.
    CONTENT_PATH = "content"
    # Template HTML file to use for formatting
    TEMPLATE_PATH = "template.html"
    
    shutil.rmtree(DESTINATION_PATH)
    os.mkdir(DESTINATION_PATH)
    source_to_destination(SOURCE_PATH, DESTINATION_PATH)
    generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, DESTINATION_PATH)

if __name__ == "__main__":
    main()