# Действия с категориями

* [Список категорий пользователя](#список-категорий-пользователя) ![flutter](https://img.shields.io/badge/user-green)


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
      "created": "2022-06-16T07:22:42.247Z",
      "updated": "2022-06-16T07:22:42.247Z",
      "title": "string",
      "due_date": "2022-06-16T07:22:42.247Z",
      "description": "string",
      "status": 1,
      "priority": 1,
      "category": 0
    }
  ]
}
HTTP Status 200 OK
```