
import datetime
from modules.colors import *
from modules.functions import *
from modules.downloader import *
from modules.statisticksDEF import Statistics
from modules.statisticksDEF import GlobalTagsInfo
from modules.statisticksDEF import Guard

import json
import time 

format_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=cat_ears'
api_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' 

format_enter_text = f'''
Format: {format_link} 
'''
working_dir = os.getcwd()
if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"



try:
  os.mkdir("logging")
  os.chdir(f'{working_dir + dir_pref + "logging"}')
  py_logger, starting_script_time = set_logger_settings()
except FileExistsError:
  os.chdir(f'{working_dir + dir_pref + "logging"}')
  py_logger, starting_script_time = set_logger_settings()

except PermissionError:
  py_logger, starting_script_time = set_logger_settings()




def inputUrl():
    print(format_enter_text)

    tags = input(f'{red}>>> {white}')
    q = check_link(tags)
    if q == False:
        while q  == False:
           tags = input(f'{red}>>> {white}')
           q = check_link(tags)
    check_internet()
    return tags



def main():
    S = Statistics(working_dir=os.getcwd(), logger=py_logger)
    T = GlobalTagsInfo(py_logger)
    G = Guard(py_logger)

    urls = []
    tags = ''

    input_tags = inputUrl()



    t = {f"{str(datetime.now()).split('.')[0]}": input_tags}
    S.statistics_format_function_ok(t)
    py_logger.info(f'[MAIN] User entered tags: {input_tags}')
    tags = formating_tags_list(input_tags, ind= 1)
    if tags == '':
        py_logger.error(f'[MAIN] The user did not enter any tags.: {input_tags}')
        return f'{red}[ERROR] {red}You have not entered tag(s): _{tags}_ ...{white}'



    print(f'''\n{'='*10}- GetDownloadFiles -{'='*10}''')
    count, _ = find_count(f'{api_link}{tags}&pid=0')
    print(f'''Count:{count}
{'-'*15}''')
    
    py_logger.info(f'''{'='*10}- [PARSER] -{'='*10}''')
    py_logger.info(f'[PARSER] Count: {count}')

    py_logger.info(f'''{'-'*8}- [Links] -{'-'*8}''')
    for i in range(0, round(count/100)+1):
        link = f'{api_link}{tags}&pid={i}'
        py_logger.info(f'[PARSER] [LINK][{i}]: {link}')
        
        urls.append(link)
    
    
    data = []
    download_links = []
    GlobalTags = []
    
    
    s = [S,T,G]

    for link in urls:
            print('\r', end='')
            _data, _download_links, __tags = replon__(_url = link, _stats = s, tagsStats = tags)
            


            for link in _data:data.append(link)
            for link in _download_links:download_links.append(link)
            for tags in __tags:GlobalTags.append(tags)
            try:
                time.sleep(5)
            except KeyboardInterrupt:break
            
    
    download_links = list(set(download_links))

    name_folder = nameFolder(input_tags)
    if not os.path.exists(name_folder):
        os.mkdir(name_folder)
    wdir = os.getcwd()
    os.chdir(name_folder)

    print(f'''\n{'='*10}- STATS -{'='*10}\n''')

    S.writeStats()
    T.ch_new_tags(input_tags = GlobalTags)
    T.writeTags()


    os.chdir(wdir)
    print(f'''\n{'='*10}- Download -{'='*10}''')

    if len(download_links) != 0:
        if input('\nDownload? (Y/N) >>> ') == 'Y':
            os.chdir(name_folder)
            download(download_links)
    else:
       print(f'{red}[!] There is nothing to download!{white}')

    


if __name__ == '__main__':
    main()

