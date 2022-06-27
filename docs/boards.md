# Действия с досками

#### Методы для работы с досками
* POST `/goals/board/create` — [cоздание доски](#Создание-доски) ![flutter](https://img.shields.io/badge/user-green)
* GET `/goals/board/list` — [просмотр списка досок](#просмотр-списка-досок) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* GET `/goals/board/‹pk›` — [просмотр доски](#просмотр-доски) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* PUT `/goals/board/‹pk›` — [редактирование доски](#редактирование-доски) ![flutter](https://img.shields.io/badge/owner-00FFFF)
* DELETE `/goals/board/‹pk›` — [удаление доски](#удаление-доски) ![flutter](https://img.shields.io/badge/owner-00FFFF)

#### Создание доски
Приложению необходимо сделать сервер-сервер запрос POST `/goals/board/create`

Пример POST запроса
```
{
  "title": "string",
  "is_deleted": true
}
```
Пример response
```
{
  "id": 0,
  "created": "2022-06-26T22:26:49.305Z",
  "updated": "2022-06-26T22:26:49.305Z",
  "title": "string",
  "is_deleted": true
}
HTTP Status 201 Created
```
#### Просмотр списка досок
Пользователю должны быть доступны все доски, в которых он является участником.
Приложению необходимо сделать сервер-сервер запрос get на endpoint `/goals/board/list`
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "created": "2022-06-26T22:39:30.077Z",
      "updated": "2022-06-26T22:39:30.077Z",
      "title": "string",
      "is_deleted": true
    }
  ]
}
HTTP Status 200 OK
```
#### Просмотр доски

Приложению необходимо сделать сервер-сервер запрос get на endpoint `/goals/board/{id}`
Где participants - перечисление участников доски, может быть несколько.
```
{
  "id": 0,
  "participants": [
    {
      "id": 0,
      "role": 1,
      "user": "string",
      "created": "2022-06-26T22:42:46.058Z",
      "updated": "2022-06-26T22:42:46.058Z",
      "board": 0
    }
  ],
  "created": "2022-06-26T22:42:46.058Z",
  "updated": "2022-06-26T22:42:46.058Z",
  "title": "string",
  "is_deleted": true
}
```
#### Редактирование доски
Для редактирования доски текущий пользователь должен обладать правами owner.
Приложению необходимо сделать сервер-сервер запрос PUT на endpoint `/goals/board/{id}`
```
{
  "participants": [
    {
      "role": 1,
      "user": "string"
    }
  ],
  "title": "string",
  "is_deleted": false
}
```
или частичное обновление
```
{
  "title": "string",
  "is_deleted": true
}
```
Пример response
```
{
  "id": 0,
  "participants": [
    {
      "id": 0,
      "role": 1,
      "user": "string",
      "created": "2022-06-27T05:36:42.968Z",
      "updated": "2022-06-27T05:36:42.968Z",
      "board": 0
    }
  ],
  "created": "2022-06-27T05:36:42.969Z",
  "updated": "2022-06-27T05:36:42.969Z",
  "title": "string",
  "is_deleted": true
}
HTTP Status 200 OK
```
#### Удаление доски
Для редактирования доски текущий пользователь должен обладать правами owner.
При удалении доски удаляются все категории `is_deleted=True`, все цели переводятся в статус архив.
Приложению необходимо сделать сервер-сервер запрос Delete на endpoint `/goals/board/{id}`

Пример response
```
HTTP Status 204 No content
```