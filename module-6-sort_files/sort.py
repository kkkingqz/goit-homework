from pathlib import Path
import re, os, shutil, sys
from collections import defaultdict

GROUP_DICT = {
    "images": [".jpeg", ".png", ".jpg", ".svg"], 
    "video": [".avi", ".mp4", ".mov", ".mkv", ".wmv"], 
    "audio": [".mp3", ".ogg", ".wav", ".amr"], 
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"], 
    "archives": [".zip", ".gz", ".tar"], 
    "other": []}


def get_all_files(path):
#получаем список файлов и папок целевой директории

    file_names, dir_names = [], []

    try:
        for file_or_dir in path.iterdir():
            if file_or_dir.is_dir() and file_or_dir.name not in GROUP_DICT:
                dir_names.append(file_or_dir)
            if file_or_dir.is_file():
                file_names.append(file_or_dir)
    except PermissionError:
        print('No permission')

    for dir in list(dir_names):
        dirs, file = get_all_files(path.joinpath(dir))
        dir_names.extend(dirs)
        file_names.extend(file)
    
    return dir_names, file_names

def sort_files(file_names):
#создаем словарь files_dict с разбивкой файлов по категориям
#ключ --> название категории
#создаем словарь ext_dict в котором считаем кол-во по расширениям

    files_dict=defaultdict(list)
    ext_dict=defaultdict(dict)

    for file in file_names:

        ext = file.suffix.lower() or 'no_ext'

        for group_name, group_ext in GROUP_DICT.items():

            if ext in group_ext:
                files_dict[group_name].append(file)

                try:
                    ext_dict[group_name][ext] += 1
                except KeyError:
                    ext_dict[group_name][ext] = 1

                break

        if file not in files_dict[group_name]:
            files_dict['other'].append(file)

            try:
                ext_dict['other'][ext] += 1
            except KeyError:
                ext_dict['other'][ext] = 1
            
    return files_dict, ext_dict

def normalize2(file):
#нормализация для объекта Path
    return Path(file.parent.joinpath(normalize(file.stem)+file.suffix))

def normalize(file_name):
#нормализация имени в соответствии с ТЗ. Принимает и отдает строку

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    new_name = ''

    for ch in file_name:
        new_name += TRANS.get(ord(ch)) or ch

    new_name = re.sub(r'[^a-zA-Z0-9]{1}','_',new_name)
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
            while os.path.exists(path.joinpath(group).joinpath(file_ifexists_prefix+normalize2(file).name)):
                file_ifexists_prefix = 'rename_'+str(file_ifexists_prefix_i)+'_'
                file_ifexists_prefix_i+=1

            shutil.copy(file, path.joinpath(group).joinpath(file_ifexists_prefix+normalize2(file).name))
            os.remove(file)
        except PermissionError:
            print('No permission for: '+str(file))

def remove_empty_dir(dir_list):
#удаляем пустые директории. в не пустых - нормализация имени

    dir_list.sort(key=lambda dir: -len(dir.parts))

    for dir in dir_list:
        try:
            os.rmdir(dir)
        except (PermissionError, OSError) as e:
            try:
                os.rename(dir, dir.parent.joinpath(normalize(dir.name)))
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

def processing_other(files, group, path):
#нормализация имени для файлов не попавших в категории

    for file in files:
        try:
            os.rename(file,normalize2(file))
        except PermissionError:
            print('No permission for: '+str(file))
        except FileExistsError:
            os.remove(file)

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
        try:
            file_ifexists_prefix=''
            file_ifexists_prefix_i = 1
            while os.path.exists(path.joinpath(group).joinpath(file_ifexists_prefix+normalize2(file).stem)):
                file_ifexists_prefix = 'rename_'+str(file_ifexists_prefix_i)+'_'
                file_ifexists_prefix_i+=1

            os.makedirs(path.joinpath(group).joinpath(file_ifexists_prefix+normalize2(file).stem))
            shutil.unpack_archive(file, path.joinpath(group).joinpath(file_ifexists_prefix+normalize2(file).stem))
            os.remove(file)
        except PermissionError:
            print('No permission for: '+str(file))


