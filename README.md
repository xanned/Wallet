Для запуска проекта необходимо клонировать репозиторий, в папке проекта запустить командой docker-compose up (или  docker-compose up -d).

Для оставновки приложения - docker stop wallet


Админ панель доступна по адресу http://127.0.0.1:8000/admin/

Пользователь: admin

Пароль: admin

Для запуска тестов необходимо выполнить команду pytest в контейнере (команда docker exec -it wallet sh)
