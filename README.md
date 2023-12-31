# Курсовая работа «Резервное копирование»

## Создание программы для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.

### Схема работы программы:
1. Программа получает фотографии профиля пользователя VK, используя метод [photos.get](https://vk.com/dev/photos.get).
2. Сохраняет информацию по фотографиям в json-файл с результатами.
3. Создаёт для загруженных фотографий свою папку на Я.Диске.
4. Сохраняет фотографии максимального размера(ширина/высота в пикселях) на Я.Диске. Для этого ипользуются методы REST API Я.Диска и ключ, полученный с [Полигона Яндекс.Диска](https://yandex.ru/dev/disk/poligon/).

### Результат:
1. Информация по фотографиям сохранена в json-файл `./photos_information.json`;
2. Ссылка на Я.диск, куда добавились фотографии: *https://disk.yandex.ru/d/AWiCcwLMifC2Qg*
3. Логика программы реализована в файле `./backup.py`.
4. Все зависимости описаны в файле `./requiremеnts.txt`.