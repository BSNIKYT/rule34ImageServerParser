import socket
from modules.colors import *

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import HTTPError
import urllib
import http
import json
import os

kyes_ = {
' '	:'%20', 
'!'	:'%21', 
'"'	:'%22', 
'#'	:'%23', 
'$'	:'%24',
# '%'	:'%25',
'&'	:'%26',
'('	:'%28',
')'	:'%29',
'*'	:'%2A',
# '-'	:'%2D',
'.'	:'%2E',
'/'	:'%2F',
# ':'	:'%3A',';'	:'%3B','<'	:'%3C','='	:'%3D','>'	:'%3E','?'	:'%3F','@'	:'%40',
# 'A'	:'%41','B'	:'%42','C'	:'%43','D'	:'%44','E'	:'%45','F'	:'%46','G'	:'%47','H'	:'%48','I'	:'%49','J'	:'%4A',
# 'K'	:'%4B','L'	:'%4C','M'	:'%4D','N'	:'%4E','O'	:'%4F','P'	:'%50','Q'	:'%51','R'	:'%52','S'	:'%53','T'	:'%54',
# 'U'	:'%55','V'	:'%56','W'	:'%57','X'	:'%58','Y'	:'%59','Z'	:'%5A','['	:'%5B','\\':'%5C',']'	:'%5D','^'	:'%5E',
# '`'	:'%60','{'	:'%7B','|'	:'%7C',
# '}'	:'%7D','~'	:'%7E',' '	:'%7F'
}


def global_tags_txt():
    pass




def check_link(text):
    if 'https://' in text:
        print(f'{red}[ERROR] {red}You must send tag(s), not a link: _{text}_ ...{white}')
        return False
    if 'http://' in text: 
        print(f'{red}[ERROR] {red}You must send tag(s), not a link: _{text}_ ...{white}')
        return False
    return True



def check_internet():
  host = 'www.google.com'
  def is_connected(host):
      try:
          host = socket.gethostbyname(host)
          socket.create_connection((host, 80), 2)
          return True
      except Exception:
          return False
      
  if is_connected(host) == True:
      pass
  else:
      print('\r', end='')
      print(f"{red}[/] Подключитесь к Интернету!{white}")
      while is_connected(host) == False:
          pass
      print('\r', end='')
      print(f"{green}[/] Подключение установлено!{white}")

    
def mask(str, maska):
				if len(str) == maska.count('#'):
					str_list = list(str)
					for i in str_list:
						maska=maska.replace("#", i, 1)
					return maska


def formating_tags_list(text, ind = 0):
  if type(text) != str:text = str(text)
  tags = ''

  if ind == 1:tags = text.replace(' ', '%20')
  else:tags = text.replace(' ', '''
''')
  # for i in list(text.split(" ")):
  #   print(len(list(text.split(" "))))
  #   if i != '':
  #       q = q + 1
  #       if q != len(list(text.split(" "))):
  #         i + '%20'     


  
  
  return tags


def parsing(text, stats = None):
  soup = bs(text, "xml")
  # print(soup)
  # i = 0
  qq = []
  download_links =[]
  _tags = []
  for tag in soup.find_all('post'):
    try:
        file_url = tag.get('file_url')
        tags     = formating_tags_list(tag.get('tags'), ind= 0)
        _id      = tag.get('id')
        download_links.append(tag.get('file_url'))
        
    except:
        file_url = None
        tags = ''
        _id = None
        download_links.append(None)
    qq.append({f'{tag.get("id")}': {
          'id': _id,
          'file_url': file_url,
          'tags': tags
        }})
    _tags.append(tags)
  return qq, download_links, _tags


def replon__(_url,tagsStats, _stats):
  data = None
  url = _url
  data, download_links, __tags = [], [], []
  try:
    r = requests.get(_url)
    r.raw.decode_content = True
    if r.status_code == 403:print(f"{red}[-] {red}403: {url}") 
    print(f'{green}[{r.status_code}] {violet}Parsing {blue}{_url}{violet} ...{white}')
    
    data, download_links, tags = parsing(r.text)


    if _stats != None:
        GTI = _stats[1]
        STATISTICS = _stats[0]
        a = {'response': 'OK',
             'data' : {
              'url' : url,
              'tags': tagsStats,
              'len': {
                  'data': len(data),
                  'download_links' : len(download_links)  
              }}}
        STATISTICS.statistics_format_function_ok(a)
        GTI.ch_new_tags(input_tags = tags)
    status_code = 200
    
    
    

  except HTTPError as err_code:
      status_code = err_code.code
      print(f"{red}[-] {red}{err_code.code}: {url}")
  except urllib.error.URLError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    else:status_code = '___'
    print(f"{red}[-] {red}{status_code}: {url}")
  except http.client.RemoteDisconnected as err_code:
    print(f"{violet}[-] {violet}101: {url}")
  except ConnectionResetError as err_code:
    print(f"{violet}[-] {violet}101: {url}")
  except ValueError as err_code:
    print(f"{violet}[?] ValueError: {url} {err_code}")
  except requests.exceptions.SSLError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    else:status_code = '___'
    print(f"{red}[-] {red}{status_code}: {url}")
  except requests.exceptions.ConnectionError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    elif "HTTPSConnectionPool" in str(err_code):status_code = 522
    else:status_code = f'___ ({err_code})'
    print(f"{red}[-] {red}{status_code}: {url}")
  # except Exception as err_code:
  #     print(f"{red}[-] {red}UnknownException: {url}")
  #     status_code = '999'

  if (_stats != None):
    if (status_code != 200):
      _stats.statistics_format_function_error(
        {'response': 'ERROR',
              'data' : {
                'url' : url,
                'tags': tagsStats,
                'errorInfo' : {
                    'code' : status_code,
                    'traceback' : err_code}
                }
          })
      __tags.append('ERROR')

  return data, download_links, __tags


def find_count(_url, dev = False):
  if dev == False:
    r = requests.get(_url)
    print(f'GET_COUNT_URL: {_url}')
    soup = bs(r.text, "xml")

  count = str(soup).split('''"><post height=""''')[0].split('''" offset="''')[0].split('<posts count="')[1]
  count = count.replace('"/>','')
  offset = 0
  return int(count), int(offset)


if str(os.name) == "nt":
  dir_pref = "\\"
else:
  dir_pref = "/"


# def statistics(working_directory):
    
#     statictics_file_name = 'statistics.json'
#     if not os.path.exists(working_directory + dir_pref + statictics_file_name):
#         with open(statictics_file_name, 'w') as file:
#           json.dump(list([]), file, indent=4, default=list)
#           data_load = json.load(file)
#     else:
#         with open(statictics_file_name, 'r') as j:
#           data_load = json.load(j)
#     # print(data_load)
    
        
