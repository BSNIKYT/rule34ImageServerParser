# Gelbooru Image Downloader

## Описание

Этот скрипт представляет собой загрузчик изображений с веб-сайта Gelbooru.com. Gelbooru - это веб-сайт, предоставляющий изображения и анимацию в различных стилях, в том числе для взрослых. Скрипт использует Gelbooru API для поиска и загрузки изображений по заданным тегам.

## Использование

1. Запустите скрипт `main.py`.
2. Введите теги для поиска изображений. Пример формата тегов: `cat_ears`.
3. Скрипт выполнит запросы к Gelbooru API и выведет количество найденных изображений.
4. Скрипт создаст папку для хранения загруженных данных.
5. В зависимости от вашего выбора, скрипт может загрузить изображения в созданную папку.

## Важно

- Скрипт поддерживает удаленный режим. Если установлен флаг `REMOTE=True`, скрипт будет запущен с использованием списка тегов из файла `tags.txt`.
- В файле `tags.txt` каждый тег должен быть указан в отдельной строке.

## Требования

- Python 3
- Библиотеки, указанные в разделе `Импорт библиотек` в `main.py`

## Автор

[Я](https://github.com/BSNIKYT/)

## Структура проекта

- `main.py`: Основной файл скрипта для загрузки изображений.
- `modules/colors.py`: Модуль с определением цветов для вывода в консоли.
- `modules/functions.py`: Модуль с вспомогательными функциями.
- `modules/downloader.py`: Модуль для загрузки изображений.
- `modules/statisticksDEF.py`: Модуль с определением классов для статистики, глобальных тегов и настроек.
