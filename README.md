# Совместный проект api_yamdb
Инструкция по установке api_yamdb

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:S71LL/api_yamdb.git
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
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
