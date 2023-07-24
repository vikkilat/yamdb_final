![Yamdb Workflow Status](https://github.com/vikkilat/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

# Проект API YaMDb
Проект API YaMDb собирает отзывы пользователей на различные произведения такие как фильмы, книги и музыка.
GitHub Actions — это облачный сервис, инструмент для автоматизации процессов тестирования и деплоя проектов.

## Описание проекта

Произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен.

Произведению может быть присвоен жанр из списка предустановленных.

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).

На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Описание Workflow
### Workflow состоит из четырёх шагов:
#### tests
- Проверка кода на соответствие PEP8, автоматический запуск тестов.
#### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
#### deploy 
- Автоматический деплой на боевой сервер при пуше в главную ветку main.
#### send_massage
- Отправка уведомления в телеграм-чат.

## Стек технологий:
* Python 3.7
* Django
* Django Rest Framework
* Docker
* Docker compose


## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/vikkilat/yamdb_final.git
cd api_yamdb
```

Установка на удаленном сервере (Ubuntu):

Подключитесь к удаленному серверу:

```
ssh <USERNAME>@<IP_ADDRESS>
```

Установите docker на сервер:

```
sudo apt install docker.io
```

Установите docker-compose на сервер:

```
sudo curl -L "https://github.com/docker/compose/releases/download/2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопируйте подготовленные файлы из корневой папки проекта на сервер:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r nginx/ <username>@<host>:/home/<username>/
```

Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

После успешного деплоя:

Зайдите на сервер и выполните команды:

Выполните миграции:

```
sudo docker-compose exec web python manage.py makemigrations --noinput
sudo docker-compose exec web python manage.py migrate --noinput
```
Подгрузите статику:

```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Загрузить базу данных из дампа:

```
sudo docker-compose exec web python manage.py loaddata fixtures.json 
```

Создать суперпользователя Django:

```
sudo docker-compose exec web python manage.py createsuperuser
```

Для проверки работоспособности приложения перейдите на страницу:

```
http:/<IP_ADDRESS>/admin/
```

Документация для YaMDb доступна по адресу:

```
http:/<IP_ADDRESS>/redoc/
```

### Команда проекта

Виктория Л./ Viktoria L. - [vikkilat](https://github.com/vikkilat) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля;

Дмитрий К./ Dmitriy K. - [Ku3mi4_51rus](https://github.com/Ku3mi4-51rus) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них;

Яна Ш./ Yana Sh. - [gwaimui](https://github.com/gwaimui) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.
