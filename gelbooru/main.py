
import datetime
from modules.colors import *
from modules.functions import *
from modules.downloader import *
from modules.statisticksDEF import Statistics
from modules.statisticksDEF import GlobalTagsInfo
from modules.statisticksDEF import Guard
from modules.statisticksDEF import Config

import json
import time


format_link = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=cat_ears'

api_link =   'https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='



format_enter_text = f'''
{blue}Format: {white}{format_link}
'''
working_dir = os.getcwd()
if str(os.name) == "nt":
    dir_pref = "\\"
else:
    dir_pref = "/"

try:
    os.mkdir("logging")
    os.chdir(f'{working_dir + dir_pref + "logging"}')
    py_logger, starting_script_time = set_logger_settings()
except FileExistsError:
    os.chdir(f'{working_dir + dir_pref + "logging"}')
    py_logger, starting_script_time = set_logger_settings()

except PermissionError:
    py_logger, starting_script_time = set_logger_settings()


def inputUrl(tags):
    """
    Получает от пользователя теги для поиска изображений на веб-сайте Gelbooru.com.

    Параметры:
    - tags (str): Строка тегов, которые вводит пользователь (может быть None).

    Возвращает:
    - str: Строка тегов, введенных пользователем.

    Описание:
    1. Если параметр tags равен None, функция выводит текст format_enter_text,
       предоставляя пользователю пример формата ввода тегов.

    2. Если tags не равен None, функция проверяет, является ли введенная строка
       корректным URL с тегами с помощью функции check_link(tags).
       - Если tags пусто, устанавливается значение q в False.
       - Если tags не является корректным URL, функция входит в цикл,
         запрашивая пользователя ввести теги снова, пока не будет введен корректный URL.

    3. После получения корректных тегов, вызывается функция check_internet()
       для проверки наличия интернет-соединения.

    4. Возвращается строка тегов, введенных пользователем.
    """
    if tags is None:
        print(format_enter_text)

    if tags is None:
        tags = input(f'{green}>>> {white}')
    else:
        q = check_link(tags)
        if tags == '':
            q = False
        if not q:
            while q == False:
                tags = input(f'{red}>>> {white}')
                q = check_link(tags)
    check_internet()
    return tags


