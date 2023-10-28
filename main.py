from modules.colors import *
from modules.functions import *
from modules.downloader import *
from modules.statisticksDEF import Statistics
from modules.statisticksDEF import GlobalTagsInfo
import json
import time 

format_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=cat_ears'
api_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='

format_enter_text = f'''
Format: {format_link}
'''


GuardOnline = False # DEV 


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

    urls = []
    tags = ''

    input_tags = inputUrl()
    tags = formating_tags_list(input_tags, ind= 1)
    if tags == '':return f'{red}[ERROR] {red}You have not entered tag(s): _{tags}_ ...{white}'



    print(f'''\n{'='*10}- GetDownloadFiles -{'='*10}''')
    count, offset = find_count(f'{api_link}{tags}&pid=0')
    print(f'''Count:{count}
{'-'*15}''')

    for i in range(0, round(count/100)+1):
        link = f'{api_link}{tags}&pid={i}'

        urls.append(link)
    
    
    data = []
    download_links = []
    GlobalTags = []
    
    S = Statistics(os.getcwd())
    T = GlobalTagsInfo()
    s = [S,T]

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
    with open('data.json', 'w') as file:json.dump(data, file, indent=4)
    with open('download_links.json', 'w') as file:json.dump(download_links, file, indent=4)
    S.writeStats()
    T.ch_new_tags(input_tags = GlobalTags)
    T.writeTags()
    print(f'''\n{'='*10}- Download -{'='*10}\n''')

    if input('Скачать? (Y/N) >>> ') == 'Y':
        if len(input_tags.split(' ')) == 1:
            nf = str(input_tags.split(' ')[0])
        else:
            nf = 'pictires'
        print(nf)
        download(download_links, nf)

    


if __name__ == '__main__':
    main()

