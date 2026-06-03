# TeamFinder

TeamFinder — веб-приложение для поиска команды в pet-проекты. Пользователи могут публиковать идеи проектов, просматривать профили участников, присоединяться к чужим проектам и сохранять интересные проекты в избранное.

Проект реализован на Django. Для хранения данных используется PostgreSQL.

## Возможности

- регистрация и вход по email и паролю;
- публичные профили пользователей;
- редактирование профиля, контактов и аватара;
- смена пароля;
- список проектов с пагинацией;
- создание и редактирование собственных проектов;
- завершение проекта владельцем;
- присоединение к проекту и отказ от участия;
- добавление проектов в избранное;
- страница избранных проектов;
- фильтрация пользователей по критериям варианта 1;
- админ-панель Django для управления пользователями и проектами;
- команда для создания тестовых данных.

## Стек

- Python 3.12;
- Django 5.2;
- PostgreSQL;
- Docker Compose;
- Pillow;
- python-decouple.

## Подготовка окружения

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Переменные окружения

Скопируйте пример файла окружения:

```bash
cp .env_example .env
```

Для Windows PowerShell:

```bash
Copy-Item .env_example .env
```

Заполните `.env`:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5436
```

Описание переменных:

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ Django. |
| `DJANGO_DEBUG` | Режим отладки. Для локального запуска можно оставить `True`. |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты через запятую. |
| `POSTGRES_DB` | Имя базы данных PostgreSQL. |
| `POSTGRES_USER` | Пользователь PostgreSQL. |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL. |
| `POSTGRES_HOST` | Хост базы данных. |
| `POSTGRES_PORT` | Порт базы данных. |

## Запуск базы данных

Запустите PostgreSQL:

```bash
docker compose up -d
```

Контейнер публикует PostgreSQL на порту `5436`.

Остановить контейнер можно командой:

```bash
docker compose down
```

## Запуск приложения

Примените миграции:

```bash
python manage.py migrate
```

Создайте тестовые данные:

```bash
python manage.py seed
```

Команда создаст несколько пользователей и проектов. Тестовый аккаунт:

```text
email: maria@yandex.ru
password: password
```

Запустите сервер разработки:

```bash
python manage.py runserver
```

Откройте приложение:

```text
http://127.0.0.1:8000/projects/list/
```

Если порт `8000` занят:

```bash
python manage.py runserver 127.0.0.1:8001
```

Тогда приложение будет доступно по адресу:

```text
http://127.0.0.1:8001/projects/list/
```

## Тесты

Запуск автоматических тестов:

```bash
python manage.py test
```

## Админ-панель

Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Админ-панель доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

## Автор

Копий Илья

- GitHub: [https://github.com/Logic777Killer](https://github.com/Logic777Killer)
- Email: ilyakopiy@gmail.com
