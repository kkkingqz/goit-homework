from pathlib import Path
import re, json, os, shutil, sys
from collections import defaultdict

def get_all_files(path, group_dict):
#получаем список файлов и папок целевой директории

    file_names, dir_names = [], []

    try:
        for file_or_dir in path.iterdir():
            if file_or_dir.is_dir() and file_or_dir.name not in group_dict.keys():
                dir_names.append(file_or_dir)
            if file_or_dir.is_file():
                file_names.append(file_or_dir)
    except PermissionError:
        print('No permission')

    for dir in list(dir_names):
        dir, file = get_all_files(path.joinpath(dir), group_dict)
        dir_names.extend(dir)
        file_names.extend(file)
    
    return dir_names, file_names

def sort_files(file_names, group_dict):
#создаем словарь files_dict с разбивкой файлов по категориям
#ключ --> название категории
#создаем словарь ext_dict в котором считаем кол-во по расширениям

    files_dict=defaultdict(list)
    ext_dict=defaultdict(dict)

    for file in file_names:

        for group_name, group_ext in group_dict.items():
            ext = file.suffix
            if ext in group_ext:
                files_dict[group_name].append(file)

                try:
                    ext_dict[group_name][ext] += 1
                except KeyError:
                    ext_dict[group_name][ext] = 1

                break

        if file not in files_dict.values():
            files_dict['other'].append(file)
            if not ext:
                ext = 'no_ext'

            try:
                ext_dict[group_name][ext] += 1
            except KeyError:
                ext_dict[group_name][ext] = 1
            
    return files_dict, ext_dict


group_dict = {
    "images": [".jpeg", ".png", ".jpg", ".svg"], 
    "video": [".avi", ".mp4", ".mov", ".mkv", ".wmv"], 
    "audio": [".mp3", ".ogg", ".wav", ".amr"], 
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"], 
    "archives": [".zip", ".gz", ".tar"], 
    "other": []}

path = Path('c:\\users\\user\\documents')
d, f = get_all_files(path, group_dict)
#print(d)
#print(f)
fd, ed = sort_files(f, group_dict)


