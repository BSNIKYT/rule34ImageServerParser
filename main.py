from modules.colors import *
from modules.functions import *
from modules.downloader import *
import json
import time 


format_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=cat_ears'
api_link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='

format_enter_text = f'''
Format: {format_link}
'''

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

    _tags = inputUrl()
    tags = formating_tags_list(_tags, ind= 1)
    if tags == '':return f'{red}[ERROR] {red}You have not entered tag(s): _{tags}_ ...{white}'


    print(f'''\n{'='*10}- GetDownloadFiles -{'='*10}''')
    count, _ = find_count(f'{api_link}{tags}&pid=0')
    print(f'''Count:{count}
{'-'*15}''')

    for i in range(0, round(count/100)+1):
        link = f'{api_link}{tags}&pid={i}'
        # print(link)
        urls.append(link)
    
    
    data = []
    download_links = []
    
    for link in urls:

            print('\r', end='')
            _data, _download_links = replon__(link)
            


            for link in _data:data.append(link)
            for link in _download_links:download_links.append(link)
            try:
                time.sleep(5)
            except KeyboardInterrupt:break
            
    
    download_links = list(set(download_links))
    with open('data.json', 'w') as file:json.dump(data, file, indent=4)
    with open('download_links.json', 'w') as file:json.dump(download_links, file, indent=4)
    print(f'''\n{'='*10}- Download -{'='*10}\n''')
    download(download_links)

    


if __name__ == '__main__':
    main()
