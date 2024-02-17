# Совместный проект API для сайта с рецензиями

### API позволяет получать из базы данных записи о рецензиях, пользователях, комментариях к рецензиям и оценкам пользователей

Выполнял роль тимлида комманды. Также моя часть проекта заключалась в реализации рецензий, комментариев и оценок пользователей

Авторы проекта: Кирилл[https://github.com/S71LL], Максим[https://github.com/makskhaliosa], Никита[https://github.com/mazazyrik]

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:S71LL/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/scripts/activate
```

Установить и обновить менеджер пакетов:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в дерикторию с файлом manage.py

```
cd api_yamdb
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Проект доступен локально
## http://127.0.0.1:8000/api/v1/

Документация проекта
## http://127.0.0.1:8000/redoc/
