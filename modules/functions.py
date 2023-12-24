
import time
import socket
import logging
from datetime import datetime

if __name__ != '__main__':
    from modules.colors import *

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import HTTPError
import urllib
import http
import json
import os

starting_script_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
starting_script_time2 = starting_script_time.replace(
    '-',
    '_').replace(
        ' ',
        '_').replace(
            ':',
    '_')

kyes_ = {
    ' ': '%20',
    '!': '%21',
    '"': '%22',
    '#': '%23',
    '$': '%24',
    '&': '%26',
    '(': '%28',
    ')': '%29',
    '*': '%2A',
    '.': '%2E',
    '/': '%2F',

}


def check_link(text):
    """
    Проверяет, является ли переданный текст ссылкой.

    Args:
        text (str): Текст для проверки.

    Returns:
        bool: True, если текст не является ссылкой, иначе False.
    """
    if text != '':
        if 'https://' in text:
            print(
                f'{red}[ERROR] {red}You must send tag(s), not a link: _{text}_ ...{white}')
            return False
        if 'http://' in text:
            print(
                f'{red}[ERROR] {red}You must send tag(s), not a link: _{text}_ ...{white}')
            return False
        return True
    else:
        return False


def check_internet():
    """
    Проверяет наличие подключения к Интернету и ожидает, если подключение отсутствует.
    """
    host = 'www.google.com'

    def is_connected(host):
        try:
            host = socket.gethostbyname(host)
            socket.create_connection((host, 80), 2)
            return True
        except Exception:
            return False

    if is_connected(host):
        pass
    else:
        print('\r', end='')
        print()
        print(f"{red}[/] Подключитесь к Интернету!{white}")
        while is_connected(host) == False:
            pass
        print('\r', end='')
        print()
        print(f"{green}[/] Подключение установлено!{white}")


def formating_tags_list(text, ind=0):
    """
    Форматирует строку тегов для использования в URL.

    Args:
        text (str): Строка тегов.
        ind (int, optional): Индикатор форматирования. По умолчанию 0.

    Returns:
        str: Отформатированная строка тегов.
    """
    if type(text) != str:
        text = str(text)
    tags = ''

    if ind == 1:
        tags = text.replace(' ', '%20')
    else:
        tags = text.replace(' ', '''
  ''')
    return tags


def parsing(text, Guard):
    """
    Парсит XML-текст, извлекая информацию о тегах и ссылках на изображения.

    Args:
        text (str): XML-текст для парсинга.
        Guard: Объект Guard для фильтрации изображений.

    Returns:
        tuple: Кортеж, содержащий список словарей (информация о каждом изображении),
               список ссылок для скачивания и список тегов.
    """
    soup = bs(text, "xml")
    qq = []
    download_links = []
    _tags = []
    tagsOut = []
    for tag in soup.find_all('post'):

        try:
            file_url = tag.get('file_url')
            tags = formating_tags_list(tag.get('tags'), ind=0)
            _id = tag.get('id')

        except BaseException:
            file_url = None
            tags = ''
            _id = None

        # print(tags)
        # while True:pass

        # tags = tags.split(' ','')
        for i in tags.split('\n'):
            i = i.replace(' ', '')
            if i != '':
                tagsOut.append(i)
        val = Guard.GuardCheck(tagsOut, file_url, _id)
        # print(tagsOut, val)
        # while True:pass

        if val:
            qq.append(
                {f'{tag.get("id")}': {'id': _id, 'file_url': file_url, 'tags': tags}})
            download_links.append(file_url)

        _tags.append(tags)
    return qq, download_links, _tags, tagsOut

# 700 - IN Code Error


