![Yamdb Workflow Status](https://github.com/vikkilat/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

## Описание проекта

Проект API YaMDb собирает отзывы пользователей на различные произведения такие как фильмы, книги и музыка.

GitHub Actions — это облачный сервис, инструмент для автоматизации процессов тестирования и деплоя проектов. 

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


## Установка

Клонировать репозиторий на локальную машину:

```
https://github.com/vikkilat/yamdb_final.git
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
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
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


## Проект будет доступен по вашему IP-адресу.

Образ на DockerHub: https://hub.docker.com/r/vikkilat/yamdb_final

### Автор
[Латышева Виктория](https://github.com/vikkilat) 
