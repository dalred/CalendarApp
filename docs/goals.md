# Действия с целями


#### Методы для работы с целями пользователя
* POST `/goals/goal/create/` — [cоздание цели](#Создание-цели) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)
* GET `/goals/goal/list` — [просмотр списка целей](#список-целей-пользователя) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* GET `/goals/goal/‹pk›` — [просмотр цели](#просмотр-цели) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* PUT `/goals/goal/‹pk›` — [редактирование цели](#редактирование-цели) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)
* DELETE `/goals/goal/‹pk›` — [удаление цели](#удаление-доски) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)


#### Создание цели
Приложению необходимо сделать сервер-сервер запрос POST `/goals/goal/create/`
> Пользователь может создавать/изменять/удалять цели только в тех категориях, в досках которых он является участником с ролью «Владелец» или «Редактор».

Пример POST запроса
```
{
  "due_date": "2022-06-28",
  "title": "string",
  "description": "string",
  "status": 1,
  "priority": 1,
  "category": 0
}
```
Пример ответа
```
{
  "id": 0,
  "due_date": "2022-06-28",
  "created": "2022-06-28T22:33:33.372Z",
  "updated": "2022-06-28T22:33:33.372Z",
  "title": "string",
  "description": "string",
  "status": 1,
  "priority": 1,
  "category": 0
}
HTTP Status 201 Created
```

## Список всех целей пользователя
В данном endpoint будут отображаться как общие цели так и цели которые принадлежат только текущему пользователю.
>Пользователю выдаются только те цели, которые находятся в категориях, в досках которых он является участником.

Приложению необходимо сделать сервер-сервер запрос GET `goals/goal/list/`.

Пример ответа
```
{
  [
    {
      "id": 0,
      "user": {
        "id": 0,
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string"
      },
      "due_date": "2022-06-28",
      "created": "2022-06-28T22:37:20.903Z",
      "updated": "2022-06-28T22:37:20.903Z",
      "title": "string",
      "description": "string",
      "status": 1,
      "priority": 1,
      "category": 0
    },
    {
      "id": 1,
      "user": {
        "id": 0,
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string"
      },
      "due_date": "2022-06-28",
      "created": "2022-06-28T22:37:20.903Z",
      "updated": "2022-06-28T22:37:20.903Z",
      "title": "string",
      "description": "string",
      "status": 1,
      "priority": 1,
      "category": 0
    },
  ]
}
HTTP Status 200 OK
```
## Просмотр цели
Приложению необходимо сделать сервер-сервер запрос GET `goals/goal/{id}`.
>Пользователю выдаются только те цели, которые находятся в категориях, в досках которых он является участником.

Пример ответа
```
{
  "id": 0,
  "user": {
    "id": 0,
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string"
  },
  "due_date": "2022-06-28",
  "created": "2022-06-28T22:38:28.677Z",
  "updated": "2022-06-28T22:38:28.677Z",
  "title": "string",
  "description": "string",
  "status": 1,
  "priority": 1,
  "category": 0
}
HTTP Status 200 OK
```
## Редактирование цели
>Для редактирования доски текущий пользователь должен обладать правами owner и writer и быть участником доски.

Приложению необходимо сделать сервер-сервер запрос PUT на endpoint `/goals/goal/{id}`

Пример запроса
```
{
  "user": {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string"
  },
  "due_date": "2022-06-28",
  "title": "string",
  "description": "string",
  "status": 1,
  "priority": 1,
  "category": 0
}
HTTP Status 200 OK
```

Пример ответа
```
{
  "id": 0,
  "user": {
    "id": 0,
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string"
  },
  "due_date": "2022-06-28",
  "created": "2022-06-28T22:37:54.306Z",
  "updated": "2022-06-28T22:37:54.306Z",
  "title": "string",
  "description": "string",
  "status": 1,
  "priority": 1,
  "category": 0
}
HTTP Status 200 OK
```
#### Удаление цели
Для редактирования цели текущий пользователь должен обладать правами owner.
Приложению необходимо сделать сервер-сервер запрос `Delete` на endpoint `/goals/goal/{id}`

Пример response
```
HTTP Status 204 No content
```