def replon__(_url, tagsStats, _stats):
    """
    Осуществляет HTTP-запрос, обрабатывает полученные данные и вызывает функцию парсинга.

    Args:
        _url (str): URL для HTTP-запроса.
        tagsStats: Статистика по тегам.
        _stats: Объект статистики сессии.

    Returns:
        tuple: Кортеж, содержащий список словарей (информация о каждом изображении),
               список ссылок для скачивания и список тегов.
    """
    url = _url
    data, download_links, __tags = [], [], []
    try:
        r = requests.get(_url)
        r.raw.decode_content = True
        if r.status_code == 403:
            print(f"{red}[-] {red}403: {url}")
        print(
            f'{green}[{r.status_code}] {violet}Parsing {blue}{_url}{violet} ...{white}')

        try:
            G = _stats[2]
        except BaseException:
            G = None
        data, download_links, tags, tags_in_pict = parsing(
            text=r.text, Guard=G)

        if _stats is not None:
            GTI = _stats[1]
            STATISTICS = _stats[0]
            a = {'response': 'OK',
                 'data': {
                     'url': url,
                     'tags': tags_in_pict,
                     'len': {
                         'data': len(data),
                         'download_links': len(download_links)
                     }}}
            STATISTICS.statistics_format_function_ok(a)
            GTI.ch_new_tags(input_tags=tags)
        status_code = 200

    except HTTPError as err_code:
        status_code = err_code.code
        print(f"{red}[-] {red}{err_code.code}: {url}")
    except urllib.error.URLError as err_code:
        if "[WinError 10054]" in str(err_code):
            status_code = 522
        elif "[Errno 99]" in str(err_code):
            status_code = 524
        elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
            status_code = 526
        else:
            status_code = '___'
        print(f"{red}[-] {red}{status_code}: {url}")
    except http.client.RemoteDisconnected as err_code:
        print(f"{violet}[-] {violet}101: {url}")
        status_code = 101
    except ConnectionResetError as err_code:
        print(f"{violet}[-] {violet}101: {url}")
        status_code = 101
    except ValueError as err_code:
        print(f"{violet}[?] ValueError: {url} {err_code}")
        status_code = 700
    except requests.exceptions.SSLError as err_code:
        if "[WinError 10054]" in str(err_code):
            status_code = 522
        elif "[Errno 99]" in str(err_code):
            status_code = 524
        elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
            status_code = 526
        else:
            status_code = '___'
        print(f"{red}[-] {red}{status_code}: {url}")
    except requests.exceptions.ConnectionError as err_code:
        if "[WinError 10054]" in str(err_code):
            status_code = 522
        elif "[Errno 99]" in str(err_code):
            status_code = 524
        elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):
            status_code = 526
        elif "HTTPSConnectionPool" in str(err_code):
            status_code = 522
        else:
            status_code = f'___ ({err_code})'
        print(f"{red}[-] {red}{status_code}: {url}")

    if (_stats is not None):
        if (status_code != 200):
            _stats.statistics_format_function_error(
                {'response': 'ERROR',
                 'data': {
                     'url': url,
                     'tags': tagsStats,
                     'errorInfo': {
                         'code': status_code,
                         'traceback': err_code}
                 }
                 })
            # __tags.append('ERROR ')

    return data, download_links, __tags


def find_count(_url, dev=False):
    """
    Определяет количество элементов на странице.

    Args:
        _url (str): URL страницы для определения количества элементов.
        dev (bool, optional): Индикатор разработки. По умолчанию False.

    Returns:
        tuple: Кортеж, содержащий количество элементов и смещение (offset).
    """
    if not dev:
        r = requests.get(_url)
        soup = bs(r.text, "xml")

    count = str(soup).split('''"><post height=""''')[0].split(
        '''" offset="''')[0].split('<posts count="')[1]
    count = count.replace('"/>', '')
    offset = 0
    return int(count), int(offset)


if str(os.name) == "nt":
    dir_pref = "\\"
else:
    dir_pref = "/"


def nameFolder(input_tags, dev=False):
    """
    Генерирует имя папки на основе введенных тегов.

    Args:
        input_tags (str): Введенные теги.
        dev (bool, optional): Индикатор разработки. По умолчанию False.

    Returns:
        str: Имя папки.
    """
    if len(input_tags.split(' ')) == 1:
        nf = str(
            input_tags.split(' ')[0].replace(
                '%20', '_').replace(
                ' ', '_'))
    else:
        nf = input_tags.replace('%20', '_').replace(' ', '_')
    return nf


do = os.getcwd()


def set_logger_settings():
    """
    Устанавливает настройки логгера.

    Returns:
        tuple: Кортеж, содержащий объект логгера и время запуска скрипта.
    """
    py_logger = logging.getLogger(__name__)
    py_logger.setLevel(logging.INFO)

    py_handler = logging.FileHandler(f"{starting_script_time2}.log", mode="w")
    py_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    py_logger.addHandler(py_handler)
    os.chdir(do)
    starting_script_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    py_logger.info(
        f"{'='*15}- STARTing script in [{starting_script_time}] -{'='*15}")

    return py_logger, starting_script_time


def check_memory(url, name_file, downloading):
    """
    Проверяет доступную память устройства.

    Args:
        url (str): URL для проверки.
        name_file (str): Имя файла.
        downloading: Функция для скачивания.

    Returns:
        None
    """

    def is_memory(url, name_file):
        status = (downloading(url, name_file))
        if status != '700':
            return True
        else:
            return False

    if is_memory(url, name_file):
        pass
    else:
        print('\r', end='')
        print()
        print(f"{red}[/] Память устройства заполнена!{white}")
        while is_memory(url, name_file) == False:
            pass
        print('\r', end='')
        print()
        print(f"{green}[/] Память для скачивания была найдена!{white}")


def reload_file_config(working_directory):
    statictics_file_name = 'config.json'
    if not os.path.exists(working_directory + dir_pref + statictics_file_name):
        q = []
        GuardVal = True
        BlockedTags = [
            "furry",
            "furry_dick",
            "shota",
            "guro",
            "futanari",
            "erect penis",
            "anthro",
            "presenting_anus",
            "presenting_penis",
            "muscular_male",
            "2boy2",
            "ugly_bastard",
            "ogre"
        ]

        q.append({
            'remote': False,
            'GuardOnline': GuardVal,
            'GuardBlockedTags': BlockedTags})
        json.dump(q, open(statictics_file_name, 'w'), indent=4, default=list)
        data_load = json.loads(open(statictics_file_name, 'r').read())

    else:
        data_load = json.loads(open(statictics_file_name, 'r').read())
    return data_load


if __name__ == '__main__':
    # print(nameFolder(input()))
    raise SystemExit('Не тот файл открываешь...')