def print_files(files_dict, path):
#печать имен файлов по группам

    def print_center(string):
        target_string_len = 80
        string = '   ' + string + '   '
        string = '*'*(target_string_len//2-len(string)//2) + string + '*'*(target_string_len//2-len(string)//2)
        return string[:len(string)-(len(string)%2)]

    def crop_filename(file):
        file_name = file.stem
        target_filename_len = 43
        target_dir_len = 13
        target_ext_len = 5

        if len(file_name) > target_filename_len:
            file_name=file_name[0:target_filename_len - 6]+'...'

        file_dir = str(file.parent.relative_to(path))
        if len(file_dir) > target_dir_len:
            file_dir='...'+file_dir[len(file_dir) - target_dir_len + 3:]

        file_ext = file.suffix or 'noext'
        if len(file_ext) > target_ext_len:
            file_ext = file_ext[:-target_ext_len]

        return (file_name, file_dir, file_ext)


    print(path)
    for group in files_dict:
        if group:
            print('*'*80+'\n'+print_center(group)+'\n'+'*'*80)
            for file in files_dict[group]:
                cr_file = crop_filename(file)
                print('***  {:^40}  ***  {:^13}  *** {:^5} ***'.format(cr_file[0], cr_file[1], cr_file[2]))
    print('*'*80+'\n'+'*'*80+'\n'+'*'*80+'\n')

def get_args():
#получаем параметры запуска. аргумент show - выводит список файлов по категориям, но ничего не копирует

    show = False
    if len(sys.argv) == 2:
        path_string = sys.argv[1]
    elif len(sys.argv) == 3 and (sys.argv[1] in ['-show', '--show']):
        path_string = sys.argv[2]
        show = True
    elif len(sys.argv) == 3 and (sys.argv[2] in ['-show', '--show']):
        path_string = sys.argv[1]
        show = True
    else:
        print('incorrect arguments')
        exit()

    path = Path(path_string)    
    if not os.path.exists(path_string) or path_string in ["\\\\", "\\", '/', '//', '.', '..', '.\\', './']:
        print('Directory '+path_string+' incorrect')
        exit()

    return path, show

def main():
    path, show = get_args()

    #path = Path('c:\\users\\user\\documents')
    #show = True

    dir_names, file_names = get_all_files(path)
    files_dict, ext_dict = sort_files(file_names)

    if show:
        print_files(files_dict, path)
        exit()

    print(path)
    print('\nFound '+str(len(file_names))+' files')

    for group in ext_dict:
        sum=0
        unique_ext = set()
        for ext in ext_dict.get(group):
            sum+=ext_dict[group][ext]
            unique_ext.add(ext)
        print(str(sum)+' files type "'+group+'"')
        print(*unique_ext)

    print('\n')
    print_files(files_dict, path)
    #while True:
    #    user_apply = input('Sort? y or n\n>>> ')
    #    if user_apply in ['y', 'n']:
    #        if user_apply == 'y':
    #            break
    #        else:
    #            exit()
    #    print('please enter y or n')

    print('\nprocessing files...') 

    for group in files_dict:
        if group == 'images':
            processing_images(files_dict[group], group, path)
        if group == 'video':
            processing_video(files_dict[group], group, path)
        if group == 'audio':
            processing_audio(files_dict[group], group, path)
        if group == 'documents':
            processing_documents(files_dict[group], group, path)
        if group == 'archives':
            processing_archives(files_dict[group], group, path)
        if group == 'other':
            processing_other(files_dict[group], group, path)

    remove_empty_dir(dir_names)
    print('done')
    print(path)
    exit()

if __name__ == '__main__':
    main()