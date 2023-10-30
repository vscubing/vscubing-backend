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
        "id": 5,
        "avg_ms": null,
        "discipline": {
            "name": "3by3"
        },
        "solve_set": [
            {
                "id": 19,
                "time_ms": 1271,
                "scramble": {
                    "position": "1"
                }
            },
            {
                "id": 20,
                "time_ms": 784,
                "scramble": {
                    "position": "2"
                }
            },
            {
                "id": 21,
                "time_ms": 1404,
                "scramble": {
                    "position": "3"
                }
            },
            {
                "id": 22,
                "time_ms": 2444,
                "scramble": {
                    "position": "4"
                }
            },
            {
                "id": 23,
                "time_ms": 6276,
                "scramble": {
                    "position": "E1"
                }
            },
            {
                "id": 24,
                "time_ms": 5008,
                "scramble": {
                    "position": "5"
                }
            }
        ]
    },
    {
        "id": 5,
        "avg_ms": null,
        "discipline": {
            "name": "3by3"
        },
        "solve_set": [
          
        ]
    }
]
```
