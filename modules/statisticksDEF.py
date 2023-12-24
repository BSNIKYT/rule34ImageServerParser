import os
import json
from modules.reloadData import reload_file_statistics

from modules.functions import reload_file_config as reload_config

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"

if str(os.name) == "nt":
    dir_pref = "\\"
else:
    dir_pref = "/"


class Config():
    """
    Класс для управления конфигурацией.

    Attributes:
        logger: Объект логгера для записи сообщений.
        remote: Флаг, указывающий на использование удаленного режима.
        GuardTagsInverse: Флаг инвертирования блокированных тегов для Guard.
        GuardOnline: Флаг активации Guard.
        BlockedTags: Список заблокированных тегов для Guard.
    """
    def __init__(self, logger):
        """
        Инициализирует объект конфигурации, загружая данные из файла `config.json`.

        Args:
            logger: Объект логгера для записи сообщений.
        """
        self.logger = logger
        self.logger.info('[Config] module has beel successfully loaded.')
        # reload_file_config(os.getcwd())[0]
        self.config = reload_config(os.getcwd())[0]
        try:self.remote = self.config['remote']
        except KeyError:self.remote = False
        try:self.GuardTagsInverse = self.config['GuardTagsInverse']
        except KeyError:self.GuardTagsInverse = False
        try:self.GuardOnline = self.config['GuardOnline']
        except KeyError:self.GuardOnline = True
        self.BlockedTags = self.config['GuardBlockedTags']
        self.logger.info(f'[Config] Remote: {self.remote}')
        self.logger.info(f'[Config] GuardOnline: {self.GuardOnline}')
        self.logger.info(f'[Config] GuardTagsInverse: {self.GuardTagsInverse}')
        self.logger.info(f'[Config] Count GuardBlockedTags: {len(self.BlockedTags)}')
        

    def reload_config(self, path, filename='config.json'):
        """
        Перезагружает конфигурацию из файла.

        Args:
            path: Путь к директории, где расположен файл конфигурации.
            filename (str, optional): Имя файла конфигурации. По умолчанию 'config.json'.

        Returns:
            dict: Словарь с данными конфигурации.
        """
        statictics_file_name = filename
        if not os.path.exists(path + dir_pref + statictics_file_name):
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
            json.dump(
                q,
                open(
                    statictics_file_name,
                    'w'),
                indent=4,
                default=list)
            data_load = json.loads(open(statictics_file_name, 'r').read())

        else:
            data_load = json.loads(open(statictics_file_name, 'r').read())
        return data_load


class Guard():
    """
    Класс для реализации Guard - фильтрации изображений по тегам.

    Attributes:
        logger: Объект логгера для записи сообщений.
        online_val: Флаг активации Guard.
        BlockedTags: Список заблокированных тегов для Guard.
        GuardTagsInverse: Флаг инвертирования блокированных тегов для Guard.
        guardON: Флаг состояния Guard.
    """
    def __init__(self, logger):
        """
        Инициализирует объект "Guard", загружая настройки из файла конфигурации.

        Args:
            logger: Объект логгера для записи сообщений.
        """
        self.logger = logger
        self.logger.info('[Guard] module has beel successfully loaded.')
        self.config_data = reload_config(os.getcwd())[0]
        self.online_val = self.config_data['GuardOnline']
        self.BlockedTags = self.config_data['GuardBlockedTags']
        self.GuardTagsInverse = self.config_data['GuardTagsInverse']
        self.logger.info(f"[Guard] {'='*11}")
        self.logger.info(f'[Guard] Online: {self.online_val}')
        self.logger.info(f"[Guard] {'-'*8}")
        for tag in self.config_data['GuardBlockedTags']:
            self.logger.info(f'[Guard] Tag: {tag}')
        self.logger.info(f"[Guard] {'='*11}")
        if self.online_val:
            print(f"{green}[+] GuardStatus: {self.online_val}")
            print(
                f"[+] {white}Number of blocked tags: {blue}{len(self.config_data['GuardBlockedTags'])}{white}")
            print(f"{green}[+] Guard protects your psyche.")
        else:
            print(f"{red}[-] GuardStatus: {self.online_val}{white}")
            print(f'{red}[-] Guard cannot protect your psyche now.{white}')

        if self.online_val:
            self.guardON = True
        else:
            self.guardON = False

    def GuardCheck(self, tags, file_url, _id):
        """
        Проверяет теги изображения на соответствие списку заблокированных тегов.

        Args:
            tags: Список тегов изображения.
            file_url: URL файла изображения.
            _id: Идентификатор изображения.

        Returns:
            bool: True, если изображение прошло проверку Guard, False в противном случае.
        """
        if self.config_data['GuardOnline']:
            if isinstance(tags, list):
                for tag in tags:
                    if self.GuardTagsInverse == False:
                        if tag in self.BlockedTags:
                            self.logger.warning(f'''{'='*10}- [FIND] -{'='*10}''')
                            self.logger.warning(
                                f'[Guard] -[ A blacklisted tag was found: {tag}')
                            self.logger.warning(f'[Guard] -[ File Url: {file_url}')
                            self.logger.warning(f'[Guard] -[ ID: {_id}')
                            self.logger.warning(f'''{'='*10}-        -{'='*10}''')
                            print(f'{red}[Guard]: A blacklisted tag was found: {tag}{white}')
                            return False
                    
                    elif self.GuardTagsInverse == True:
                        if tag not in self.BlockedTags:return False
                        else:
                            self.logger.warning(f'''{'='*10}- [FIND] -{'='*10}''')
                            self.logger.warning(f'[Guard] -[ A unblacklisted tag was found: {tag}')
                            self.logger.warning(f'[Guard] -[ File Url: {file_url}')
                            self.logger.warning(f'[Guard] -[ ID: {_id}')
                            self.logger.warning(f'''{'='*10}-        -{'='*10}''')
                            print(f'{green}[Guard]: A unblacklisted tag was found: {tag}{white}')
                            return True
                    else: return None
                return True
        else:
            return True


