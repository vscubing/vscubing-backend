# Show Contest

Show all solve of this contest

**URL** : `/contests/contest/<int:contest_number>/<str:discipline>/`

**Method** : `GET`

**Auth required** : if contest is ongoing YES, elso NO 

**Permissions required** : if contest is ongoing YES, elso NONE

## Success Responses

**Code** : `200 OK`


```json
[
    {
        "id": 1,
        "username": "savytskyi.work",
        "time_ms": 1710,
        "discipline": "3by3",
        "scramble_position": "1"
    },
    {
        "id": 2,
        "username": "savytskyi.work",
        "time_ms": 2468,
        "discipline": "3by3",
        "scramble_position": "2"
    },
    {
        "id": 3,
        "username": "savytskyi.work",
        "time_ms": 1139,
        "discipline": "3by3",
        "scramble_position": "3"
    },
    {
        "id": 4,
        "username": "savytskyi.work",
        "time_ms": 27236,
        "discipline": "3by3",
        "scramble_position": "4"
    },
    {
        "id": 6,
        "username": "savytskyi.work",
        "time_ms": 2456,
        "discipline": "3by3",
        "scramble_position": "E1"
    },
    {
        "id": 7,
        "username": "antonsav123",
        "time_ms": 1464,
        "discipline": "3by3",
        "scramble_position": "1"
    },
    {
        "id": 9,
        "username": "antonsav123",
        "time_ms": 4136,
        "discipline": "3by3",
        "scramble_position": "E1"
    },
    {
        "id": 10,
        "username": "antonsav123",
        "time_ms": 2171,
        "discipline": "3by3",
        "scramble_position": "3"
    },
    {
        "id": 11,
        "username": "antonsav123",
        "time_ms": 568,
        "discipline": "3by3",
        "scramble_position": "4"
    },
    {
        "id": 12,
        "username": "antonsav123",
        "time_ms": 1187,
        "discipline": "3by3",
        "scramble_position": "5"
    }
]
```
