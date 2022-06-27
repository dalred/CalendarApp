# Действия с категориями


#### Методы для работы с категориями пользователя
* POST `/goals/goal_category/create/` — [cоздание категории](#Создание-категории) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)
* GET `/goals/goal_category/list` — [просмотр списка категорий](#список-категорий-пользователя) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* GET `/goals/goal_category/‹pk›` — [просмотр категории](#просмотр-категории) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* PUT `/goals/goal_category/‹pk›` — [редактирование категории](#редактирование-категории) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)
* DELETE `/goals/goal_category/‹pk›` — [удаление категории](#удаление-доски) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)


#### Создание категории
Приложению необходимо сделать сервер-сервер запрос POST `/goals/goal_category/create/`

Пример POST запроса
```
{
  "title": "string",
  "is_deleted": false,
  "board": 0
}
```
Пример ответа
```
{
  "id": 0,
  "created": "2022-06-27T06:37:41.763Z",
  "updated": "2022-06-27T06:37:41.763Z",
  "title": "string",
  "is_deleted": false,
  "board": 0
}
HTTP Status 201 Created
```

## Список категорий пользователя
Приложению необходимо сделать сервер-сервер запрос GET `goals/goal_category/list/`.

Пример ответа
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "user": {
        "id": 0,
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string"
      },
      "created": "2022-06-27T06:27:05.618Z",
      "updated": "2022-06-27T06:27:05.618Z",
      "title": "string",
      "is_deleted": false,
      "board": 0
    }
  ]
}
HTTP Status 200 OK
```
## Просмотр категории
Приложению необходимо сделать сервер-сервер запрос GET `goals/goal_category/{id}`.
Пользователю выдаются только те категории, в досках которых он является участником.
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
  "created": "2022-06-27T06:50:33.232Z",
  "updated": "2022-06-27T06:50:33.232Z",
  "title": "string",
  "is_deleted": false,
  "board": 0
}
HTTP Status 200 OK
```
## Редактирование категории
Для редактирования доски текущий пользователь должен обладать правами owner и writer и быть участником доски.
Приложению необходимо сделать сервер-сервер запрос PUT на endpoint `/goals/goal_category/{id}`

Пример запроса
```
{
  "title": "string",
  "is_deleted": true
}
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
  "created": "2022-06-27T06:53:45.801Z",
  "updated": "2022-06-27T06:53:45.801Z",
  "title": "string",
  "is_deleted": false,
  "board": 0
}
HTTP Status 200 OK
```
#### Удаление категории
Для редактирования категории текущий пользователь должен обладать правами owner.
Приложению необходимо сделать сервер-сервер запрос Delete на endpoint `/goals/goal_category/{id}`

Пример response
```
HTTP Status 204 No content
```