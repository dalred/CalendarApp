# Действия с пользователями

* [Регистрация пользователя](#регистрация-пользователя) ![flutter](https://img.shields.io/badge/anonymous-blueviolet)
* [Авторизация пользователя](#авторизация-пользователя) ![flutter](https://img.shields.io/badge/anonymous-blueviolet)
* [Получение информации о пользователе](#получение-информации-о-пользователе) ![flutter](https://img.shields.io/badge/user-green)
* [Изменение информации о пользователе](#изменение-информации-о-пользователе) ![flutter](https://img.shields.io/badge/user-green)
* [Изменение пароля пользователя](#изменение-пароля-пользователя) ![flutter](https://img.shields.io/badge/user-green)
* [Выход пользователя из профиля](#выход-пользователя-из-профиля) ![flutter](https://img.shields.io/badge/user-green)


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
## Изменение информации о пользователе
Приложению необходимо сделать сервер-сервер запрос PUT `/core/profile/`.

Пример PUT запроса
```
{
    "email": "test@test.ru"
}
```
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
## Изменение пароля пользователя
Приложению необходимо сделать сервер-сервер запрос PUT `/core/update_password/`.

Пример PUT запроса
```
{
    "old_password": string,
    "new_password": string
}
```
Пример ответа
```
HTTP Status 204 NO CONTENT
```

## Выход пользователя из профиля
Приложению необходимо сделать сервер-сервер запрос DELETE `/core/profile/`.

Пример ответа
```
HTTP Status 204 NO CONTENT
```
