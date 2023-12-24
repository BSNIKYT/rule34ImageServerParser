import urllib
import http
from urllib.request import HTTPError
import os
import time
from time import sleep
from modules.functions import check_internet
from modules.Exceptions import GuardFoundForbiddenElement
from alive_progress import alive_bar
from modules.functions import check_memory

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"

files_extension = {
    'gif': '.gif', 'jpg': '.jpg', 'mp4': '.mp4',
    'webp': '.webp', 'jpeg': '.jpeg'}


def download(data, logger):
    """
    Загружает изображения из списка URL-адресов.

    Args:
        data (list): Список URL-адресов изображений для загрузки.
        logger (Logger): Объект логгера для записи информации о загрузке.
    """
    name_folder = 'pictures'
    if not os.path.exists(name_folder):
        os.mkdir(name_folder)

    wdir = os.getcwd()
    os.chdir(name_folder)

    i = 0
    KeyboardInterruptValue = False
    with alive_bar(len(data)) as bar:
        for url in data:
            if not KeyboardInterruptValue:
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
                    # try:
                    status = (downloading(url, name_file, logger))

                    if status != "200":
                        if status == '103':
                            sleep(5)
                            status = (downloading(url, name_file, logger))
                            if status != "200":
                                break
                        elif status == '101':
                            check_internet()
                            pass
                        elif status == '999':
                            KeyboardInterruptValue = True
                            break
                        elif status == '700':
                            time.sleep(30)
                            check_memory(url, name_file, downloading)

                        elif status == '000':
                            pass
                        else:
                            break
                    else:
                        pass
                    # except Exception as err:
                    #   print("Error downloading %s: %s" % (url, err))
                    #   break
                bar()
    os.chdir(wdir)


def downloading(url, name_file, logger):
    """
    Загружает одно изображение из заданного URL-адреса.

    Args:
        url (str): URL-адрес изображения.
        name_file (str): Имя файла для сохранения изображения.
        logger (Logger): Объект логгера для записи информации о загрузке.

    Returns:
        str: Код состояния, указывающий результат загрузки.
    """
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
        err_code = ''

    except HTTPError as err_code:
        print(
            f"{red}[-] {red}{err_code.code}: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = f'{err_code.code}'

    except urllib.error.URLError as err_code:
        if "[WinError 10054]" in str(err_code):
            print(
                f"{red}[-] {red}522: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'522'

        elif "[Errno 99]" in str(err_code):
            print(
                f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'524'

        elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
            print(
                f"{red}[-] {red}526: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'526'

        elif "[Errno 11001]" in str(err_code):
            print(
                f"{red}[-] {red}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'101'

        elif "[WinError 10060]" in str(err_code):
            print(
                f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'524'

        elif "[Errno 104]" in str(err_code):
            print(
                f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'524'

        elif "<urlopen error retrieval incomplete:" in str(err_code):
            print(
                f"{violet}[?] 103: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'103'

        elif '[WinError 10053]' in str(err_code):
            print(
                f"{violet}[?] 103: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = '103'

        else:
            print('\r', end='')
            err_code = str(err_code).replace(
                '<',
                '').replace(
                '>',
                '').replace(
                'urlopen error ',
                '')
            print(
                f"{violet}[?] ___ ('{err_code}): {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'___ ({err_code})'
    except OSError as err_code:
        if "[Errno 28]" in str(err_code):
            print(
                f"{red}[-] {red}700: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'700'
        elif '[WinError 10053]' in str(err_code):
            print(
                f"{violet}[?] 103: {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = '103'
        else:
            err_code = str(err_code).replace(
                '<',
                '').replace(
                '>',
                '').replace(
                'urlopen error ',
                '')
            print(
                f"{violet}[?] ___ ('{err_code}): {blue}{name_file}{white}  URL: {url[0:ind]}")
            status = f'___ ({err_code})'

    except http.client.RemoteDisconnected as err_code:
        print(
            f"{violet}[-] {violet}RemoteDisconnected: {blue}{name_file}{white}  URL: {url[0:ind]}")

        status = f'101'

    except ConnectionResetError as err_code:
        print(
            f"{violet}[-] {violet}ConnectionResetError: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = f'101'

    except ValueError as err_code:
        print(
            f"{violet}[?] ValueError: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = f'102'

    except KeyboardInterrupt as err_code:
        print(
            f"{red}[!] KeyboardInterrupt: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = '999'

    except GuardFoundForbiddenElement as err_code:
        print(
            f"{red}[-] GuardFoundForbiddenElement: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = '000'

    except FileExistsError as err_code:
        print(
            f"{violet}[-] FileExistsError: {blue}{name_file}{white}  URL: {url[0:ind]}")
        status = '200'

    logger.info(
        f'[Download] URL: {url} Status: {status} Error Message: {err_code}')

    # except Exception as err:
    #   # if '[Errno 28]' in str(err):
    #   #    print('НЕХВАТАЕТ ПАМЯТИ')
    #   print(f"{violet}[?] ___  ({err}): {blue}{name_file}{white}  URL: {url[0:ind]}")
    #   status = f'___ ({err})'

    return status