def main(input_, REMOTE):
    """
    Основная функция скрипта для загрузки изображений с веб-сайта Gelbooru.com.

    Параметры:
    - input_ (str): Строка тегов для поиска изображений (может быть None).
    - REMOTE (bool): Флаг, указывающий, запущен ли скрипт удаленно.

    Возвращает:
    - str: Строка с информацией об успешности выполнения или ошибке.

    Описание:
    1. Инициализация объектов S, T, G для статистики, глобальной информации по тегам и
       защиты (предполагается, что эти классы определены в других частях вашего кода).

    2. Инициализация пустого списка urls для хранения URL-адресов запросов к API Gelbooru.com.

    3. Получение тегов с помощью функции inputUrl(input_).

    4. Вывод информации о введенных тегах и запись статистики о сессии в журнал.

    5. Форматирование тегов и проверка их наличия.
       - Если теги не введены, возвращается сообщение об ошибке.
       - Выводится количество найденных изображений по тегам.

    6. Заполнение списка urls URL-адресами для запросов к Gelbooru.com в зависимости от количества изображений.

    7. Инициализация пустых списков для хранения данных, ссылок на загрузку и глобальных тегов.

    8. Цикл по списку urls:
       - Запуск функции replon__ для каждого URL-адреса.
       - Обновление списков data, download_links, GlobalTags данными из функции replon__.

    9. Создание папки input для хранения данных.

    10. Преобразование списка download_links в уникальный список.

    11. Создание папки name_folder с уникальным именем на основе введенных тегов.

    12. Вывод информации о статистике и тегах.

    13. Загрузка изображений, если флаг REMOTE равен Y или если пользователь подтверждает загрузку.

    14. Возврат строки с информацией об успешности выполнения.

    Пример:
    ```python
    result = main(None, REMOTE=False)
    print(result)
    ```

    Примечания:
    - Функции inputUrl(), formating_tags_list(), check_link(), find_count(),
      replon__(), download() и другие, предположительно, определены в других частях вашего кода.
    - Функции S.statistics_format_function_ok(), T.ch_new_tags() и T.writeTags() вызываются извне
      и, вероятно, также определены в других частях вашего кода.
    - Переменные api_link, format_enter_text, green, white, red, api_link, S, T, G, urls, data,
      download_links, GlobalTags, C, os, find_count(), download(), check_internet() и другие
      предположительно определены в других частях вашего кода.
    """
    py_logger.info(f'[SEP]')
    py_logger.info(f'[MAIN] {"-"*5} NEW SESSION')
    S = Statistics(working_dir=os.getcwd(), logger=py_logger)
    T = GlobalTagsInfo(py_logger)
    G = Guard(py_logger)

    urls = []  # $ autopep8 --in-place --aggressive --aggressive main.py

    input_tags = inputUrl(input_)
    print(f'{green}Input Tags: {violet}{input_tags}{white}')

    S.statistics_format_function_ok({
        "timestamp": str(datetime.now()).split('.')[0],
        "input": input_tags
    })
    py_logger.info(f'[MAIN] User entered tags: {input_tags}')
    tags = formating_tags_list(input_tags, ind=1)
    if tags == '':
        py_logger.error(
            f'[MAIN] The user did not enter any tags.: {input_tags}')
        return f'{red}[ERROR] {red}You have not entered tag(s): _{tags}_ ...{white}'

    print(f'''\n{'='*10}- GetDownloadFiles -{'='*10}''')
    count, _ = find_count(f'{api_link}{tags}&pid=0')
    print(f'''Count:{count}
{'-'*15}''')

    py_logger.info(f'''{'='*10}- [PARSER] -{'='*10}''')
    py_logger.info(f'[PARSER] Count: {count}')

    py_logger.info(f'''{'-'*8}- [Links] -{'-'*8}''')
    for i in range(0, round(count / 100) + 1):
        link = f'{api_link}{tags}&pid={i}'
        py_logger.info(f'[PARSER] [LINK][{i}]: {link}')

        urls.append(link)

    data = []
    download_links = []
    GlobalTags = []

    s = [S, T, G]

    for link in urls:
        print('\r', end='')
        _data, _download_links, __tags = replon__(
            _url=link, _stats=s, tagsStats=tags)

        for link in _data:
            data.append(link)
        for link in _download_links:
            download_links.append(link)
        for tags in __tags:
            GlobalTags.append(tags)
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break

    if not os.path.exists('input'):
        os.mkdir("input")
        os.chdir(f'{working_dir + dir_pref + "input"}')
    os.chdir(f'{working_dir + dir_pref + "input"}')

    download_links = list(set(download_links))

    name_folder = nameFolder(input_tags)
    if not os.path.exists(name_folder):
        os.mkdir(name_folder)
    wdir = os.getcwd()
    os.chdir(name_folder)

    print(f'''\n{'='*10}- STATS -{'='*10}\n''')

    S.writeStats()
    T.ch_new_tags(input_tags=GlobalTags)
    T.writeTags()

    os.chdir(wdir)
    print(f'''\n{'='*10}- Download -{'='*10}''')

    if REMOTE:
        ch_download = 'Y'
    else:
        ch_download = 'NONE'

    if len(download_links) != 0 and download_links[0] != None:
        if ch_download != 'Y':
            if input('\nDownload? (Y/N) >>> ') == 'Y':
                os.chdir(name_folder)
                download(download_links, py_logger)
        else:
            os.chdir(name_folder)
            download(download_links, py_logger)
    else:
        print(f'{red}[!] There is nothing to download!{white}')

    os.chdir(working_dir)


if __name__ == '__main__':
    C = Config(py_logger)

    if C.remote:
        with open("tags.txt", "r") as file1:
            for line in file1:
                main(line.strip(), REMOTE=True)
    else:
        main(None, REMOTE=False)
    
    input()