class GlobalTagsInfo():
    """
    Класс для отслеживания глобальных тегов.

    Attributes:
        logger: Объект логгера для записи сообщений.
        tagsGlobal: Список глобальных тегов.
    """
    tagsGlobal = []

    def __init__(self, logger):
        """
        Инициализирует объект для отслеживания глобальных тегов.

        Args:
            logger: Объект логгера для записи сообщений.
        """
        self.logger = logger

    def ch_new_tags(self, input_tags):
        """
        Обновляет список глобальных тегов.

        Args:
            input_tags: Новые теги, которые нужно добавить.
        """
        if not isinstance(input_tags, list):
            input_tags = input_tags.split(' ')
        for new_or_old_tags in input_tags:
            if new_or_old_tags not in self.tagsGlobal:
                self.tagsGlobal.append(input_tags)

    def FrSTRtoList(self, input_tags):
        """
        Преобразует строку тегов в список.

        Args:
            input_tags: Строка тегов.

        Returns:
            list: Список тегов.
        """
        tagsOut = []
        self.data_load = self.input_tags
        for i in range(0, len(self.data_load)):
            zn = self.data_load[i][0]
            if zn not in tagsOut:
                zn = zn.replace(' ', '')
                for tag in zn.split('\n'):
                    if tag != '':
                        if tag not in tagsOut:
                            tagsOut.append(str(tag))
        return tagsOut

    def writeTags(self):
        """
        Записывает текущий список глобальных тегов в файл "GlobalTagsInput.json".
        """
        data_load = self.tagsGlobal
        tagsOut = []
        for i in range(0, len(data_load)):
            zn = data_load[i][0]
            if zn not in tagsOut:
                zn = zn.replace(' ', '')
                for tag in zn.split('\n'):
                    if tag != '':
                        if tag not in tagsOut:
                            tagsOut.append(str(tag))

        tagsOut = sorted(tagsOut)
        with open("GlobalTagsInput.json", "w") as outfile:
            json.dump(tagsOut, outfile, indent=4)
        self.logger.info(
            '[GlobalTagsInfo] File created [GlobalTagsInput.json]')
        print('File created [GlobalTagsInput.json]')


class Statistics():
    """
    Класс для отслеживания статистики сессии.

    Attributes:
        logger: Объект логгера для записи сообщений.
        working_directory: Рабочая директория.
        data_stats: Статистика сессии.
    """

    def __init__(self, working_dir, logger):
        """
        Инициализирует объект для отслеживания статистики сессии.

        Args:
            working_dir: Рабочая директория.
            logger: Объект логгера для записи сообщений.
        """
        self.logger = logger
        self.logger.info('[Statistics] module has beel successfully loaded.')
        self.logger.info(f"[Statistics] {'='*11}")
        self.working_directory = working_dir
        self.logger.info(
            f'[Statistics] Working Directory: {self.working_directory}')
        self.data_load = reload_file_statistics(self.working_directory)
        self.logger.info(f'[Statistics] Data loaded successfully.')
        self.data_stats = self.data_load

    def statistics_format_function_ok(self, data):
        """
        Добавляет успешное событие в статистику.

        Args:
            data: Данные о событии.
        """
        self.data_stats.append(data)

    def statistics_format_function_error(self, data):
        """
        Добавляет ошибочное событие в статистику.

        Args:
            data: Данные о событии.
        """
        self.data_stats.append(data)

    def writeStats(self):
        """
        Записывает статистику в файл "statistics.json".
        """
        with open("statistics.json", "w") as outfile:
            json.dump(self.data_stats, outfile, indent=4)
        self.logger.info('[Statistics] File created [statistics.json]')
        print('File created [statistics.json]')


class CheckAvailableMemoryDevice():
    """
    Класс для проверки доступной памяти устройства.
    """

    def __init__(self):
        """
        Инициализирует объект для проверки доступной памяти устройства.
        """
        pass

    def check(self):
        """
        Пустой метод. Находится в бесконечном цикле, предположительно для постоянной проверки доступной памяти (не реализовано).
        """
        dostypnaia_pamuat = True
        while dostypnaia_pamuat:
            pass


if __name__ == "__main__":
    print(Guard())
