import re
import os
import sys

import shutil

from pathlib import Path

def get_extensions(file_name):
    return Path(file_name).suffix[1:].lower()

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(file_name: str) -> str:
    file_name, *extension = file_name.split('.')
    new_name = file_name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"



def handle_file(item, new_name = ''):
    new_folder = Path(sys.argv[1])/new_name
    new_folder.mkdir(exist_ok=True, parents=True)
    item.replace(new_folder / normalize(file_name = item.name))

def handle_archive(item, new_name = ''):
    archive_folder = Path(sys.argv[1])/new_name
    archive_folder.mkdir(exist_ok=True, parents=True)
    
    base = normalize(item.stem)
    

    target_folder = archive_folder / base
 
    try:
        shutil.unpack_archive(str(item.resolve()), str(target_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    item.unlink()

def remove_empty_folders(path):
    folder = Path(path)
    for item in folder.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
                #print(f"{item} removed")
            except OSError:
                pass
#remove_empty_folders('test')
            
Pictures = ('jpeg', 'png', 'jpg', 'svg')
Docs = ('txt', 'docx', 'doc', 'pdf', 'xlsx', 'pptx')
Videos = ('mp4', 'avi', 'mov', 'mkv')
Archives = ('zip', 'tar', 'gz')
Music = ('mp3', 'ogg', 'wav', 'amr')

extensions = set()
others = set()

def sort_objects(path):
    folder = Path(path)
    for item in folder.iterdir():
        if item.is_dir():
            sort_objects(item)
        else:
            extension = get_extensions(file_name=item.name)
            if not extension: 
                pass 
            else:
                extensions.add(extension)
                if extension in Pictures: 
                   handle_file(item, new_name ='Pictures')
                         
                elif extension in Docs: 
                   handle_file(item, new_name = 'Docs')

                elif extension in Videos: 
                   handle_file(item, new_name = 'Videos')

                elif extension in Music: 
                   handle_file(item, new_name = 'Music')
                   
                elif extension in Archives: 
                   handle_archive(item, new_name = 'Archives')            
                
                else:
                   handle_file(item, new_name  = 'Others') 
                   others.add(extension)                          
                             
    return extensions - others, others

def print_folders(path):
    folder = Path(path)
    for item in folder.iterdir():
        print(item.name)
        files_list = set()
        for file in item.iterdir():
            files_list.add(file.name)
        print(files_list)  


def main(path):
    sort_objects(path)
    remove_empty_folders(path)
    print_folders(path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())
    
    
    




