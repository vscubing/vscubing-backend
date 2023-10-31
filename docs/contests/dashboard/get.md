# Show Dashboard 

**URL** : `/api/contests/`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
{
    "contests": [
        {
            "id": 3,
            "contest_number": 1,
            "start": "2023-10-28T17:35:19.730994Z",
            "end": null,
            "ongoing": false
        },
        {
            "id": 4,
            "contest_number": 2,
            "start": "2023-10-28T22:02:40.883873Z",
            "end": null,
            "ongoing": false
        },
        {
            "id": 5,
            "contest_number": 3,
            "start": "2023-10-29T11:48:30.826796Z",
            "end": null,
            "ongoing": true
        }
    ],
    "best_solves": [
        {
            "id": 20,
            "time_ms": 784,
            "contest_number": 1,
            "scramble": {
                "id": 9
            },
            "discipline": {
                "name": "3by3"
            },
            "user": {
                "username": "antonsav123"
            }
        }
    ]
}
     
```
