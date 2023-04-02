# API YaMDb

Проект API YaMDb собирает отзывы пользователей на различные произведения такие как фильмы, книги и музыка.


### Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/vikkilat/infra_sp2.git
```

Перейти в папку infra и запустить docker-compose.yaml
(при установленном и запущенном Docker)
```
cd infra_sp2/infra
docker-compose up
```

Для пересборки контейнеров выполнять команду:
(находясь в папке infra, при запущенном Docker)
```
docker-compose up -d --build
```

В контейнере web выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Загрузить базу данных из дампа:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

Проверьте работоспособность приложения, для этого перейдите на страницу:

```
http://localhost/admin/
```


Шаблон наполнения .env расположенный по пути infra/.env
```
DB_ENGINE=<...> # указываем, что работаем с postgresql
DB_NAME=<...> # имя базы данных
POSTGRES_USER=<...> # логин для подключения к базе данных
POSTGRES_PASSWORD=<...> # пароль для подключения к БД (установите свой)
DB_HOST=<...> # название сервиса (контейнера)
DB_PORT=<...> # порт для подключения к БД 
```

### Автор
[Латышева Виктория](https://github.com/vikkilat) 