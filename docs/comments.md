# Действия с целями


#### Методы для работы с целями пользователя
* POST `/goals/goal_comment/create/` — [cоздание комментария](#Создание-комментария) ![flutter](https://img.shields.io/badge/owner-00FFFF) ![flutter](https://img.shields.io/badge/writer-C0C0C0)
* GET `/goals/goal_comment/list` — [просмотр списка комментариев](#список-комментариев-пользователя) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* GET `/goals/goal_comment/‹pk›` — [просмотр комментария](#просмотр-комментария) ![flutter](https://img.shields.io/badge/boardparticipant-0000FF)
* PUT `/goals/goal_comment/‹pk›` — [редактирование комментария](#редактирование-комментария) ![flutter](https://img.shields.io/badge/currentuser-00FF7F)
* DELETE `/goals/goal_comment/‹pk›` — [удаление комментария](#удаление-комментария) ![flutter](https://img.shields.io/badge/currentuser-00FF7F)


#### Создание комментария
Приложению необходимо сделать сервер-сервер запрос POST `/goals/goal_comment/create/`
> Пользователь может создавать/изменять/удалять комментария только в тех категориях, в досках которых он является участником с ролью «Владелец» или «Редактор».

Пример POST запроса
```
{
  "text": "string",
  "goal": 0
}
```
Пример ответа
```
{
  "id": 0,
  "created": "2022-07-07T01:33:47.711Z",
  "updated": "2022-07-07T01:33:47.711Z",
  "text": "string",
  "goal": 0
}
HTTP Status 201 Created
```

## Список всех комментариев пользователя
В данном endpoint будут отображаться как общие комментарии так и комментарии которые принадлежат только текущему пользователю.
>Пользователю выдаются только те комментарии, которые находятся в целях, в досках которых он является участником.

Приложению необходимо сделать сервер-сервер запрос GET `goals/goal_comment/list/`.

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
      "created": "2022-07-07T01:35:04.733Z",
      "updated": "2022-07-07T01:35:04.733Z",
      "text": "string",
      "goal": 0
    }
  ]
}
HTTP Status 200 OK
```
## Просмотр комментария
Приложению необходимо сделать сервер-сервер запрос GET `goals/goal_comment/{id}`.
>Пользователю выдаются только те комментарии, которые находятся в целях, в досках которых он является участником.

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
  "created": "2022-07-07T01:36:38.173Z",
  "updated": "2022-07-07T01:36:38.173Z",
  "text": "string",
  "goal": 0
}
HTTP Status 200 OK
```
## Редактирование комментария
>Пользователь всё так же не может редактировать/удалять чужие комментарии.

Приложению необходимо сделать сервер-сервер запрос PUT на endpoint `/goals/goal_comment/{id}`

Пример запроса
```
{
  "text": "string"
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
  "created": "2022-07-07T01:37:45.670Z",
  "updated": "2022-07-07T01:37:45.670Z",
  "text": "string",
  "goal": 0
}
HTTP Status 200 OK
```
#### Удаление комментария
>Пользователь всё так же не может редактировать/удалять чужие комментарии.

>Приложению необходимо сделать сервер-сервер запрос `Delete` на endpoint `/goals/goal_comment/{id}`

Пример response
```
HTTP Status 204 No content
```