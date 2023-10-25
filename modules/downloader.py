import urllib
import http
from urllib.request import HTTPError
import os
from time import sleep
from modules.functions import check_internet
from alive_progress import alive_bar

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"


def download(data,):
  if not os.path.exists('pictures'):
     os.mkdir('pictures')
  wdir = os.getcwd()
  os.chdir('pictures')
  




  i = 0
  KeyboardInterruptValue = False
  with alive_bar(len(data)) as bar:
    for url in data:
      if KeyboardInterruptValue != True:
        i = i + 1
        if "mp4" in url:
                  exten = f".mp4"
        else:
                  if "gif" in url:
                    exten = f".gif"
                  else:
                    if "jpg" in url:
                      exten = f".jpg"
                    else:
                      if "webp" in url:
                        exten = f".webp"
                      else:
                        if "webm" in url:
                          exten = f".webm"
                        else:
                          if 'jpeg' in url:
                            exten = f".jpeg"
                          else:
                            exten = f".png"

        name_file = f"{i}{exten}"
        while not os.path.exists(name_file):
                  try:
                    status  = (downloading(url, name_file))

                    if status != "200":
                        if status == '103':
                            sleep(5)
                            status = (downloading(url, name_file))
                            if status != "200":break
                        elif status == '101':
                            check_internet()
                            pass
                        elif status == '999':
                            KeyboardInterruptValue = True
                            break
                        else:break
                    else:pass
                  except Exception as err_:
                    break
        bar()
  os.chdir(wdir)


def downloading(url, name_file):
  url = url.replace(" ", "%20")

  if "?size=" in url:
    ind = url.find("?size=")
  else:
    if "?extra=" in url:
      ind = url.find("?extra=")
    else:
      ind = len(url)

  print('\r', end='')

  try:
    urllib.request.urlretrieve(str(url), name_file)
    print(f"{green}[+] 200: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = '200'

  except HTTPError as err_code:
    print(f"{red}[-] {red}{err_code.code}: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'{err_code.code}'

  except urllib.error.URLError as err_code:
    if "[WinError 10054]" in str(err_code):
      print(f"{red}[-] {red}522: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'522'

    elif "[Errno 99]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'

    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
      print(f"{red}[-] {red}526: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'526'

    elif "[Errno 11001]" in str(err_code):
      print(f"{red}[-] {red}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'101'

    elif "[WinError 10060]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524'    

    elif "[Errno 104]" in str(err_code):
      print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'524' 

    elif "<urlopen error retrieval incomplete:" in str(err_code):
      print(f"{violet}[?] 103: {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'103' 

    else:
      # print(err_code)
      print('\r', end='')
      err_code = str(err_code).replace('<','').replace('>','').replace('urlopen error ','')
      print(f"{violet}[?] ___ ('{err_code}): {blue}{name_file}{white}  URL: {url[0:ind]}")
      status = f'___ ({err_code})'

  except http.client.RemoteDisconnected:
    print(f"{violet}[-] {violet}RemoteDisconnected: {blue}{name_file}{white}  URL: {url[0:ind]}")

    status = f'101'

  except ConnectionResetError:
    print(f"{violet}[-] {violet}ConnectionResetError: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'101'

  except ValueError as err:
    print(f"{violet}[?] ValueError: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'102'
  
  except KeyboardInterrupt:
    print(f"{red}[!] KeyboardInterrupt: {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = '999'
  


  except Exception as err:
    print(f"{violet}[?] ___  (]{err}): {blue}{name_file}{white}  URL: {url[0:ind]}")
    status = f'___ ({err})'

  return status