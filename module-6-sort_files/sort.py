from pathlib import Path
import re, json, os, shutil, sys
from collections import defaultdict
from unicodedata import name

def get_all_files(path, GROUP_DICT):
#получаем список файлов и папок целевой директории

    file_names, dir_names = [], []

    try:
        for file_or_dir in path.iterdir():
            if file_or_dir.is_dir() and file_or_dir.name not in GROUP_DICT.keys():
                dir_names.append(file_or_dir)
            if file_or_dir.is_file():
                file_names.append(file_or_dir)
    except PermissionError:
        print('No permission')

    for dir in list(dir_names):
        dirs, file = get_all_files(path.joinpath(dir), GROUP_DICT)
        dir_names.extend(dirs)
        file_names.extend(file)
    
    return dir_names, file_names

def sort_files(file_names, GROUP_DICT):
#создаем словарь files_dict с разбивкой файлов по категориям
#ключ --> название категории
#создаем словарь ext_dict в котором считаем кол-во по расширениям

    files_dict=defaultdict(list)
    ext_dict=defaultdict(dict)

    for file in file_names:

        ext = file.suffix or 'no_ext'

        for group_name, group_ext in GROUP_DICT.items():

            if ext in group_ext:
                files_dict[group_name].append(file)

                try:
                    ext_dict[group_name][ext] += 1
                except KeyError:
                    ext_dict[group_name][ext] = 1

                break

        if file not in files_dict.values():
            files_dict['other'].append(file)

            #if not ext:
            #    ext = 'no_ext'

            try:
                ext_dict[group_name][ext] += 1
            except KeyError:
                ext_dict[group_name][ext] = 1
            
    return files_dict, ext_dict

def normalize(file_name):
#нормализация имени

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    new_name = ''

    for ch in str(file_name.stem):
        new_name += TRANS.get(ord(ch)) or ch

    new_name = re.sub(r'[^a-zA-Z0-9]{1}','_',new_name)
    new_name += file_name.suffix

    return new_name

def simple_copy(files, group, path):
#копирование и нормализация имен файлов

    try:
        os.makedirs(path.joinpath(group))
    except FileExistsError:
        print('directory "'+group+'" exists')
    except PermissionError:
        print('no permission to create directory')
        return False

    for file in files:
        try:
            file_ifexists_prefix=''
            file_ifexists_prefix_i = 1
            while os.path.exists(path.joinpath(group).joinpath(file_ifexists_prefix+normalize(file))):
                file_ifexists_prefix = 'rename_'+str(file_ifexists_prefix_i)+'_'
                file_ifexists_prefix_i+=1

            shutil.copy(file, path.joinpath(group).joinpath(file_ifexists_prefix+normalize(file)))
            os.remove(file)
        except PermissionError:
            print('No permission for: '+str(file))

def remove_empty_dir(dir_list):
#удаляем пустые директории. в не пустых - нормализация имени

    #def pathsort(s):
    #    return -len(s.parts)
    dir_list.sort(key=lambda dir: -len(dir.parts))

    for dir in dir_list:
        try:
            os.rmdir(dir)
        except (PermissionError, OSError) as e:
            try:
                os.rename(d, d.parent.joinpath(normalize(dir.name)))
            except (PermissionError, OSError) as ee:
                pass

#в соответствии с описанием задания - отдельные ф-ции для обработки
#каждой категории. поскольку разной логики нет - они одинаковые
def processing_images(files, group, path):
    simple_copy(files, group, path)

def processing_video(files, group, path):
    simple_copy(files, group, path)

def processing_audio(files, group, path):
    simple_copy(files, group, path)

def processing_documents(files, group, path):
    simple_copy(files, group, path)

def processing_else(files, group, path):
#нормализация имени для файлов не попавших в категории

    for file in files:
        try:
            os.rename(file,file.parent.joinpath(normalize(file)))
        except PermissionError:
            print('No permission for: '+str(file))

def processing_archives(files, group, path):
#распаковка архивов

    try:
        os.makedirs(path.joinpath(group))
    except FileExistsError:
        print('directory "'+group+'" exists')
    except PermissionError:
        print('no permission to create directory')
        return False

    for file in files:
        #if f[0].name[:-7] == '.tar.gz':
        #    f[1]='.tar.gz'
        try:
            file_ifexists_prefix=''
            file_ifexists_prefix_i = 1
            while os.path.exists(path.joinpath(group).joinpath(file_ifexists_prefix+normalize(file))):
                file_ifexists_prefix = 'rename_'+str(file_ifexists_prefix_i)+'_'
                file_ifexists_prefix_i+=1

            os.makedirs(path.joinpath(group).joinpath(Path(file_ifexists_prefix+normalize(file)).stem))
            shutil.unpack_archive(file, path.joinpath(group).joinpath(Path(file_ifexists_prefix+normalize(file)).stem))
            os.remove(file)
        except PermissionError:
            print('No permission for: '+str(file))

#не было в ТЗ ----------------------------------------
def print_files(files_dict, path):
#печать файлов по группам.

    def print_center(string):
        string = '   ' + string + '   '
        string = '*'*(40-len(string)//2) + string + '*'*(40-len(string)//2)
        return string[:len(string)-(len(string)%2)]

    def crop_filename(file):
        file_name = file.stem
        if len(file_name)>43:
            file_name=file_name[0:37]+'...'

        file_dir = str(file.parent.relative_to(path))
        if len(file_dir)>13:
            file_dir='...'+file_dir[len(file_dir)-10:]

        file_ext = file.suffix or 'noext'
        if len(file_ext)>5:
            file_ext = file_ext[0:5]

        return (file_name, file_dir, file_ext)


    print(path)
    for group in files_dict.keys():
        if group:
            print('*'*80+'\n'+print_center(group)+'\n'+'*'*80)
            for file in files_dict[group]:
                cr_file = crop_filename(file)
                print('***  {:^40}  ***  {:^13}  *** {:^5} ***'.format(cr_file[0], cr_file[1], cr_file[2]))
    print('*'*80+'\n'+'*'*80+'\n'+'*'*80+'\n')
#--------------------------------------------------------------------

GROUP_DICT = {
    "images": [".jpeg", ".png", ".jpg", ".svg"], 
    "video": [".avi", ".mp4", ".mov", ".mkv", ".wmv"], 
    "audio": [".mp3", ".ogg", ".wav", ".amr"], 
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"], 
    "archives": [".zip", ".gz", ".tar"], 
    "other": []}

path = Path('c:\\users\\user\\documents')
d, f = get_all_files(path, GROUP_DICT)
#print(d)
#print(f)
fd, ed = sort_files(f, GROUP_DICT)
#print(print_center('image'))
#print('*'*80)
print(print_files(fd, path))