import json
import logging
from json import JSONDecodeError
import re

from flask import request, render_template

# Добавляем логирование
logging.basicConfig(filename="log.log", encoding='utf-8', level=logging.INFO)

# Скачиваем json файл
try:
    with open('./posts/posts.json', "r", encoding='utf-8') as f:
        publication = json.load(f)
except FileNotFoundError as err:
    print(err)
    print('Файл не найден')
except JSONDecodeError:
    print('Файл не удается преобразовать')

# Создаем множество расширений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def is_filename_allowed(filename):
    # Получаем расширение файла
    extension = filename.split(".")[-1].lower()
    # Проверка, есть ли в списке расширение файла
    if extension in ALLOWED_EXTENSIONS:
        return True
    logging.info('Загруженный файл не картинка')
    return False


def loading(picture_name, content_name):
    try:
        # Получаем объект картинки и текста из формы
        picture = request.files.get(picture_name)
        content = request.values.get(content_name)
        # Проверка: загружен ли файл?
        if picture and content:
            # Получаем имя файла у загруженного файла
            filename = picture.filename
            # file_url = picture
            # Проверка расширения
            if is_filename_allowed(filename):
                # Сохраняем картинку под родным именем в папку uploads
                picture.save(f'./uploads/images/{filename}')
                # добавляем пост в список
                publication_dict = {'pic': f'./uploads/images/{filename}', 'content': content}
                publication.insert(0, publication_dict)
                with open('./posts/posts.json', 'w') as file:
                    json.dump(publication, file, indent=4, ensure_ascii=False)
                return render_template('post_uploaded.html', picture=filename, text=content)

            else:
                logging.info('Файл - не изображние')
                extension = filename.split(".")[-1].lower()
                return f'Ну такое не подходит: {extension}'
        else:
            return 'Должен быть текст и картинка'
    except FileNotFoundError:
        logging.error('Ошибка при загрузке файла')
        return 'Ошибка при загрузке файла'


def found_posts_func():
    search = request.args['s'].lower()
    logging.info(f'Слово для поиска {search}')
    list_posts = []
    for post in publication:
        clean_text = re.sub(r"\W", " ", post['content'].lower())
        if search in clean_text.split():  # post['content'].lower().replace(',', '').split()
            found_posts = {'pic': post['pic'], 'content': post['content']}
            list_posts.append(found_posts)
    return render_template('post_list.html', search=search, list_posts=list_posts)
