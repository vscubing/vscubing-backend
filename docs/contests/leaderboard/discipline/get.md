# Show 

**URL** : `/api/leaderboard/<str:discipline>/`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
[
    {
        "id": 50,
        "time_ms": 708,
        "created": "2023-11-01T00:47:33.644764Z",
        "scramble": {
            "id": 35,
            "scramble": "F2 B2 L"
        },
        "discipline": {
            "name": "3by3"
        },
        "user": {
            "id": 4,
            "username": "antonsav2005"
        },
        "contest": {
            "contest_number": 1
        }
    },
    {
        "id": 60,
        "time_ms": 1280,
        "created": "2023-11-01T00:47:33.644764Z",
        "scramble": {
            "id": 32,
            "scramble": "D F B'"
        },
        "discipline": {
            "name": "3by3"
        },
        "user": {
            "id": 2,
            "username": "savytskyi.work"
        },
        "contest": {
            "contest_number": 1
        }
    }
]
     
```
