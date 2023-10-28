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
            "id": 1,
            "contest_number": 1,
            "start": "2023-10-27T12:59:03.062297Z",
            "end": null,
            "ongoing": false
        },
        {
            "id": 2,
            "contest_number": 2,
            "start": "2023-10-27T13:30:54.087349Z",
            "end": null,
            "ongoing": false
        }
    ],
    "best_solves": [
        {
            "id": 11,
            "time_ms": 568,
            "username": "antonsav123",
            "contest_number": 1,
            "discipline": "3by3"
        }
    ]
}
     
```
