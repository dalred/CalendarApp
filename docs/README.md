# Действия с пользователями

* [Регистрация пользователя](#регистрация-пользователя) ![flutter](https://img.shields.io/badge/anonymous-brightgreen)
* [Авторизация пользователя](#авторизация-пользователя) ![flutter](https://img.shields.io/badge/anonymous-brightgreen)
* [Получение информации о пользователе](#получение-информации-о-пользователе) ![flutter](https://img.shields.io/badge/user-brightgreen)



## Регистрация пользователя
Приложению необходимо сделать сервер-сервер запрос POST `/core/signup/`.
В теле запроса необходимо передать обязательные параметры: `username`, `password`, `password_repeat`.

Пример POST запроса
```
{
    "username": "test@test.ru",
    "password": "test",
    "password_repeat": "test"
}
```
Пример ответа
```
{
    "id": int,
    "username": "test@test.ru",
    "first_name": "Unknown",
    "last_name": "Unknown",
    "email": null
}
HTTP Status 201 Created
```

## Авторизация пользователя

Приложению необходимо сделать сервер-сервер запрос POST `/core/login/`.
В теле запроса необходимо передать обязательные параметры: `username`, `password`.

Пример POST запроса
```
{
    "username": "test@test.ru",
    "password": "test"
}
```
Пример ответа
```
{
    "username": "test@test.ru",
    "password": "test"
}
HTTP Status 200 OK
```


## Получение информации о пользователе
Приложению необходимо сделать сервер-сервер запрос GET `/core/profile/`.

Пример ответа
```
{
    "id": int,
    "username": string,
    "email": string,
    "first_name": string,
    "last_name": string"
}
HTTP Status 200 OK
```


